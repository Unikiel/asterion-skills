#!/usr/bin/env python3
"""Deterministic checks for a *written* Periplus final brochure.

Important: document checks cannot independently validate web facts. They check that
claimed facts are attributable and the requested scope has a real manuscript.
"""
from __future__ import annotations

import argparse
from datetime import date, timedelta
import json
from pathlib import Path
import re
import sys

REQUIRED = (
    "Arrival & Departure", "Accommodation", "Brief Sketch", "History",
    "Geography", "Climate", "Population", "Politics", "Economy", "Education",
    "Culture", "Transportation", "Attractions & Schedule", "Attractions",
    "Schedule", "Sightseeing & Adventure", "Around Area", "Tours",
    "Delicacy & Shopping", "Restaurant & Café & Bar", "Supermarket & Store & Market",
    "Recommends & Tips", "Tourist Travel Pass & Ticket", "Tourist Center",
    "Tickets & Prices", "Practical Information", "Currency", "Embassy",
    "Important Numbers", "Useful links"
)
TRACKED = ("Administrative Region", "Religion", "International Exchange", "Subculture",
           "Art & Craft", "Architecture", "Museum", "Language & Dialect",
           "Localism", "Sports", "Media", "Literature", "Events & Festivals")
PLACEHOLDERS = (r"\[(?:Attraction|Area|Map|Hotel|Name|Destination|City|Date|YYYY|PHOTO|IMAGE|Restaurant|Store|Tour)[^\]]*\]",
                r"\b(?:TODO|TBD|TBC)\b", r"REPLACE_WITH", r"(?:在此填写|待补充|待研究)")


def assess(project: Path, mode: str):
    errors, warnings = [], []
    for name in ("request.json", "project.json", "TASKS.md", "research/EVIDENCE_LEDGER.md"):
        if not (project / name).is_file():
            errors.append("Missing " + name)
    try:
        request = json.loads((project / "request.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        errors.append("Cannot read request.json")
        return errors, warnings
    out = project / "exports" / "Seven_Ninths_Travel_Brochure.md"
    if not out.exists():
        errors.append("No finished travel brochure exists at exports/Seven_Ninths_Travel_Brochure.md")
        return errors, warnings
    text = out.read_text(encoding="utf-8")
    header_names = [re.sub(r"\s*\{#.+\}\s*$", "", x.strip()).casefold()
                    for x in re.findall(r"^#{1,6}\s+([^\n]+)", text, re.M)]
    for key in REQUIRED:
        if not any(h == key.casefold() or h.startswith(key.casefold() + " ") for h in header_names):
            errors.append("Missing required substantive heading: " + key)
    for category in TRACKED:
        if not any(category.casefold() in h for h in header_names):
            errors.append("Missing inherited historical subcategory: " + category)
    for name, val in (("outbound", request.get("flights", {}).get("outbound", {}).get("flight_number", "")),
                      ("return", request.get("flights", {}).get("return", {}).get("flight_number", ""))):
        if not val or str(val).upper() not in text.upper():
            errors.append(f"Request {name} flight absent from final brochure: {val}")
    try:
        start = date.fromisoformat(request["start_date"])
        end = date.fromisoformat(request["end_date"])
        for offset in range((end - start).days + 1):
            day = (start + timedelta(days=offset)).isoformat()
            if day not in text:
                errors.append(f"Missing day in finished date-specific itinerary: {day}")
    except (KeyError, ValueError):
        errors.append("Invalid request dates")
    if request.get("destination", "").strip().casefold() not in text.casefold():
        errors.append("Primary destination name absent from output")
    if re.search(r"^#{1,3}\s+(?:Cover|Content|Contents|Table of Contents)\s*$", text, re.I | re.M):
        errors.append("Manuscript must not author a manual Cover or Content heading: publisher supplies both")
    if "Around Aera" in text and "Around Area" not in text:
        errors.append("Old typo Around Aera without correct separate Around Area chapter")
    match = re.search(r"^##\s+Around Area(?:\s|$)(.*?)(?=^#{1,2}\s+|\Z)", text, re.M | re.S | re.I)
    if match:
        block = match.group(1)
        if not re.search(r"(往返|当天返回|当日返回|same.day|round.trip|return journey|返回)", block, re.I):
            errors.append("Around Area lacks same-day return-trip analysis")
        place = request.get("destination", "").strip().casefold()
        trips = [h.strip().casefold() for h in re.findall(r"^###\s+([^\n]+)", block, re.M)]
        if place and any(h == place for h in trips):
            errors.append("Main destination incorrectly appears as an Around Area subdestination")
    else:
        errors.append("Around Area must be a real H2 section under Sightseeing & Adventure")
    for pattern in PLACEHOLDERS:
        hit = re.search(pattern, text, re.I)
        if hit:
            errors.append("Unfilled skeleton placeholder: " + hit.group(0))
    if mode == "final":
        cjk = len(re.findall(r"[\u3400-\u9fff]", text))
        words = len(text.split())
        if len(text) < 7000 or len(re.findall(r"\w", text, re.UNICODE)) < 4500:
            errors.append(f"Brochure too brief for completed compendium: {len(text)} characters, {cjk} Han characters")
        links = set(re.findall(r"https?://[^\s\]>]+", text))
        if len(links) < 8:
            errors.append(f"Too few attributable URLs in published brochure: {len(links)} (expected >=8)")
        ledger = (project / "research/EVIDENCE_LEDGER.md")
        if ledger.exists():
            source_urls = set(re.findall(r"https?://[^\s\]|>]+", ledger.read_text(encoding="utf-8")))
            if len(source_urls) < 8:
                errors.append(f"Evidence ledger lacks diversity of actual sources: {len(source_urls)} URL(s)")
        name_index = project / "research/NAME_INDEX.md"
        if not name_index.is_file() or name_index.stat().st_size < 300:
            errors.append("Missing complete research/NAME_INDEX.md for bilingual naming and local pronunciations")
        else:
            idx_text = name_index.read_text(encoding="utf-8")
            if "English" not in idx_text and "英文" not in idx_text:
                errors.append("NAME_INDEX.md missing English name column")
            if "中文" not in idx_text:
                errors.append("NAME_INDEX.md missing Chinese name column")
            destination_country = str(request.get("country", "")).casefold()
            if "japan" in destination_country or "日本" in destination_country:
                if not ("かな" in idx_text or "假名" in idx_text or "よみ" in idx_text):
                    errors.append("Japanese NAME_INDEX.md must track kana readings")
                if not ("romaji" in idx_text.casefold() or "罗马字" in idx_text):
                    errors.append("Japanese NAME_INDEX.md must track romaji pronunciation")
        quality = project / "research/QUALITY_REPORT.md"
        if not quality.is_file() or quality.stat().st_size < 250:
            errors.append("Missing substantive research/QUALITY_REPORT.md")
        if (project / "research/RESEARCH_BLOCKER.md").exists():
            errors.append("Research blocker present: cannot publish as fully researched")
        tasks = (project / "TASKS.md").read_text(encoding="utf-8")
        if "- [ ] " in tasks:
            errors.append("Not all workflow phases are completed")
    return errors, warnings


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", required=True)
    p.add_argument("--mode", choices=["draft", "final"], default="draft")
    args = p.parse_args(argv)
    errors, warnings = assess(Path(args.project).expanduser().resolve(), args.mode)
    for msg in errors:
        print("ERROR:", msg)
    for msg in warnings:
        print("WARN:", msg)
    if errors:
        print(f"FAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS — deterministic document checks passed ({len(warnings)} warnings). Actual web facts still require source review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
