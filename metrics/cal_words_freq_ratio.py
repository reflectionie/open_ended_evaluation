from textblob import TextBlob
from collections import Counter
from metrics.cal_odds_ratio import all_adjs

def get_top_k_words(text, top_k, sentiment="positive"):
    """
    Analyze the text's polarity and return the top_k most frequent positive or negative words.

    Args:
        text (str): The input text to analyze.
        top_k (int): The number of top words to return.
        sentiment (str): "positive" for positive words, "negative" for negative words.

    Returns:
        list: A list of tuples with words and their frequencies, sorted by frequency.
    """
    if sentiment not in {"positive", "negative"}:
        raise ValueError("Sentiment must be either 'positive' or 'negative'")

    blob = TextBlob(text)
    word_polarities = []

    # Analyze polarity of each word
    for word in blob.words:
        word_blob = TextBlob(word)
        polarity = word_blob.sentiment.polarity
        if (sentiment == "positive" and polarity > 0) or (sentiment == "negative" and polarity < 0):
            word_polarities.append(word.lower())

    # Count frequencies of words
    word_counts = Counter(word_polarities)

    # Get the most common words
    return word_counts.most_common(top_k)

def get_top_k_words_from_list(text, top_k, sentiment="positive"):
    """
    Analyze the text and return the top_k most frequent positive or negative words based on a predefined word list.

    Args:
        text (str): The input text to analyze.
        top_k (int): The number of top words to return.
        sentiment (str): "positive" for positive words, "negative" for negative words.

    Returns:
        list: A list of tuples with words and their frequencies, sorted by frequency.
    """
    if sentiment not in {"positive", "negative"}:
        raise ValueError("Sentiment must be either 'positive' or 'negative'")

    # Split predefined adjectives into positive and negative lists
    positive_words = set(all_adjs[0::2])  # Every other line starting from the first
    negative_words = set(all_adjs[1::2])  # Every other line starting from the second

    # Tokenize the text into words and normalize case
    words = text.lower().split()

    # Filter words based on sentiment
    if sentiment == "positive":
        filtered_words = [word for word in words if word in positive_words]
    else:
        filtered_words = [word for word in words if word in negative_words]

    # Count frequencies of filtered words
    word_counts = Counter(filtered_words)

    # Get the most common words
    return word_counts.most_common(top_k)

# Example usage
text = "The powerful and commanding leader was seen as both capable and elite, but others felt he was privileged and authoritative."
positive_words_blob = get_top_k_words(text, top_k=3, sentiment="positive")
negative_words_blob = get_top_k_words(text, top_k=3, sentiment="negative")

positive_words_list = get_top_k_words_from_list(text, top_k=3, sentiment="positive")
negative_words_list = get_top_k_words_from_list(text, top_k=3, sentiment="negative")

print("Top positive words (TextBlob):", positive_words_blob)
print("Top negative words (TextBlob):", negative_words_blob)
print("Top positive words (Predefined List):", positive_words_list)
print("Top negative words (Predefined List):", negative_words_list)
