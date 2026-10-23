"""
Utility helper functions for EduSense WSD engine.
Handles NLTK resource verification, downloading, and safety checks.
"""

import sys
import logging
import nltk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EduSense.Utils")

REQUIRED_NLTK_RESOURCES = [
    ('corpora/wordnet.zip', 'wordnet'),
    ('corpora/omw-1.4.zip', 'omw-1.4'),
    ('tokenizers/punkt', 'punkt'),
    ('tokenizers/punkt_tab', 'punkt_tab'),
    ('corpora/stopwords', 'stopwords'),
    ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
    ('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng')
]


def ensure_nltk_resources():
    """
    Checks and downloads all necessary NLTK corpora and models.
    Guarantees offline reliability once downloaded.
    """
    for resource_path, resource_name in REQUIRED_NLTK_RESOURCES:
        try:
            nltk.data.find(resource_path)
            logger.info(f"NLTK resource '{resource_name}' found.")
        except LookupError:
            logger.info(f"Downloading missing NLTK resource: '{resource_name}'...")
            try:
                nltk.download(resource_name, quiet=True)
            except Exception as e:
                logger.warning(f"Failed to download {resource_name}: {e}")

    # Verify WordNet specifically
    try:
        from nltk.corpus import wordnet as wn
        syns = wn.synsets('bank')
        if not syns:
            raise ValueError("WordNet returned no synsets for 'bank'.")
        logger.info("WordNet interface successfully verified.")
        return True
    except Exception as err:
        logger.error(f"Critical error initializing WordNet: {err}")
        return False


def get_pos_name(pos_code: str) -> str:
    """
    Converts WordNet POS code to human-readable string.
    """
    mapping = {
        'n': 'Noun',
        'v': 'Verb',
        'a': 'Adjective',
        's': 'Adjective Satellite',
        'r': 'Adverb'
    }
    return mapping.get(pos_code, 'Unknown')


def safe_float_format(val: float, precision: int = 4) -> float:
    """
    Safely rounds float values.
    """
    try:
        return round(float(val), precision)
    except (ValueError, TypeError):
        return 0.0
