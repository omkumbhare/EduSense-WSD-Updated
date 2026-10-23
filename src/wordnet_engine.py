"""
WordNet Engine Module for EduSense WSD Engine.
Interfaces with NLTK WordNet to retrieve candidate senses (synsets),
gloss definitions, examples, lemmas, hypernyms/hyponyms, and thesaurus synonym expansions.
"""

from typing import List, Dict, Any, Optional, Set
import nltk
from nltk.corpus import wordnet as wn
from src.preprocessing import preprocess_text, get_wordnet_pos, normalize_text
from src.utils import get_pos_name


def get_candidate_synsets(target_word: str, pos: Optional[str] = None) -> List[Any]:
    """
    Retrieves all candidate WordNet synsets for a target word, optionally filtered by POS.
    """
    clean_target = normalize_text(target_word)
    if not clean_target:
        return []

    synsets = wn.synsets(clean_target)
    if pos:
        wn_pos = get_wordnet_pos(pos)
        synsets = [s for s in synsets if s.pos() == wn_pos]

    return synsets


def extract_synset_details(synset: Any) -> Dict[str, Any]:
    """
    Extracts complete detailed information for a single candidate WordNet synset:
    - Synset name / ID (e.g. bank.n.01)
    - Part of Speech
    - Definition / Gloss
    - Example sentences
    - Lemma names
    - Hypernyms (broader terms)
    - Hyponyms (narrower terms)
    - Preprocessed gloss tokens & lemmas
    - Preprocessed example tokens & lemmas
    """
    name = synset.name()
    pos_code = synset.pos()
    pos_display = get_pos_name(pos_code)
    definition = synset.definition()
    examples = synset.examples()
    lemmas = [lemma.name().replace('_', ' ') for lemma in synset.lemmas()]

    # Extract hypernyms and hyponyms for background knowledge
    hypernyms = [h.name().split('.')[0].replace('_', ' ') for h in synset.hypernyms()[:5]]
    hyponyms = [h.name().split('.')[0].replace('_', ' ') for h in synset.hyponyms()[:5]]

    # Preprocess gloss text
    gloss_prep = preprocess_text(definition)

    # Preprocess example texts combined
    combined_examples = " ".join(examples) if examples else ""
    example_prep = preprocess_text(combined_examples)

    return {
        'synset_name': name,
        'synset_obj': synset,
        'pos_code': pos_code,
        'pos_display': pos_display,
        'definition': definition,
        'examples': examples,
        'lemmas': lemmas,
        'hypernyms': hypernyms,
        'hyponyms': hyponyms,
        'gloss_tokens': gloss_prep['filtered_tokens'],
        'gloss_lemmas': gloss_prep['unique_lemmas'],
        'example_tokens': example_prep['filtered_tokens'],
        'example_lemmas': example_prep['unique_lemmas']
    }


def get_synonym_expansion(context_lemmas: List[str], max_synonyms_per_word: int = 3) -> Dict[str, List[str]]:
    """
    Thesaurus-style semantic expansion:
    For context lemmas, retrieves their WordNet synonyms (lemmas from top synsets).
    Returns a mapping of context_word -> list of synonyms, as well as a flattened set.
    """
    expansion = {}
    flattened_synonyms: Set[str] = set()

    for word in context_lemmas:
        if len(word) <= 2:
            continue
        synsets = wn.synsets(word)
        word_syns = set()
        for syn in synsets[:2]:  # Limit to top 2 senses to avoid topic drift
            for lemma in syn.lemmas():
                clean_lemma = lemma.name().lower().replace('_', ' ')
                if clean_lemma != word and len(clean_lemma) > 2:
                    word_syns.add(clean_lemma)
                    if len(word_syns) >= max_synonyms_per_word:
                        break
            if len(word_syns) >= max_synonyms_per_word:
                break

        if word_syns:
            expansion[word] = list(word_syns)
            flattened_synonyms.update(word_syns)

    return {
        'word_synonyms': expansion,
        'all_synonyms': list(flattened_synonyms)
    }
