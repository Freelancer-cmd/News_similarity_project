import unittest
from unittest.mock import patch, MagicMock
import os
import json

from model.web_scraper import fetch_articles, append_articles_to_json

class TestWebScraper(unittest.TestCase):

    @patch("model.web_scraper.Article")
    @patch("model.web_scraper.requests.get")
    def test_fetch_articles(self, mock_get, mock_article):

        # Mock NewsAPI response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "articles": [
                {
                    "title": "Test Title",
                    "url": "http://example.com",
                    "publishedAt": "2025-03-22T10:00:00Z",
                    "description": "Short description"
                }
            ]
        }

        # Mock newspaper3k's Article parsing
        mock_article_instance = MagicMock()
        mock_article.return_value = mock_article_instance
        mock_article_instance.download.return_value = None
        mock_article_instance.parse.return_value = None
        mock_article_instance.title = "Test Title"
        mock_article_instance.text = "Full article content."

        results = fetch_articles("technology", 1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "http://example.com")
        self.assertEqual(results[0][1], "Test Title")
        self.assertEqual(results[0][2], "Full article content.")
        self.assertEqual(results[0][3], "2025-03-22T10:00:00Z")

    def test_append_articles_to_json(self):
        test_file = "test_articles.json"
        test_data = [
            ("http://example.com", "Sample Title", "Sample content", "2025-03-22T10:00:00Z")
        ]

        # Clean up test file if it exists
        if os.path.exists(test_file):
            os.remove(test_file)

        append_articles_to_json(test_data, json_file=test_file)

        with open(test_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Sample Title")
        self.assertEqual(data[0]["url"], "http://example.com")

        # Clean up
        os.remove(test_file)

if __name__ == "__main__":
    unittest.main()
