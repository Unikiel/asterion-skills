#!/usr/bin/env python3
"""Regression coverage for reader voice, product scope and real connection margins."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from reader_qa import audit_reader_text, audit_transport_plan
from generate import ensure_request

class ReaderQATests(unittest.TestCase):
    def plan(self):
        return {'legs':[{'id':'arrival','role':'outbound','mode':'rail','origin':'Airport A','destination':'Hotel station',
          'operator':'Exercise railway','status':'recommended','service':'Train 42','source_urls':['https://www.jreast.co.jp/'],'checked_on':'2026-10-14',
          'departure':'2026-11-05T19:30:00+09:00','arrival':'2026-11-05T20:15:00+09:00',
          'preceding':{'type':'international_flight','ends_at':'2026-11-05T17:20:00+09:00','buffer_minutes':{
              'disembarkation':10,'immigration':45,'baggage':20,'customs':10,'terminal_transfer':15,'ticketing_boarding':10,'delay_reserve':20}}},
          {'id':'return','role':'return','mode':'taxi','origin':'Hotel','destination':'Airport A','operator':'Exercise taxi',
           'status':'continuous','route':'Airport transfer','source_urls':['https://www.jreast.co.jp/'],'checked_on':'2026-10-14'}],
          'considered_modes':[{'mode':m,'status':'viable','route':'Airport transfer','source_url':'https://www.jreast.co.jp/','note':'Exercise alternative'} for m in ['rail','bus','taxi']]}
    def audit(self, plan):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'research';p.mkdir();(p/'TRANSPORT_PLAN.json').write_text(json.dumps(plan))
            return audit_transport_plan(t,'Train 42 19:30 → 20:15',{})
    def test_safe_international_connection(self): self.assertEqual(self.audit(self.plan()),[])
    def test_early_train_rejected(self):
        p=self.plan();p['legs'][0]['departure']='2026-11-05T18:40:00+09:00';self.assertTrue(any('buffers finish' in e for e in self.audit(p)))
    def test_previous_activity_crosses_midnight(self):
        p=self.plan();l=p['legs'][0];l['departure']='2026-11-06T00:20:00+09:00';l['arrival']='2026-11-06T01:00:00+09:00';l['preceding']={'type':'workshop','ends_at':'2026-11-05T23:45:00+09:00','buffer_minutes':{'exit':10,'walking':15,'boarding':15}}
        self.assertTrue(any('buffers finish' in e for e in self.audit(p)))
    def test_offsets_compared_as_instants(self):
        p=self.plan();p['legs'][0]['preceding']['ends_at']='2026-11-05T16:20:00+08:00';self.assertEqual(self.audit(p),[])
    def test_naive_times_rejected(self):
        p=self.plan();p['legs'][0]['departure']='2026-11-05T19:30:00';self.assertTrue(any('UTC offset' in e for e in self.audit(p)))
    def test_negative_and_boolean_buffers_rejected(self):
        for v in [-2,True]:
            p=self.plan();p['legs'][0]['preceding']['buffer_minutes']['baggage']=v;self.assertTrue(self.audit(p))
    def test_missing_immigration_component_rejected(self):
        p=self.plan();del p['legs'][0]['preceding']['buffer_minutes']['immigration'];self.assertTrue(any('incomplete' in e for e in self.audit(p)))
    def test_missing_service_is_not_an_input_blocker(self):
        p={'destination':'City B','start_date':'2026-11-05','end_date':'2026-11-07','journey':{'outbound':{'mode':'rail','origin':'Station A'},'return':{'mode':'rail','destination':'Station C'}}}
        self.assertEqual(ensure_request(p)['journey']['outbound']['origin'],'Station A')
    def test_recommendation_needs_specific_service(self):
        p=self.plan();del p['legs'][0]['service'];self.assertTrue(any('actual service' in e for e in self.audit(p)))
    def test_historical_data_gap_requires_disclosure(self):
        p=self.plan();l=p['legs'][0];l['status']='historical_unavailable';del l['departure'];del l['arrival'];self.assertTrue(any('limitation' in e for e in self.audit(p)));l['limitation']='Original July timetable not found';self.assertEqual(self.audit(p),[])
    def test_missing_alternatives_rejected(self):
        p=self.plan();del p['considered_modes'];self.assertTrue(any('multimodal' in e for e in self.audit(p)))
    def test_two_modes_need_geographical_reason(self):
        p=self.plan();p["considered_modes"]=p["considered_modes"][:2];self.assertTrue(any("three modes" in e for e in self.audit(p)));p["alternatives_limitation"]="Exercise island has no road access";self.assertEqual(self.audit(p),[])
    def test_transfer_without_prior_rejected(self):
        p=self.plan();l=copy.deepcopy(p["legs"][0]);l["id"]="transfer";l["role"]="transfer";del l["preceding"];p["legs"].append(l);self.assertTrue(any("lacks preceding" in e for e in self.audit(p)))
    def test_internal_monologue_rejected(self):
        text='# Sightseeing & Adventure\n## Around Area\n\u672c\u624b\u518c\u8981\u6c42Around Area\u5fc5\u987b\u4e00\u65e5\u5f80\u8fd4。\n### \u5f18\u524d\u4e00\u65e5\u5f80\u8fd4\n';self.assertEqual(len(audit_reader_text(text,{})),2)
    def test_product_prices_valid_but_budget_rejected(self):
        self.assertEqual(audit_reader_text('## Tickets & Prices \u901a\u7968\n\u7ec4\u5408900\u65e5\u5143，\u5206\u4e701200，\u5c11300。',{}),[])
        self.assertTrue(audit_reader_text('## Tickets & Prices\n\u56db\u5929\u9884\u7b9768000\u65e5\u5143。',{}))
    def test_reader_useful_caveat_valid(self):
        self.assertEqual(audit_reader_text('## Around Area\n### \u5f18\u524d / Hirosaki\n\u8fd4\u56de\u9752\u68ee16:50；\u9047\u665a\u70b9\u4e58\u4e0b\u4e00\u73ed。\n## Tickets & Prices\n\u672a\u627e\u5230\u4e03\u6708\u539f\u59cb\u65f6\u523b\u8868。',{}),[])

if __name__=='__main__':unittest.main()
