"""
Baseline WSD Module for EduSense.
Provides NLTK Simplified Lesk algorithm baseline implementation for comparative evaluation.
"""

from typing import Dict, Any, Optional
import nltk
from nltk.wsd import lesk
from src.preprocessing import tokenize_text, get_wordnet_pos


def run_nltk_lesk(transcript: str, target_word: str, pos: Optional[str] = None) -> Dict[str, Any]:
    """
    Runs NLTK's built-in simplified lesk algorithm as an academic baseline.

    Returns:
    {
        'predicted_synset': str or None,
        'definition': str or None,
        'method': 'NLTK Simplified Lesk Baseline'
    }
    """
    tokens = tokenize_text(transcript.lower())

    wn_pos = get_wordnet_pos(pos) if pos else None

    try:
        if wn_pos:
            best_synset = lesk(tokens, target_word.lower(), pos=wn_pos)
        else:
            best_synset = lesk(tokens, target_word.lower())
    except Exception:
        best_synset = None

    if best_synset:
        return {
            'predicted_synset': best_synset.name(),
            'definition': best_synset.definition(),
            'pos': best_synset.pos(),
            'method': 'NLTK Simplified Lesk Baseline'
        }
    else:
        return {
            'predicted_synset': None,
            'definition': "No sense predicted by NLTK Lesk.",
            'pos': 'n/a',
            'method': 'NLTK Simplified Lesk Baseline'
        }
