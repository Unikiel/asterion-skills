#!/usr/bin/env python3
"""Download explicitly licensed real photos/maps enumerated in MEDIA_MANIFEST.json.

The research agent MUST first confirm each download_url is a legitimate direct
image URL and inspect its source_url for provenance and image reuse rights.
No copyrighted image may be downloaded for reuse without appropriate rights.
"""
from __future__ import annotations
import argparse
import io
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from PIL import Image, ImageOps
from version import SKILL_VERSION

MAX_BYTES=20*1024*1024


def fetch_assets(project, timeout=25):
    project=Path(project)
    mf=project/'research/MEDIA_MANIFEST.json'
    raw=json.loads(mf.read_text(encoding='utf8'))
    assets=raw.get('assets',[])
    if not isinstance(assets,list):raise ValueError('Invalid media manifest')
    errors=[]
    for a in assets:
        path=Path(a.get('file',''))
        kind=a.get('kind')
        if kind not in ('photo','illustration','map') or path.is_absolute() or '..' in path.parts or path.parts[0] != ('maps' if kind=='map' else 'photos'):
            errors.append(f'Invalid local media path: {path}');continue
        dest=project/path
        if dest.is_file():
            print('Already exists:', dest);continue
        url=a.get('download_url')
        if not isinstance(url,str) or not url.startswith('https://'):
            errors.append(f'Missing confirmed direct HTTPS image download URL: {path}');continue
        if not all(a.get(k) for k in ('source_url','creator','license','attribution','subject')):
            errors.append(f'Missing rights/provenance before downloading: {path}');continue
        if any(x in (a.get('license','')+' '+a.get('source_url','')).lower() for x in ('test only','example.org','test.invalid')):
            errors.append(f'Test/example provenance is not a publication source: {path}');continue
        try:
            req=Request(url,headers={'User-Agent':f'PeriplusTravelBrochure/{SKILL_VERSION} (media usage audit; non-bulk)','Accept':'image/png,image/jpeg,image/webp'})
            with urlopen(req,timeout=timeout) as resp:
                if not str(resp.headers.get('Content-Type','')).startswith('image/'):
                    raise ValueError('URL did not serve an image')
                if int(resp.headers.get('Content-Length','0') or 0)>MAX_BYTES:raise ValueError('File too large')
                raw=resp.read(MAX_BYTES+1)
            if len(raw)>MAX_BYTES: raise ValueError('File too large')
            with Image.open(io.BytesIO(raw)) as im:
                im=ImageOps.exif_transpose(im)
                w,h=im.size
                if w<700 or h<450:raise ValueError(f'Resolution too low {w}x{h}')
                if im.mode not in ('RGB','RGBA'):im=im.convert('RGB')
                dest.parent.mkdir(parents=True,exist_ok=True)
                if dest.suffix.lower() in ('.jpg','.jpeg'):
                    im.convert('RGB').save(dest,'JPEG',quality=90,optimize=True)
                else:
                    im.save(dest,'PNG',optimize=True)
            print('Downloaded real asset:',dest)
        except Exception as ex:
            errors.append(f'{path}: {ex}')
    if errors:
        raise RuntimeError('Asset acquisition not complete:\n - '+'\n - '.join(errors))
    return len(assets)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',required=True)
    args=p.parse_args()
    try:print('Assets present:',fetch_assets(Path(args.project)))
    except (ValueError,RuntimeError) as e:
        print('ERROR:',e,file=sys.stderr);raise SystemExit(2)
