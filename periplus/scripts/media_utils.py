#!/usr/bin/env python3
"""Periplus real-media acceptance gates.

Offline validation cannot prove a photo depicts the right place or that map coordinates
are correct. Research phase must verify provenance, license, subject and grounding.
This script rejects empty/broken, uncredited, unembedded or remote-only visuals.
"""
from __future__ import annotations
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import zipfile
from trip_dates import trip_days

ROOT_NAME = 'Seven_Ninths_Travel_Brochure'
IMAGE_PATTERN = re.compile(r'!\[([^\]]+)\]\(([^\s)]+)(?:\s+"[^"]*")?\)')
REQUIRED_MEDIA_FIELDS = ('id','kind','file','source_url','creator','license','attribution','subject')
ENTRY_CATEGORIES = {'attraction', 'shopping', 'dining', 'hotel'}
HEADING_PATTERN = re.compile(r'^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$', re.M)
ENTRY_MARKER_PATTERN = re.compile(r'<!--[ \t]*periplus-entry:[ \t]*([^\s<>]+)[ \t]*-->')

def entry_records(project):
    path = Path(project) / 'research/ENTRY_CATALOGUE.json'
    if not path.is_file():
        raise FileNotFoundError('research/ENTRY_CATALOGUE.json does not exist; every venue requires an entry and its own photo coverage')
    data = json.loads(path.read_text(encoding='utf8'))
    if not isinstance(data, dict) or not isinstance(data.get('entries'), list) or not data['entries']:
        raise ValueError('ENTRY_CATALOGUE.json requires a nonempty {"entries": []}')
    return data['entries']

def audit_entry_photo_coverage(project, text, assets):
    """Check each inventoried venue's own heading block, across all chapters.

    Markers are an editorial inventory contract, not venue-name inference. Every
    named attraction/shop/restaurant/hotel must be inventoried during research;
    human QA must also compare that inventory with every published venue. Ordinary
    thematic headings and city headings need not pretend to be venue entries.
    """
    errors = []
    try: entries = entry_records(project)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as ex: return [str(ex)]
    by_id = {}; by_heading = {}; photos = {}; asset_ids = set()
    for asset in assets:
        if not isinstance(asset, dict): continue
        asset_id = asset.get('id')
        if isinstance(asset_id, str) and asset_id.strip():
            if asset_id in asset_ids: errors.append(f'Duplicate media asset id: {asset_id}')
            asset_ids.add(asset_id)
        if asset.get('kind') == 'photo' and isinstance(asset_id, str):
            photos[asset_id] = asset
            linked = asset.get('entry_ids')
            # Cover/transport/ticket photos may supplement venue photos without
            # asserting venue coverage. Any asserted links must still be valid.
            if linked is not None and (not isinstance(linked, list) or any(not isinstance(x, str) or not x.strip() for x in linked)):
                errors.append(f'Photo entry_ids must be a list of valid entry ids: {asset_id}')
            elif isinstance(linked, list) and len(linked) != len(set(linked)):
                errors.append(f'Photo repeats entry_ids: {asset_id}')
    for entry in entries:
        if not isinstance(entry, dict): errors.append('Catalogue entry is not an object'); continue
        missing = [k for k in ('id', 'category', 'name', 'heading') if not isinstance(entry.get(k), str) or not entry[k].strip()]
        if missing: errors.append(f'Catalogue entry missing {missing}: {entry.get("id", "?")}'); continue
        eid = entry['id']; heading = entry['heading']
        if re.search(r'\s|[<>]', eid): errors.append(f'Entry id cannot contain whitespace or angle brackets: {eid}')
        if eid in by_id: errors.append(f'Duplicate catalogue entry id: {eid}')
        if heading in by_heading: errors.append(f'Duplicate catalogue entry heading: {heading}')
        if entry['category'] not in ENTRY_CATEGORIES: errors.append(f'Invalid entry category for {eid}: {entry["category"]}')
        pids = entry.get('photo_ids')
        if not isinstance(pids, list) or not pids or any(not isinstance(x, str) or not x.strip() for x in pids):
            errors.append(f'Entry requires at least one photo_id: {eid}')
        elif len(pids) != len(set(pids)): errors.append(f'Entry repeats photo_ids: {eid}')
        by_id[eid] = entry; by_heading[heading] = eid
    headings = list(HEADING_PATTERN.finditer(text)); markers = list(ENTRY_MARKER_PATTERN.finditer(text))
    marked_blocks = {}
    for marker in markers:
        eid = marker.group(1)
        if eid not in by_id: errors.append(f'Unregistered venue entry marker: {eid}')
        if eid in marked_blocks: errors.append(f'Duplicate entry marker in manuscript: {eid}')
        prior = next((h for h in reversed(headings) if h.end() <= marker.start()), None)
        if not prior or text[prior.end():marker.start()].strip():
            errors.append(f'Entry marker must immediately follow its heading: {eid}'); continue
        if len(prior.group(1)) < 3:
            errors.append(f'Entry heading must be H3 or deeper: {eid}')
        if eid in by_id and prior.group(2).strip() != by_id[eid]['heading']:
            errors.append(f'Entry marker heading does not exactly match catalogue: {eid}')
        end = next((h.start() for h in headings if h.start() > prior.start() and len(h.group(1)) <= len(prior.group(1))), len(text))
        marked_blocks[eid] = text[marker.end():end]
    for eid, entry in by_id.items():
        matches = [h for h in headings if h.group(2).strip() == entry['heading']]
        if len(matches) != 1: errors.append(f'Catalogue heading must occur exactly once: {eid} ({len(matches)} occurrences)')
        if eid not in marked_blocks:
            errors.append(f'Catalogue entry missing marked manuscript heading: {eid}'); continue
        try: used_here = {path for _, path in referenced_files(marked_blocks[eid])}
        except ValueError as ex: errors.append(str(ex)); used_here = set()
        valid = False
        pids = entry.get('photo_ids')
        for pid in pids if isinstance(pids, list) else []:
            if not isinstance(pid, str): continue
            photo = photos.get(pid)
            if not photo:
                errors.append(f'Entry photo_id is missing or is not a photograph: {eid} / {pid}'); continue
            if eid not in (photo.get('entry_ids') if isinstance(photo.get('entry_ids'), list) else []):
                errors.append(f'Photo lacks reciprocal entry_ids link: {eid} / {pid}'); continue
            if photo.get('file') in used_here: valid = True
            else: errors.append(f'Entry photograph is outside its own heading block or absent: {eid} / {pid}')
        if not valid: errors.append(f'Entry has no relevant photograph embedded inside its own heading block: {eid}')
    for pid, photo in photos.items():
        linked = photo.get('entry_ids')
        for eid in linked if isinstance(linked, list) else []:
            if not isinstance(eid, str): continue
            if eid not in by_id: errors.append(f'Photo links to unregistered entry: {pid} / {eid}')
            elif pid not in (by_id[eid].get('photo_ids') if isinstance(by_id[eid].get('photo_ids'), list) else []):
                errors.append(f'Catalogue lacks reciprocal photo_ids link: {pid} / {eid}')
    return errors

def media_records(project):
    path = Path(project)/'research/MEDIA_MANIFEST.json'
    if not path.is_file():
        raise FileNotFoundError('research/MEDIA_MANIFEST.json does not exist')
    data=json.loads(path.read_text(encoding='utf8'))
    if not isinstance(data,dict) or not isinstance(data.get('assets'),list):
        raise ValueError('MEDIA_MANIFEST.json requires {"assets": []}')
    return data['assets']

def referenced_files(manuscript):
    out=[]
    for alt, rel in IMAGE_PATTERN.findall(manuscript):
        if re.match(r'https?://', rel):
            raise ValueError(f'Image is external-only, not embedded: {rel}')
        if not alt.strip():
            raise ValueError(f'Media missing descriptive caption/alt text: {rel}')
        resolved=(Path('exports')/rel).as_posix()
        normalized=Path(resolved)
        if '..' in normalized.parts:
            normalized=Path('exports') / rel
        from os.path import normpath
        out.append((alt, normpath(str(normalized)).replace('\\','/')))
    return out

def audit_media(project, text, request):
    errors=[]; project=Path(project)
    try: assets=media_records(project)
    except (ValueError,FileNotFoundError,json.JSONDecodeError) as e: return [str(e)]
    try: used=referenced_files(text)
    except ValueError as ex: errors.append(str(ex)); used=[]
    errors.extend(audit_entry_photo_coverage(project, text, assets))
    by_file={}
    for a in assets:
        if not isinstance(a,dict): errors.append('Media record is not an object'); continue
        absent=[x for x in REQUIRED_MEDIA_FIELDS if not isinstance(a.get(x),str) or not a[x].strip()]
        if absent: errors.append(f'Media asset missing {absent}: {a.get("id", "? ")}');continue
        if a['kind'] not in ('photo','map','illustration'):errors.append(f'Invalid media kind {a["kind"]}');continue
        path=Path(a['file'])
        if path.is_absolute() or '..' in path.parts or not path.parts or (path.parts[0] != ('maps' if a['kind']=='map' else 'photos')):
            errors.append(f'Wrong/outside media folder: {a["file"]}');continue
        file=project/path
        if not file.is_file():errors.append(f'Actual media file missing: {a["file"]}');continue
        if path.suffix.lower() not in ('.jpg','.jpeg','.png'):
            errors.append(f'Media must be PNG/JPEG for reliable PDF export: {a["file"]}');continue
        try:
            from PIL import Image
            with Image.open(file) as im:
                im.verify()
            with Image.open(file) as im:
                w,h=im.size
            minw,minh=(850,500) if a['kind']=='map' else (700,450)
            if w<minw or h<minh:errors.append(f'Low-resolution {a["kind"]}: {a["file"]} {w}x{h}')
        except (OSError,ImportError) as ex:
            errors.append(f'Unusable image {a["file"]}: {ex}')
        if not re.match(r'https?://',a['source_url']):
            errors.append(f'Invalid source URL for {a["file"]}')
        # Reject obvious templates/fake attribution, even though machine validation
        # cannot authenticate whether an otherwise plausible license claim is true.
        low=' '.join(str(a.get(k,'')) for k in ('source_url','license','creator','attribution','subject')).casefold()
        if any(x in low for x in ('example.org','example.com','test.invalid','replace_with','test only','test fixture','not for publication')):
            errors.append(f'Placeholder/example media provenance is forbidden: {a["file"]}')
        if a['kind']=='map':
            if not str(a.get('map_id','')).strip():errors.append(f'Map lacks Map ID: {a["file"]}')
            if not (a.get('map_data_source') or a.get('source_url')):errors.append(f'Map data provenance absent: {a["file"]}')
        by_file[a['file']]=a
    used_set={path for _,path in used}
    for path in used_set:
        if path not in by_file:errors.append(f'Embedded image not registered with provenance: {path}')
    for path in by_file:
        if path not in used_set: errors.append(f'Registered photo/map not actually embedded in manuscript: {path}')
    length=sum(1 for _ in trip_days(request))
    photo_count=sum(1 for a in assets if isinstance(a,dict) and a.get('kind')=='photo')
    map_count=sum(1 for a in assets if isinstance(a,dict) and a.get('kind')=='map')
    minimum_photos=3 if length<=3 else 6
    minimum_maps=1 if length<=3 else 2
    if photo_count<minimum_photos:errors.append(f'Too few actual photographs: {photo_count} (min {minimum_photos})')
    if map_count<minimum_maps:errors.append(f'Too few actual georeferenced maps: {map_count} (min {minimum_maps})')
    map_headings=re.findall(r'^#{1,5}\s+(Map [A-Z])\s*[–—:\-]',text,re.M|re.I)
    for mh in set(map_headings):
        matches=[a for a in assets if isinstance(a,dict) and a.get('kind')=='map' and str(a.get('map_id','')).casefold()==mh.casefold()]
        if not matches:errors.append(f'Area section {mh} has no sourced real map in media manifest')
        elif not any(a['file'] in used_set for a in matches):
            errors.append(f'Area section {mh} map not embedded in manuscript')
    return errors

def verify_heading_pagination(docx_path,pdf_path):
    from docx import Document
    import fitz
    doc=Document(docx_path)
    headings=[]
    for p in doc.paragraphs:
        if p.style.name not in ('Heading 1','Heading 2'):continue
        if not p.paragraph_format.page_break_before:
            raise RuntimeError(f'Missing new-page rule for {p.style.name}: {p.text}')
        headings.append((1 if p.style.name=='Heading 1' else 2,p.text))
    if not headings:raise RuntimeError('No Heading 1/2 found for page-break audit')
    pdf=fitz.open(str(pdf_path))
    try:
        outline=pdf.get_toc()
        next_at=0
        for level, heading in headings:
            found=False
            for j in range(next_at,len(outline)):
                outline_level,outline_heading,page_number = outline[j][:3]
                if outline_level == level and outline_heading.strip() == heading.strip():
                    target=pdf[page_number-1]
                    matches=target.search_for(heading[:min(len(heading),70)])
                    if not matches or not any(rect.y0 <= 175 for rect in matches):
                        raise RuntimeError(f'Heading {level} does not start near top of destination page {page_number}: {heading}')
                    next_at=j+1;found=True;break
            if not found:
                raise RuntimeError(f'Heading missing from PDF outline, cannot certify page start: {heading}')
    finally:pdf.close()

def verify_published_media(project, manuscript_path, docx_path, pdf_path):
    project=Path(project)
    req=json.loads((project/'request.json').read_text(encoding='utf8'))
    text=Path(manuscript_path).read_text(encoding='utf8')
    problems=audit_media(project,text,req)
    if problems:raise RuntimeError('Media QA failed: '+'; '.join(problems[:12]))
    assets=media_records(project)
    with zipfile.ZipFile(docx_path) as doc:
        medias={hashlib.sha256(doc.read(name)).hexdigest() for name in doc.namelist() if name.startswith('word/media/')}
    missing=[]
    for a in assets:
        digest=hashlib.sha256((project/a['file']).read_bytes()).hexdigest()
        if digest not in medias:missing.append(a['file'])
    if missing:raise RuntimeError(f'Actual images not embedded in DOCX: {missing}')
    import fitz
    pdf=fitz.open(str(pdf_path))
    try:
        # get_images() lists page resources, which can include unused/global
        # resources. get_image_info() reports actual physical image placements.
        count=sum(len(p.get_image_info()) for p in pdf)
        if count<len(assets):
            raise RuntimeError(f'PDF seems to be missing actual embedded photos/maps ({count} instances, expected >={len(assets)})')
    finally:pdf.close()
    verify_heading_pagination(docx_path,pdf_path)
