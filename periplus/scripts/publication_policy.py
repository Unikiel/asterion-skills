"""Verify screenshot provenance and keep media-only URLs out of final travel links.

Machine metadata checks complement visual and rights review; they cannot prove
that a screenshot is accurate, readable or permitted for a distribution scope.
"""
import re
from urllib.parse import urlparse

def google_maps_url(value):
    try:
        u=urlparse(value)
        return u.scheme=='https' and bool(re.fullmatch(r'(?:www\.|maps\.)?google\.(?:com|co\.jp|com\.hk|[a-z]{2})',u.hostname or '')) and ('maps' in u.path or (u.hostname or '').startswith('maps.'))
    except (ValueError,TypeError):return False

def audit_map_capture(asset, actual_size):
    errors=[];name=asset.get('file','?')
    if asset.get('provider')!='Google Maps' or asset.get('capture_method')!='browser_screenshot':
        errors.append('Map must be a genuine Google Maps browser screenshot: '+name)
    if not google_maps_url(asset.get('capture_url','')):
        errors.append('Map capture URL must identify Google Maps: '+name)
    viewport=asset.get('viewport_css');scale=asset.get('device_scale_factor')
    if not isinstance(viewport,list) or len(viewport)!=2 or any(type(n) is not int or n<=0 for n in viewport) or type(scale) not in (int,float) or scale<2:
        errors.append('Map needs native viewport and device scale >=2: '+name)
    elif tuple(round(n*scale) for n in viewport)!=tuple(actual_size):
        errors.append('Map pixels do not match native capture; no artificial upscaling: '+name)
    if list(actual_size)!=asset.get('screenshot_pixels'):
        errors.append('Map screenshot pixel metadata differs from actual file: '+name)
    if actual_size[0]<2000 or actual_size[1]<1200:
        errors.append('Map screenshot must be at least 2000x1200 native pixels: '+name)
    if asset.get('attribution_visible') is not True or asset.get('print_readability_checked') is not True:
        errors.append('Map attribution and final print readability require visual checks: '+name)
    if not asset.get('captured_on'):
        errors.append('Map capture date missing: '+name)
    return errors

def audit_photo_resolution(asset,actual_size):
    """A native small original can print sharply at a genuinely small size."""
    w,h=actual_size
    if w>=700 and h>=450:return []
    width=asset.get('print_width_cm')
    if (w>=300 and h>=200 and type(width) in (int,float) and width>0
        and w/(width/2.54)>=240 and asset.get('native_resolution')==[w,h]
        and asset.get('small_print_reviewed') is True):return []
    return ['Low-resolution photo requires a verified native original printed at >=240 ppi: '+asset.get('file','?')]

def audit_pdf_map_resolution(assets,placements):
    """Final PDF must retain the native screenshot pixels, not just its DOCX."""
    from collections import Counter
    expected=Counter(tuple(a['screenshot_pixels']) for a in assets if a.get('kind')=='map' and a.get('screenshot_pixels'))
    actual=Counter((p['width'],p['height']) for p in placements)
    return ['PDF map screenshots were downsampled or omitted: expected at least '+str(n)+' native '+str(size)+' placements, found '+str(actual[size]) for size,n in expected.items() if actual[size]<n]

def audit_final_reference_links(text,assets):
    errors=[];forbidden=set()
    for a in assets:
        for k in ('download_url','license_url'):
            if a.get(k):forbidden.add(a[k])
        if a.get('source_url') and not a.get('source_is_travel_resource'):
            forbidden.add(a['source_url'])
    headings=list(re.finditer(r'^(#{1,6})\s+(.+)\s*$',text,re.M))
    for i,h in enumerate(headings):
        name=h.group(2).strip()
        credits=bool(re.search(r'(?:image|photo|map).*(?:sources|credits)',name,re.I))
        references=bool(re.search(r'^(?:References|Bibliography|Useful Links|Source Bibliography|\u53c2\u8003\u8d44\u6599|\u53c2\u8003\u6587\u732e|\u5b9e\u7528\u94fe\u63a5)\b',name,re.I))
        if not (credits or references):continue
        end=next((n.start() for n in headings[i+1:] if len(n.group(1))<=len(h.group(1))),len(text))
        urls=re.findall(r'(?<!!)\[[^\]]+\]\((https?://[^\s)]+)\)',text[h.end():end])
        for url in urls:
            host=(urlparse(url).hostname or '').lower()
            media_host=host in ('commons.wikimedia.org','upload.wikimedia.org','openverse.org','unsplash.com','pexels.com','pixabay.com','flickr.com','www.flickr.com','creativecommons.org')
            direct=bool(re.search(r'\.(?:jpe?g|png|webp|gif|tiff?)(?:\?|$)',url,re.I))
            if credits or url in forbidden or media_host or direct:
                errors.append('Image-only source/credit URL must stay out of final travel links: '+url)
    return errors
