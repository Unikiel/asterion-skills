#!/usr/bin/env python3
"""Deterministic venue-photo and physical PDF-placement acceptance tests.

These fixtures exercise structural validation; they are not publishable media.
Editorial subject, rights, and complete venue-inventory review remain necessary.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from media_utils import audit_entry_photo_coverage, audit_media, verify_published_media


class EntryCoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        (self.project / 'research').mkdir()
        self.entries = [self.entry('museum', 'attraction', 'Museum'),
                        self.entry('hotel', 'hotel', 'Hotel')]
        self.assets = [self.photo('museum_photo', 'museum'), self.photo('hotel_photo', 'hotel')]
        self.text = ('## Attractions\n### Museum\n<!-- periplus-entry: museum -->\n'
                     '![Museum](../photos/museum_photo.png)\n'
                     '## Accommodation\n### Hotel\n<!-- periplus-entry: hotel -->\n'
                     '![Hotel](../photos/hotel_photo.png)\n')

    @staticmethod
    def entry(eid, category, heading):
        return {'id': eid, 'category': category, 'name': heading, 'heading': heading,
                'photo_ids': [eid + '_photo']}

    @staticmethod
    def photo(pid, *eids):
        return {'id': pid, 'kind': 'photo', 'file': 'photos/' + pid + '.png', 'entry_ids': list(eids)}

    def audit(self, text=None, entries=None, assets=None):
        (self.project / 'research/ENTRY_CATALOGUE.json').write_text(
            json.dumps({'entries': self.entries if entries is None else entries}), encoding='utf8')
        return audit_entry_photo_coverage(self.project, self.text if text is None else text,
                                         self.assets if assets is None else assets)

    def assertProblem(self, fragment, **kwargs):
        self.assertTrue(any(fragment in x for x in self.audit(**kwargs)), fragment)

    def test_valid_all_categories(self):
        entries = copy.deepcopy(self.entries)
        assets = copy.deepcopy(self.assets)
        text = self.text
        for eid, cat in [('shop', 'shopping'), ('cafe', 'dining')]:
            entries.append(self.entry(eid, cat, eid.title()))
            assets.append(self.photo(eid + '_photo', eid))
            text += f'### {eid.title()}\n<!-- periplus-entry: {eid} -->\n![{eid}](../photos/{eid}_photo.png)\n'
        self.assertEqual(self.audit(text=text, entries=entries, assets=assets), [])

    def test_missing_catalogue(self):
        problems = audit_entry_photo_coverage(self.project, self.text, self.assets)
        self.assertTrue(any('ENTRY_CATALOGUE.json does not exist' in x for x in problems))

    def test_empty_or_malformed_catalogue(self):
        self.assertProblem('nonempty', entries=[])
        (self.project / 'research/ENTRY_CATALOGUE.json').write_text('{broken', encoding='utf8')
        self.assertTrue(audit_entry_photo_coverage(self.project, self.text, self.assets))

    def test_maps_cannot_substitute_for_photos(self):
        assets = copy.deepcopy(self.assets); assets[0]['kind'] = 'map'
        self.assertProblem('not a photograph', assets=assets)

    def test_supplementary_photos_need_no_invented_venue(self):
        extra = self.photo('cover')
        self.assertEqual(self.audit(assets=self.assets + [extra]), [])
        del extra['entry_ids']
        self.assertEqual(self.audit(assets=self.assets + [extra]), [])

    def test_authentic_illustration_cannot_satisfy_venue_photo(self):
        extra = {'id': 'ticket_diagram', 'kind': 'illustration', 'file': 'photos/ticket.png'}
        self.assertEqual(self.audit(assets=self.assets + [extra]), [])
        entries = copy.deepcopy(self.entries); entries[0]['photo_ids'] = ['ticket_diagram']
        self.assertProblem('not a photograph', entries=entries, assets=self.assets + [extra])

    def test_supplementary_photo_invalid_claim_still_fails(self):
        extra = self.photo('cover', 'missing')
        self.assertProblem('unregistered entry', assets=self.assets + [extra])
        extra['entry_ids'] = ['hotel']
        self.assertProblem('reciprocal photo_ids', assets=self.assets + [extra])
        extra['entry_ids'] = 'hotel'
        self.assertProblem('must be a list', assets=self.assets + [extra])

    def test_orphan_catalogue_entry(self):
        self.assertProblem('missing marked manuscript heading', text=self.text.split('## Accommodation')[0])

    def test_photo_elsewhere_does_not_cover_entry(self):
        text = self.text.replace('![Museum](../photos/museum_photo.png)\n', '')
        text += '## Photo index\n![Museum](../photos/museum_photo.png)\n'
        self.assertProblem('outside its own heading block', text=text)

    def test_hotel_also_requires_embedded_photo(self):
        self.assertProblem('no relevant photograph', text=self.text.replace('![Hotel](../photos/hotel_photo.png)', ''))

    def test_unregistered_marker_anywhere(self):
        for chapter in ['Tours', 'Around Area', 'Accommodation', 'Shopping']:
            with self.subTest(chapter=chapter):
                self.assertProblem('Unregistered venue entry marker',
                                   text=self.text + f'## {chapter}\n#### Cafe\n<!-- periplus-entry: cafe -->\n')

    def test_exact_heading_and_marker_position(self):
        self.assertProblem('does not exactly match', text=self.text.replace('### Museum', '### Other Museum'))
        self.assertProblem('immediately follow', text=self.text.replace('### Museum\n', '### Museum\nDescription.\n'))
        self.assertProblem('H3 or deeper', text=self.text.replace('### Museum', '## Museum'))

    def test_duplicate_ids_and_headings_rejected(self):
        self.assertProblem('Duplicate catalogue entry id', entries=self.entries + [copy.deepcopy(self.entries[0])])
        extra = self.entry('branch', 'attraction', 'Museum')
        self.assertProblem('Duplicate catalogue entry heading', entries=self.entries + [extra])
        self.assertProblem('Duplicate entry marker', text=self.text + '\n### Museum\n<!-- periplus-entry: museum -->\n')
        self.assertProblem('Duplicate media asset id', assets=self.assets + [copy.deepcopy(self.assets[0])])

    def test_same_names_at_different_branches_allowed(self):
        entries = copy.deepcopy(self.entries); entries[1]['name'] = entries[0]['name']
        self.assertEqual(self.audit(entries=entries), [])

    def test_reciprocal_links_required(self):
        assets = copy.deepcopy(self.assets); assets[0]['entry_ids'] = ['hotel']
        self.assertProblem('reciprocal entry_ids', assets=assets)
        assets = copy.deepcopy(self.assets); assets[0]['entry_ids'].append('missing')
        self.assertProblem('unregistered entry', assets=assets)
        assets = copy.deepcopy(self.assets); assets[0]['entry_ids'].append('hotel')
        self.assertProblem('reciprocal photo_ids', assets=assets)

    def test_shared_photo_requires_explicit_links_and_embedding_in_each_entry(self):
        entries = copy.deepcopy(self.entries)
        for entry in entries: entry['photo_ids'] = ['shared']
        assets = [self.photo('shared', 'museum', 'hotel')]
        text = self.text.replace('museum_photo', 'shared').replace('hotel_photo', 'shared')
        self.assertEqual(self.audit(text=text, entries=entries, assets=assets), [])
        self.assertProblem('outside its own heading block', entries=entries, assets=assets,
                           text=text.replace('![Hotel](../photos/shared.png)', ''))

    def test_nested_subheadings_allowed_for_entry_details(self):
        text = self.text.replace('![Museum]', '#### Collection and access\n![Museum]')
        self.assertEqual(self.audit(text=text), [])

    def test_external_image_and_empty_photo_list_rejected(self):
        self.assertProblem('external-only', text=self.text.replace('../photos/museum_photo.png', 'https://photos.invalid/museum.png'))
        entries = copy.deepcopy(self.entries); entries[0]['photo_ids'] = []
        self.assertProblem('at least one photo_id', entries=entries)

    def test_global_media_audit_invokes_entry_gate(self):
        (self.project / 'research/MEDIA_MANIFEST.json').write_text(json.dumps({'assets': []}), encoding='utf8')
        problems = audit_media(self.project, '', {'start_date': '2026-07-12', 'end_date': '2026-07-15'})
        self.assertTrue(any('ENTRY_CATALOGUE' in x for x in problems))
        self.assertTrue(any('Too few actual georeferenced maps' in x for x in problems))

    def test_global_media_audit_accepts_sourced_illustration_in_photos(self):
        from PIL import Image
        assets = copy.deepcopy(self.assets)
        assets += [self.photo('cover'),
                   {'id': 'map', 'kind': 'map', 'file': 'maps/map.png', 'map_id': 'Map A'},
                   {'id': 'ticket', 'kind': 'illustration', 'file': 'photos/ticket.png'}]
        text = self.text
        for asset in assets:
            asset.update(source_url='https://commons.wikimedia.org/wiki/File:Internal_QA.png',
                         creator='QA author', license='CC0', attribution='CC0', subject=asset['id'])
            target = self.project / asset['file']; target.parent.mkdir(exist_ok=True)
            Image.new('RGB', (900, 600), (70, 90, 120)).save(target)
            if asset['id'] not in ('museum_photo', 'hotel_photo'):
                text += f'\n![{asset["id"]}](../{asset["file"]})\n'
        self.audit()  # Write the catalogue; full audit below reads it itself.
        (self.project / 'research/MEDIA_MANIFEST.json').write_text(json.dumps({'assets': assets}), encoding='utf8')
        self.assertEqual(audit_media(self.project, text,
                                    {'start_date': '2026-07-12', 'end_date': '2026-07-14'}), [])


class PhysicalPdfPlacementTests(unittest.TestCase):
    def test_unused_image_resource_cannot_pass_publication_gate(self):
        import fitz
        from PIL import Image
        from docx import Document
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'research').mkdir(); (project / 'photos').mkdir()
            photo = project / 'photos/photo.png'
            Image.new('RGB', (750, 500), (70, 90, 120)).save(photo)
            (project / 'request.json').write_text('{}', encoding='utf8')
            manuscript = project / 'manuscript.md'; manuscript.write_text('![Photo](../photos/photo.png)', encoding='utf8')
            (project / 'research/MEDIA_MANIFEST.json').write_text(
                json.dumps({'assets': [{'file': 'photos/photo.png'}]}), encoding='utf8')
            doc = Document(); doc.add_picture(str(photo)); docx = project / 'brochure.docx'; doc.save(docx)
            pdf = fitz.open(); page = pdf.new_page(); page.insert_image(fitz.Rect(30, 30, 200, 150), filename=str(photo))
            for xref in page.get_contents(): pdf.update_stream(xref, b'')
            self.assertEqual(len(page.get_images()), 1)
            self.assertEqual(len(page.get_image_info()), 0)
            target = project / 'brochure.pdf'; pdf.save(target); pdf.close()
            with patch('media_utils.audit_media', return_value=[]), patch('media_utils.verify_heading_pagination'):
                with self.assertRaisesRegex(RuntimeError, 'missing actual embedded photos/maps'):
                    verify_published_media(project, manuscript, docx, target)


if __name__ == '__main__':
    unittest.main()
