#!/usr/bin/env python3
"""Deterministic, non-invasive operations for Obsidian vaults.

Mutating commands are dry-run by default and require --apply.  On an existing
vault this tool never creates directories or edits .obsidian state.  Empty
vault scaffolding is a separate, guarded operation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import unquote

try:
    import yaml
except ImportError:  # pragma: no cover - handled with a useful runtime error
    yaml = None


IGNORED_PARTS = {".obsidian", ".git", ".trash", "node_modules", ".cache"}
CONTENT_SUFFIXES = {".md", ".canvas", ".base"}
WIKILINK_RE = re.compile(r"(!?)\[\[([^\]\n]+)\]\]")
MD_LINK_RE = re.compile(r"(!?)\[([^\]\n]*)\]\(([^)\n]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
BLOCK_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9-]+)\s*$", re.MULTILINE)
INVALID_FILENAME_CHARS = set('<>:"/\\|?*#^[]')


class AmberError(RuntimeError):
    pass


@dataclass(frozen=True)
class LinkRef:
    source: Path
    raw: str
    target: str
    embed: bool
    kind: str


def require_yaml() -> None:
    if yaml is None:
        raise AmberError("PyYAML is required for YAML frontmatter and Base operations")


def emit(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def vault_root(value: str | Path) -> Path:
    start = Path(value).expanduser().resolve()
    if start.is_file():
        start = start.parent
    for candidate in (start, *start.parents):
        if (candidate / ".obsidian").is_dir():
            return candidate
    raise AmberError(f"no Obsidian vault found at or above: {start}")


def rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def safe_path(root: Path, value: str, *, suffix: str | None = None) -> Path:
    from parse_batch import safe_path as checked_path
    if suffix and not PurePosixPath(value).suffix:
        value += suffix
    return checked_path(root, value)


def validate_filename(path: Path) -> None:
    for part in path.parts:
        if any(ch in INVALID_FILENAME_CHARS for ch in part) or part.rstrip(". ") != part:
            raise AmberError(f"non-portable filename component: {part!r}")


def content_files(root: Path, suffixes: set[str] | None = None) -> Iterable[Path]:
    suffixes = suffixes or CONTENT_SUFFIXES
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in suffixes:
            relative_parts = path.relative_to(root).parts
            if not any(part in IGNORED_PARTS for part in relative_parts):
                yield path


def structure_snapshot(root: Path) -> list[str]:
    return sorted(
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_dir() and not any(x in IGNORED_PARTS for x in p.relative_to(root).parts)
    )


def ensure_existing_parent(root: Path, target: Path) -> None:
    if not target.parent.is_dir():
        raise AmberError(
            f"refusing to create directory in an existing vault: {rel(root, target.parent)}"
        )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str, *, apply: bool) -> dict[str, Any]:
    changed = not path.exists() or read_text(path) != text
    if apply and changed:
        path.write_text(text, encoding="utf-8", newline="\n")
    return {"path": str(path), "changed": changed, "applied": bool(apply and changed)}


def split_frontmatter(text: str) -> tuple[dict[str, Any], str, bool]:
    require_yaml()
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, text, False
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        raise AmberError("unterminated YAML frontmatter")
    from parse_batch import UniqueLoader
    data = yaml.load(match.group(1), Loader=UniqueLoader) or {}
    if not isinstance(data, dict):
        raise AmberError("frontmatter must be a YAML mapping")
    return data, text[match.end() :], True


def compose_note(properties: dict[str, Any], body: str, include_frontmatter: bool = True) -> str:
    if not include_frontmatter and not properties:
        return body
    require_yaml()
    dumped = yaml.safe_dump(properties, allow_unicode=True, sort_keys=False).rstrip()
    return f"---\n{dumped}\n---\n{body.lstrip()}"


def parse_json_object(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    data = json.loads(value)
    if not isinstance(data, dict):
        raise AmberError("expected a JSON object")
    return data


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(read_text(path))
    except (json.JSONDecodeError, OSError):
        return default


def settings(root: Path) -> dict[str, Any]:
    obsidian = root / ".obsidian"
    return {
        "app": load_json(obsidian / "app.json", {}),
        "core_plugins": load_json(obsidian / "core-plugins.json", {}),
        "community_plugins": load_json(obsidian / "community-plugins.json", []),
    }


def convention_fingerprint(root: Path) -> dict[str, Any]:
    notes = list(content_files(root, {".md"}))
    sampled = notes[: min(30, len(notes))]
    frontmatter = 0
    wikilinks = 0
    markdown_links = 0
    property_types: dict[str, set[str]] = {}
    for note in sampled:
        text = read_text(note)
        try:
            props, _, present = split_frontmatter(text)
        except AmberError:
            props, present = {}, False
        frontmatter += int(present)
        wikilinks += len(WIKILINK_RE.findall(text))
        markdown_links += len(MD_LINK_RE.findall(text))
        for key, value in props.items():
            property_types.setdefault(str(key), set()).add(type(value).__name__)
    cfg = settings(root)
    return {
        "vault": str(root),
        "top_level": sorted(p.name for p in root.iterdir() if p.name != ".obsidian"),
        "counts": {
            suffix: sum(1 for _ in content_files(root, {suffix}))
            for suffix in (".md", ".canvas", ".base")
        },
        "sample_size": len(sampled),
        "notes_with_frontmatter": frontmatter,
        "link_style_counts": {"wikilink": wikilinks, "markdown": markdown_links},
        "property_types": {k: sorted(v) for k, v in property_types.items()},
        "new_link_format": cfg["app"].get("newLinkFormat"),
        "attachment_folder": cfg["app"].get("attachmentFolderPath"),
        "enabled_core_plugins": sorted(k for k, v in cfg["core_plugins"].items() if v)
        if isinstance(cfg["core_plugins"], dict)
        else sorted(cfg["core_plugins"]),
        "enabled_community_plugins": sorted(cfg["community_plugins"]),
    }


def note_index(root: Path) -> tuple[dict[str, list[Path]], dict[str, Path]]:
    basenames: dict[str, list[Path]] = {}
    paths: dict[str, Path] = {}
    for note in content_files(root, {".md"}):
        relative = note.relative_to(root).with_suffix("").as_posix()
        paths[relative.casefold()] = note
        basenames.setdefault(note.stem.casefold(), []).append(note)
    return basenames, paths


def parse_wikilink_target(raw: str) -> str:
    return raw.split("|", 1)[0].split("#", 1)[0].strip()


def find_links(root: Path) -> list[LinkRef]:
    refs: list[LinkRef] = []
    for source in content_files(root, {".md"}):
        text = read_text(source)
        for match in WIKILINK_RE.finditer(text):
            target = parse_wikilink_target(match.group(2))
            if target:
                refs.append(LinkRef(source, match.group(0), target, bool(match.group(1)), "wiki"))
        for match in MD_LINK_RE.finditer(text):
            target = match.group(3).split("#", 1)[0].strip()
            if target and not re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                refs.append(LinkRef(source, match.group(0), unquote(target), bool(match.group(1)), "markdown"))
    return refs


def resolve_link(root: Path, ref: LinkRef, basenames: dict[str, list[Path]], paths: dict[str, Path]) -> tuple[str, Path | None]:
    target = ref.target.replace("\\", "/").lstrip("/")
    if ref.kind == "markdown":
        candidate = (ref.source.parent / target).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            return "outside", None
        return ("resolved", candidate) if candidate.exists() else ("unresolved", None)
    without_ext = target[:-3] if target.lower().endswith(".md") else target
    direct = paths.get(without_ext.casefold())
    if direct:
        return "resolved", direct
    matches = basenames.get(PurePosixPath(without_ext).name.casefold(), [])
    if len(matches) == 1:
        return "resolved", matches[0]
    if len(matches) > 1:
        return "ambiguous", None
    attachment = safe_path(root, target)
    if attachment.exists():
        return "resolved", attachment
    return "unresolved", None


def validate_markdown(root: Path, path: Path) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    text = read_text(path)
    try:
        props, _, _ = split_frontmatter(text)
        if len(props) != len(set(props)):
            issues.append({"path": rel(root, path), "kind": "duplicate-property"})
    except (AmberError, Exception) as exc:
        issues.append({"path": rel(root, path), "kind": "invalid-frontmatter", "detail": str(exc)})
    return issues


def validate_canvas(root: Path, path: Path) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    try:
        data = json.loads(read_text(path))
        nodes, edges = data.get("nodes", []), data.get("edges", [])
        node_ids = [n.get("id") for n in nodes]
        edge_ids = [e.get("id") for e in edges]
        if None in node_ids or len(node_ids) != len(set(node_ids)):
            issues.append({"path": rel(root, path), "kind": "invalid-or-duplicate-node-id"})
        if None in edge_ids or len(edge_ids) != len(set(edge_ids)):
            issues.append({"path": rel(root, path), "kind": "invalid-or-duplicate-edge-id"})
        node_set = set(node_ids)
        for edge in edges:
            if edge.get("fromNode") not in node_set or edge.get("toNode") not in node_set:
                issues.append({"path": rel(root, path), "kind": "dangling-canvas-edge", "edge": edge.get("id")})
        for node in nodes:
            if node.get("type") == "file" and node.get("file"):
                target = safe_path(root, str(node["file"]))
                if not target.exists():
                    issues.append({"path": rel(root, path), "kind": "missing-canvas-file", "target": node["file"]})
    except Exception as exc:
        issues.append({"path": rel(root, path), "kind": "invalid-canvas", "detail": str(exc)})
    return issues


def validate_base(root: Path, path: Path) -> list[dict[str, Any]]:
    require_yaml()
    try:
        data = yaml.safe_load(read_text(path)) or {}
        if not isinstance(data, dict):
            raise AmberError("Base must contain a top-level YAML mapping")
        return []
    except Exception as exc:
        return [{"path": rel(root, path), "kind": "invalid-base", "detail": str(exc)}]


def audit(root: Path) -> dict[str, Any]:
    from parse_batch import snapshot
    from vault_links import link_issues
    files, _ = snapshot(root)
    issues = [{"path": p, "kind": k + "-link" if k in {"unresolved", "ambiguous"} else k, "detail": d}
              for p, k, d in sorted(link_issues(files))]
    for name in files:
        path = root / name
        if name.lower().endswith(".md"):
            issues.extend(validate_markdown(root, path))
        elif name.lower().endswith(".canvas"):
            issues.extend(validate_canvas(root, path))
        elif name.lower().endswith(".base"):
            issues.extend(validate_base(root, path))
    basenames, _ = note_index(root)
    for name, matches in basenames.items():
        if len(matches) > 1:
            issues.append({"kind": "duplicate-basename", "name": name, "paths": [rel(root, p) for p in matches]})
    return {"vault": str(root), "issues": issues, "issue_count": len(issues)}


def cmd_inspect(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    result = convention_fingerprint(root)
    if args.audit:
        result["integrity"] = audit(root)
    emit(result)


def cmd_validate(args: argparse.Namespace) -> None:
    result = audit(vault_root(args.vault))
    emit(result)
    if result["issue_count"]:
        raise SystemExit(2)


def cmd_bootstrap(args: argparse.Namespace) -> None:
    target = Path(args.vault).expanduser().resolve()
    existing_items = [p for p in target.iterdir()] if target.exists() else []
    if existing_items:
        raise AmberError("bootstrap is only allowed for an empty directory; existing vaults are adopted in place")
    dirs = args.folders or ["Inbox", "Notes", "Projects", "Sources", "Daily", "Templates", "Attachments"]
    for folder in dirs:
        validate_filename(Path(folder))
    plan = {"operation": "bootstrap-empty-vault", "root": str(target), "directories": [".obsidian", *dirs], "applied": args.apply}
    if args.apply:
        target.mkdir(parents=True, exist_ok=True)
        (target / ".obsidian").mkdir()
        for folder in dirs:
            (target / folder).mkdir()
    emit(plan)


def note_target(root: Path, value: str) -> Path:
    target = safe_path(root, value, suffix=".md")
    validate_filename(target.relative_to(root))
    ensure_existing_parent(root, target)
    return target


def cmd_create(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    before = structure_snapshot(root)
    target = note_target(root, args.path)
    if target.exists():
        raise AmberError(f"refusing to overwrite existing note: {rel(root, target)}")
    body = args.body or ""
    properties = parse_json_object(args.properties)
    if args.template:
        template = safe_path(root, args.template, suffix=".md")
        if not template.is_file():
            raise AmberError(f"template not found: {rel(root, template)}")
        template_props, template_body, present = split_frontmatter(read_text(template))
        template_props.update(properties)
        properties = template_props
        body = template_body + (("\n" + body) if body else "")
        include = present or bool(properties)
    else:
        include = bool(properties)
    text = compose_note(properties, body, include)
    result = write_text(target, text, apply=args.apply)
    result["path"] = rel(root, target)
    result["operation"] = "create-note"
    result["structure_preserved"] = structure_snapshot(root) == before
    emit(result)


def cmd_properties(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    path = safe_path(root, args.path, suffix=".md")
    if not path.is_file():
        raise AmberError(f"note not found: {rel(root, path)}")
    props, body, present = split_frontmatter(read_text(path))
    updates = parse_json_object(args.set)
    for key, value in updates.items():
        if key in props and props[key] is not None and value is not None and type(props[key]) is not type(value):
            raise AmberError(f"property type change refused for {key!r}: {type(props[key]).__name__} -> {type(value).__name__}")
        props[key] = value
    for key in args.remove or []:
        props.pop(key, None)
    result = write_text(path, compose_note(props, body, present or bool(props)), apply=args.apply)
    result.update({"path": rel(root, path), "operation": "set-properties"})
    emit(result)


def cmd_append(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    path = safe_path(root, args.path, suffix=".md")
    if not path.is_file():
        raise AmberError(f"note not found: {rel(root, path)}")
    old = read_text(path)
    separator = "" if old.endswith("\n") else "\n"
    text = old + separator + args.text.rstrip() + "\n"
    result = write_text(path, text, apply=args.apply)
    result.update({"path": rel(root, path), "operation": "append-note"})
    emit(result)


def cmd_move(args: argparse.Namespace) -> None:
    from parse_batch import build_plan, digest, execute, preview
    root = vault_root(args.vault)
    source = safe_path(root, args.source, suffix=".md")
    target = note_target(root, args.destination)
    plan = build_plan({"version": 1, "vault": str(root), "items": [{
        "source": rel(root, source), "source_sha256": digest(source.read_bytes()),
        "disposition": "file", "destination": rel(root, target),
        "reason": "User-directed single-note move",
    }]}, allow_outside_intake=True)
    if args.plan_output:
        output = Path(args.plan_output).resolve()
        if output.is_relative_to(root):
            raise AmberError("save plans outside the vault")
        with output.open("x", encoding="utf-8") as stream:
            json.dump(plan, stream, ensure_ascii=False, indent=2)
    if args.apply:
        if not args.state_dir:
            raise AmberError("move-note --apply requires --state-dir outside the vault on the same filesystem")
        emit(execute(plan, args.state_dir, apply=True))
    else:
        emit(dict(preview(plan), applied=False))


def daily_settings(root: Path) -> dict[str, Any]:
    for name in ("daily-notes.json", "daily-notes/data.json"):
        path = root / ".obsidian" / name
        if path.exists():
            return load_json(path, {})
    return {}


def obsidian_date_format(fmt: str, value: dt.date) -> str:
    replacements = [("YYYY", "%Y"), ("MMMM", "%B"), ("MMM", "%b"), ("MM", "%m"), ("DD", "%d"), ("dddd", "%A"), ("ddd", "%a")]
    result = fmt
    for old, new in replacements:
        result = result.replace(old, new)
    return value.strftime(result)


def cmd_daily(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    cfg = daily_settings(root)
    date = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    fmt = cfg.get("format") or "YYYY-MM-DD"
    folder = cfg.get("folder") or ""
    path = f"{folder}/{obsidian_date_format(fmt, date)}".strip("/")
    template = args.template or cfg.get("template")
    create_args = argparse.Namespace(vault=str(root), path=path, body=args.body, properties=args.properties, template=template, apply=args.apply)
    cmd_create(create_args)


def cmd_attach(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    source = Path(args.source).expanduser().resolve()
    if not source.is_file():
        raise AmberError(f"attachment source not found: {source}")
    note = safe_path(root, args.note, suffix=".md")
    if not note.is_file():
        raise AmberError(f"note not found: {rel(root, note)}")
    cfg_folder = settings(root)["app"].get("attachmentFolderPath")
    folder_value = args.folder or cfg_folder
    if not folder_value or folder_value in {"./", "."}:
        folder = note.parent
    elif folder_value.startswith("./"):
        folder = safe_path(root, f"{rel(root, note.parent)}/{folder_value[2:]}")
    else:
        folder = safe_path(root, folder_value)
    if not folder.is_dir():
        raise AmberError(f"refusing to create attachment directory: {rel(root, folder)}")
    target = folder / (args.name or source.name)
    validate_filename(target.relative_to(root))
    if target.exists():
        raise AmberError(f"attachment destination exists: {rel(root, target)}")
    link_target = rel(root, target)
    original = read_text(note)
    embed = f"![[{link_target}]]"
    updated = original + ("" if original.endswith("\n") else "\n") + embed + "\n"
    plan = {"operation": "attach", "source": str(source), "destination": link_target, "note": rel(root, note), "embed": embed, "applied": args.apply}
    if args.apply:
        shutil.copy2(source, target)
        note.write_text(updated, encoding="utf-8", newline="\n")
    emit(plan)


def cmd_canvas(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    target = safe_path(root, args.path, suffix=".canvas")
    ensure_existing_parent(root, target)
    if target.exists():
        raise AmberError(f"refusing to overwrite Canvas: {rel(root, target)}")
    nodes = json.loads(args.nodes or "[]")
    edges = json.loads(args.edges or "[]")
    data = {"nodes": nodes, "edges": edges}
    temp_text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    result = write_text(target, temp_text, apply=args.apply)
    if args.apply:
        issues = validate_canvas(root, target)
        if issues:
            target.unlink()
            raise AmberError(f"invalid Canvas: {issues}")
    result.update({"path": rel(root, target), "operation": "create-canvas"})
    emit(result)


def cmd_base(args: argparse.Namespace) -> None:
    require_yaml()
    root = vault_root(args.vault)
    target = safe_path(root, args.path, suffix=".base")
    ensure_existing_parent(root, target)
    if target.exists():
        raise AmberError(f"refusing to overwrite Base: {rel(root, target)}")
    data = yaml.safe_load(args.yaml)
    if not isinstance(data, dict):
        raise AmberError("Base YAML must be a top-level mapping")
    text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    result = write_text(target, text, apply=args.apply)
    result.update({"path": rel(root, target), "operation": "create-base"})
    emit(result)


def cmd_query(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    target = safe_path(root, args.path, suffix=".md")
    ensure_existing_parent(root, target)
    block = f"```query\n{args.query.strip()}\n```\n"
    if target.exists() and not args.append:
        raise AmberError(f"refusing to overwrite note: {rel(root, target)}; use --append")
    text = (read_text(target) + ("" if read_text(target).endswith("\n") else "\n") if target.exists() else "") + block
    result = write_text(target, text, apply=args.apply)
    result.update({"path": rel(root, target), "operation": "write-search-query"})
    emit(result)


def cmd_research(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    props = {
        "type": "source",
        "title": args.title,
        "authors": args.author or [],
        "published": args.published or None,
        "accessed": args.accessed or dt.date.today().isoformat(),
        "url": args.url or None,
        "tags": args.tag or [],
        "status": "processed",
    }
    props = {k: v for k, v in props.items() if v is not None}
    sections = [f"# {args.title}", "", "## Relevant claims", "", args.claims or "", "", "## Evidence and locators", "", args.evidence or "", "", "## Interpretation and uncertainty", "", args.interpretation or "", ""]
    cmd_create(argparse.Namespace(vault=str(root), path=args.path, body="\n".join(sections), properties=json.dumps(props), template=None, apply=args.apply))


def cmd_synthesis(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    sources = args.source or []
    basenames, paths = note_index(root)
    resolved: list[str] = []
    missing: list[str] = []
    probe = next(iter(content_files(root, {".md"})), root / "placeholder.md")
    for source in sources:
        status, target = resolve_link(root, LinkRef(probe, source, source, False, "wiki"), basenames, paths)
        if status == "resolved" and target:
            resolved.append(rel(root, target.with_suffix("")))
        else:
            missing.append(source)
    if missing:
        raise AmberError(f"synthesis source links must resolve uniquely: {missing}")
    props = {"type": "synthesis", "status": args.status, "sources": [f"[[{p}]]" for p in resolved]}
    sections = [
        f"# {args.title}", "", "## Conclusion", "", args.conclusion or "",
        "", "## Evidence", "", *[f"- [[{p}]]" for p in resolved],
        "", "## Disagreement and uncertainty", "", args.uncertainty or "",
        "", "## Next research step", "", args.next_step or "", "",
    ]
    cmd_create(argparse.Namespace(vault=str(root), path=args.path, body="\n".join(sections), properties=json.dumps(props), template=None, apply=args.apply))


def cmd_plugins(args: argparse.Namespace) -> None:
    root = vault_root(args.vault)
    cfg = settings(root)
    installed: list[dict[str, Any]] = []
    plugins_dir = root / ".obsidian" / "plugins"
    if plugins_dir.is_dir():
        for manifest in plugins_dir.glob("*/manifest.json"):
            data = load_json(manifest, {})
            installed.append({"id": data.get("id", manifest.parent.name), "name": data.get("name"), "version": data.get("version"), "enabled": data.get("id", manifest.parent.name) in cfg["community_plugins"]})
    emit({"vault": str(root), "core": convention_fingerprint(root)["enabled_core_plugins"], "community": sorted(installed, key=lambda x: x["id"])})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("inspect"); p.add_argument("vault"); p.add_argument("--audit", action="store_true"); p.set_defaults(func=cmd_inspect)
    p = sub.add_parser("validate"); p.add_argument("vault"); p.set_defaults(func=cmd_validate)
    p = sub.add_parser("bootstrap"); p.add_argument("vault"); p.add_argument("--folders", nargs="*"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_bootstrap)

    p = sub.add_parser("create-note"); p.add_argument("vault"); p.add_argument("path"); p.add_argument("--body"); p.add_argument("--properties"); p.add_argument("--template"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_create)
    p = sub.add_parser("set-properties"); p.add_argument("vault"); p.add_argument("path"); p.add_argument("--set"); p.add_argument("--remove", nargs="*"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_properties)
    p = sub.add_parser("append-note"); p.add_argument("vault"); p.add_argument("path"); p.add_argument("text"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_append)
    p = sub.add_parser("move-note"); p.add_argument("vault"); p.add_argument("source"); p.add_argument("destination"); p.add_argument("--apply", action="store_true"); p.add_argument("--state-dir"); p.add_argument("--plan-output"); p.set_defaults(func=cmd_move)
    p = sub.add_parser("daily-note"); p.add_argument("vault"); p.add_argument("--date"); p.add_argument("--body"); p.add_argument("--properties"); p.add_argument("--template"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_daily)
    p = sub.add_parser("attach"); p.add_argument("vault"); p.add_argument("note"); p.add_argument("source"); p.add_argument("--folder"); p.add_argument("--name"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_attach)
    p = sub.add_parser("create-canvas"); p.add_argument("vault"); p.add_argument("path"); p.add_argument("--nodes"); p.add_argument("--edges"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_canvas)
    p = sub.add_parser("create-base"); p.add_argument("vault"); p.add_argument("path"); p.add_argument("--yaml", required=True); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_base)
    p = sub.add_parser("write-query"); p.add_argument("vault"); p.add_argument("path"); p.add_argument("query"); p.add_argument("--append", action="store_true"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_query)
    p = sub.add_parser("research-source"); p.add_argument("vault"); p.add_argument("path"); p.add_argument("--title", required=True); p.add_argument("--author", action="append"); p.add_argument("--published"); p.add_argument("--accessed"); p.add_argument("--url"); p.add_argument("--tag", action="append"); p.add_argument("--claims"); p.add_argument("--evidence"); p.add_argument("--interpretation"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_research)
    p = sub.add_parser("synthesis-note"); p.add_argument("vault"); p.add_argument("path"); p.add_argument("--title", required=True); p.add_argument("--source", action="append", required=True); p.add_argument("--conclusion"); p.add_argument("--uncertainty"); p.add_argument("--next-step"); p.add_argument("--status", default="active"); p.add_argument("--apply", action="store_true"); p.set_defaults(func=cmd_synthesis)
    p = sub.add_parser("plugins"); p.add_argument("vault"); p.set_defaults(func=cmd_plugins)
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        args = build_parser().parse_args(argv)
        args.func(args)
        return 0
    except (AmberError, ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
