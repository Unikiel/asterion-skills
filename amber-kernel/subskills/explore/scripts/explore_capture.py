#!/usr/bin/env python3
"""Save agent-researched URL explorations in an existing intake directory.

No network access or summarization occurs here. The agent must actually read
sources, author the report, and accurately declare coverage before invoking it.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

# Locate shared modules when invoked directly from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from urllib.parse import quote, urlsplit, urlunsplit

import yaml

from scripts.vault_state import BatchError, all_issues, properties, root_path, safe_path, snapshot
from media_extract import route


def source_kind(source):
    hint = route(source["url"])
    kind = source.get("kind", hint["kind"])
    if kind not in {"web", "text", "document", "image", "audio", "video", "channel", "playlist", "file"}:
        raise BatchError("unknown source media kind")
    if hint.get("platform") == "youtube" and hint["kind"] in {"video", "channel", "playlist"} and kind != hint["kind"]:
        raise BatchError("YouTube source kind must match the identified URL target")
    return kind


def validate_media(source):
    kind = source_kind(source)
    needed = {"image": {"visual"}, "audio": {"audio"}, "video": {"audio", "visual"},
              "document": {"text"}, "channel": {"metadata"}, "playlist": {"metadata"}}.get(kind, set())
    modalities = source.get("modalities", [])
    if not isinstance(modalities, list):
        raise BatchError("modalities must be a list")
    seen = {}
    for entry in modalities:
        name = entry.get("type")
        if name not in {"text", "audio", "visual", "metadata"} or name in seen:
            raise BatchError("modality types must be unique text, audio, visual, or metadata")
        state = entry.get("status")
        if state not in {"observed", "partial", "unavailable", "not_applicable"}:
            raise BatchError("unknown modality coverage status")
        if state in {"observed", "partial"}:
            line(entry.get("method"), "modality extraction method")
            line(entry.get("locator"), "modality coverage locator")
        if state != "observed":
            line(entry.get("limitation"), "modality limitation or scope exclusion")
        seen[name] = entry
    if not needed.issubset(seen):
        raise BatchError(f"{kind} requires coverage for: {', '.join(sorted(needed))}")
    if seen and source["status"] == "read":
        if any(e["status"] in {"partial", "unavailable"} for e in modalities):
            raise BatchError("source with incomplete modalities must be partial or unavailable")
        if not any(e["status"] == "observed" for e in modalities):
            raise BatchError("a read source needs at least one observed modality")
    if seen and source["status"] == "partial" and not any(e["status"] in {"observed", "partial"} for e in modalities):
        raise BatchError("a wholly inaccessible media source must be unavailable")
    return kind


def normalize_url(value: str) -> str:
    if not isinstance(value, str) or re.search(r'[\s<>"\\\x00-\x1f]', value):
        raise BatchError("expected a nonempty HTTP(S) URL without whitespace or credentials")
    try:
        parts = urlsplit(value)
        if parts.scheme.lower() not in {"http", "https"} or not parts.hostname or parts.username is not None or parts.password is not None:
            raise ValueError("invalid URL")
        host = parts.hostname.lower().encode("idna").decode("ascii")
        if ":" in host:
            host = "[" + host + "]"
        port = parts.port
    except (ValueError, UnicodeError) as exc:
        raise BatchError("expected a valid HTTP(S) URL without credentials") from exc
    authority = host + (f":{port}" if port and (parts.scheme.lower(), port) not in {("http", 80), ("https", 443)} else "")
    # Query parameters and fragments can identify meaningful content; keep them.
    return urlunsplit((parts.scheme.lower(), authority, parts.path or "/", parts.query, parts.fragment))


def line(value, name):
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise BatchError(f"{name} must be a nonempty single line")
    return value.strip()


def date(value):
    try:
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError()
        dt.date.fromisoformat(value)
    except (ValueError, TypeError) as exc:
        raise BatchError("accessed must be a real YYYY-MM-DD date") from exc
    return value


def media_identity(url):
    """Deduplicate YouTube watch/short/live/share URLs by the actual video ID."""
    normalized = normalize_url(url)
    hint = route(normalized)
    return "youtube:" + hint["video_id"] if hint.get("video_id") else normalized


def substantive(source):
    return any(m.get("type") != "metadata" and m.get("status") in {"observed", "partial"}
               for m in source.get("modalities", []))


def collection_counts(collection):
    inventory = collection["inventory"]
    return {"discovered": len(inventory), **{
        state: sum(item["status"] == state for item in inventory)
        for state in ("complete", "partial", "pending", "unavailable")}}


def validate_collection(collection, identifiers, seed, cited, status):
    if not isinstance(collection, dict) or collection.get("scope") != "all":
        raise BatchError("collection scope must be all; an explicit sample uses sampling instead")
    if collection.get("discovery_status") not in {"complete", "partial"}:
        raise BatchError("collection discovery_status must be complete or partial")
    line(collection.get("discovery_note"), "collection discovery evidence and scope")
    inventory = collection.get("inventory")
    if not isinstance(inventory, list):
        raise BatchError("collection inventory must be a list")
    seen = set()
    for entry in inventory:
        if not isinstance(entry, dict):
            raise BatchError("collection inventory entries must be objects")
        key = media_identity(entry["url"])
        if key in seen:
            raise BatchError("duplicate collection item; merge URL variants by media identity")
        if key == media_identity(seed["url"]):
            raise BatchError("collection seed cannot be its own inventory item")
        seen.add(key)
        state = entry.get("status")
        if state not in {"complete", "partial", "pending", "unavailable"}:
            raise BatchError("unknown collection item status")
        if state != "complete":
            line(entry.get("limitation"), "collection item limitation or next step")
        identifier = entry.get("source_id")
        if state in {"pending", "unavailable"}:
            if identifier is not None:
                raise BatchError("pending/unavailable items have no substantive source_id")
            continue
        source = identifiers.get(identifier)
        if source is None or source is seed or identifier not in cited:
            raise BatchError("researched collection items require an actually cited non-seed source")
        if media_identity(source["url"]) != key:
            raise BatchError("collection item and source must identify the same media")
        expected = "read" if state == "complete" else "partial"
        if source["status"] != expected or not substantive(source):
            raise BatchError("collection item status must match substantive media evidence")
    if status == "complete":
        if collection["discovery_status"] != "complete" or not inventory or any(i["status"] != "complete" for i in inventory):
            raise BatchError("complete collection requires completed discovery and every item complete")
    else:
        line(collection.get("resume_note"), "collection checkpoint and resume instructions")


def validate_report(report):
    if not isinstance(report, dict) or report.get("version") != 1:
        raise BatchError("report version must be 1")
    requested = normalize_url(report["url"])
    resolved = normalize_url(report.get("resolved_url", report["url"]))
    title = line(report["title"], "title")
    accessed = date(report["accessed"])
    status = report.get("status")
    if status not in {"complete", "partial", "blocked"}:
        raise BatchError("status must be complete, partial, or blocked")
    if status != "complete":
        line(report.get("coverage_note"), "coverage_note for limited access")
    body = report.get("body")
    if not isinstance(body, str) or not body.strip():
        raise BatchError("body must contain the researched explanation or access limitation")
    if "[S" in body and re.search(r"^\s*\[S\d+\]:", body, re.M):
        raise BatchError("source definitions are generated from the ledger; do not redefine them in body")
    if re.search(r"\[S\d+\][\[(]", body):
        raise BatchError("use plain [S1] reference citations; do not override their destinations")
    sources = report.get("sources")
    if not isinstance(sources, list) or not sources:
        raise BatchError("sources must include the seed, even when access was blocked")
    identifiers = {}
    for source in sources:
        identifier = source.get("id", "")
        if not re.fullmatch(r"S[1-9]\d*", identifier) or identifier in identifiers:
            raise BatchError("source IDs must be unique S1, S2, ... labels")
        normalize_url(source["url"])
        line(source["title"], "source title")
        date(source.get("accessed", accessed))
        if source.get("status") not in {"read", "partial", "unavailable"}:
            raise BatchError("each source needs a read, partial, or unavailable status")
        if source["status"] != "read":
            line(source.get("limitation"), "source limitation")
        validate_media(source)
        identifiers[identifier] = source
    seed = identifiers.get(report.get("seed_source"))
    if seed is None or normalize_url(seed["url"]) not in {requested, resolved}:
        raise BatchError("seed_source must identify the requested or resolved URL in the source ledger")
    if seed["status"] == "unavailable" and status != "blocked":
        raise BatchError("an unread seed requires blocked status")
    if status == "blocked" and seed["status"] != "unavailable":
        raise BatchError("blocked status requires an unavailable seed")
    if status == "complete" and any(s["status"] != "read" for s in sources):
        raise BatchError("complete coverage cannot include partially read or unavailable sources")
    cited = set(re.findall(r"\[(S[1-9]\d*)\]", body))
    if status != "blocked" and not cited:
        raise BatchError("a researched body requires source citations such as [S1]")
    if status != "blocked" and report["seed_source"] not in cited:
        raise BatchError("the researched body must cite its seed source")
    for identifier in cited:
        if identifier not in identifiers or identifiers[identifier]["status"] == "unavailable":
            raise BatchError(f"citation has no readable source: {identifier}")
    if source_kind(seed) in {"channel", "playlist"} and status != "blocked":
        if "collection" in report:
            if "sampling" in report:
                raise BatchError("use collection or sampling, not both")
            validate_collection(report["collection"], identifiers, seed, cited, status)
        else:
            validate_sampling(report, identifiers, seed, cited, status)
    elif "collection" in report or "sampling" in report:
        raise BatchError("collection/sampling requires an accessible channel or playlist seed")
    if not isinstance(report.get("properties", {}), dict):
        raise BatchError("properties must be a mapping following existing conventions")
    return requested, resolved, title, accessed, status


def validate_sampling(report, identifiers, seed, cited, status):
    # Legacy samples remain readable, but cannot establish full collection coverage.
    # New sample runs are permitted only when the user explicitly narrows scope.
    sampling = report.get("sampling")
    if not isinstance(sampling, dict):
        raise BatchError("channel/playlist exploration requires a collection or sampling record")
    line(sampling.get("scope"), "sampling scope")
    line(sampling.get("rationale"), "sampling rationale")
    selected = sampling.get("selected_sources")
    if not isinstance(selected, list) or len(set(selected)) != len(selected):
        raise BatchError("selected_sources must list unique source IDs")
    if status == "complete" and not selected:
        raise BatchError("metadata-only channel research cannot be complete")
    for identifier in selected:
        item = identifiers.get(identifier)
        if item is None or item is seed or identifier not in cited:
            raise BatchError("each selected item must be an actually cited non-seed source")
        if not substantive(item):
            raise BatchError("sampled items require substantive media evidence, not just metadata")
    if status == "complete":
        raise BatchError("a sample cannot establish complete channel/playlist coverage")


def markdown_label(value):
    return re.sub(r"([\\\[\]*_`])", r"\\\1", value)


def render(report):
    requested, resolved, title, accessed, status = validate_report(report)
    lines = []
    if report.get("properties"):
        lines += ["---", yaml.safe_dump(report["properties"], allow_unicode=True, sort_keys=False).rstrip(), "---", ""]
    lines += ["# " + markdown_label(title), "", f"**Input URL:** <{requested}>"]
    if resolved != requested:
        lines.append(f"**Resolved URL:** <{resolved}>")
    lines += [f"**Accessed:** {accessed}", f"**Research coverage:** {status}"]
    if report.get("coverage_note"):
        lines.append("**Coverage note:** " + line(report["coverage_note"], "coverage_note"))
    source_urls = {source["id"]: normalize_url(source["url"]) for source in report["sources"]}
    body = re.sub(r"\[(S[1-9]\d*)\]", lambda match: f"[{match[1]}](<{source_urls[match[1]]}>)", report["body"].strip())
    lines += ["", body]
    if report.get("collection"):
        collection = report["collection"]
        counts = collection_counts(collection)
        lines += ["", "## Collection coverage", "", "Scope: all discoverable items.",
                  "Discovery: " + collection["discovery_status"] + ". " + collection["discovery_note"],
                  "Progress: " + "; ".join(f"{name}: {value}" for name, value in counts.items()) + "."]
        if collection.get("resume_note"):
            lines += ["Resume: " + line(collection["resume_note"], "resume_note")]
        lines += [""]
        for entry in collection["inventory"]:
            detail = f"- [{entry.get('source_id', 'Item')}](<{normalize_url(entry['url'])}>) — {entry['status']}"
            if entry.get("limitation"):
                detail += "; " + entry["limitation"]
            lines.append(detail)
    if report.get("sampling"):
        sampling = report["sampling"]
        lines += ["", "## Exploration scope", "", "Scope: " + line(sampling["scope"], "sampling scope"),
                  "Selection: " + line(sampling["rationale"], "sampling rationale"),
                  "Sampled sources: " + (", ".join(sampling["selected_sources"]) or "No substantive media could be inspected.")]
    lines += ["", "## Sources", ""]
    for source in report["sources"]:
        identifier = source["id"]
        url = normalize_url(source["url"])
        label = markdown_label(source["title"])
        # All ledger entries are navigable; unavailable entries cannot support body citations.
        lines.append(f"- {identifier}: [{label}](<{url}>) — {source['status']}; accessed {source.get('accessed', accessed)}.")
        if source.get("locator"):
            lines.append("  Locator: " + line(source["locator"], "locator"))
        if source.get("limitation"):
            lines.append("  Limitation: " + line(source["limitation"], "limitation"))
        if source.get("modalities"):
            lines.append("  Media kind: " + source_kind(source))
            for entry in source["modalities"]:
                detail = f"  - {entry['type']}: {entry['status']}"
                if entry.get("method"):
                    detail += "; " + line(entry["method"], "method")
                if entry.get("locator"):
                    detail += "; " + line(entry["locator"], "locator")
                if entry.get("limitation"):
                    detail += "; " + line(entry["limitation"], "limitation")
                lines.append(detail)
    lines.append("")
    for source in report["sources"]:
        if source["status"] != "unavailable":
            lines.append(f"[{source['id']}]: <{normalize_url(source['url'])}>")
    return "\n".join(lines).rstrip() + "\n"


def duplicates(files, urls):
    matches = []
    for path, content in files.items():
        if not path.lower().endswith(".md"):
            continue
        try:
            text = content.decode("utf-8-sig")
            captured = re.findall(r"^\*\*(?:Input|Resolved) URL:\*\* <([^>\n]+)>\s*$", text, re.M)
            props = properties(content)
            # Also recognize established source-note metadata when it holds a URL.
            captured += [props[k] for k in ("url", "source_url") if isinstance(props.get(k), str)]
            for value in captured:
                try:
                    if normalize_url(value) in urls:
                        matches.append(path)
                        break
                except BatchError:
                    pass
        except (ValueError, yaml.YAMLError):
            continue
    return sorted(matches)


def destination_name(title, url):
    title = re.sub(r'[<>:"/\\|?*#^\[\]\x00-\x1f%]', " ", title)
    title = re.sub(r"\s+", " ", title).strip(" .")[:80].rstrip(" .") or "URL exploration"
    key = hashlib.sha256(url.encode()).hexdigest()[:12]
    return f"Explore - {title} - {key}.md"


def capture(vault, report, *, intake="LandingField", apply=False, new_capture=False):
    requested, resolved, title, accessed, status = validate_report(report)
    root = root_path(vault)
    directory = safe_path(root, intake)
    if not directory.is_dir():
        raise BatchError("intake must be an existing directory")
    before, dirs = snapshot(root)
    previous = duplicates(before, {requested, resolved})
    if previous and not new_capture:
        return {"status": "already-captured", "existing": previous, "applied": False}
    relative = intake.rstrip("/") + "/" + destination_name(title, requested)
    if new_capture:
        stem = Path(relative).stem
        relative = intake.rstrip("/") + f"/{stem} - {accessed}.md"
        number = 2
        while any(p.casefold() == relative.casefold() for p in before):
            relative = intake.rstrip("/") + f"/{stem} - {accessed} ({number}).md"
            number += 1
    path = safe_path(root, relative)
    if any(p.casefold() == relative.casefold() for p in before):
        raise BatchError("destination collision; existing content will not be overwritten")
    text = render(report)
    if previous:
        text += "\n## Earlier captures\n\n" + "\n".join(
            f"- [{markdown_label(Path(p).stem)}]({quote(os.path.relpath(root / p, path.parent).replace(os.sep, '/'), safe='/.-_~')})" for p in previous) + "\n"
    data = text.encode("utf-8")
    after = dict(before, **{relative: data})
    issues = all_issues(after) - all_issues(before)
    if issues:
        raise BatchError("new integrity findings: " + json.dumps(sorted(issues), ensure_ascii=False))
    known = {}
    for name, content in before.items():
        if name.lower().endswith(".md"):
            try:
                for key, value in properties(content).items():
                    if value is not None:
                        known.setdefault(key, set()).add(type(value))
            except (ValueError, yaml.YAMLError):
                pass
    for key, value in properties(data).items():
        if value is not None and len(known.get(key, set())) == 1 and type(value) not in known[key]:
            raise BatchError(f"property type conflicts with existing vault convention: {key}")
    result = {"status": status, "path": relative, "applied": False,
              "sources_read": sum(s["status"] in {"read", "partial"} for s in report["sources"]),
              "sources_partial": sum(s["status"] == "partial" for s in report["sources"]),
              "earlier_captures": previous}
    if report.get("collection"):
        result["collection"] = {"discovery_status": report["collection"]["discovery_status"],
                                **collection_counts(report["collection"])}
    if apply:
        # A single new file is staged and linked exclusively; existing notes are never overwritten.
        fd, temporary = tempfile.mkstemp(prefix=".amber-explore-", suffix=".tmp", dir=directory)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            current, current_dirs = snapshot(root)
            current.pop(Path(temporary).relative_to(root).as_posix(), None)
            if current != before or current_dirs != dirs:
                raise BatchError("vault changed since preview; rebuild the capture")
            os.link(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        current, current_dirs = snapshot(root)
        if current.get(relative) != data or current_dirs != dirs or all_issues(current) - all_issues(before):
            raise BatchError(f"post-write validation failed; capture may exist at {relative}")
        result["applied"] = True
    return result


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault")
    parser.add_argument("report", help="agent-authored JSON report from actually read sources")
    parser.add_argument("--intake", default="LandingField")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--new-capture", action="store_true", help="requested revisit or resumed collection snapshot; never overwrites prior notes")
    args = parser.parse_args(argv)
    try:
        report = json.loads(Path(args.report).read_text(encoding="utf-8-sig"))
        result = capture(args.vault, report, intake=args.intake, apply=args.apply, new_capture=args.new_capture)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError, yaml.YAMLError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
