"""Conservative reference resolution for planned vault edits (standard library).

Unsupported dynamic references stop an affected move rather than receiving a
textual search/replace. This is deliberately not a complete Markdown parser.
"""
from __future__ import annotations

import json
import posixpath
import re
from dataclasses import dataclass
from urllib.parse import quote, unquote


class ReferenceError(ValueError):
    pass


@dataclass
class Reference:
    start: int
    end: int
    target: str
    kind: str


def visible(text: str) -> str:
    """Mask literal code/comments without shifting link offsets."""
    result = list(text)
    fence = None
    offset = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip())
        if fence:
            for i in range(offset, offset + len(line)):
                result[i] = "\n" if text[i] == "\n" else " "
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
            result[offset:offset + len(line)] = ["\n" if c == "\n" else " " for c in line]
        offset += len(line)
    masked = "".join(result)
    for pattern in (r"<!--.*?-->", r"(?<!`)`+[^`\n]*`+(?!`)"):
        masked = re.sub(pattern, lambda m: " " * len(m[0]), masked, flags=re.S)
    return masked


def references(text: str) -> list[Reference]:
    masked = visible(text)
    result = []
    for m in re.finditer(r"(?<!!)(?:!)?\[\[([^\]\n]+)\]\]", masked):
        raw = m[1].split("|", 1)[0]
        result.append(Reference(m.start(1), m.start(1) + len(raw), raw, "wiki"))
    # Inline destinations support angle brackets, titles and balanced parentheses.
    for m in re.finditer(r"!?\[(?:\\.|[^\]\n])*\]\(", masked):
        start = m.end()
        while start < len(masked) and masked[start] in " \t":
            start += 1
        if start == len(masked):
            continue
        if masked[start] == "<":
            end = masked.find(">", start + 1)
            if end != -1:
                result.append(Reference(start + 1, end, text[start + 1:end], "markdown"))
            continue
        end, depth = start, 0
        while end < len(masked):
            c = masked[end]
            if c == "\\":
                end += 2
                continue
            if c == "(":
                depth += 1
            elif c == ")":
                if not depth:
                    break
                depth -= 1
            elif c.isspace() and not depth:
                break
            end += 1
        if end > start:
            result.append(Reference(start, end, text[start:end], "markdown"))
    # Reference-style Markdown links: update the definition, not each usage.
    for m in re.finditer(r"^ {0,3}\[[^\]\n]+\]:[ \t]*(?:<([^>\n]+)>|(\S+))", masked, re.M):
        group = 1 if m[1] is not None else 2
        result.append(Reference(m.start(group), m.end(group), m[group], "markdown"))
    return sorted(result, key=lambda r: r.start)


def split_target(raw: str) -> tuple[str, str]:
    path, separator, anchor = raw.partition("#")
    return path, separator + anchor


def resolve(source: str, raw: str, kind: str, files: set[str]) -> tuple[str, str | None]:
    path, _ = split_target(raw)
    path = unquote(path).replace("\\", "/")
    if re.match(r"^[a-z][a-z0-9+.-]*:", path, re.I) or path.startswith("//"):
        return "external", None
    if not path:
        return "resolved", source
    lookup: dict[str, list[str]] = {}
    for name in files:
        lookup.setdefault(name.casefold(), []).append(name)

    def exact(candidate: str) -> list[str]:
        normalized = posixpath.normpath(candidate).lstrip("/")
        if normalized == ".." or normalized.startswith("../"):
            return []
        found = lookup.get(normalized.casefold(), [])
        if not found and not posixpath.splitext(normalized)[1]:
            found = lookup.get((normalized + ".md").casefold(), [])
        return found

    if kind == "markdown":
        candidates = exact(path if path.startswith("/") else posixpath.join(posixpath.dirname(source), path))
    elif "/" in path:
        candidates = exact(posixpath.join(posixpath.dirname(source), path)) if path.startswith(".") else exact(path)
    else:
        # With duplicate basenames, require an explicit path; never guess a
        # renderer-specific nearest-note preference during an automatic move.
        candidates = [name for name in files if posixpath.basename(name).casefold() in
                      {path.casefold(), (path + ".md").casefold()}]
    if len(candidates) == 1:
        return "resolved", candidates[0]
    return ("ambiguous" if candidates else "unresolved"), None


def anchor_exists(text: str, anchor: str) -> bool:
    anchor = unquote(anchor.lstrip("#"))
    if not anchor:
        return True
    if anchor.startswith("^"):
        return re.search(r"(?:^|\s)" + re.escape(anchor) + r"\s*$", visible(text), re.M) is not None
    headings = re.findall(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", visible(text), re.M)
    canonical = lambda s: re.sub(r"[^\w\s-]", "", s).strip().casefold()
    return any(canonical(h) == canonical(anchor) or canonical(h).replace(" ", "-") == canonical(anchor)
               for h in headings)


def link_issues(files: dict[str, bytes]) -> set[tuple[str, str, str]]:
    issues = set()
    names = set(files)
    for name, content in files.items():
        if not name.lower().endswith(".md"):
            continue
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            continue
        for ref in references(text):
            status, target = resolve(name, ref.target, ref.kind, names)
            if status not in {"resolved", "external"}:
                issues.add((name, status, ref.target))
            elif target and target.lower().endswith(".md"):
                _, anchor = split_target(ref.target)
                if anchor and not anchor_exists(files[target].decode("utf-8-sig"), anchor):
                    issues.add((name, "missing-anchor", ref.target))
    return issues


def rewrite_markdown(old_name: str, new_name: str, content: bytes,
                     moves: dict[str, str], before: set[str], after: set[str]) -> bytes:
    text = content.decode("utf-8-sig")
    edits = []
    for ref in references(text):
        status, target = resolve(old_name, ref.target, ref.kind, before)
        path, anchor = split_target(ref.target)
        if not path:
            continue
        if status == "ambiguous" and any(posixpath.basename(s).removesuffix(".md").casefold() ==
                                          posixpath.basename(unquote(path)).removesuffix(".md").casefold()
                                          for s in moves):
            raise ReferenceError(f"ambiguous link in {old_name}: {ref.target}")
        if target is None:
            continue
        destination = moves.get(target, target)
        # Leave a reference alone when it still resolves to the intended target.
        if resolve(new_name, ref.target, ref.kind, after) == ("resolved", destination):
            continue
        if ref.kind == "wiki":
            replacement = destination[:-3] if destination.lower().endswith(".md") and not path.lower().endswith(".md") else destination
        else:
            replacement = quote(posixpath.relpath(destination, posixpath.dirname(new_name) or "."), safe="/.-_~")
        edits.append((ref.start, ref.end, replacement + anchor))
    for start, end, value in reversed(edits):
        text = text[:start] + value + text[end:]
    if not edits:
        return content
    return (b"\xef\xbb\xbf" if content.startswith(b"\xef\xbb\xbf") else b"") + text.encode("utf-8")


def repair_references(before: dict[str, bytes], after: dict[str, bytes], moves: dict[str, str]) -> dict[str, bytes]:
    """Repair understood references; defer moves with relevant executable queries."""
    if not moves:
        return after
    result = dict(after)
    inverse = {v: k for k, v in moves.items()}
    needles = {part.casefold() for old in moves for part in (old, old.removesuffix(".md"), posixpath.basename(old), posixpath.dirname(old)) if part}
    for name, content in after.items():
        if not name.lower().endswith((".md", ".base", ".canvas")):
            continue
        text = content.decode("utf-8-sig")
        original_name = inverse.get(name, name)
        if name.lower().endswith(".md"):
            queries = re.findall(r"(?ms)^ {0,3}(?:`{3,}|~{3,})(?:dataview\w*|query|tasks|templater)\b.*?^ {0,3}(?:`{3,}|~{3,})\s*$", text)
            queries += re.findall(r"`\$?=[^`]+`", text)
            if any(any(n in q.casefold() for n in needles) or "dataviewjs" in q.casefold() for q in queries):
                raise ReferenceError(f"query dependency needs review before moving: {name}")
            if re.search(r"<(?:a|img)\b", text, re.I) and any(n in text.casefold() for n in needles):
                raise ReferenceError(f"HTML reference needs review before moving: {name}")
            result[name] = rewrite_markdown(original_name, name, content, moves, set(before), set(after))
        elif name.lower().endswith(".base"):
            # Dynamic Base formulas are not safe to transform with string replacement.
            if any(n in text.casefold() for n in needles):
                raise ReferenceError(f"Base dependency needs review before moving: {name}")
        else:
            canvas = json.loads(text)
            changed = False
            for node in canvas.get("nodes", []):
                if node.get("type") == "file":
                    path, anchor = split_target(str(node.get("file", "")))
                    for old, new in moves.items():
                        if path.casefold() == old.casefold():
                            node["file"] = new + anchor
                            changed = True
                elif node.get("type") == "text" and node.get("text"):
                    repaired = rewrite_markdown(original_name, name, node["text"].encode(), moves, set(before), set(after)).decode()
                    changed |= repaired != node["text"]
                    node["text"] = repaired
            if changed:
                result[name] = (json.dumps(canvas, ensure_ascii=False, indent=2) + "\n").encode()
    return result
