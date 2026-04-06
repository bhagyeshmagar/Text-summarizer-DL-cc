"""
text_cleaner.py — Preprocessing pipeline for text summarization.

Strips markdown syntax, HTML tags, URLs, emails, bullet markers,
normalizes Unicode, and collapses whitespace. Returns clean prose
ready for tokenization and summarization.
"""

import re
import unicodedata


def clean_text(text: str) -> str:
    """Master cleaning function. Runs all preprocessing steps in order.

    Args:
        text: Raw input text, possibly containing markdown, HTML, etc.

    Returns:
        Cleaned, readable prose.
    """
    text = strip_html_tags(text)
    text = strip_markdown(text)
    text = remove_urls(text)
    text = remove_emails(text)
    text = strip_bullet_markers(text)
    text = normalize_unicode(text)
    text = collapse_whitespace(text)
    return text.strip()


def strip_html_tags(text: str) -> str:
    """Remove HTML/XML tags like <div>, <p>, <br/>, etc."""
    return re.sub(r'<[^>]+>', ' ', text)


def strip_markdown(text: str) -> str:
    """Remove common markdown formatting symbols."""
    # Remove image syntax ![alt](url)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    # Remove link syntax [text](url) → keep text
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    # Remove bold/italic markers: ***, **, *, ___, __, _
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
    # Remove strikethrough ~~text~~
    text = re.sub(r'~~([^~]+)~~', r'\1', text)
    # Remove inline code `text`
    text = re.sub(r'`([^`]*)`', r'\1', text)
    # Remove code fences ```...```
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove heading markers (# at start of line)
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    # Remove blockquote markers (> at start of line)
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    # Remove horizontal rules (---, ***, ___)
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
    return text


def remove_urls(text: str) -> str:
    """Remove http/https/ftp URLs."""
    return re.sub(r'https?://\S+|ftp://\S+|www\.\S+', '', text)


def remove_emails(text: str) -> str:
    """Remove email addresses."""
    return re.sub(r'\S+@\S+\.\S+', '', text)


def strip_bullet_markers(text: str) -> str:
    """Remove bullet and numbered list markers at start of lines."""
    # Numbered lists: 1. 2. 3. etc
    text = re.sub(r'^\s*\d+[.)]\s+', '', text, flags=re.MULTILINE)
    # Bullet markers: - * + at start of line
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    return text


def normalize_unicode(text: str) -> str:
    """Normalize fancy Unicode characters to ASCII equivalents."""
    # Normalize to NFKD form first
    text = unicodedata.normalize('NFKD', text)
    # Replace common fancy chars
    replacements = {
        '\u2018': "'", '\u2019': "'",  # Smart single quotes
        '\u201c': '"', '\u201d': '"',  # Smart double quotes
        '\u2013': '-', '\u2014': '-',  # En/em dashes
        '\u2026': '...',               # Ellipsis
        '\u00a0': ' ',                 # Non-breaking space
        '\u200b': '',                  # Zero-width space
        '\u00b7': ' ',                 # Middle dot
        '\u2022': ' ',                 # Bullet point
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def collapse_whitespace(text: str) -> str:
    """Collapse multiple spaces/tabs into single space, normalize newlines."""
    # Replace multiple newlines with single newline
    text = re.sub(r'\n{2,}', '\n', text)
    # Replace tabs and multiple spaces with single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Clean up spaces around newlines
    text = re.sub(r' *\n *', '\n', text)
    return text
