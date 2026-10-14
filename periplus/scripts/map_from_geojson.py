#!/usr/bin/env python3
"""Render a *real* geographically grounded map from a verified GeoJSON data file.

No synthetic/fantasy geography is generated. The input must contain actual
geographic features obtained from OSM/official datasets with legitimate reuse
rights. Publisher/research agent is responsible for data accuracy and license.

Usage:
  python scripts/map_from_geojson.py \
    --geojson maps/source/kyoto_central.geojson \
    --pins maps/source/kyoto_central_pins.json \
    --output maps/map_a.png \
    --title 'Map A — Kyoto Central' \
    --attribution '© OpenStreetMap contributors (ODbL)'
"""
from __future__ import annotations
import argparse
import json
import math
import os
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


from functools import lru_cache
import unicodedata

@lru_cache(maxsize=1)
def _oswald_path():
    candidates = []
    if os.name == 'nt':
        for base in (os.environ.get('LOCALAPPDATA', ''), os.environ.get('WINDIR', 'C:/Windows')):
            if base:
                candidates.extend(Path(base, 'Microsoft', 'Windows', 'Fonts').glob('Oswald*.ttf'))
                candidates.extend(Path(base, 'Fonts').glob('Oswald*.ttf'))
    else:
        for d in (Path.home()/'.local/share/fonts', Path.home()/'Library/Fonts', Path('/usr/share/fonts'), Path('/usr/local/share/fonts')):
            if d.exists(): candidates.extend(d.rglob('*Oswald*.ttf'))
    for path in candidates:
        if path.is_file(): return str(path)
    try:
        family = subprocess.check_output(['fc-match', '-f', '%{family}', 'Oswald'], text=True, timeout=3)
        if 'Oswald' in family:
            path = subprocess.check_output(['fc-match', '-f', '%{file}', 'Oswald'], text=True, timeout=3).strip()
            if Path(path).is_file(): return path
    except (OSError, subprocess.SubprocessError): pass
    raise RuntimeError('Oswald font not installed. Install from https://fonts.google.com/specimen/Oswald before map rendering.')


def latin_font(size):
    return ImageFont.truetype(_oswald_path(), size)


def font(size):
    paths=(
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/System/Library/Fonts/PingFang.ttc',
    )
    for p in paths:
        if Path(p).is_file():
            try:return ImageFont.truetype(p,size)
            except OSError: pass
    return ImageFont.load_default()


def draw_mixed(draw, xy, value, size, fill, **opts):
    # Latin with diacritics/romaji (e.g. Kyōto) and digits use Oswald.
    # CJK ideographs and Japanese kana use a font with corresponding glyphs.
    from itertools import groupby
    def is_latin(ch):
        return ord(ch) < 128 or 'LATIN' in unicodedata.name(ch, '')
    x, y = xy
    for latin, chars in groupby(str(value), key=is_latin):
        group = ''.join(chars)
        f = latin_font(size) if latin else font(size)
        draw.text((x, y), group, fill=fill, font=f, **opts)
        x += draw.textlength(group, font=f)


def flatten_coords(geometry):
    if not isinstance(geometry,dict):return []
    typ=geometry.get('type');coords=geometry.get('coordinates')
    if typ=='Point': return [[coords]]
    if typ in ('LineString','MultiPoint'):return [coords]
    if typ in ('MultiLineString','Polygon'):return coords
    if typ=='MultiPolygon': return [r for poly in coords for r in poly]
    if typ=='GeometryCollection':return [v for child in geometry.get('geometries',[]) for v in flatten_coords(child)]
    return []


def mercator(lat):
    lat=max(-85.0,min(85.0,float(lat)))
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def render(geodata, pins, output, title, attribution, width=1500,height=1000):
    if not isinstance(geodata,dict) or geodata.get('type')!='FeatureCollection':
        raise ValueError('Map input must be a real GeoJSON FeatureCollection with sourced features')
    features=geodata.get('features',[])
    if len(features)<5:
        raise ValueError('Too few sourced geographic features for a true area map (min 5)')
    polygons=[];roads=[];water=[];stations=[]
    points=[]
    for f in features:
        geom=f.get('geometry',{});props=f.get('properties') or {}
        kind=str(props.get('highway','') or props.get('class','') or props.get('type','') or props.get('natural','') or props.get('waterway','')).lower()
        for line in flatten_coords(geom):
            if not isinstance(line,list) or not line:continue
            line=[c for c in line if isinstance(c,list) and len(c)>=2 and isinstance(c[0],(int,float)) and isinstance(c[1],(int,float))]
            if not line:continue
            points.extend(line)
            if geom.get('type') in ('Polygon','MultiPolygon'):
                polygons.append((line,kind))
            elif 'water' in kind or 'river' in kind or 'stream' in kind:
                water.append((line,kind))
            elif 'station' in kind or 'railway' in kind:
                stations.append((line,kind))
            else:
                roads.append((line,kind))
    if not roads and not stations:
        raise ValueError('Map has no street/rail/cartographic network; do not call this a real area map')
    for p in pins:
        if not all(k in p for k in ('lat','lon','label')):raise ValueError('Each pin needs verified lat/lon/label')
        points.append([p['lon'],p['lat']])
    if not points:raise ValueError('No geocoordinates in map')
    xs=[p[0] for p in points];ys=[mercator(p[1]) for p in points]
    xmin,xmax=min(xs),max(xs);ymin,ymax=min(ys),max(ys)
    if xmax-xmin>0.5 or ymax-ymin>0.5:
        raise ValueError('Map covers unusually large area; split into geographically coherent maps')
    dx=max(0.0008,(xmax-xmin)*.07);dy=max(.0008,(ymax-ymin)*.07)
    xmin-=dx;xmax+=dx;ymin-=dy;ymax+=dy
    pad_x,pad_y=90,125
    scale=min((width-2*pad_x)/(xmax-xmin),(height-pad_y-95)/(ymax-ymin))
    cx=(xmin+xmax)/2;cy=(ymin+ymax)/2
    def project(lon,lat):
        return (int((lon-cx)*scale+width/2),int((cy-mercator(lat))*scale+(height+pad_y-95)/2))
    image=Image.new('RGB',(width,height),'#f7f8f6');d=ImageDraw.Draw(image)
    for line,kind in polygons:
        xy=[project(*c[:2]) for c in line]
        if len(xy)>2:
            fill='#dae9d8' if any(x in kind for x in ('park','grass','forest','wood')) else '#e7ebec'
            d.polygon(xy,fill=fill)
    for line,_ in water:
        if len(line)>1:d.line([project(*c[:2]) for c in line],fill='#75bdd1',width=6)
    for line,kind in roads:
        if len(line)<2:continue
        w=6 if any(x in kind for x in ('primary','trunk','major')) else 3
        xy=[project(*c[:2]) for c in line]
        d.line(xy,fill='#ffffff',width=w+2);d.line(xy,fill='#9da5a9',width=w)
    for line,_ in stations:
        if len(line)>1:d.line([project(*c[:2]) for c in line],fill='#516876',width=4)
    label_font_size=23; title_font_size=35; credit_font_size=19
    for i,p in enumerate(pins):
        x,y=project(p['lon'],p['lat']);r=12
        d.ellipse((x-r,y-r,x+r,y+r),fill='#c82338',outline='#ffffff',width=3)
        draw_mixed(d,(x+17,y-20),str(p['label']),label_font_size,'#142533',stroke_width=3,stroke_fill='#f7f8f6')
    d.rectangle((0,0,width,80),fill='#152b3e');draw_mixed(d,(36,18),title,title_font_size,'white')
    d.rectangle((0,height-45,width,height),fill='#ffffff');draw_mixed(d,(18,height-35),attribution,credit_font_size,'#304250')
    draw_mixed(d,(width-90,110),'N ↑',label_font_size,'#192939')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);image.save(output)
    return output


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--geojson',required=True)
    p.add_argument('--pins',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--title',required=True)
    p.add_argument('--attribution',required=True)
    a=p.parse_args()
    geojson=json.loads(Path(a.geojson).read_text(encoding='utf8'))
    pins=json.loads(Path(a.pins).read_text(encoding='utf8'))
    render(geojson,pins,a.output,a.title,a.attribution)

if __name__=='__main__':main()
