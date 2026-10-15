#!/usr/bin/env python3
"""Hard-fail audit of the canonical, immutable Seven Ninths section headings.

The source template contains example/place-specific headings; only fixed topic
headings and Maps A-J are locked. Working-only appendices are audited
separately so procedural material cannot leak into the published brochure.
"""
from __future__ import annotations
import argparse
from collections import Counter
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKELETON = ROOT / 'assets' / 'Seven_Ninths_Master_Skeleton.md'
TOPICS = {
    'Arrival & Departure', 'Accommodation', 'Brief Sketch', 'Attractions & Schedule',
    'Sightseeing & Adventure', 'Delicacy & Shopping', 'Recommends & Tips',
}
NOT_PUBLISHED = {'COVER', 'Content', 'Appendix / Working Notes'}
# Route-mode options are source-data-driven; all other inherited topical headings are compulsory.
MODE_ONLY = {'Flight', 'Airport Bus', 'Other Transfer', 'Primary Journey', 'Railway'}


def get_fixed_headings(template: str | None = None):
    """Read the English-only canonical template, preserving original title levels."""
    source = template if template is not None else SKELETON.read_text(encoding='utf8')
    fixed = []
    in_private_appendix = False
    for m in re.finditer(r'^(#{1,3})\s+([^\n]+)', source, re.M):
        level, label = len(m.group(1)), m.group(2).strip()
        if label.startswith('Appendix / Working Notes'):
            in_private_appendix = True
        if in_private_appendix:
            continue
        if level == 1 and label not in TOPICS:
            continue
        if label.startswith('Map ') and re.match(r'Map [A-J]\s+[\u2013\u2014-]', label):
            match = re.match(r'Map ([A-J])', label)
            if match:
                fixed.append((3, f'Map {match.group(1)}'))
            continue
        if '`' in label or label.startswith('['):
            continue
        # Existing modal qualifiers describe when transport headings are relevant.
        label = re.sub(r'\s*\([^)]*(?:actual journey|actual modes)[^)]*\)\s*$', '', label)
        label = label.split(' (use the actual modes)')[0]
        if label.startswith('Primary Journey'):
            continue
        if label in MODE_ONLY:
            continue
        if label.startswith('Appendix / Working Notes'):
            continue
        if label in ('Around Aera',):
            raise ValueError('Canonical skeleton still contains old Around Aera typo')
        fixed.append((level, label))
    return list(dict.fromkeys(fixed))


def normalize(label):
    return re.sub(r'\s+', ' ', label.strip())


def title_is(label, fixed):
    actual = normalize(label)
    if fixed.startswith('Map '):
        return bool(re.fullmatch(re.escape(fixed) + r'\s+[\-\u2013\u2014]\s+.+', actual))
    return actual == fixed or actual.startswith(fixed + ' \u2014 ') or actual.startswith(fixed + ' - ')


def audit_skeleton(manuscript: str):
    errors = []
    tokens = [(len(m.group(1)), normalize(m.group(2)), m.start()) for m in re.finditer(r'^(#{1,6})\s+([^\n]+)', manuscript, re.M)]
    if not tokens:
        return ['Manuscript is missing Markdown headings']
    # Assess the required hierarchy, not merely whether topic words appear on any page.
    template = SKELETON.read_text(encoding='utf8')
    expected_context = {}
    ancestor_h1 = ancestor_h2 = ''
    for m in re.finditer(r'^(#{1,3})\s+([^\n]+)',template,re.M):
        lev, label = len(m.group(1)), m.group(2).strip()
        if label.startswith('Appendix / Working Notes'): break
        if lev == 1:
            ancestor_h1, ancestor_h2 = label, ''
        elif lev == 2:
            ancestor_h2 = label
        for fixed_lvl, fixed_label in get_fixed_headings():
            if fixed_lvl == lev and (label == fixed_label or (fixed_label.startswith('Map ') and label.startswith(fixed_label + ' '))):
                expected_context.setdefault((fixed_lvl,fixed_label),(ancestor_h1,ancestor_h2))
    # Precompute the H1/H2 owner of each actual heading.
    annotated=[]
    in_h1 = in_h2 = ''
    for lev, name, pos in tokens:
        if lev == 1: in_h1, in_h2 = name, ''
        elif lev == 2: in_h2 = name
        annotated.append((lev,name,pos,in_h1,in_h2))
    for lvl, name in get_fixed_headings():
        eligible = [r for r in annotated if r[0] == lvl and title_is(r[1],name)]
        if not eligible:
            errors.append(f'Missing / renamed / wrong-level immutable heading: H{lvl} {name}')
            continue
        parent1,parent2 = expected_context.get((lvl,name),('',''))
        if parent1 in TOPICS and not any(title_is(r[3],parent1) and (lvl != 3 or not parent2 or '`' in parent2 or parent2.startswith('[') or title_is(r[4],parent2)) for r in eligible):
            errors.append(f'Wrong parent for immutable heading: H{lvl} {name}; expected {parent1} / {parent2}')
    if any(re.search(r'\bAround Aera\b', name) for _, name, _ in tokens):
        errors.append('Historical typo Around Aera is not permitted; use Around Area')
    if any(lvl == 1 and name not in TOPICS for lvl, name, _ in tokens):
        bad = [name for lvl, name, _ in tokens if lvl == 1 and name not in TOPICS]
        errors.append(f'Unapproved additional/replaced H1 headings: {bad}')
    # Reject obvious markup in titles that inverts bilingual order.
    for lvl, name, _ in tokens:
        if name.startswith(('Map ', 'Arrival - ', 'Departure - ')):
            continue
        han = re.search(r'[\u3400-\u9fff]', name)
        latin = re.search(r'[A-Za-z]', name)
        if han and (not latin or latin.start() > han.start()):
            errors.append(f'Title must begin in English, then Chinese where present (H{lvl}): {name}')
    # Fixed H1 chapter order is contractual; title-only boilerplate sections are not accepted.
    canonical = ['Arrival & Departure','Accommodation','Brief Sketch','Attractions & Schedule',
                 'Sightseeing & Adventure','Delicacy & Shopping','Recommends & Tips']
    positions = []
    for name in canonical:
        hits = [pos for lvl, label, pos in tokens if lvl == 1 and title_is(label, name)]
        if len(hits) != 1:
            errors.append(f'Expected exactly one H1 {name}; got {len(hits)}')
        elif hits:
            positions.append(hits[0])
    if positions != sorted(positions):
        errors.append('Historical H1 chapter order has been changed')
    if re.search(r'^#{1,6}\s+(?:Appendix / Working Notes|Visual Asset Checklist|Final QA Checklist|Structural Coverage Audit)(?:\s|$)',manuscript,re.M):
        errors.append('Private skeleton/QA appendix must not be published in the guide')
    if re.search(r'^#{1,6}\s+(?:Content|COVER)\s*$',manuscript,re.M):
        errors.append('Cover and Content are generated by exporter and must not be manuscript sections')
    return errors


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--project',type=Path,required=True)
    a=ap.parse_args(argv)
    p=a.project/'exports/Seven_Ninths_Travel_Brochure.md'
    if not p.is_file():
        print('FAIL: manuscript missing',p);return 2
    errors=audit_skeleton(p.read_text(encoding='utf8'))
    if errors:
        for error in errors: print('FAIL:',error)
        return 1
    print('PASS: immutable headings, chapter order, title language order and no internal appendix')
    return 0

if __name__=='__main__':raise SystemExit(main())
