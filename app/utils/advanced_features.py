from collections import Counter
from datetime import datetime
import re

STOPWORDS = {"the", "is", "in", "and", "of", "to", "a", "for", "on", "with"}

def extract_keywords(data):
    """Extract top 5 most frequent meaningful words from titles."""
    text = " ".join([item["title"] for item in data])
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    common = Counter(filtered).most_common(5)
    return [word for word, _ in common]

def calculate_confidence(data):
    """Base score: 50. Add +5 for each valid data point. Max cap: 90."""
    score = 50 + len(data) * 5
    return min(score, 90)

def analyze_sentiment(data):
    """Return 'Positive', 'Neutral', or 'Negative' based on simple keyword approach."""
    positive_words = ["growth", "increase", "boost", "profit", "expansion", "rising", "success"]
    negative_words = ["decline", "loss", "risk", "fall", "crisis", "drop", "failure"]

    text = " ".join([item["title"].lower() for item in data])

    pos = sum(word in text for word in positive_words)
    neg = sum(word in text for word in negative_words)

    if pos > neg:
        return "Positive"
    elif neg > pos:
        return "Negative"
    return "Neutral"

def get_timestamp():
    """Return current date-time string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
