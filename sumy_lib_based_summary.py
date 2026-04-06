from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
from text_cleaner import clean_text
import nltk
from typing import Tuple

nltk.download("punkt")


def common_process(text: str):
    """Clean the text and convert to a sumy parser object.

    Args:
        text: Raw input text.

    Returns:
        PlaintextParser object ready for summarization.
    """
    cleaned = clean_text(text)
    parser = PlaintextParser.from_string(cleaned, Tokenizer("english"))
    return parser


def common_return_process(sentences: Tuple) -> str:
    """Join summarized sentence objects into a single string.

    Args:
        sentences: Tuple of sentence objects from sumy summarizer.

    Returns:
        Joined summary string.
    """
    return " ".join(str(s).strip() for s in sentences)


def main(text: str, model_name: str, sentence_on_output: int = 2) -> str:
    """Summarize text using a sumy library model.

    Args:
        text: Raw input text.
        model_name: One of 'Lex Rank', 'LSA', 'Text Rank'.
        sentence_on_output: Number of sentences in output.

    Returns:
        Summary string.
    """
    summarizers = {
        "Lex Rank": LexRankSummarizer,
        "LSA": LsaSummarizer,
        "Text Rank": TextRankSummarizer,
    }

    if model_name not in summarizers:
        raise ValueError(f"Unknown model: {model_name}. Choose from: {list(summarizers.keys())}")

    summarizer = summarizers[model_name]()
    parser = common_process(text=text)
    summary = summarizer(parser.document, sentence_on_output)
    return common_return_process(sentences=summary)
