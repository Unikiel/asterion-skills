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

ROOT_NAME = 'Seven_Ninths_Travel_Brochure'
IMAGE_PATTERN = re.compile(r'!\[([^\]]+)\]\(([^\s)]+)(?:\s+"[^"]*")?\)')
REQUIRED_MEDIA_FIELDS = ('id','kind','file','source_url','creator','license','attribution','subject')

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
    used=referenced_files(text)
    by_file={}
    for a in assets:
        if not isinstance(a,dict): errors.append('Media record is not an object'); continue
        absent=[x for x in REQUIRED_MEDIA_FIELDS if not isinstance(a.get(x),str) or not a[x].strip()]
        if absent: errors.append(f'Media asset missing {absent}: {a.get("id", "? ")}');continue
        if a['kind'] not in ('photo','map'):errors.append(f'Invalid media kind {a["kind"]}');continue
        path=Path(a['file'])
        if path.is_absolute() or '..' in path.parts or (path.parts[0] != ('photos' if a['kind']=='photo' else 'maps')):
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
            minw,minh=(700,450) if a['kind']=='photo' else (850,500)
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
    length=(date.fromisoformat(request['end_date'])-date.fromisoformat(request['start_date'])).days+1
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
        count=sum(len(p.get_images(full=True)) for p in pdf)
        if count<len(assets):
            raise RuntimeError(f'PDF seems to be missing actual embedded photos/maps ({count} instances, expected >={len(assets)})')
    finally:pdf.close()
    verify_heading_pagination(docx_path,pdf_path)
