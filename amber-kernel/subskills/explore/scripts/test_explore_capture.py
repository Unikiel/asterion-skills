import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import explore_capture as explore
from scripts.vault_state import BatchError, snapshot


class ExploreCaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "Vault"
        for name in (".obsidian", "LandingField", "Observatory"):
            (self.root / name).mkdir(parents=True, exist_ok=True)
        self.report = {
            "version": 1, "url": "https://example.org/article?version=2#evidence",
            "title": "Evidence and a useful mechanism", "accessed": "2026-09-12",
            "status": "complete", "seed_source": "S1",
            "body": "## Summary\n\nThe fixture article describes a mechanism. [S1]\n\n## Deeper understanding\n\nA primary source explains its assumptions. [S2]\n\n## Interpretation and questions\n\nInterpretation: the scope may be narrower than the headline. [S1] [S2]\n",
            "sources": [
                {"id": "S1", "url": "https://example.org/article?version=2#evidence", "title": "Fixture article", "status": "read", "locator": "Evidence section"},
                {"id": "S2", "url": "https://example.org/research", "title": "Fixture primary evidence", "status": "read"}
            ]
        }

    def test_preview_and_apply_one_cited_note_without_directory_changes(self):
        original = snapshot(self.root)
        preview = explore.capture(str(self.root), self.report)
        self.assertFalse(preview["applied"])
        self.assertEqual(snapshot(self.root), original)
        result = explore.capture(str(self.root), self.report, apply=True)
        self.assertTrue(result["applied"])
        self.assertEqual(result["sources_read"], 2)
        files, dirs = snapshot(self.root)
        self.assertEqual(dirs, original[1])
        self.assertEqual(len(files), 1)
        text = files[result["path"]].decode()
        self.assertIn("[S1]: <https://example.org/article?version=2#evidence>", text)
        self.assertIn("Research coverage:** complete", text)
        self.assertFalse(text.startswith("---"))
        self.assertFalse(list((self.root / "LandingField").glob("*.tmp")))

    def test_rerun_finds_capture_after_parse_move_and_rename(self):
        result = explore.capture(str(self.root), self.report, apply=True)
        moved = self.root / "Observatory/A renamed source.md"
        (self.root / result["path"]).rename(moved)
        changed = copy.deepcopy(self.report)
        changed["title"] = "An updated title"
        receipt = explore.capture(str(self.root), changed, apply=True)
        self.assertEqual(receipt["status"], "already-captured")
        self.assertEqual(receipt["existing"], ["Observatory/A renamed source.md"])
        self.assertEqual(len(snapshot(self.root)[0]), 1)

    def test_explicit_revisit_preserves_and_links_prior_capture(self):
        first = explore.capture(str(self.root), self.report, apply=True)
        original = (self.root / first["path"]).read_bytes()
        second = explore.capture(str(self.root), self.report, apply=True, new_capture=True)
        third = explore.capture(str(self.root), self.report, apply=True, new_capture=True)
        self.assertNotEqual(first["path"], second["path"])
        self.assertNotEqual(second["path"], third["path"])
        self.assertEqual((self.root / first["path"]).read_bytes(), original)
        self.assertIn("Earlier captures", (self.root / second["path"]).read_text(encoding="utf-8"))

    def test_partial_access_and_blocked_seed_are_honest(self):
        self.report["status"] = "partial"
        self.report["coverage_note"] = "Only the opening section was accessible."
        self.report["sources"][0].update(status="partial", limitation="Full text unavailable.")
        text = explore.render(self.report)
        self.assertIn("Research coverage:** partial", text)
        self.assertIn("Full text unavailable", text)
        self.report.update(status="blocked", body="The target could not be read. Revisit with accessible text.")
        self.report["sources"] = [dict(self.report["sources"][0], status="unavailable")]
        receipt = explore.capture(str(self.root), self.report, apply=True)
        self.assertEqual(receipt["sources_read"], 0)
        self.assertEqual(receipt["status"], "blocked")

    def test_unavailable_source_cannot_support_a_claim(self):
        self.report.update(status="partial", coverage_note="A supporting source is unavailable.")
        self.report["sources"][1].update(status="unavailable", limitation="Access denied")
        with self.assertRaisesRegex(BatchError, "no readable source"):
            explore.render(self.report)

    def test_invalid_or_redirected_citation_is_rejected(self):
        for body in ("Unsupported assertion [S99]", "A fact [S1](https://other.example/)", "A fact [S1]\n\n[S1]: https://other.example/", "An uncited summary"):
            with self.subTest(body=body), self.assertRaises(BatchError):
                explore.render(dict(self.report, body=body))

    def test_seed_provenance_and_coverage_mismatch_are_rejected(self):
        bad = copy.deepcopy(self.report)
        bad["sources"][0]["url"] = "https://other.example/"
        with self.assertRaisesRegex(BatchError, "seed_source"):
            explore.render(bad)
        bad = copy.deepcopy(self.report)
        bad["sources"][0].update(status="unavailable", limitation="Not read")
        with self.assertRaisesRegex(BatchError, "unread seed"):
            explore.render(bad)
        with self.assertRaisesRegex(BatchError, "coverage_note"):
            explore.render(dict(self.report, status="partial"))

    def test_url_normalization_preserves_semantic_query_and_fragment(self):
        self.assertEqual(explore.normalize_url("HTTPS://EXAMPLE.org:443/article?q=one#part"), "https://example.org/article?q=one#part")
        self.assertNotEqual(explore.normalize_url("https://example.org/?id=1"), explore.normalize_url("https://example.org/?id=2"))
        for url in ("file:///private", "javascript:alert(1)", "https://user:pass@example.org/", "not-a-url", "https://example.org:bad/", "https://example.org/a b"):
            with self.subTest(url=url), self.assertRaises(BatchError):
                explore.normalize_url(url)

    def test_redirect_and_existing_source_metadata_deduplicate(self):
        self.report["resolved_url"] = "https://example.org/canonical"
        self.report["sources"][0]["url"] = self.report["resolved_url"]
        existing = self.root / "Observatory/Prior.md"
        existing.write_text('---\nurl: https://example.org/canonical\n---\nExisting user material', encoding="utf-8")
        receipt = explore.capture(str(self.root), self.report, apply=True)
        self.assertEqual(receipt["existing"], ["Observatory/Prior.md"])
        self.assertEqual(len(snapshot(self.root)[0]), 1)

    def test_filename_safety_collision_and_missing_intake(self):
        self.report["title"] = 'CON: difficult / title * # [a]'
        preview = explore.capture(str(self.root), self.report)
        self.assertNotIn(":", preview["path"])
        (self.root / preview["path"]).write_text("User file at same name", encoding="utf-8")
        with self.assertRaisesRegex(BatchError, "collision"):
            explore.capture(str(self.root), self.report, apply=True)
        for intake in ("Missing", ".obsidian", "../Other"):
            with self.subTest(intake=intake), self.assertRaises(BatchError):
                explore.capture(str(self.root), self.report, intake=intake, apply=True)

    def test_existing_property_types_and_broken_links(self):
        (self.root / "Observatory/Existing.md").write_text("---\ntags: [source]\n---\n[[Already missing]]", encoding="utf-8")
        with self.assertRaisesRegex(BatchError, "property type"):
            explore.capture(str(self.root), dict(self.report, properties={"tags": "source"}))
        with self.assertRaisesRegex(BatchError, "integrity"):
            explore.capture(str(self.root), dict(self.report, body=self.report["body"] + "\n[[New broken link]]"))
        self.assertTrue(explore.capture(str(self.root), self.report, apply=True)["applied"])

    def test_atomic_creation_failure_preserves_existing_files(self):
        before = snapshot(self.root)
        with patch.object(explore.os, "link", side_effect=OSError("filesystem refused link")):
            with self.assertRaises(OSError):
                explore.capture(str(self.root), self.report, apply=True)
        self.assertEqual(snapshot(self.root), before)

    def test_cli_handles_unicode_content(self):
        self.report["title"] = "探索：知识与证据 ✨"
        self.report["body"] = "## 解释\n\n来源提出了一种机制。 [S1]\n\n## 限制\n\n支持证据的适用范围有限。 [S2]"
        manifest = Path(self.temp.name) / "report.json"
        manifest.write_text(json.dumps(self.report, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run([sys.executable, str(Path(explore.__file__)), str(self.root), str(manifest), "--apply"], capture_output=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertIn("知识", (self.root / receipt["path"]).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
