#!/usr/bin/env python3
"""English-source policy, multilingual behavior and canonical release consistency."""
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from version import SKILL_VERSION,SCHEMA_VERSION
from generate import ensure_request,create_project

ROOT=Path(__file__).resolve().parent.parent

class ReleaseTests(unittest.TestCase):
    def request(self):
        return {'destination':'\u9752\u68ee','country':'\u65e5\u672c',
          'start_date':'2026-07-12','end_date':'2026-07-15',
          'journey':{'outbound':{'mode':'rail','origin':'\u4e0a\u91ce\u99c5'},'return':{'mode':'rail','destination':'\u516b\u6238\u99c5'}}}
    def test_package_source_is_english(self):
        remaining=[]
        pattern=re.compile(r'[\u3400-\u9fff\u3040-\u30ff\uac00-\ud7af]')
        for p in ROOT.rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts:continue
            try:content=p.read_text(encoding='utf8')
            except UnicodeDecodeError:continue
            if pattern.search(content):remaining.append(str(p.relative_to(ROOT)))
        self.assertEqual(remaining,[])
    def test_version_visible_and_consistent(self):
        self.assertEqual((ROOT/'VERSION').read_text().strip(),SKILL_VERSION)
        for name in ['SKILL.md','README.md','INSTALL.md']:
            self.assertIn(SKILL_VERSION,(ROOT/name).read_text(encoding='utf8'))
        actual=subprocess.check_output([sys.executable,str(ROOT/'scripts/generate.py'),'--version'],text=True).strip()
        self.assertEqual(actual,'Periplus '+SKILL_VERSION)
    def test_chinese_input_default_and_override(self):
        req=ensure_request(self.request());self.assertEqual(req['destination'],'\u9752\u68ee');self.assertEqual(req['customization']['language'],'zh-CN')
        req=self.request();req['customization']={'language':'en'};self.assertEqual(ensure_request(req)['customization']['language'],'en')
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp)/'trip';create_project(ensure_request(self.request()),project)
            metadata=json.loads((project/'project.json').read_text())
            self.assertEqual(metadata['skill_version'],SKILL_VERSION);self.assertEqual(metadata['schema_version'],SCHEMA_VERSION)
    def test_manifest_covers_source_distribution(self):
        declared=set((ROOT/'manifest.txt').read_text().splitlines())
        actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
        self.assertEqual(declared,actual)
    def test_supplementary_illustration_download_uses_release(self):
        from PIL import Image
        from fetch_media import fetch_assets
        raw=io.BytesIO();Image.new('RGB',(750,500),'white').save(raw,'PNG')
        class Response(io.BytesIO):
            headers={'Content-Type':'image/png'}
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/'research').mkdir()
            asset={'id':'diagram','kind':'illustration','file':'photos/diagram.png','download_url':'https://commons.wikimedia.org/image.png','source_url':'https://commons.wikimedia.org/wiki/File:Fixture.png','creator':'Fixture owner','license':'CC0','attribution':'Fixture owner','subject':'Internal unit fixture'}
            (project/'research/MEDIA_MANIFEST.json').write_text(json.dumps({'assets':[asset]}))
            with patch('fetch_media.urlopen',return_value=Response(raw.getvalue())) as open_mock:
                self.assertEqual(fetch_assets(project),1)
            request=open_mock.call_args.args[0]
            self.assertIn(SKILL_VERSION,request.get_header('User-agent'));self.assertTrue((project/'photos/diagram.png').exists())

if __name__=='__main__':unittest.main()
