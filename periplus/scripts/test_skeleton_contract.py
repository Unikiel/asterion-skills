#!/usr/bin/env python3
"""Regression guards for historical chapter immutability and bilingual title order."""
from pathlib import Path
import re
import unittest
from skeleton_audit import get_fixed_headings,audit_skeleton


class ImmutableHeadingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lines=[]
        for level,name in get_fixed_headings():
            title = name + (' \u2013 Example area' if name.startswith('Map ') else '')
            lines.append('#'*level+' '+title+'\nFact-based destination-specific visitor information.')
        cls.good='\n\n'.join(lines)

    def test_complete_canonical_skeleton_accepted(self):
        self.assertEqual(audit_skeleton(self.good),[])

    def test_missing_historical_variant_is_not_auto_merged(self):
        for heading in ['Literature & Art','Events','Diet & Cuisine','Railways & Metro','Highway','Metro']:
            with self.subTest(heading=heading):
                changed=re.sub(r'^### '+re.escape(heading)+r'$', '### Removed Venue', self.good, flags=re.M)
                self.assertTrue(any(heading in e for e in audit_skeleton(changed)))

    def test_approved_around_area_spelling(self):
        bad=self.good.replace('## Around Area','## Around Aera')
        self.assertTrue(any('Around Area' in e for e in audit_skeleton(bad)))

    def test_bilingual_title_english_before_chinese(self):
        self.assertEqual(audit_skeleton(self.good+'\n### Museum — '+chr(0x4e2d)+chr(0x6587)+'\n'),[])
        bad=self.good+'\n### '+chr(0x4e2d)+chr(0x6587)+' — Museum\n'
        self.assertTrue(any('English' in e for e in audit_skeleton(bad)))

    def test_moved_topic_fails_parent_check(self):
        bad=self.good.replace('### Literature & Art','### Placeholder')+'\n### Literature & Art\n'
        self.assertTrue(any('Literature & Art' in e for e in audit_skeleton(bad)))

    def test_process_appendix_cannot_be_exported(self):
        bad=self.good+'\n# Appendix / Working Notes\n## Visual Asset Checklist\n'
        self.assertTrue(any('appendix' in e.lower() for e in audit_skeleton(bad)))

    def test_required_maps_are_not_optional(self):
        bad=self.good.replace('### Map J \u2013 Example area','### Map J')
        self.assertTrue(any('Map J' in e for e in audit_skeleton(bad)))

if __name__=='__main__':unittest.main()
