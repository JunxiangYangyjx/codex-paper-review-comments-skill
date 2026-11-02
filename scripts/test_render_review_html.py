"""Regression checks for reusable illustrated reviews; no manuscript data required."""

import base64
import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from render_review_html import auto_copy_ready, render
from validate_review_html import ReportReferences


class IllustratedReviewTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            "paper_id": "Example",
            "paper_title": "A Generic Engineering Study",
            "recommendation": {"decision": "Major Revision"},
            "summary": {"en": "A focused contribution with a validation gap."},
            "comments_to_editor": {"en": "EDITOR ONLY"},
            "major_comments": [{"en": "Clarify the stated mechanism."}],
            "minor_comments": [],
        }

    def illustrated(self):
        data = copy.deepcopy(self.data)
        data["source_pdf"] = "source paper.pdf"
        data["paper_understanding"] = {
            "overview": "READER ONLY 中文介绍",
            "sections": [{
                "key": "work", "title": "研究内容", "question": "What was studied?",
                "answer_html": "<p>Explain the mechanism.</p><p>State its limits.</p>",
                "sources": [{"page": 2, "label": "Fig. 1"}],
                "illustrations": [
                    {"src": "figure.png", "title": "Architecture", "tip": "Trace the signal path.", "placement": "main"},
                    {"src": "figure.png", "title": "Auxiliary model", "tip": "Compare the assumptions.", "placement": "detail"},
                ],
            }],
        }
        return data

    def test_legacy_data_needs_no_understanding_module(self):
        page = render(self.data, Path("review.html"))
        self.assertNotIn('id="paper-understanding"', page)
        self.assertIn("Clarify the stated mechanism.", page)

    def test_figures_sources_and_submission_separation(self):
        data = self.illustrated()
        before = auto_copy_ready(data)
        page = render(data, Path("review.html"))
        refs = ReportReferences()
        refs.feed(page)
        self.assertEqual(set(refs.anchors) - set(refs.ids), set())
        self.assertEqual(len(refs.images), 2)
        self.assertIn('source%20paper.pdf#page=2', page)
        self.assertLess(page.index('Architecture</h4>'), page.index('State its limits.'))
        self.assertIn('<details class="qa-detail">', page)
        self.assertEqual(before, auto_copy_ready(data))
        self.assertNotIn("READER ONLY", before)
        self.assertNotIn("EDITOR ONLY", before)
        self.assertNotIn("中文", before)

    def test_duplicate_section_keys_are_rejected(self):
        data = self.illustrated()
        data['paper_understanding']['sections'] *= 2
        with self.assertRaises(ValueError):
            render(data, Path('review.html'))

    def test_validation_detects_missing_images_and_broken_links(self):
        # Use an isolated directory which TemporaryDirectory removes after the test.
        with tempfile.TemporaryDirectory(prefix="review-skill-test-") as directory:
            folder = Path(directory)
            (folder / 'figure.png').write_bytes(base64.b64decode(
                'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j7H0AAAAASUVORK5CYII='
            ))
            output = folder / 'review.html'
            page = render(self.illustrated(), output)
            output.write_text(page, encoding='utf-8')
            command = [sys.executable, str(Path(__file__).with_name('validate_review_html.py')), str(output)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            output.write_text(page.replace('src="figure.png"', 'src="missing.png"'), encoding='utf-8')
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            output.write_text(page.replace('href="#qa-work"', 'href="#missing"'), encoding='utf-8')
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)


if __name__ == '__main__':
    unittest.main()
