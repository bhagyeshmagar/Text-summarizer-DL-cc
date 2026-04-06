# imported library
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from text_cleaner import clean_text

nltk.download("stopwords")
nltk.download("punkt")
stop_words = set(stopwords.words("english"))

# Minimum / maximum words in a sentence to be considered
MIN_SENTENCE_WORDS = 5
MAX_SENTENCE_WORDS = 60

# Position bias: first and last sentences get a small ranking boost
POSITION_BIAS = 1.15


def compute_tf(words: list) -> dict:
    """Compute term frequency for a list of words."""
    tf = {}
    total = len(words)
    for word in words:
        tf[word] = tf.get(word, 0) + 1
    # Normalize by total word count
    for word in tf:
        tf[word] = tf[word] / total
    return tf


def compute_idf(sentences_words: list) -> dict:
    """Compute inverse document frequency across sentences.

    Each sentence is treated as a 'document'. Words that appear
    in many sentences get a lower weight (they are less informative).
    """
    n_sentences = len(sentences_words)
    idf = {}
    # Count how many sentences contain each word
    for words in sentences_words:
        seen = set(words)
        for word in seen:
            idf[word] = idf.get(word, 0) + 1
    # Apply IDF formula: log(N / df)
    for word in idf:
        idf[word] = math.log(n_sentences / idf[word])
    return idf


def main(text: str, sentence_on_output: int) -> str:
    """Summarize text using TF-IDF weighted sentence ranking with position bias.

    Args:
        text: Raw input text.
        sentence_on_output: Number of sentences to include in summary.

    Returns:
        Summary string with the most important sentences in original order.
    """
    # Step 1: Clean the text
    cleaned = clean_text(text)
    if not cleaned.strip():
        return text.strip()

    # Step 2: Sentence tokenize on cleaned text (retains proper casing)
    sentences = sent_tokenize(cleaned)
    if len(sentences) <= sentence_on_output:
        return cleaned

    # Step 3: Tokenize each sentence into lowercase words, removing stopwords
    sentences_words = []
    for sentence in sentences:
        words = [
            w.lower()
            for w in word_tokenize(sentence)
            if w.lower() not in stop_words and w.isalnum()
        ]
        sentences_words.append(words)

    # Step 4: Build a flat list of all meaningful words for TF calculation
    all_words = [w for words in sentences_words for w in words]
    if not all_words:
        return cleaned

    tf = compute_tf(all_words)
    idf = compute_idf(sentences_words)

    # Step 5: Score each sentence
    sentence_scores = {}
    for i, (sentence, words) in enumerate(zip(sentences, sentences_words)):
        word_count = len(word_tokenize(sentence))

        # Skip sentences that are too short or too long
        if word_count < MIN_SENTENCE_WORDS or word_count > MAX_SENTENCE_WORDS:
            continue

        # TF-IDF score for this sentence
        score = 0.0
        for word in words:
            if word in tf and word in idf:
                score += tf[word] * idf[word]

        # Normalize by sentence length to avoid bias toward longer sentences
        if len(words) > 0:
            score = score / len(words)

        # Position bias: boost first few and last few sentences
        if i < 2 or i >= len(sentences) - 2:
            score *= POSITION_BIAS

        sentence_scores[i] = score

    if not sentence_scores:
        return cleaned

    # Step 6: Pick top N sentences by score
    ranked_indices = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    top_indices = sorted(ranked_indices[:sentence_on_output])

    # Step 7: Assemble summary in original order
    summary_sentences = [sentences[i].strip() for i in top_indices]
    return " ".join(summary_sentences)
