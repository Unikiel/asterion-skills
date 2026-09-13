"""Shared vault paths, snapshots, frontmatter, and integrity validation."""
from __future__ import annotations
import json
import os
import re
from pathlib import Path, PurePosixPath
import yaml
from scripts.vault_links import link_issues

EXCLUDED = {".obsidian", ".trash", ".git", ".cache", "__pycache__", "node_modules"}


class BatchError(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key, value in node.value:
        key = loader.construct_object(key, deep=deep)
        if key in result:
            raise BatchError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def root_path(value: str) -> Path:
    root = Path(value).expanduser().resolve()
    if not root.is_dir() or not (root / ".obsidian").is_dir():
        raise BatchError("vault must be an existing root containing .obsidian")
    return root


def safe_path(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise BatchError(f"expected a vault-relative path with /: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"..", "."} or part.casefold() in EXCLUDED for part in path.parts):
        raise BatchError(f"unsafe or excluded path: {value}")
    for part in path.parts:
        if re.search(r'[<>:"|?*\x00-\x1f]', part) or part.endswith((".", " ")) or re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", part, re.I):
            raise BatchError(f"non-portable path: {value}")
    target = root.joinpath(*path.parts)
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise BatchError(f"linked paths are unsupported: {value}")
    if not target.resolve().is_relative_to(root):
        raise BatchError(f"path escapes vault: {value}")
    if not target.parent.is_dir():
        raise BatchError(f"destination parent must already exist: {value}")
    return target


def snapshot(root: Path) -> tuple[dict[str, bytes], list[str]]:
    files = {}
    directories = []
    for directory, children, names in os.walk(root, followlinks=False):
        current = Path(directory)
        children[:] = sorted(c for c in children if c.casefold() not in EXCLUDED)
        for child in children:
            p = current / child
            if p.is_symlink() or not p.resolve().is_relative_to(root):
                raise BatchError(f"linked directory unsupported: {p}")
            directories.append(p.relative_to(root).as_posix())
        for name in sorted(names):
            p = current / name
            relative = p.relative_to(root).as_posix()
            safe_path(root, relative)
            files[relative] = p.read_bytes()
    return files, sorted(directories)


def properties(data: bytes) -> dict:
    text = data.decode("utf-8-sig")
    if not re.match(r"^---\r?\n", text):
        return {}
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        raise BatchError("unterminated frontmatter")
    props = yaml.load(match[1], Loader=UniqueLoader) or {}
    if not isinstance(props, dict):
        raise BatchError("frontmatter must be a mapping")
    return props


def format_issues(files: dict[str, bytes]) -> set[tuple[str, str, str]]:
    issues = set()
    for name, content in files.items():
        try:
            if name.lower().endswith(".md"):
                properties(content)
            elif name.lower().endswith(".base"):
                if not isinstance(yaml.load(content.decode("utf-8-sig"), Loader=UniqueLoader), dict):
                    raise BatchError("Base must be a mapping")
            elif name.lower().endswith(".canvas"):
                data = json.loads(content)
                nodes, edges = data.get("nodes", []), data.get("edges", [])
                ids = [node.get("id") for node in nodes]
                edge_ids = [edge.get("id") for edge in edges]
                if any(not isinstance(i, str) or not i for i in ids + edge_ids) or len(set(ids)) != len(ids) or len(set(edge_ids)) != len(edge_ids):
                    raise BatchError("invalid or duplicate Canvas IDs")
                for edge in edges:
                    if edge.get("fromNode") not in ids or edge.get("toNode") not in ids:
                        raise BatchError("dangling Canvas edge")
                for node in nodes:
                    if node.get("type") == "file" and str(node.get("file", "")).split("#", 1)[0] not in files:
                        raise BatchError("missing Canvas file: " + str(node.get("file")))
        except (ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
            issues.add((name, "invalid-format", str(exc)))
    return issues


def all_issues(files):
    return format_issues(files) | link_issues(files)

