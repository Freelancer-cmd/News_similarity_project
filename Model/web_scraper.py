import requests
import json
from newspaper import Article
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY") 
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_articles(category: str, num_articles: int):
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
        "category": category,
        "language": "en",
        "pageSize": num_articles,
        "country": "us"
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

    return results


def append_articles_to_json(articles, json_file="data/web_scraped_articles.json"):
    """
    Appends a list of articles to a JSON file.

    Args:
        articles (list of tuples): List of (url, title, content, date)
        json_file (str): Path to the JSON file
    """
    formatted_articles = []
    for url, title, content, date in articles:
        formatted_articles.append({
            "url": url,
            "title": title,
            "content": content,
            "date": date
        })

    try:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_data.extend(formatted_articles)

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2)

        print(f"Successfully saved {len(formatted_articles)} articles to '{json_file}'")
    except Exception as e:
        print(f"Failed to write to JSON: {e}")

article = fetch_articles("technology", 5)
append_articles_to_json(article)