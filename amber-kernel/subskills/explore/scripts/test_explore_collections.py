import copy
import json
import tempfile
import unittest
from pathlib import Path

import explore_capture as capture
import test_media_extract as fixtures
from scripts.vault_state import BatchError


class CollectionCoverageTests(unittest.TestCase):
    def report(self, count=7):
        report = fixtures.MediaCoverageTests().channel_report()
        del report["sampling"]
        report["sources"] = report["sources"][:1]
        report["body"] = "Fixture channel metadata. [S1]"
        inventory = []
        for number in range(count):
            identifier = f"S{number + 2}"
            video = fixtures.MediaCoverageTests().source()
            video.update(id=identifier, url=f"https://youtube.com/watch?v={number:011d}", status="read")
            video.pop("limitation")
            video["modalities"][1] = {"type": "visual", "status": "observed", "method": "fixture visual inspection", "locator": "explanations throughout 00:00–08:20"}
            report["sources"].append(video)
            report["body"] += f"\nVideo {number} contributes a distinct lesson. [{identifier}]"
            inventory.append({"url": video["url"], "status": "complete", "source_id": identifier})
        report.update(status="complete", collection={"scope": "all", "discovery_status": "complete",
                      "discovery_note": "Fixture Videos, Shorts, and Streams listings enumerated to their ends.", "inventory": inventory})
        return report

    def test_all_seven_items_saved_without_sample_cap(self):
        report = self.report()
        rendered = capture.render(report)
        self.assertIn("discovered: 7; complete: 7", rendered)
        for item in report["collection"]["inventory"]:
            self.assertIn(item["url"], rendered)

    def test_discovery_and_pending_items_prevent_completion(self):
        for failure in ("discovery", "pending", "unavailable", "empty"):
            with self.subTest(failure=failure):
                report = self.report()
                collection = report["collection"]
                if failure == "discovery":
                    collection["discovery_status"] = "partial"
                elif failure == "empty":
                    collection["inventory"] = []
                else:
                    collection["inventory"].append({"url": "https://youtu.be/abcdefghijk", "status": failure, "limitation": "Extraction remains to attempt or unavailable"})
                with self.assertRaisesRegex(BatchError, "every item complete"):
                    capture.render(report)

    def test_url_variants_deduplicated_by_stable_video_id(self):
        report = self.report(1)
        for variant in ("https://youtu.be/00000000000?t=2", "https://youtube.com/shorts/00000000000", "https://youtube.com/watch?v=00000000000&list=PLx"):
            with self.subTest(variant=variant):
                duplicate = copy.deepcopy(report)
                duplicate["collection"]["inventory"].append({"url": variant, "status": "complete", "source_id": "S2"})
                with self.assertRaisesRegex(BatchError, "duplicate collection item"):
                    capture.render(duplicate)

    def test_source_must_match_media_identity_and_be_cited(self):
        for failure in ("identity", "citation"):
            with self.subTest(failure=failure):
                report = self.report(1)
                if failure == "identity":
                    report["collection"]["inventory"][0]["url"] = "https://youtu.be/abcdefghijk"
                else:
                    report["body"] = "Only profile knowledge. [S1]"
                with self.assertRaises(BatchError):
                    capture.render(report)

    def test_partial_media_cannot_be_counted_complete(self):
        report = self.report(1)
        report.update(status="partial", coverage_note="Visual evidence missing")
        report["collection"]["resume_note"] = "Checkpoint: fixture.json; inspect remaining visuals"
        source = report["sources"][1]
        source.update(status="partial", limitation="Visual evidence missing")
        source["modalities"][1] = {"type": "visual", "status": "unavailable", "limitation": "No visual access"}
        with self.assertRaisesRegex(BatchError, "status must match"):
            capture.render(report)
        report["collection"]["inventory"][0].update(status="partial", limitation="Visual evidence missing")
        self.assertIn("complete: 0; partial: 1", capture.render(report))

    def test_partial_capture_requires_durable_resume_instructions(self):
        report = self.report()
        report.update(status="partial", coverage_note="Discovery unfinished")
        report["collection"]["discovery_status"] = "partial"
        with self.assertRaisesRegex(BatchError, "checkpoint and resume"):
            capture.render(report)

    def test_metadata_is_not_extracted_video_knowledge(self):
        report = self.report(1)
        source = report["sources"][1]
        source["modalities"] = [
            {"type": "audio", "status": "not_applicable", "limitation": "Fixture excluded"},
            {"type": "visual", "status": "not_applicable", "limitation": "Fixture excluded"},
            {"type": "metadata", "status": "observed", "method": "title", "locator": "listing"}]
        with self.assertRaisesRegex(BatchError, "substantive media evidence"):
            capture.render(report)

    def test_sample_cannot_claim_complete_channel(self):
        report = self.report(1)
        del report["collection"]
        report["sampling"] = {"scope": "One video", "rationale": "User requested sample", "selected_sources": ["S2"]}
        with self.assertRaisesRegex(BatchError, "sample cannot establish complete"):
            capture.render(report)

    def test_resume_from_json_keeps_prior_snapshot_and_completed_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vault = root / "vault"
            (vault / ".obsidian").mkdir(parents=True)
            (vault / "LandingField").mkdir()
            report = self.report(4)
            report.update(status="partial", coverage_note="One pending video")
            report["collection"]["resume_note"] = f"Checkpoint: {root / 'checkpoint.json'}; process pending video"
            final_item = report["collection"]["inventory"][-1]
            final_source = report["sources"].pop()
            report["body"] = report["body"].rsplit("\n", 1)[0]
            final_item.update(status="pending", limitation="Process next batch")
            del final_item["source_id"]
            checkpoint = root / "checkpoint.json"
            checkpoint.write_text(json.dumps(report), encoding="utf-8")
            first = capture.capture(vault, report, apply=True)
            original = (vault / first["path"]).read_bytes()
            resumed = json.loads(checkpoint.read_text(encoding="utf-8"))
            prior_sources = copy.deepcopy(resumed["sources"])
            resumed["sources"].append(final_source)
            resumed["body"] += "\nLast video's distinct lesson. [S5]"
            resumed["collection"]["inventory"][-1] = {"url": final_source["url"], "status": "complete", "source_id": "S5"}
            resumed["status"] = "complete"
            resumed["coverage_note"] = "Discovery and all four items complete"
            resumed["collection"].pop("resume_note")
            second = capture.capture(vault, resumed, apply=True, new_capture=True)
            self.assertEqual(second["collection"]["complete"], 4)
            self.assertEqual(resumed["sources"][:-1], prior_sources)
            self.assertEqual((vault / first["path"]).read_bytes(), original)
            self.assertNotEqual(first["path"], second["path"])
            self.assertEqual(second["earlier_captures"], [first["path"]])


if __name__ == "__main__":
    unittest.main()
