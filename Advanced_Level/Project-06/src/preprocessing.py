import re

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "and", "or", "but", "if", "so", "of", "at", "by", "for", "with",
    "about", "to", "from", "in", "on", "it", "this", "that", "these",
    "those", "i", "you", "he", "she", "we", "they", "them", "my", "your",
    "his", "her", "its", "our", "their", "as", "than", "then", "there",
    "here", "just", "do", "does", "did", "have", "has", "had", "will",
    "would", "can", "could", "should"
}


def clean_text(text: str, remove_stopwords: bool = True) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)          # urls
    text = re.sub(r"[^a-z\s]", " ", text)                   # keep letters only
    text = re.sub(r"\s+", " ", text).strip()

    if remove_stopwords:
        words = [w for w in text.split() if w not in STOPWORDS]
        text = " ".join(words)

    return text


def clean_series(texts):
    """Apply clean_text over a list/Series of strings, returns a list."""
    return [clean_text(t) for t in texts]
