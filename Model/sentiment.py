from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon', quiet=True)

sia = SentimentIntensityAnalyzer()

def get_sentiment(title: str, content: str) -> float:
    """
    Returns a continuous sentiment score between -1 (negative) and +1 (positive)
    based on the title and content of a news article.
    """
    combined_text = f"{title}. {content}"
    sentiment = sia.polarity_scores(combined_text)
    return sentiment['compound']