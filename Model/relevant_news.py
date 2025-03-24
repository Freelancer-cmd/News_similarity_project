from Model.sentiment import get_sentiment
from Model.web_scraper import fetch_articles
from Model.rag import NewsSearchEngine


def enrich_articles_with_sentiment(query, num_articles=10):
    """
    Fetch articles using a query, append sentiment score.

    Returns:
        List of tuples: (url, title, content, date, sentiment)
    """
    raw_articles = fetch_articles(query, num_articles)
    print("Number of articles fetched:", len(raw_articles))
    enriched = []

    for url, title, content, date in raw_articles:
        sentiment = get_sentiment(title,content)
        enriched.append((url, title, content, date, sentiment))

    return enriched, len(raw_articles)


def search_relevant_articles(query, top_k=5):
    """
    Returns the top-k relevant articles enriched with sentiment scores.
    """
    enriched_articles, num_articles = enrich_articles_with_sentiment(query, num_articles=100)

    if num_articles == 0:
        return []

    documents = [title + ". " + content for (_, title, content, _, _) in enriched_articles]

    search_engine = NewsSearchEngine()
    embeddings = search_engine.create_embeddings(documents)

    print("Size of embeddings:", embeddings.shape)

    search_engine.build_index(embeddings, min(top_k, num_articles))

    results = search_engine.search(query, top_k=top_k)

    top_articles = []
    for r in results:
        idx = r["index"]
        article = enriched_articles[idx]
        top_articles.append({
            "url": article[0],
            "title": article[1],
            "content": article[2],
            "date": article[3],
            "sentiment": article[4],
            "distance": r["distance"]
        })

    return top_articles


#Test the function
if __name__ == "__main__":
    query = "Trump"
    results = search_relevant_articles(query, top_k=3)
    for i, article in enumerate(results, 1):
        print(f"\nResult {i}:")
        print("Title:", article["title"])
        print("Sentiment:", article["sentiment"])
        print("Distance:", article["distance"])
        print("Date:", article["date"])
        print("URL:", article["url"])
        print("Snippet:", article["content"][:300], "...")
