"""
Thin functional wrapper around src.models.DictionaryThesaurusWSD.

The WSD algorithm itself lives in src/models.py (single source of truth).
This module only keeps the functional `disambiguate_word` API used by the
Flask app, tests and evaluation runner.
"""

from typing import Dict, Any, Optional
from src.models import DictionaryThesaurusWSD, POSTaggerModel, DEFAULT_WEIGHTS


def infer_target_pos(context_tokens, target_word) -> Optional[str]:
    return POSTaggerModel.infer_pos(context_tokens, target_word)


def disambiguate_word(
    transcript: str,
    target_word: str,
    window_size: int = 10,
    occurrence_index: int = 0,
    weights: Optional[Dict[str, float]] = None,
    use_pos_filter: bool = True,
) -> Dict[str, Any]:
    model = DictionaryThesaurusWSD(weights=weights)
    return model.disambiguate(
        transcript=transcript,
        target_word=target_word,
        window_size=window_size,
        occurrence_index=occurrence_index,
        use_pos_filter=use_pos_filter,
    )
