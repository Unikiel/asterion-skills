#!/usr/bin/env python3
"""Plan and apply agent-authored intake decisions; never infer their meaning.

State is explicit, local and outside the vault. Applying a saved plan is
repeatable; recover can finish or roll back interrupted work without clobbering
files that no longer match either recorded version.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path, PurePosixPath

# Locate shared modules when invoked directly from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from typing import Any

import yaml

from scripts.vault_state import BatchError, UniqueLoader, root_path, safe_path, snapshot, properties, format_issues, all_issues
from scripts.vault_links import ReferenceError, link_issues, repair_references


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def load_json(path: str | Path) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise BatchError("expected a JSON object")
    return value


def effective_options(manifest: dict, preferences: dict | None = None) -> dict:
    result = {"develop": False, "integrate": False}
    for values in ((preferences or {}).get("options", {}), manifest.get("options", {})):
        if not isinstance(values, dict) or any(k not in result or type(v) is not bool for k, v in values.items()):
            raise BatchError("options accept only boolean develop and integrate")
        result.update(values)
    return result


def encode(data: bytes | None):
    return None if data is None else base64.b64encode(data).decode("ascii")


def decode(data: str | None):
    return None if data is None else base64.b64decode(data, validate=True)


def build_plan(manifest: dict, preferences: dict | None = None, *, allow_outside_intake=False) -> dict:
    if manifest.get("version") != 1:
        raise BatchError("manifest version must be 1")
    root = root_path(manifest["vault"])
    before, directories = snapshot(root)
    after = dict(before)
    intake = manifest.get("intake", "LandingField").rstrip("/")
    if not allow_outside_intake and not safe_path(root, intake).is_dir():
        raise BatchError("intake directory does not exist")
    options = effective_options(manifest, preferences)
    moves, items, owned = {}, [], set()
    if not isinstance(manifest.get("items"), list):
        raise BatchError("items must be a list")

    def claim(path):
        safe_path(root, path)
        key = path.casefold()
        if key in owned:
            raise BatchError(f"multiple changes to {path}; combine them into one item")
        owned.add(key)

    for item in manifest["items"]:
        source = item["source"]
        safe_path(root, source)
        if not allow_outside_intake and not source.startswith(intake + "/"):
            raise BatchError(f"source outside selected intake: {source}")
        if source not in before or digest(before[source]) != item.get("source_sha256"):
            raise BatchError(f"source missing or changed: {source}")
        if not isinstance(item.get("reason"), str) or not item["reason"].strip():
            raise BatchError("each item needs a disposition reason")
        disposition = item.get("disposition")
        if disposition not in {"file", "retain", "integrate", "defer"}:
            raise BatchError(f"unknown disposition: {disposition}")
        claim(source)
        if type(item.get("developed", False)) is not bool:
            raise BatchError("developed must be a boolean")
        if item.get("developed") and not options["develop"]:
            raise BatchError("development is not enabled")
        if (item.get("integrations") or disposition == "integrate") and not options["integrate"]:
            raise BatchError("integration is not enabled")
        if disposition == "defer":
            if any(k in item for k in ("destination", "text", "outputs", "integrations")) or item.get("developed"):
                raise BatchError("deferred items cannot contain changes")
            items.append(dict(item))
            continue
        destination = item.get("destination", source)
        if disposition == "file" and destination == source:
            raise BatchError("file disposition requires a distinct destination")
        if destination != source:
            claim(destination)
            if any(p.casefold() == destination.casefold() for p in before):
                raise BatchError(f"destination collision: {destination}")
            moves[source] = destination
            del after[source]
        content = before[source]
        if "text" in item:
            if not source.lower().endswith((".md", ".txt")) or not isinstance(item["text"], str):
                raise BatchError("only Markdown/plain-text sources accept replacement text")
            content = item["text"].encode("utf-8")
        if Path(source).suffix.lower() != Path(destination).suffix.lower():
            raise BatchError("moving a source must preserve its extension")
        after[destination] = content
        for output in item.get("outputs", []):
            path = output["path"]
            claim(path)
            if not path.lower().endswith(".md") or any(p.casefold() == path.casefold() for p in before):
                raise BatchError(f"output must be a new Markdown note: {path}")
            after[path] = output["text"].encode("utf-8")
        for integration in item.get("integrations", []):
            path = integration["path"]
            claim(path)
            if not path.lower().endswith(".md") or path not in before or digest(before[path]) != integration.get("sha256"):
                raise BatchError(f"integration target missing or changed: {path}")
            after[path] = integration["text"].encode("utf-8")
        items.append(dict(item, destination=destination))

    after = repair_references(before, after, moves)
    previous = {(moves.get(path, path), kind, detail) for path, kind, detail in all_issues(before)}
    regressions = all_issues(after) - previous
    if regressions:
        raise BatchError("new integrity findings: " + json.dumps(sorted(regressions), ensure_ascii=False))
    inverse = {v: k for k, v in moves.items()}
    established_types = {}
    for path, content in before.items():
        if path.lower().endswith(".md"):
            try:
                for key, value in properties(content).items():
                    if value is not None:
                        established_types.setdefault(key, set()).add(type(value))
            except (ValueError, yaml.YAMLError):
                pass
    for path, content in after.items():
        original = inverse.get(path, path)
        if path.lower().endswith(".md") and content != before.get(original):
            for key, value in properties(content).items():
                known = established_types.get(key, set())
                if value is not None and len(known) == 1 and type(value) not in known:
                    raise BatchError(f"property type conflicts with vault convention in {path}: {key}")
        if path.lower().endswith(".md") and original in before and content != before[original]:
            old_props, new_props = properties(before[original]), properties(content)
            for key in old_props.keys() & new_props.keys():
                if type(old_props[key]) is not type(new_props[key]):
                    raise BatchError(f"property type change in {path}: {key}")
    changed = [path for path in sorted(set(before) | set(after)) if before.get(path) != after.get(path)]
    # Write destinations and repairs before removing move sources.
    changed.sort(key=lambda p: (p not in after, p))
    plan = {
        "version": 1, "vault": str(root), "intake": intake, "options": options,
        "run_nonce": manifest.get("run_nonce"),
        "directories": directories, "readset": {p: digest(b) for p, b in before.items()},
        "moves": moves, "items": items, "baseline_issues": sorted(previous),
        "changes": [{"path": p, "before": encode(before.get(p)), "after": encode(after.get(p))} for p in changed],
    }
    plan["id"] = digest(canonical(plan))
    return plan


def verify_plan(plan):
    if plan.get("version") != 1 or plan.get("id") != digest(canonical({k: v for k, v in plan.items() if k != "id"})):
        raise BatchError("plan integrity check failed; rebuild rather than editing a saved plan")


def state_path(value: str, root: Path) -> Path:
    state = Path(value).expanduser().resolve()
    if not state.is_dir() or state.is_relative_to(root):
        raise BatchError("state-dir must be an existing directory outside the vault")
    if state.stat().st_dev != root.stat().st_dev:
        raise BatchError("state-dir must be on the vault's filesystem for atomic writes")
    return state


def atomic_json(path: Path, value):
    fd, temporary = tempfile.mkstemp(prefix=".amber-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(canonical(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def state_lock(state):
    with (state / "amber-kernel.lock").open("a+b") as lock:
        lock.seek(0, 2)
        if not lock.tell():
            lock.write(b"0")
            lock.flush()
        lock.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise BatchError("another operation is using this state directory") from exc
        try:
            yield
        finally:
            lock.seek(0)
            if os.name == "nt":
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lock, fcntl.LOCK_UN)


def current_bytes(path):
    return path.read_bytes() if path.is_file() else None


def preconditions(plan, root, *, partial=False):
    current, directories = snapshot(root)
    if directories != plan["directories"]:
        raise BatchError("directory tree changed since planning")
    changes = {c["path"]: c for c in plan["changes"]}
    expected_names = set(plan["readset"])
    if set(current) - expected_names - set(changes):
        raise BatchError("vault files were added since planning; rebuild the plan")
    for name in expected_names | set(changes):
        data = current.get(name)
        if name in changes:
            change = changes[name]
            allowed = [decode(change["before"])]
            if partial:
                allowed.append(decode(change["after"]))
            if data not in allowed:
                raise BatchError(f"concurrent edit or collision: {name}")
        elif data is None or digest(data) != plan["readset"][name]:
            raise BatchError(f"context changed since planning: {name}")


def write_change(root, change, *, rollback=False, staging_dir=None):
    path = safe_path(root, change["path"])
    before, after = decode(change["before"]), decode(change["after"])
    expected, desired = (after, before) if rollback else (before, after)
    current = current_bytes(path)
    if current == desired:
        return
    if current != expected:
        raise BatchError(f"concurrent edit: {change['path']}")
    if desired is None:
        path.unlink()
    else:
        fd, temporary = tempfile.mkstemp(prefix=".amber-", dir=staging_dir)
        try:
            with os.fdopen(fd, "wb") as output:
                output.write(desired)
                output.flush()
                os.fsync(output.fileno())
            if current_bytes(path) != expected:
                raise BatchError(f"concurrent edit: {change['path']}")
            if current is None:
                # Atomic, exclusive creation: never replace an unexpected target.
                os.link(temporary, path)
            else:
                os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


def preview(plan):
    return {"id": plan["id"], "vault": plan["vault"], "options": plan["options"],
            "items": [{k: i[k] for k in ("source", "destination", "disposition", "reason", "developed") if k in i} for i in plan["items"]],
            "changes": [{"path": c["path"], "operation": "create" if c["before"] is None else "remove-moved-source" if c["after"] is None else "edit"} for c in plan["changes"]],
            "baseline_issue_count": len(plan["baseline_issues"])}


def execute(plan, state_dir, *, apply=False, recover=False, rollback=False):
    verify_plan(plan)
    root = root_path(plan["vault"])
    state = state_path(state_dir, root)
    journal_path = state / (plan["id"] + ".json")
    if not apply:
        return dict(preview(plan), applied=False, recovery=bool(recover), rollback=bool(rollback))
    with state_lock(state):
        journal = load_json(journal_path) if journal_path.exists() else None
        if journal and journal.get("plan") != plan:
            raise BatchError("saved journal does not match this plan")
        if journal and journal["status"] == "verified" and not recover:
            # Report prior completion, never reapply outputs over subsequent user edits.
            return dict(preview(plan), applied=False, status="already-verified", journal=str(journal_path))
        if journal and journal["status"] == "rolled-back":
            raise BatchError("this run was rolled back; build a new plan with a new run nonce")
        if journal and not recover:
            raise BatchError("unfinished run exists; use recover to resume or roll back")
        if recover and journal is None:
            raise BatchError("no saved run to recover")
        if rollback and not recover:
            raise BatchError("rollback requires recover")
        if rollback:
            # Only affected files matter for undo; unrelated later work is preserved.
            for c in plan["changes"]:
                if current_bytes(safe_path(root, c["path"])) not in [decode(c["before"]), decode(c["after"])]:
                    raise BatchError(f"cannot undo a subsequently edited file: {c['path']}")
        else:
            preconditions(plan, root, partial=recover)
        journal = journal or {"plan": plan, "status": "prepared"}
        journal["status"] = "rolling-back" if rollback else "applying"
        atomic_json(journal_path, journal)
        try:
            for change in reversed(plan["changes"]) if rollback else plan["changes"]:
                write_change(root, change, rollback=rollback, staging_dir=state)
            files, directories = snapshot(root)
            for change in plan["changes"]:
                if files.get(change["path"]) != decode(change["before"] if rollback else change["after"]):
                    raise BatchError("post-write content verification failed")
            if not rollback:
                if directories != plan["directories"] or all_issues(files) - set(map(tuple, plan["baseline_issues"])):
                    raise BatchError("post-write integrity verification failed")
            journal["status"] = "rolled-back" if rollback else "verified"
            journal.pop("error", None)
            atomic_json(journal_path, journal)
        except Exception as exc:
            journal["status"], journal["error"] = "interrupted", str(exc)
            atomic_json(journal_path, journal)
            raise
    return dict(preview(plan), applied=True, status=journal["status"], journal=str(journal_path))


def inventory(vault, intake="LandingField", state_dir=None):
    root = root_path(vault)
    files, directories = snapshot(root)
    if not safe_path(root, intake).is_dir():
        raise BatchError("intake directory does not exist")
    processed = set()
    if state_dir:
        for path in state_path(state_dir, root).glob("*.json"):
            try:
                journal = load_json(path)
                if journal.get("status") == "verified" and journal.get("plan", {}).get("vault") == str(root):
                    for item in journal["plan"]["items"]:
                        if item["disposition"] != "defer":
                            processed.add((item["source"], item["source_sha256"]))
                            destination = item.get("destination", item["source"])
                            for change in journal["plan"]["changes"]:
                                if change["path"] == destination and change["after"] is not None:
                                    processed.add((destination, digest(decode(change["after"])) ))
            except (ValueError, KeyError):
                continue
    entries = []
    index = []
    for path, content in files.items():
        if path.startswith(intake.rstrip("/") + "/"):
            entries.append({"path": path, "sha256": digest(content), "bytes": len(content), "processed": (path, digest(content)) in processed,
                            "text_readable": path.lower().endswith((".md", ".txt"))})
        if path.lower().endswith(".md"):
            try:
                props = properties(content)
                index.append({"path": path, "sha256": digest(content), "title": Path(path).stem,
                              "aliases": props.get("aliases", []), "tags": props.get("tags", [])})
            except (ValueError, yaml.YAMLError):
                index.append({"path": path, "sha256": digest(content), "metadata_error": True})
    return {"vault": str(root), "intake": intake, "items": entries, "index": index, "directories": directories}


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("inventory")
    p.add_argument("vault"); p.add_argument("--intake", default="LandingField"); p.add_argument("--state-dir")
    p = commands.add_parser("plan")
    p.add_argument("manifest"); p.add_argument("--preferences"); p.add_argument("--output")
    for name in ("apply", "recover"):
        p = commands.add_parser(name)
        p.add_argument("plan"); p.add_argument("--state-dir", required=True); p.add_argument("--apply", action="store_true")
        if name == "recover":
            p.add_argument("--rollback", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "inventory":
            result = inventory(args.vault, args.intake, args.state_dir)
        elif args.command == "plan":
            manifest = load_json(args.manifest)
            plan = build_plan(manifest, load_json(args.preferences) if args.preferences else None)
            if args.output:
                output = Path(args.output).resolve()
                if output.is_relative_to(root_path(manifest["vault"])) or output.exists():
                    raise BatchError("plan output must be a new file outside the vault")
                with output.open("x", encoding="utf-8") as stream:
                    json.dump(plan, stream, ensure_ascii=False, indent=2)
            result = preview(plan)
        else:
            result = execute(load_json(args.plan), args.state_dir, apply=args.apply,
                             recover=args.command == "recover", rollback=getattr(args, "rollback", False))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (BatchError, ReferenceError, KeyError, TypeError, OSError, ValueError, yaml.YAMLError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
