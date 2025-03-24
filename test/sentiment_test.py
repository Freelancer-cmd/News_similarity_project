import unittest
from model.sentiment import get_sentiment  # Adjust path based on your project structure

class TestSentimentAnalysis(unittest.TestCase):
    
    def test_sentiment_output_type(self):
        title = "Great News!"
        content = "Everything is going fantastic. We're so happy with the progress."
        score = get_sentiment(title, content)
        self.assertIsInstance(score, float)

    def test_sentiment_range(self):
        title = "Neutral Title"
        content = "This is a neutral sentence."
        score = get_sentiment(title, content)
        self.assertGreaterEqual(score, -1.0)
        self.assertLessEqual(score, 1.0)

    def test_positive_sentiment(self):
        title = "Amazing breakthrough!"
        content = "This discovery is groundbreaking and brings hope to millions."
        score = get_sentiment(title, content)
        self.assertGreater(score, 0.3)  # Should lean clearly positive

    def test_negative_sentiment(self):
        title = "Disaster strikes the region"
        content = "Many people are feared dead in the worst flood of the decade."
        score = get_sentiment(title, content)
        self.assertLess(score, -0.3)  # Should lean clearly negative

if __name__ == '__main__':
    unittest.main()