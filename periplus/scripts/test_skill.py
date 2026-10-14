#!/usr/bin/env python3
"""Offline tests of request validation, pipeline orchestration, resumability and publication gates."""
from __future__ import annotations
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from generate import ensure_request, main, PHASES
from trip_dates import publication_stem


class PeriplusTests(unittest.TestCase):
    def request(self):
        return {"destination": "Kyoto", "country": "Japan", "start_date": "2026-11-05",
                "end_date": "2026-11-07", "flights": {
                    "outbound": {"flight_number": "MU123", "departure_airport": "Shanghai Pudong", "arrival_airport": "Kansai"},
                    "return": {"flight_number": "MU124", "departure_airport": "Kansai", "arrival_airport": "Beijing Capital"}},
                "customization": {"notes": "Architecture and photography"}}

    def test_input_validation(self):
        req = self.request()
        self.assertEqual(ensure_request(req)["flights"]["return"]["flight_number"], "MU124")
        self.assertEqual(ensure_request(req)["customization"]["language"], "zh-CN")
        self.assertEqual(ensure_request(req)["customization"]["name_languages"], ["zh-CN", "en", "local"])
        jp = self.request(); jp["destination"] = "\u4eac\u90fd"; jp["customization"]["notes"] = "\u5efa\u7bc9、\u9244\u9053、\u5199\u771f"
        self.assertEqual(ensure_request(jp)["destination"], "\u4eac\u90fd")
        es = self.request(); es["customization"]["notes"] = "visitar museos y estaciones"
        self.assertEqual(ensure_request(es)["customization"]["notes"], "visitar museos y estaciones")
        # Old flight-based request is accepted for backward compatibility.
        old = self.request()
        converted = ensure_request(old)
        self.assertEqual(converted['journey']['outbound']['mode'], 'flight')
        self.assertEqual(converted['journey']['outbound']['service'], 'MU123')
        # Core mode-agnostic request: rail transport and an optional booked hotel.
        rail = {"destination":"Kyoto", "start_date":"2026-11-05", "end_date":"2026-11-07",
                "journey":{"outbound":{"mode":"rail", "service":"Nozomi 123", "origin":"Tokyo Station", "destination":"Kyoto Station"},
                           "return":{"mode":"rail", "service":"Nozomi 456", "origin":"Kyoto Station", "destination":"Osaka Station"}},
                "hotel":{"name":"Kyoto Station Hotel", "address":"1 Station Road", "status":"booked"}}
        valid = ensure_request(rail)
        self.assertEqual(valid['hotel']['status'], 'booked')
        self.assertEqual(valid['journey']['outbound']['mode'], 'rail')
        self.assertEqual(valid['journey']['outbound']['origin'], 'Tokyo Station')
        self.assertEqual(valid['journey']['return']['destination'], 'Osaka Station')
        missing_start = json.loads(json.dumps(rail))
        del missing_start['journey']['outbound']['origin']
        with self.assertRaisesRegex(ValueError, 'origin required'):
            ensure_request(missing_start)
        missing_end = json.loads(json.dumps(rail))
        del missing_end['journey']['return']['destination']
        with self.assertRaisesRegex(ValueError, 'destination required'):
            ensure_request(missing_end)
        self.assertIsNone(valid.get('flights'))
        water = {**rail, "journey":{"outbound":{"mode":"ferry", "service":"Ferry A", "origin":"Osaka Port"},
                                    "return":{"mode":"drive", "route":"Home expressway", "destination":"Kobe"}}}
        self.assertEqual(ensure_request(water)['journey']['return']['mode'], 'drive')
        bad = {**rail, "journey":{"outbound":{"mode":"teleport", "origin":"Tokyo"}, "return":{"mode":"rail", "destination":"Osaka"}}}
        with self.assertRaises(ValueError):ensure_request(bad)
        bad2 = self.request()
        bad2["end_date"] = "2026-11-02"
        with self.assertRaises(ValueError):
            ensure_request(bad2)

    def test_english_font_default(self):
        from export_brochure import WESTERN_FONT, EAST_ASIAN_FONT, style_font
        from docx import Document
        self.assertEqual(WESTERN_FONT, 'Oswald')
        doc = Document()
        style_font(doc.styles['Normal'])
        self.assertEqual(doc.styles['Normal'].font.name, 'Oswald')
        from docx.oxml.ns import qn
        self.assertEqual(doc.styles['Normal']._element.rPr.rFonts.get(qn('w:eastAsia')), EAST_ASIAN_FONT)

    def test_dry_run_does_not_fake_final(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "request.json"
            inp.write_text(json.dumps(self.request()), encoding="utf-8")
            rc = main(["--request", str(inp), "--out", tmp, "--dry-run"])
            self.assertEqual(rc, 0)
            project = Path(tmp) / "2026-11-05-kyoto-2026-11-07"
            self.assertTrue((project / "TASKS.md").is_file())
            self.assertFalse((project / "exports/Seven_Ninths_Travel_Brochure.md").exists())
            self.assertEqual(json.loads((project / "project.json").read_text())["release_status"], "IN_PROGRESS")

    def test_seven_phases_and_release_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "request.json"
            inp.write_text(json.dumps(self.request()), encoding="utf-8")
            invoked = []

            def simulate_agent(binary, proj, phase):
                invoked.append(phase)
                targets = dict(PHASES)
                target = proj / targets[phase]
                target.parent.mkdir(exist_ok=True, parents=True)
                if phase == "06_compose_publish":
                    titles = ["Arrival & Departure", "Accommodation", "Brief Sketch", "History", "Geography", "Climate", "Population", "Politics", "Economy", "Education", "Culture", "Transportation", "Attractions & Schedule", "Attractions", "Schedule", "Sightseeing & Adventure"]
                    body = "# Japan Kyoto — Seven Ninths Travel Brochure\n\n"
                    body += "\n".join("## " + x + "\n" + "\u4eac\u90fd\u8fd9\u5ea7\u57ce\u5e02\u62e5\u6709\u503c\u5f97\u8bb0\u5f55\u7684\u4e30\u5bcc\u5efa\u7b51、\u516c\u5171\u4ea4\u901a\u548c\u8857\u533a\u751f\u6d3b。" * 8 for x in titles)
                    body += "\n".join("\n### " + x + "\n" + "\u4eac\u90fd\u62e5\u6709\u4e30\u5bcc\u7684\u5386\u53f2\u6587\u5316\u80cc\u666f。" * 5 for x in ["Administrative Region", "Religion", "International Exchange", "Subculture", "Art & Craft", "Architecture", "Museum", "Language & Dialect", "Localism", "Sports", "Media", "Literature", "Events & Festivals"])
                    body += "\n## Around Area\n### Uji\n\u5b87\u6cbb：\u5f53\u5929\u8fd4\u56de\u4eac\u90fd，\u94c1\u8def\u5f80\u8fd4\u548c\u89c2\u5149\u8def\u7ebf\u9700\u8981\u63d0\u524d\u6838\u5b9e。\n"
                    body += "\n".join("## " + x + "\n" + "\u4eac\u90fd\u7684\u5b9e\u9645\u5386\u53f2\u6587\u5316\u666f\u70b9\u503c\u5f97\u4ed4\u7ec6\u7814\u7a76。" * 5 for x in ["Tours", "Delicacy & Shopping", "Restaurant & Café & Bar", "Supermarket & Store & Market", "Recommends & Tips", "Tourist Travel Pass & Ticket", "Tourist Center", "Tickets & Prices", "Practical Information", "Currency", "Embassy", "Important Numbers", "Useful links"])
                    body += "\nMU123  MU124  Shanghai Pudong  Beijing Capital  \u4eac\u90fd Kyoto\n"
                    body += "\n" + "\n".join(f"### Fixture venue {i}\n<!-- periplus-entry: fixture_{i} -->\n![\u6d4b\u8bd5\u7d20\u6750](../photos/test_photo_{i}.png)" for i in range(1,4)) + "\n![Map A \u5730\u56fe](../maps/map_a.png)"
                    body += "\n### Map A – Kyoto Station\n\u5730\u56fe\u4ec5\u7528\u4e8e\u5355\u5143\u6d4b\u8bd5。\n"
                    body += "\n".join(["### " + x + "\n\u7814\u7a76\u4e2d\u7684\u5b8c\u6574\u884c\u7a0b\u4fe1\u606f。" for x in ["2026-11-05", "2026-11-06", "2026-11-07"]])
                    body += "\n".join(f"https://example{i}.org/path" for i in range(12))
                    body += "\n" + ("\u4eac\u90fd\u5e02\u7684\u5efa\u7b51、\u6587\u5316、\u57ce\u5e02\u4ea4\u901a\u4e0e\u5730\u57df\u73af\u5883\u4e3a\u65c5\u884c\u8005\u63d0\u4f9b\u591a\u5c42\u6b21\u7684\u89c2\u5bdf\u4e0e\u8bb0\u5f55\u7ef4\u5ea6。" * 180)
                    target.write_text(body, encoding="utf-8")
                else:
                    target.write_text("\u8c03\u67e5\u5185\u5bb9。" * 150, encoding="utf-8")
                if phase == "03_attractions_around_area":
                    from PIL import Image
                    records=[]
                    for i in range(1,4):
                        file=f"photos/test_photo_{i}.png"
                        Image.new('RGB',(750,500),(i*30,70,110)).save(proj/file)
                        records.append({"id":f"photo_{i}","kind":"photo","entry_ids":[f"fixture_{i}"],"file":file,
                            "source_url":f"https://commons.wikimedia.org/wiki/File:Internal_QA_{i}.png","creator":"Unit-test author",
                            "license":"CC0", "attribution":"CC0", "subject":"Test photo"})
                    Image.new('RGB',(1000,650),(50,60,90)).save(proj/'maps/map_a.png')
                    records.append({"id":"map_a", "kind":"map", "map_id":"Map A", "file":"maps/map_a.png",
                        "source_url":"https://www.openstreetmap.org/copyright", "creator":"Unit-test author", "license":"CC0",
                        "attribution":"CC0", "subject":"Map A Test"})
                    (proj/'research/MEDIA_MANIFEST.json').write_text(json.dumps({"assets":records}),encoding='utf8')
                    (proj/"research/ENTRY_CATALOGUE.json").write_text(json.dumps({"entries":[{"id":f"fixture_{i}","category":"attraction","name":f"Fixture venue {i}","heading":f"Fixture venue {i}","photo_ids":[f"photo_{i}"]} for i in range(1,4)]}),encoding="utf8")
                    (proj / "research/NAME_INDEX.md").write_text(
                        "| \u4e2d\u6587 | English | \u65e5\u672c\u8a9e | \u5047\u540d | Romaji | URL |\n"
                        "| --- | --- | --- | --- | --- | --- |\n" +
                        "| \u4eac\u90fd\u7ad9 | Kyoto Station | \u4eac\u90fd\u99c5 | \u304d\u3087\u3046\u3068\u3048\u304d | Kyōto-eki | https://example.org/kyoto |\n" * 12,
                        encoding="utf-8")
                if phase == "01_research_operations":
                    (proj/"research/TRANSPORT_PLAN.json").write_text(json.dumps({"legs":[{"id":role,"role":role,"mode":"flight","origin":"Shanghai Pudong" if role=="outbound" else "Kansai","destination":"Kansai" if role=="outbound" else "Beijing Capital","status":"recommended","operator":"Fixture airline","service":"MU123" if role=="outbound" else "MU124","departure":"2026-11-05T09:00:00+08:00" if role=="outbound" else "2026-11-07T09:00:00+09:00","arrival":"2026-11-05T13:00:00+09:00" if role=="outbound" else "2026-11-07T13:00:00+08:00","source_urls":["https://www.jreast.co.jp/"],"checked_on":"2026-10-14"} for role in ["outbound","return"]],"considered_modes":[{"mode":mode,"status":"viable","route":"Fixture transfer","source_url":"https://www.jreast.co.jp/","note":"Unit fixture only"} for mode in ["rail","bus","taxi"]]}),encoding="utf8")
                    (proj / "research/EVIDENCE_LEDGER.md").write_text("# Evidence\n" + "\n".join(f"https://example{i}.org/path" for i in range(12)), encoding="utf-8")
                return 0

            def fake_export(project, formats):
                # Unit-test the release orchestration without depending on LO/Codex CLI.
                out = []
                for ext in formats:
                    target = Path(project) / "exports" / f"{publication_stem(self.request())}.{ext}"
                    target.write_bytes(b"MOCK_ONLY_DO_NOT_DISTRIBUTE" * 100)
                    out.append(target)
                return out

            with patch("generate.shutil.which", return_value="codex"), \
                 patch("generate.run_codex", side_effect=simulate_agent), \
                 patch("media_utils.audit_media", return_value=[]), \
                 patch("export_brochure.export_project", side_effect=fake_export):
                code = main(["--request", str(inp), "--out", tmp])
            self.assertEqual(code, 0)
            self.assertEqual(invoked, [p for p, _ in PHASES])
            project = Path(tmp) / "2026-11-05-kyoto-2026-11-07"
            self.assertEqual(json.loads((project / "project.json").read_text())["release_status"], "FINAL")
            # Resume should not execute any phase again.
            with patch("generate.shutil.which", return_value="codex"), \
                 patch("generate.run_codex") as mock_run, \
                 patch("media_utils.audit_media", return_value=[]), \
                 patch("export_brochure.export_project", side_effect=fake_export):
                self.assertEqual(main(["--resume", "--project", str(project)]), 0)
                mock_run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
