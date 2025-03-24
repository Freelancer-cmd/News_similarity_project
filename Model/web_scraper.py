import requests
import json
from newspaper import Article
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY") 
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_articles(query: str, num_articles: int =5):
    """
    Fetches news articles using NewsAPI and extracts full content using newspaper3k.

    Args:
        category (str): News category: business, entertainment, general, health, science, sports, technology.
        num_articles (int): Number of articles to fetch.

    Returns:
        list of tuples: Each tuple contains (url, title, content, date).
    """
    params = {
    "apiKey": NEWS_API_KEY,
    "language": "en",
    "pageSize": num_articles,
    "sources": ",".join([
        "breitbart-news",
        "fox-news",
        "the-wall-street-journal",
        "the-new-york-times",
        "mother-jones"
    ]),
    "q": query
}

    response = requests.get(NEWS_API_URL, params=params)
    results = []

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        for article in articles:
            url = article.get("url")
            date = article.get("publishedAt")

            try:
                news = Article(url)
                news.download()
                news.parse()

                title = news.title
                content = news.text

                results.append((url, title, content, date))
            except Exception as e:
                print(f"Failed to process article at {url}: {e}")
    else:
        print(f"NewsAPI request failed with status {response.status_code}")
        print("Response:", response.text)

    if len(results) == 0:
        print("No articles found. Please try a different keyword.")

    return results
