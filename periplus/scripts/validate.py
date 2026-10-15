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
from trip_dates import trip_days, audit_schedule_periods
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
                r"\b(?:TODO|TBD|TBC)\b", r"REPLACE_WITH", r"(?:\u5728\u6b64\u586b\u5199|\u5f85\u8865\u5145|\u5f85\u7814\u7a76)")


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
    journey = request.get("journey", {})
    if not journey and request.get("flights"):
        journey = {key:{"mode":"flight", "service":request["flights"].get(key,{}).get("flight_number","")}
                   for key in ("outbound", "return")}
    for key in ("outbound", "return"):
        leg = journey.get(key, {})
        if not leg.get("mode"):
            errors.append(f"Missing {key} journey mode")
        if key == "outbound":
            start = str(leg.get("origin") or "").strip()
            if not start or start.casefold() not in text.casefold():
                errors.append(f"Outbound origin absent from brochure: {start or '[missing]'}")
        else:
            end = str(leg.get("destination") or "").strip()
            if not end or end.casefold() not in text.casefold():
                errors.append(f"Return final destination absent from brochure: {end or '[missing]'}")
        marker = str(leg.get("service") or leg.get("route") or "").strip()
        if marker and marker.casefold() not in text.casefold():
            errors.append(f"Journey {key} service/route missing in brochure: {marker}")
    hotel = request.get("hotel")
    if hotel and (hotel.get("name") or hotel.get("address")):
        for key in ("name", "address"):
            value = str(hotel.get(key) or "").strip()
            if value and value.casefold() not in text.casefold():
                errors.append(f"User-provided hotel {key} omitted from brochure: {value}")
    try:
        errors.extend(audit_schedule_periods(text, request))
        for travel_day in trip_days(request):
            day = travel_day.isoformat()
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
        if not re.search(r"(\u5f80\u8fd4|\u5f53\u5929\u8fd4\u56de|\u5f53\u65e5\u8fd4\u56de|same.day|round.trip|return journey|\u8fd4\u56de)", block, re.I):
            errors.append("Around Area lacks same-day return-trip analysis")
        place = request.get("destination", "").strip().casefold()
        trips = [h.strip().casefold() for h in re.findall(r"^###\s+([^\n]+)", block, re.M)]
        if place and any(h == place for h in trips):
            errors.append("Main destination incorrectly appears as an Around Area subdestination")
    else:
        errors.append("Around Area must be a real H2 section under Sightseeing & Adventure")
    for pattern in PLACEHOLDERS:
        hit = re.search(pattern, re.sub(r"!\[[^\]]*\]\([^\n]*?\)", "", text), re.I)
        if hit:
            errors.append("Unfilled skeleton placeholder: " + hit.group(0))
    if mode == "final":
        from skeleton_audit import audit_skeleton
        errors.extend(audit_skeleton(text))
        from reader_qa import audit_reader_text, audit_transport_plan
        errors.extend(audit_reader_text(text, request))
        errors.extend(audit_transport_plan(project, text, request))
        cjk = len(re.findall(r"[\u3400-\u9fff]", text))
        words = len(text.split())
        if len(text) < 7000 or len(re.findall(r"\w", text, re.UNICODE)) < 4500:
            errors.append(f"Brochure too brief for completed compendium: {len(text)} characters, {cjk} Han characters")
        try:
            from media_utils import audit_media
            errors.extend(audit_media(project, text, request))
        except ImportError:
            errors.append("Media validator unavailable")
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
            if "English" not in idx_text and "\u82f1\u6587" not in idx_text:
                errors.append("NAME_INDEX.md missing English name column")
            if "\u4e2d\u6587" not in idx_text and "Chinese" not in idx_text:
                errors.append("NAME_INDEX.md missing Chinese name column")
            destination_country = str(request.get("country", "")).casefold()
            if "japan" in destination_country or "\u65e5\u672c" in destination_country:
                if not ("\u304b\u306a" in idx_text or "\u5047\u540d" in idx_text or "\u3088\u307f" in idx_text or "kana" in idx_text.casefold()):
                    errors.append("Japanese NAME_INDEX.md must track kana readings")
                if not ("romaji" in idx_text.casefold() or "\u7f57\u9a6c\u5b57" in idx_text):
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
