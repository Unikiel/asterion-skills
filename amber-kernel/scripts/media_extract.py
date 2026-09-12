#!/usr/bin/env python3
"""Local extraction of text evidence and URL routing hints for explore.

No downloading, transcription, OCR, or visual interpretation is pretended.
Media requiring another capability is returned as needs-backend, not extracted.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit, urlencode, urlunsplit

from parse_batch import BatchError

LIMIT = 20 * 1024 * 1024
EXTENSIONS = {
    "text": {".txt", ".md", ".csv", ".tsv", ".json", ".xml", ".html", ".htm", ".srt", ".vtt"},
    "document": {".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls", ".epub"},
    "image": {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".tiff", ".bmp", ".avif"},
    "audio": {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus"},
    "video": {".mp4", ".webm", ".mov", ".mkv", ".m4v", ".avi"},
}


def route(url):
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username is not None:
        raise BatchError("provide an HTTP(S) URL without embedded credentials")
    host = parts.hostname.lower()
    pieces = [p for p in parts.path.split("/") if p]
    query = parse_qs(parts.query)
    video = None
    kind = "web"
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtube-nocookie.com", "www.youtube-nocookie.com", "youtu.be"}:
        if host == "youtu.be" and pieces:
            video = pieces[0]
        elif pieces and pieces[0] == "watch":
            video = query.get("v", [None])[0]
        elif len(pieces) > 1 and pieces[0] in {"shorts", "live", "embed"}:
            video = pieces[1]
        if video and re.fullmatch(r"[A-Za-z0-9_-]{11}", video):
            kind = "video"
        elif pieces and (pieces[0].startswith("@") or pieces[0] in {"channel", "c", "user"}):
            kind = "channel"
            video = None
        elif pieces and pieces[0] == "playlist" and query.get("list"):
            kind = "playlist"
            video = None
        else:
            video = None
        return {"url": url, "kind": kind, "platform": "youtube", "video_id": video,
                "playlist_context": query.get("list", [None])[0], "hint_only": True}
    extension = Path(parts.path).suffix.lower()
    for candidate, endings in EXTENSIONS.items():
        if extension in endings:
            kind = candidate
            break
    return {"url": url, "kind": kind, "hint_only": True}


def timestamp(value):
    match = re.fullmatch(r"(?:(\d+):)?(\d{2}):(\d{2})(?:[.,](\d{1,3}))?", value)
    if not match or int(match[2]) >= 60 or int(match[3]) >= 60:
        raise BatchError(f"invalid timestamp: {value}")
    return int(match[1] or 0) * 3600 + int(match[2]) * 60 + int(match[3]) + int((match[4] or "0").ljust(3, "0")) / 1000


def timed_url(url, seconds):
    if not isinstance(seconds, (float, int)) or isinstance(seconds, bool) or seconds < 0:
        raise BatchError("timestamp seconds must be nonnegative")
    target = route(url)
    if target.get("platform") != "youtube" or not target.get("video_id"):
        raise BatchError("timestamp links require an identified YouTube video")
    return "https://www.youtube.com/watch?" + urlencode({"v": target["video_id"], "t": int(seconds)})


def captions(text):
    cues = []
    # Blank lines delimit both SRT and WebVTT cues; cue IDs and style settings
    # are not speech. Preserve timing/overlap instead of inventing alignment.
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip()):
        lines = block.splitlines()
        if not lines or lines[0].startswith(("NOTE", "STYLE", "REGION")):
            continue
        for index, row in enumerate(lines):
            match = re.match(r"\s*(\S+)\s+-->\s+(\S+)", row)
            if not match:
                continue
            start, end = timestamp(match[1]), timestamp(match[2])
            if end < start:
                raise BatchError("subtitle cue ends before it starts")
            words = html.unescape(re.sub(r"<[^>]*>", "", " ".join(lines[index + 1:]))).strip()
            if words:
                cues.append({"start_seconds": start, "end_seconds": end, "text": words})
            break
    if not cues:
        raise BatchError("no timed caption cues found; do not invent transcript timestamps")
    return cues


class TextHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.hidden += 1
        if tag in {"p", "br", "div", "h1", "h2", "h3", "li", "tr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def ooxml(path):
    segments = []
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
        if sum(m.file_size for m in members) > LIMIT:
            raise BatchError("expanded document exceeds the bounded extraction limit")
        names = {m.filename for m in members}
        visuals = any(n.startswith(("word/media/", "ppt/media/", "word/charts/", "ppt/charts/")) for n in names)
        if path.suffix.lower() == ".docx":
            if "word/document.xml" not in names:
                raise BatchError("not a valid DOCX document")
            xml = ET.fromstring(archive.read("word/document.xml"))
            for number, paragraph in enumerate(xml.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"), 1):
                text = "".join(n.text or "" for n in paragraph.iter() if n.tag.endswith("}t"))
                if text.strip():
                    segments.append({"locator": f"paragraph {number}", "text": text})
            if any(n.startswith(("word/header", "word/footer", "word/footnotes", "word/endnotes")) for n in names):
                visuals = True  # Signals content outside this text extraction, not an image claim.
        else:
            slides = sorted((n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)), key=lambda n: int(re.search(r"slide(\d+)", n)[1]))
            if not slides:
                raise BatchError("no slides found in PPTX")
            for name in slides:
                xml = ET.fromstring(archive.read(name))
                text = "\n".join(n.text for n in xml.iter() if n.tag.endswith("}t") and n.text)
                segments.append({"locator": "slide " + re.search(r"slide(\d+)", name)[1], "text": text})
            visuals = True  # Text alone cannot establish the rendered slide's meaning.
    return {"status": "extracted" if segments else "partial", "coverage": "text-only", "segments": segments,
            "additional_inspection_required": visuals,
            "limitation": "Layout, visuals, notes, and other non-body content are not interpreted."}


def extract(path, encoding="utf-8-sig"):
    path = Path(path).resolve()
    if not path.is_file() or path.stat().st_size > LIMIT:
        raise BatchError("input must be a file of at most 20 MiB")
    suffix = path.suffix.lower()
    if suffix in {".docx", ".pptx"}:
        return dict(ooxml(path), path=str(path))
    if suffix == ".pdf":
        if importlib.util.find_spec("pypdf") is None:
            return {"status": "needs-backend", "path": str(path), "required": "PDF extraction/rendering tool or pypdf"}
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            return {"status": "needs-backend", "path": str(path), "required": "authorized access to the encrypted PDF"}
        segments = [{"locator": f"page {number}", "text": page.extract_text() or ""} for number, page in enumerate(reader.pages, 1)]
        return {"status": "extracted" if all(s["text"].strip() for s in segments) else "partial", "coverage": "text-only", "segments": segments,
                "additional_inspection_required": True, "limitation": "Scans, figures and layout need separate visual/OCR inspection."}
    if suffix in EXTENSIONS["text"]:
        text = path.read_text(encoding=encoding)
        if suffix in {".srt", ".vtt"}:
            return {"status": "extracted", "coverage": "caption-text-only", "segments": captions(text),
                    "limitation": "Caption accuracy, audio delivery, and visuals have not been verified."}
        if suffix in {".html", ".htm"}:
            parser = TextHTML()
            parser.feed(text)
            text = "\n".join(row.strip() for row in "".join(parser.parts).splitlines() if row.strip())
        return {"status": "extracted" if text.strip() else "partial", "coverage": "text-only", "segments": [{"locator": "file text", "text": text}]}
    for kind in ("image", "audio", "video"):
        if suffix in EXTENSIONS[kind]:
            return {"status": "needs-backend", "path": str(path), "kind": kind,
                    "required": {"image": "actual visual inspection and OCR where useful", "audio": "audio-capable tool or transcript/ASR", "video": "caption/audio extraction and visual inspection"}[kind]}
    return {"status": "needs-backend", "path": str(path), "required": "format-appropriate extraction tool"}


def capabilities():
    return {"built_in": ["UTF text", "HTML text", "SRT", "WebVTT", "DOCX body text", "PPTX slide text"],
            "optional_modules": {name: importlib.util.find_spec(name) is not None for name in ("pypdf", "PIL", "faster_whisper", "whisper", "yt_dlp")},
            "optional_executables": {name: shutil.which(name) for name in ("ffmpeg", "ffprobe", "tesseract")},
            "note": "Presence is discovery only; speech/OCR/download tools are not invoked by this helper."}


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("capabilities")
    p = commands.add_parser("route"); p.add_argument("url")
    p = commands.add_parser("extract"); p.add_argument("path"); p.add_argument("--encoding", default="utf-8-sig")
    p = commands.add_parser("timestamp-url"); p.add_argument("url"); p.add_argument("seconds", type=float)
    args = parser.parse_args(argv)
    try:
        result = capabilities() if args.command == "capabilities" else route(args.url) if args.command == "route" else extract(args.path, args.encoding) if args.command == "extract" else {"url": timed_url(args.url, args.seconds)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
