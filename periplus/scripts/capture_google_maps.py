#!/usr/bin/env python3
"""Capture native high-resolution Google Maps screenshots; visual review remains required."""
import argparse,json
from pathlib import Path
from publication_policy import google_maps_url

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',required=True);p.add_argument('--output-dir',required=True);args=p.parse_args()
    config=json.loads(Path(args.config).read_text(encoding='utf8'));out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    from playwright.sync_api import sync_playwright
    from datetime import datetime,timezone
    records=[]
    with sync_playwright() as pw:
        options={'headless':True}
        if config.get('browser_executable'):options['executable_path']=config['browser_executable']
        browser=pw.chromium.launch(**options)
        try:
            for panel in config['panels']:
                url=panel['url'];viewport=panel.get('viewport_css',[1000,700]);scale=panel.get('device_scale_factor',2)
                if not google_maps_url(url):raise ValueError('Expected Google Maps URL')
                if len(viewport)!=2 or scale<2 or viewport[0]*scale<2000 or viewport[1]*scale<1200:raise ValueError('Native capture must be >=2000x1200 at scale >=2')
                filename=panel.get('output',panel['id']+'.png')
                if Path(filename).name!=filename or not filename.endswith('.png'):raise ValueError('Expected simple PNG filename')
                context=browser.new_context(viewport={'width':viewport[0],'height':viewport[1]},device_scale_factor=scale,locale=config.get('locale','en-US'))
                try:
                    page=context.new_page()
                    if 'output=embed' in url or '/maps/embed' in url:
                        import html
                        page.set_content('<html><body style="margin:0;overflow:hidden"><iframe title="Google Maps" style="border:0;width:100vw;height:100vh" src="'+html.escape(url,quote=True)+'"></iframe></body></html>',wait_until='domcontentloaded')
                    else:page.goto(url,wait_until='commit',timeout=60000)
                    ready=False;capture_url=url
                    for attempt in range(24):
                        page.wait_for_timeout(10000)
                        for frame in page.frames:
                            body=frame.locator('body').inner_text(timeout=5000)
                            loaded=frame.locator('img').evaluate_all("imgs=>imgs.filter(i=>i.src.includes('/maps/')||i.src.includes('maps.')).filter(i=>i.complete&&i.naturalWidth>100).length")
                            credited=bool(__import__('re').search(r'Map data|\u5730\u56f3\u30c7\u30fc\u30bf|\u5730\u56fe\u6570\u636e',body))
                            if credited and (loaded>=2 or frame.locator('canvas').count()):ready=True;capture_url=frame.url;break
                        if ready:break
                    if not ready:raise RuntimeError('No fully rendered, attributed map; inspect consent, network or loading blocker')
                    page.wait_for_timeout(3000)
                    page.screenshot(path=str(out/filename))
                    records.append(dict(id=panel['id'],file=filename,provider='Google Maps',capture_method='browser_screenshot',capture_url=capture_url,viewport_css=viewport,device_scale_factor=scale,screenshot_pixels=[round(n*scale) for n in viewport],captured_on=datetime.now(timezone.utc).date().isoformat(),attribution_visible=False,print_readability_checked=False))
                finally:context.close()
        finally:browser.close()
    (out/'capture_metadata.json').write_text(json.dumps({'assets':records},indent=2),encoding='utf8')
    print('Captured',len(records),'panels. Inspect identity, attribution and final print readability before approving metadata.')

if __name__=='__main__':main()
