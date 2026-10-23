"""
Text Preprocessing Module for EduSense WSD Engine.
Provides modular, transparent text normalization, sentence segmentation, tokenization, stop-word removal, POS tagging, and lemmatization.
"""

import re
import string
from typing import List, Dict, Any, Tuple, Optional
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

_lemmatizer = None
_stop_words = None


def get_lemmatizer():
    global _lemmatizer
    if _lemmatizer is None:
        _lemmatizer = WordNetLemmatizer()
    return _lemmatizer


def get_stopwords_set():
    global _stop_words
    if _stop_words is None:
        try:
            _stop_words = set(stopwords.words('english'))
        except LookupError:
            _stop_words = {
                "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
                "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
                "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
                "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
                "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
                "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
                "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not",
                "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over",
                "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
                "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
                "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
                "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
                "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
                "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
                "you've", "your", "yours", "yourself", "yourselves"
            }
    return _stop_words


def get_wordnet_pos(treebank_tag: str) -> str:
    """
    Maps NLTK Penn Treebank POS tag to WordNet POS tag.
    """
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return wn.NOUN


def normalize_text(text: str) -> str:
    """
    Lowercases text and strips extraneous whitespace.
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def segment_sentences(text: str) -> List[str]:
    """
    Sentence segmentation for raw speech-to-text transcripts (NLTK punkt, regex fallback).
    """
    if not text or not text.strip():
        return []
    try:
        sents = nltk.sent_tokenize(text)
    except Exception:
        sents = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sents if s.strip()]


def tokenize_text(text: str) -> List[str]:
    """
    Tokenizes text into words using NLTK word_tokenize with fallback regex.
    """
    if not text:
        return []
    try:
        tokens = nltk.word_tokenize(text)
    except Exception:
        tokens = re.findall(r'\b\w+\b', text)
    return tokens


def remove_punctuation_and_stopwords(tokens: List[str], preserve_words: Optional[List[str]] = None) -> List[str]:
    """
    Removes punctuation tokens, numbers, and stop-words.
    Optionally preserves specific target words even if they match stop-words.
    """
    stops = get_stopwords_set()
    preserve = set(preserve_words) if preserve_words else set()

    filtered = []
    for tok in tokens:
        clean_tok = tok.strip(string.punctuation)
        if not clean_tok:
            continue
        if clean_tok.isdigit():
            continue
        if clean_tok in preserve or clean_tok not in stops:
            filtered.append(clean_tok)
    return filtered


def lemmatize_tokens(tokens: List[str], use_pos: bool = True) -> List[str]:
    """
    Lemmatizes tokens to their root dictionary form using NLTK WordNetLemmatizer.
    """
    lemmatizer = get_lemmatizer()
    if not tokens:
        return []

    if use_pos:
        try:
            pos_tags = nltk.pos_tag(tokens)
            lemmas = [lemmatizer.lemmatize(tok, get_wordnet_pos(tag)) for tok, tag in pos_tags]
        except Exception:
            lemmas = [lemmatizer.lemmatize(tok) for tok in tokens]
    else:
        lemmas = [lemmatizer.lemmatize(tok) for tok in tokens]

    return lemmas


def preprocess_text(text: str, preserve_target: Optional[str] = None) -> Dict[str, Any]:
    """
    Full text preprocessing pipeline returning structured steps for visibility in the UI.

    Returns:
    {
        'raw_text': str,
        'normalized': str,
        'tokens': List[str],
        'filtered_tokens': List[str],
        'lemmas': List[str],
        'unique_lemmas': List[str]
    }
    """
    normalized = normalize_text(text)
    tokens = tokenize_text(normalized)

    preserve = [preserve_target.lower()] if preserve_target else None
    filtered = remove_punctuation_and_stopwords(tokens, preserve_words=preserve)
    lemmas = lemmatize_tokens(filtered, use_pos=True)

    # Maintain insertion order for unique lemmas
    unique_lemmas = list(dict.fromkeys(lemmas))

    return {
        'raw_text': text,
        'normalized': normalized,
        'tokens': tokens,
        'filtered_tokens': filtered,
        'lemmas': lemmas,
        'unique_lemmas': unique_lemmas
    }
