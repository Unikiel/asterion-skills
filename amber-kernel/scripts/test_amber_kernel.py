import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("amber_kernel.py")


class AmberKernelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "Vault"
        (self.root / ".obsidian").mkdir(parents=True)
        (self.root / "Notes").mkdir()
        (self.root / "Assets").mkdir()
        (self.root / ".obsidian" / "app.json").write_text('{"attachmentFolderPath":"Assets"}', encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], text=True, capture_output=True)
        if ok and result.returncode != 0:
            self.fail(result.stderr)
        return result

    def dirs(self):
        return sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*") if p.is_dir())

    def test_dry_run_and_create_preserve_directories(self):
        before = self.dirs()
        result = self.run_cli("create-note", self.root, "Notes/New", "--body", "Hello")
        self.assertFalse((self.root / "Notes/New.md").exists())
        self.assertEqual(before, self.dirs())
        self.run_cli("create-note", self.root, "Notes/New", "--body", "Hello", "--apply")
        self.assertEqual("Hello", (self.root / "Notes/New.md").read_text(encoding="utf-8"))
        self.assertEqual(before, self.dirs())

    def test_refuses_new_directory(self):
        result = self.run_cli("create-note", self.root, "NewFolder/New", "--apply", ok=False)
        self.assertNotEqual(0, result.returncode)
        self.assertFalse((self.root / "NewFolder").exists())

    def test_move_updates_wikilink_and_canvas_without_directory_change(self):
        (self.root / "Notes/A.md").write_text("A", encoding="utf-8")
        (self.root / "Notes/B.md").write_text("[[Notes/A|label]]", encoding="utf-8")
        canvas = {"nodes": [{"id": "n1", "type": "file", "file": "Notes/A.md"}], "edges": []}
        (self.root / "Map.canvas").write_text(json.dumps(canvas), encoding="utf-8")
        before = self.dirs()
        self.run_cli("move-note", self.root, "Notes/A", "Notes/Renamed", "--state-dir", self.temp.name, "--apply")
        self.assertIn("[[Notes/Renamed|label]]", (self.root / "Notes/B.md").read_text(encoding="utf-8"))
        self.assertIn("Notes/Renamed.md", (self.root / "Map.canvas").read_text(encoding="utf-8"))
        self.assertEqual(before, self.dirs())

    def test_property_types_are_guarded(self):
        (self.root / "Notes/A.md").write_text("---\ntags:\n- one\n---\nBody", encoding="utf-8")
        result = self.run_cli("set-properties", self.root, "Notes/A", "--set", '{"tags":"one"}', "--apply", ok=False)
        self.assertNotEqual(0, result.returncode)

    def test_validate_canvas_and_links(self):
        (self.root / "Notes/A.md").write_text("[[Missing]]", encoding="utf-8")
        (self.root / "Bad.canvas").write_text('{"nodes":[],"edges":[{"id":"e","fromNode":"x","toNode":"y"}]}', encoding="utf-8")
        result = self.run_cli("inspect", self.root, "--audit")
        data = json.loads(result.stdout)
        kinds = {item["kind"] for item in data["integrity"]["issues"]}
        self.assertIn("unresolved-link", kinds)
        self.assertIn("dangling-canvas-edge", kinds)

    def test_synthesis_requires_resolved_sources(self):
        (self.root / "Notes/Source.md").write_text("Source", encoding="utf-8")
        self.run_cli("synthesis-note", self.root, "Notes/Synthesis", "--title", "Finding", "--source", "Notes/Source", "--conclusion", "Supported", "--apply")
        text = (self.root / "Notes/Synthesis.md").read_text(encoding="utf-8")
        self.assertIn("[[Notes/Source]]", text)
        bad = self.run_cli("synthesis-note", self.root, "Notes/Bad", "--title", "Bad", "--source", "Missing", "--apply", ok=False)
        self.assertNotEqual(0, bad.returncode)


if __name__ == "__main__":
    unittest.main()
