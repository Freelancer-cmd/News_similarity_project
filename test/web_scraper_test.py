import unittest
from unittest.mock import patch, MagicMock
import os
import json

from model.web_scraper import fetch_articles, append_articles_to_json

class TestWebScraper(unittest.TestCase):

    @patch("model.web_scraper.Article")
    @patch("model.web_scraper.requests.get")
    def test_fetch_articles(self, mock_get, mock_article_class):
        # Simulate NewsAPI JSON response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "articles": [
                {
                    "url": "https://example.com/test-article",
                    "publishedAt": "2025-03-24T12:00:00Z"
                }
            ]
        }

        # Simulate newspaper.Article parsing
        mock_article_instance = MagicMock()
        mock_article_instance.title = "Mocked Article Title"
        mock_article_instance.text = "Mocked full article content"
        mock_article_class.return_value = mock_article_instance

        # Call the function
        articles = fetch_articles("climate", 1)

        # Assertions
        self.assertEqual(len(articles), 1)
        url, title, content, date = articles[0]
        self.assertEqual(url, "https://example.com/test-article")
        self.assertEqual(title, "Mocked Article Title")
        self.assertEqual(content, "Mocked full article content")
        self.assertEqual(date, "2025-03-24T12:00:00Z")


if __name__ == "__main__":
    unittest.main()
