import unittest
from WBSO.src.pdf.matcher import PDFMatcher


class TestPDFMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = PDFMatcher()

    def test_find_matches_no_match(self):
        text = "This is a sample text without keywords."
        patterns = ["findme", "keyword"]
        self.assertEqual(self.matcher.find_matches(text, patterns), [])

    def test_find_matches_with_match(self):
        text = "This text contains the keyword pattern1 and also pattern2."
        patterns = ["pattern1", "pattern2", "missing"]
        expected = ["Found: pattern1", "Found: pattern2"]
        # The current placeholder returns f"Found: {pattern}", so order is preserved based on input patterns
        self.assertEqual(self.matcher.find_matches(text, patterns), expected)

    def test_find_matches_empty_text(self):
        text = ""
        patterns = ["keyword"]
        self.assertEqual(self.matcher.find_matches(text, patterns), [])

    def test_find_matches_empty_patterns(self):
        text = "Some text here."
        patterns = []
        self.assertEqual(self.matcher.find_matches(text, patterns), [])


if __name__ == "__main__":
    unittest.main()
