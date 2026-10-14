#!/usr/bin/env python3
"""Offline tests of request validation, pipeline orchestration, resumability and publication gates."""
from __future__ import annotations
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from generate import ensure_request, main, PHASES


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
        jp = self.request(); jp["destination"] = "京都"; jp["customization"]["notes"] = "建築、鉄道、写真"
        self.assertEqual(ensure_request(jp)["destination"], "京都")
        es = self.request(); es["customization"]["notes"] = "visitar museos y estaciones"
        self.assertEqual(ensure_request(es)["customization"]["notes"], "visitar museos y estaciones")
        # Old flight-based request is accepted for backward compatibility.
        old = self.request()
        converted = ensure_request(old)
        self.assertEqual(converted['journey']['outbound']['mode'], 'flight')
        self.assertEqual(converted['journey']['outbound']['service'], 'MU123')
        # Core v2.4 request: rail transport and an optional booked hotel.
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
                    body += "\n".join("## " + x + "\n" + "京都这座城市拥有值得记录的丰富建筑、公共交通和街区生活。" * 8 for x in titles)
                    body += "\n".join("\n### " + x + "\n" + "京都拥有丰富的历史文化背景。" * 5 for x in ["Administrative Region", "Religion", "International Exchange", "Subculture", "Art & Craft", "Architecture", "Museum", "Language & Dialect", "Localism", "Sports", "Media", "Literature", "Events & Festivals"])
                    body += "\n## Around Area\n### Uji\n宇治：当天返回京都，铁路往返和观光路线需要提前核实。\n"
                    body += "\n".join("## " + x + "\n" + "京都的实际历史文化景点值得仔细研究。" * 5 for x in ["Tours", "Delicacy & Shopping", "Restaurant & Café & Bar", "Supermarket & Store & Market", "Recommends & Tips", "Tourist Travel Pass & Ticket", "Tourist Center", "Tickets & Prices", "Practical Information", "Currency", "Embassy", "Important Numbers", "Useful links"])
                    body += "\nMU123  MU124  Shanghai Pudong  Beijing Capital  京都 Kyoto\n"
                    body += "\n" + "\n".join("![测试素材](../" + f + ")" for f in ["photos/test_photo_1.png", "photos/test_photo_2.png", "photos/test_photo_3.png", "maps/map_a.png"])
                    body += "\n### Map A – Kyoto Station\n地图仅用于单元测试。\n"
                    body += "\n".join(["### " + x + "\n研究中的完整行程信息。" for x in ["2026-11-05", "2026-11-06", "2026-11-07"]])
                    body += "\n".join(f"https://example{i}.org/path" for i in range(12))
                    body += "\n" + ("京都市的建筑、文化、城市交通与地域环境为旅行者提供多层次的观察与记录维度。" * 180)
                    target.write_text(body, encoding="utf-8")
                else:
                    target.write_text("调查内容。" * 150, encoding="utf-8")
                if phase == "03_attractions_around_area":
                    from PIL import Image
                    records=[]
                    for i in range(1,4):
                        file=f"photos/test_photo_{i}.png"
                        Image.new('RGB',(750,500),(i*30,70,110)).save(proj/file)
                        records.append({"id":f"photo_{i}","kind":"photo","file":file,
                            "source_url":f"https://commons.wikimedia.org/wiki/File:Internal_QA_{i}.png","creator":"Unit-test author",
                            "license":"CC0", "attribution":"CC0", "subject":"Test photo"})
                    Image.new('RGB',(1000,650),(50,60,90)).save(proj/'maps/map_a.png')
                    records.append({"id":"map_a", "kind":"map", "map_id":"Map A", "file":"maps/map_a.png",
                        "source_url":"https://www.openstreetmap.org/copyright", "creator":"Unit-test author", "license":"CC0",
                        "attribution":"CC0", "subject":"Map A Test"})
                    (proj/'research/MEDIA_MANIFEST.json').write_text(json.dumps({"assets":records}),encoding='utf8')
                    (proj / "research/NAME_INDEX.md").write_text(
                        "| 中文 | English | 日本語 | 假名 | Romaji | URL |\n"
                        "| --- | --- | --- | --- | --- | --- |\n" +
                        "| 京都站 | Kyoto Station | 京都駅 | きょうとえき | Kyōto-eki | https://example.org/kyoto |\n" * 12,
                        encoding="utf-8")
                if phase == "01_research_operations":
                    (proj / "research/EVIDENCE_LEDGER.md").write_text("# Evidence\n" + "\n".join(f"https://example{i}.org/path" for i in range(12)), encoding="utf-8")
                return 0

            def fake_export(project, formats):
                # Unit-test the release orchestration without depending on LO/Codex CLI.
                out = []
                for ext in formats:
                    target = Path(project) / "exports" / f"Seven_Ninths_Travel_Brochure.{ext}"
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
