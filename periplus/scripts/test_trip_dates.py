#!/usr/bin/env python3
import copy
from datetime import date,timedelta
from pathlib import Path
import tempfile
import unittest
from trip_dates import normalize_trip_dates, trip_days, trip_periods, display_trip_dates, publication_stem, audit_schedule_periods
from generate import ensure_request, parse_args, from_args
from export_brochure import cover_text

class TripDateTests(unittest.TestCase):
    def request(self):
        return {'destination':'Tokyo','country':'Japan','date_ranges':[{'start_date':'2026-07-11','end_date':'2026-07-12'},{'start_date':'2026-07-17','end_date':'2026-07-19'}],
                'journey':{'outbound':{'mode':'rail','origin':'Ueno Station'},'return':{'mode':'rail','destination':'Hachinohe Station'}}}
    def test_exact_user_example(self): self.assertEqual(publication_stem(self.request()),'2026.Japan.Tokyo.0711-0712.0717-0719')
    def test_active_days_exclude_gap(self):self.assertEqual([d.isoformat() for d in trip_days(self.request())],['2026-07-11','2026-07-12','2026-07-17','2026-07-18','2026-07-19'])
    def test_legacy_single_range(self):
        p=self.request();del p['date_ranges'];p.update(start_date='2026-07-11',end_date='2026-07-19');self.assertEqual(publication_stem(ensure_request(p)),'2026.Japan.Tokyo.0711-0719')
    def test_twenty_periods_not_fixed_to_two(self):
        p=self.request();p['date_ranges']=[{'start_date':(date(2026,1,1)+timedelta(days=3*i)).isoformat(),'end_date':(date(2026,1,1)+timedelta(days=3*i)).isoformat()} for i in range(20)]
        self.assertEqual(len(trip_periods(ensure_request(p))),20);self.assertEqual(len(publication_stem(p).split('.')),23);self.assertEqual(len(list(trip_days(p))),20)
    def test_sort_periods_without_merging(self):
        p=self.request();p['date_ranges'].reverse();self.assertEqual(publication_stem(p),'2026.Japan.Tokyo.0711-0712.0717-0719')
    def test_adjacent_periods_stay_distinct(self):
        p=self.request();p['date_ranges'][1]={'start_date':'2026-07-13','end_date':'2026-07-14'};self.assertEqual(publication_stem(p),'2026.Japan.Tokyo.0711-0712.0713-0714')
    def test_overlap_and_duplicate_rejected(self):
        for period in [{'start_date':'2026-07-12','end_date':'2026-07-14'},{'start_date':'2026-07-11','end_date':'2026-07-12'}]:
            p=self.request();p['date_ranges'][1]=period
            with self.assertRaisesRegex(ValueError,'overlap'): ensure_request(p)
    def test_conflicting_envelope_rejected(self):
        p=self.request();p['end_date']='2026-07-20'
        with self.assertRaisesRegex(ValueError,'conflicts'):ensure_request(p)
    def test_empty_and_inverted_ranges(self):
        for ranges in [[],[{'start_date':'2026-07-19','end_date':'2026-07-11'}]]:
            p=self.request();p['date_ranges']=ranges
            with self.assertRaises(ValueError):ensure_request(p)
    def test_chinese_input_uses_verified_english_labels(self):
        p=self.request();p.update(destination='\u4e1c\u4eac',country='\u65e5\u672c',destination_en='Tokyo',country_en='Japan');name=publication_stem(p);self.assertEqual(name,'2026.Japan.Tokyo.0711-0712.0717-0719');self.assertTrue(name.isascii())
    def test_non_english_filename_needs_researched_label(self):
        p=self.request();p['destination']='\u4e1c\u4eac'
        with self.assertRaisesRegex(ValueError,'destination_en'):publication_stem(p)
    def test_ascii_safe_components(self):
        p=self.request();p.update(country='United Kingdom',destination='New York');self.assertTrue(publication_stem(p).startswith('2026.United-Kingdom.New-York.'))
    def test_cross_year_unambiguous(self):
        p=self.request();p['date_ranges']=[{'start_date':'2026-12-30','end_date':'2027-01-02'},{'start_date':'2027-03-10','end_date':'2027-03-12'}];self.assertEqual(publication_stem(p),'2026-2027.Japan.Tokyo.20261230-20270102.20270310-20270312')
    def test_month_crossing(self):
        p=self.request();p['date_ranges']=[{'start_date':'2026-07-30','end_date':'2026-08-02'}];self.assertEqual(publication_stem(p),'2026.Japan.Tokyo.0730-0802')
    def test_cover_retains_both_ranges(self):
        dates=cover_text(self.request(),'Tokyo')[2];self.assertEqual(dates,'2026.07.11 – 2026.07.12\n2026.07.17 – 2026.07.19')
    def test_cli_repeatable_ranges(self):
        args=parse_args(['--destination','Tokyo','--country','Japan','--outbound-origin','Ueno','--return-destination','Hachinohe','--date-range','2026-07-11:2026-07-12','--date-range','2026-07-17:2026-07-19']);self.assertEqual(len(from_args(args)['date_ranges']),2)
    def test_hotel_and_journey_per_period_preserved(self):
        p=self.request();p['date_ranges'][1]['hotel']={'name':'Second hotel'};p=ensure_request(p);self.assertEqual(p['date_ranges'][1]['hotel']['name'],'Second hotel');self.assertEqual(p['start_date'],'2026-07-11');self.assertEqual(p['end_date'],'2026-07-19')

    def test_gap_and_duplicate_schedule_rejected(self):
        text="## Schedule\n### 2026-07-11 Saturday\n### 2026-07-13 Monday\n### 2026-07-11 Duplicate\n## Another section\n### 2026-07-14 Not schedule\n"
        errors=audit_schedule_periods(text,self.request());self.assertEqual(len(errors),2)
    def test_period_group_heading_is_not_a_day_card(self):
        text="## Schedule\n### 2026-07-11 \u81f3 2026-07-12\n#### 2026-07-11 Saturday\n#### 2026-07-12 Sunday\n### 2026-07-17 \u81f3 2026-07-19\n#### 2026-07-17 Friday\n"
        self.assertEqual(audit_schedule_periods(text,self.request()),[])
    def test_exporter_writes_actual_period_based_paths(self):
        from unittest.mock import patch,MagicMock
        from export_brochure import export_project
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'exports').mkdir();(root/'request.json').write_text(json.dumps(self.request()));(root/'exports/Seven_Ninths_Travel_Brochure.md').write_text('# Arrival & Departure\nFixture only')
            def writer(source,dest,**kwargs):dest.write_bytes(b'FORMAT_ROUTING_FIXTURE_ONLY');return []
            def converter(docx,dest):dest.write_bytes(b'FORMAT_ROUTING_FIXTURE_ONLY');return MagicMock()
            with patch('export_brochure.write_docx',side_effect=writer),patch('export_brochure.pdf_from_docx',side_effect=converter),patch('export_brochure.outline_pages',return_value={}),patch('export_brochure.audit_toc'),patch('reader_qa.audit_reader_text',return_value=[]),patch('reader_qa.audit_transport_plan',return_value=[]),patch('media_utils.verify_published_media'):
                outputs=export_project(root,['docx','pdf','md'])
            self.assertEqual([p.name for p in outputs],['2026.Japan.Tokyo.0711-0712.0717-0719.docx','2026.Japan.Tokyo.0711-0712.0717-0719.pdf','2026.Japan.Tokyo.0711-0712.0717-0719.md']);self.assertTrue(all(p.exists() for p in outputs));self.assertTrue((root/'exports/Seven_Ninths_Travel_Brochure.md').exists())

if __name__=='__main__':unittest.main()
