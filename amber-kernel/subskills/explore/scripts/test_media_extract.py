import copy
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import explore_capture as capture
import media_extract as media
from scripts.vault_state import BatchError


class MediaExtractionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_youtube_target_routing_and_playlist_context(self):
        for url in ("https://youtu.be/abcdefghijk", "https://www.youtube.com/shorts/abcdefghijk", "https://www.youtube.com/live/abcdefghijk", "https://youtube.com/watch?v=abcdefghijk&list=PL123"):
            with self.subTest(url=url):
                self.assertEqual(media.route(url)["kind"], "video")
                self.assertEqual(media.route(url)["video_id"], "abcdefghijk")
        self.assertEqual(media.route("https://youtube.com/@creator/videos")["kind"], "channel")
        self.assertEqual(media.route("https://youtube.com/channel/UC123")["kind"], "channel")
        self.assertEqual(media.route("https://youtube.com/playlist?list=PL123")["kind"], "playlist")
        self.assertEqual(media.route("https://youtube.com.evil.example/watch?v=abcdefghijk")["kind"], "web")

    def test_file_extensions_are_only_hints(self):
        self.assertEqual(media.route("https://example.org/asset.mp4?download=1")["kind"], "video")
        self.assertTrue(media.route("https://example.org/asset.pdf")["hint_only"])
        self.assertEqual(media.route("https://example.org/no-extension")["kind"], "web")

    def test_srt_and_vtt_preserve_timing_and_unicode(self):
        cues = media.captions("WEBVTT\n\n1\n00:01.250 --> 00:03.000 align:start\n<v Speaker>你好 &amp; hello</v>\n\n00:03.000 --> 00:05.000\nA second concept\n")
        self.assertEqual(cues[0]["start_seconds"], 1.25)
        self.assertEqual(cues[0]["text"], "你好 & hello")
        srt = self.root / "speech.srt"
        srt.write_text("1\n00:01:02,125 --> 00:01:03,250\nEvidence.\n", encoding="utf-8")
        result = media.extract(srt)
        self.assertEqual(result["coverage"], "caption-text-only")
        self.assertEqual(result["segments"][0]["start_seconds"], 62.125)

    def test_bad_caption_timing_and_missing_cues_are_rejected(self):
        for text in ("A description without captions", "00:65.000 --> 00:66.000\nInvalid", "00:03.000 --> 00:01.000\nBackwards"):
            with self.subTest(text=text), self.assertRaises(BatchError):
                media.captions(text)

    def test_timestamp_link_addresses_the_actual_video(self):
        self.assertEqual(media.timed_url("https://youtube.com/watch?v=abcdefghijk&list=PLx&t=4", 192.9), "https://www.youtube.com/watch?v=abcdefghijk&t=192")
        with self.assertRaises(BatchError):
            media.timed_url("https://youtube.com/@creator", 3)

    def test_html_scripts_are_not_text_evidence(self):
        page = self.root / "page.html"
        page.write_text("<h1>Concept</h1><script>stealSecrets()</script><p>Evidence &amp; context.</p>", encoding="utf-8")
        result = media.extract(page)
        self.assertIn("Evidence & context", result["segments"][0]["text"])
        self.assertNotIn("stealSecrets", result["segments"][0]["text"])

    def test_docx_and_pptx_text_keep_locators_and_visual_limits(self):
        document = self.root / "source.docx"
        with zipfile.ZipFile(document, "w") as z:
            z.writestr("word/document.xml", '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:r><w:t>Concept one</w:t></w:r></w:p></w:document>')
            z.writestr("word/media/image1.png", b"fixture")
        result = media.extract(document)
        self.assertEqual(result["segments"][0]["locator"], "paragraph 1")
        self.assertTrue(result["additional_inspection_required"])
        slides = self.root / "slides.pptx"
        with zipfile.ZipFile(slides, "w") as z:
            for number in (10, 2):
                z.writestr(f"ppt/slides/slide{number}.xml", f'<a:p xmlns:a="urn:fixture"><a:t>Slide {number}</a:t></a:p>')
        result = media.extract(slides)
        self.assertEqual([s["locator"] for s in result["segments"]], ["slide 2", "slide 10"])

    def test_unavailable_media_backend_is_not_claimed_as_extraction(self):
        for suffix in (".png", ".mp3", ".mp4", ".unknown"):
            with self.subTest(suffix=suffix):
                path = self.root / ("asset" + suffix)
                path.write_bytes(b"fixture")
                result = media.extract(path)
                self.assertEqual(result["status"], "needs-backend")
                self.assertNotIn("segments", result)

    def test_optional_pdf_backend_absence_is_explicit(self):
        path = self.root / "source.pdf"
        path.write_bytes(b"%PDF-1.7 fixture")
        with patch.object(media.importlib.util, "find_spec", return_value=None):
            self.assertEqual(media.extract(path)["status"], "needs-backend")


class MediaCoverageTests(unittest.TestCase):
    def source(self):
        return {"id": "S1", "url": "https://youtube.com/watch?v=abcdefghijk", "title": "Fixture video", "kind": "video", "status": "partial", "limitation": "Visuals not inspected",
                "modalities": [{"type": "audio", "status": "observed", "method": "creator captions", "locator": "00:00–08:20, complete caption text"},
                               {"type": "visual", "status": "unavailable", "limitation": "No visual inspection tool used"}]}

    def report(self, source=None):
        source = source or self.source()
        return {"version": 1, "url": source["url"], "title": "Video knowledge", "accessed": "2026-09-12", "status": "partial", "coverage_note": "Only speech evidence inspected", "seed_source": "S1", "body": "The speaker explains a concept. [S1]", "sources": [source]}

    def test_transcript_only_is_partial_by_default_and_renders_method(self):
        text = capture.render(self.report())
        self.assertIn("audio: observed; creator captions", text)
        self.assertIn("visual: unavailable", text)
        self.assertIn("00:00–08:20", text)

    def test_transcript_cannot_masquerade_as_full_video_inspection(self):
        source = self.source()
        source["status"] = "read"
        with self.assertRaisesRegex(BatchError, "incomplete modalities"):
            capture.render(self.report(source))

    def test_explicit_transcript_scope_excludes_visuals_with_reason(self):
        source = self.source()
        source["status"] = "read"
        source["modalities"][1] = {"type": "visual", "status": "not_applicable", "limitation": "User explicitly requested transcript-only analysis"}
        report = self.report(source)
        report.update(status="complete", coverage_note="Complete within requested transcript-only scope")
        self.assertIn("transcript-only scope", capture.render(report))

    def test_missing_media_coverage_is_rejected_even_without_kind(self):
        source = self.source()
        del source["kind"]
        del source["modalities"]
        with self.assertRaisesRegex(BatchError, "requires coverage"):
            capture.render(self.report(source))

    def test_image_requires_actual_visual_evidence(self):
        source = {"id": "S1", "url": "https://example.org/diagram.png", "title": "Diagram", "kind": "image", "status": "read", "modalities": [{"type": "metadata", "status": "observed", "method": "filename", "locator": "page"}]}
        with self.assertRaisesRegex(BatchError, "visual"):
            capture.render(self.report(source))

    def channel_report(self):
        seed = {"id": "S1", "url": "https://youtube.com/@creator", "title": "Creator channel", "kind": "channel", "status": "read",
                "modalities": [{"type": "metadata", "status": "observed", "method": "channel page", "locator": "About and visible video list"}]}
        video = self.source()
        video["id"] = "S2"
        report = self.report(seed)
        report.update(body="The channel introduces its topic. [S1]\nThe sampled video explains a mechanism. [S2]", sources=[seed, video],
                      sampling={"scope": "One accessible video; not the whole channel", "rationale": "Relevant to the requested concept", "selected_sources": ["S2"]})
        return report

    def test_channel_sample_provenance_is_rendered(self):
        text = capture.render(self.channel_report())
        self.assertIn("not the whole channel", text)
        self.assertIn("Sampled sources: S2", text)

    def test_channel_without_sampling_is_rejected(self):
        report = self.channel_report()
        del report["sampling"]
        with self.assertRaisesRegex(BatchError, "sampling record"):
            capture.render(report)

    def test_channel_metadata_only_cannot_be_complete(self):
        report = self.channel_report()
        report["sources"] = report["sources"][:1]
        report["body"] = "A topic is visible in the profile. [S1]"
        report["sampling"]["selected_sources"] = []
        report["status"] = "complete"
        with self.assertRaisesRegex(BatchError, "metadata-only"):
            capture.render(report)
        report["status"] = "partial"
        self.assertIn("No substantive media", capture.render(report))

    def test_metadata_only_video_is_not_a_substantive_sample(self):
        report = self.channel_report()
        video = report["sources"][1]
        video["modalities"][0] = {"type": "audio", "status": "unavailable", "limitation": "No transcript"}
        video["modalities"].append({"type": "metadata", "status": "observed", "method": "title and thumbnail", "locator": "video listing"})
        with self.assertRaisesRegex(BatchError, "substantive media evidence"):
            capture.render(report)


if __name__ == "__main__":
    unittest.main()
