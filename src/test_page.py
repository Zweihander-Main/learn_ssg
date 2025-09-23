import unittest

from page import extract_title


class TestUtils(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Sample Title\n\nSome content here."
        title = extract_title(markdown)
        self.assertEqual(title, "Sample Title")

        with self.assertRaises(ValueError):
            _ = extract_title("No title here")

    def test_extract_title_with_whitespace(self):
        markdown = "#    Title with leading spaces   \n\nContent."
        title = extract_title(markdown)
        self.assertEqual(title, "Title with leading spaces")
