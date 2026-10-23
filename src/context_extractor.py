"""
Context Extraction Module for EduSense.
Extracts configurable context windows around target words in transcripts,
handles multiple target word occurrences, and provides highlighted context markup.
"""

import re
from typing import List, Dict, Any, Optional
from src.preprocessing import tokenize_text, normalize_text


def find_target_occurrences(transcript: str, target_word: str) -> List[Dict[str, Any]]:
    """
    Finds all occurrences of the target word in the transcript text,
    returning token indices and character offsets.
    """
    if not transcript or not target_word:
        return []

    tokens = tokenize_text(normalize_text(transcript))
    target_clean = normalize_text(target_word)

    occurrences = []
    for idx, token in enumerate(tokens):
        # Match exact word token or lemmatized match
        if token.strip(".,!?:;\"'()[]{}") == target_clean:
            occurrences.append({
                'occurrence_index': len(occurrences),
                'token_index': idx,
                'token_text': token
            })

    return occurrences


def extract_context(
    transcript: str,
    target_word: str,
    window_size: int = 10,
    occurrence_index: int = 0
) -> Dict[str, Any]:
    """
    Extracts a surrounding context window of `window_size` words before and after
    the specified occurrence of `target_word`.

    Returns structured context info including:
    - raw_context_string: text excerpt
    - context_tokens: list of tokens in window
    - highlighted_html: string with <mark> tags around target word
    - occurrence_info: details on selected occurrence out of total occurrences
    """
    target_clean = normalize_text(target_word)
    tokens = tokenize_text(transcript)  # Preserve original casing for display

    occurrences = []
    for idx, token in enumerate(tokens):
        clean_tok = normalize_text(token.strip(".,!?:;\"'()[]{}"))
        if clean_tok == target_clean:
            occurrences.append(idx)

    if not occurrences:
        # Target word not found as exact token, try substring fallback
        for idx, token in enumerate(tokens):
            if target_clean in normalize_text(token):
                occurrences.append(idx)

    if not occurrences:
        # Target word not found anywhere
        return {
            'found': False,
            'target_word': target_word,
            'raw_transcript': transcript,
            'context_tokens': [],
            'context_text': transcript,
            'highlighted_html': transcript,
            'occurrence_count': 0,
            'selected_occurrence': 0,
            'error_message': f"Target word '{target_word}' was not found in the transcript."
        }

    # Bound occurrence_index safely
    selected_occurrence_idx = max(0, min(occurrence_index, len(occurrences) - 1))
    target_token_idx = occurrences[selected_occurrence_idx]

    start_idx = max(0, target_token_idx - window_size)
    end_idx = min(len(tokens), target_token_idx + window_size + 1)

    window_tokens = tokens[start_idx:end_idx]
    context_text = " ".join(window_tokens)

    # Highlight target word in context HTML
    highlighted_tokens = []
    for idx in range(start_idx, end_idx):
        tok = tokens[idx]
        clean_tok = normalize_text(tok.strip(".,!?:;\"'()[]{}"))
        if clean_tok == target_clean:
            highlighted_tokens.append(f'<mark class="wsd-highlight">{tok}</mark>')
        else:
            highlighted_tokens.append(tok)

    highlighted_html = " ".join(highlighted_tokens)

    return {
        'found': True,
        'target_word': target_word,
        'raw_transcript': transcript,
        'context_tokens': window_tokens,
        'context_text': context_text,
        'highlighted_html': highlighted_html,
        'window_size': window_size,
        'occurrence_count': len(occurrences),
        'selected_occurrence': selected_occurrence_idx,
        'target_token_index': target_token_idx,
        'error_message': None
    }
