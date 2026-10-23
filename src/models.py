"""
Models Module for EduSense WSD System.
Fulfills required deliverable: src/models.py
Contains POS taggers, Dictionary-based and Thesaurus-based WSD algorithms, WordNet lexical model, and baseline models.
"""

from typing import List, Dict, Any, Optional
import nltk
from nltk.corpus import wordnet as wn
from src.preprocessing import preprocess_text, get_wordnet_pos, normalize_text
from src.context_extractor import extract_context
from src.wordnet_engine import (
    get_candidate_synsets,
    extract_synset_details,
    get_synonym_expansion
)

DEFAULT_WEIGHTS = {
    'alpha_direct': 1.5,   # Direct exact token overlap
    'beta_lemma': 1.2,     # Lemma token overlap
    'gamma_example': 1.0,  # Example sentence lemma overlap
    'delta_synonym': 0.7,  # Thesaurus synonym overlap
    'epsilon_hyper': 0.5   # Hypernym/Hyponym hierarchy overlap
}

class POSTaggerModel:
    """
    POS Tagger model for educational transcripts.
    Uses Penn Treebank tagging mapped to WordNet syntactic categories.
    """
    @staticmethod
    def infer_pos(context_tokens: List[str], target_word: str) -> Optional[str]:
        if not context_tokens or not target_word:
            return None
        try:
            pos_tags = nltk.pos_tag(context_tokens)
            target_clean = normalize_text(target_word)
            for tok, tag in pos_tags:
                if normalize_text(tok) == target_clean:
                    return get_wordnet_pos(tag)
        except Exception:
            pass
        return None


class DictionaryThesaurusWSD:
    """
    Core Dictionary and Thesaurus-based Word Sense Disambiguation Model.
    Implements multi-factor gloss overlap scoring with WordNet synsets,
    example sentence overlap, and thesaurus synonym expansion.
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = dict(weights) if weights else dict(DEFAULT_WEIGHTS)

    def disambiguate(
        self,
        transcript: str,
        target_word: str,
        window_size: int = 10,
        occurrence_index: int = 0,
        use_pos_filter: bool = True
    ) -> Dict[str, Any]:
        """
        Disambiguates target word sense within educational lecture transcript.
        """
        # 1. Context Extraction
        context_info = extract_context(transcript, target_word, window_size, occurrence_index)
        if not context_info['found']:
            return {
                'success': False,
                'error_message': context_info['error_message'],
                'target_word': target_word,
                'transcript': transcript
            }

        # 2. Text Preprocessing
        context_prep = preprocess_text(context_info['context_text'], preserve_target=target_word)

        # 3. POS Inference & Candidate Retrieval
        inferred_pos = None
        if use_pos_filter:
            inferred_pos = POSTaggerModel.infer_pos(context_info['context_tokens'], target_word)

        candidate_synsets = get_candidate_synsets(target_word, pos=inferred_pos)
        if not candidate_synsets:
            candidate_synsets = get_candidate_synsets(target_word, pos=None)

        if not candidate_synsets:
            return {
                'success': False,
                'error_message': f"No WordNet synsets found for target word '{target_word}'.",
                'target_word': target_word,
                'transcript': transcript
            }

        # 4. Thesaurus Synonym Expansion
        target_clean = normalize_text(target_word)
        ctx_lemmas_no_target = [l for l in context_prep['unique_lemmas'] if l != target_clean]
        synonym_expansion = get_synonym_expansion(ctx_lemmas_no_target)

        # 5. Overlap Scoring
        scored_candidates = []
        for wn_order, synset in enumerate(candidate_synsets):
            syn_details = extract_synset_details(synset)
            scores = self._calculate_overlap(context_prep, syn_details, synonym_expansion, target_clean)

            candidate_item = {
                'wn_order': wn_order,
                'synset_name': syn_details['synset_name'],
                'pos_display': syn_details['pos_display'],
                'definition': syn_details['definition'],
                'examples': syn_details['examples'],
                'lemmas': syn_details['lemmas'],
                'hypernyms': syn_details['hypernyms'],
                'hyponyms': syn_details['hyponyms'],
                'direct_score': scores['direct_score'],
                'lemma_score': scores['lemma_score'],
                'example_score': scores['example_score'],
                'synonym_score': scores['synonym_score'],
                'hyper_score': scores['hyper_score'],
                'final_score': scores['final_score'],
                'direct_matches': scores['direct_matches'],
                'lemma_matches': scores['lemma_matches'],
                'example_matches': scores['example_matches'],
                'synonym_matches': scores['synonym_matches'],
                'hyper_matches': scores['hyper_matches'],
                'all_evidence_words': scores['all_evidence_words']
            }
            scored_candidates.append(candidate_item)

        # 6. Ranking
        scored_candidates.sort(
            key=lambda x: (-x['final_score'], -x['direct_score'], -x['lemma_score'], x['wn_order'])
        )

        for idx, cand in enumerate(scored_candidates):
            cand['rank'] = idx + 1

        top_candidate = scored_candidates[0]

        # 7. Relative Confidence
        total_score_sum = sum(c['final_score'] for c in scored_candidates)
        num_candidates = len(scored_candidates)
        if total_score_sum > 0:
            relative_confidence = round(top_candidate['final_score'] / total_score_sum, 4)
        else:
            relative_confidence = round(1.0 / num_candidates, 4) if num_candidates > 0 else 0.0

        # 8. Decision Explanation
        explanation = {
            'predicted_synset': top_candidate['synset_name'],
            'definition': top_candidate['definition'],
            'pos': top_candidate['pos_display'],
            'inferred_pos': inferred_pos,
            'matched_direct_words': top_candidate['direct_matches'],
            'matched_lemma_words': top_candidate['lemma_matches'],
            'matched_example_words': top_candidate['example_matches'],
            'matched_synonym_words': top_candidate['synonym_matches'],
            'matched_hyper_words': top_candidate['hyper_matches'],
            'total_evidence_count': len(top_candidate['all_evidence_words']),
            'explanation_text': (
                f"Synset '{top_candidate['synset_name']}' selected because context vocabulary "
                f"({', '.join(top_candidate['all_evidence_words']) if top_candidate['all_evidence_words'] else 'general context fallback'}) "
                f"matched its dictionary gloss, examples, thesaurus synonyms, or hypernym hierarchy."
            )
        }

        return {
            'success': True,
            'target_word': target_word,
            'raw_transcript': transcript,
            'context_info': context_info,
            'preprocessing_steps': context_prep,
            'synonym_expansion': synonym_expansion,
            'predicted_sense': top_candidate,
            'candidate_rankings': scored_candidates,
            'candidate_count': len(scored_candidates),
            'relative_confidence': relative_confidence,
            'explanation': explanation,
            'scoring_weights': self.weights
        }

    def _calculate_overlap(
        self,
        context_prep: Dict[str, Any],
        synset_details: Dict[str, Any],
        synonym_expansion: Dict[str, Any],
        target_clean: str
    ) -> Dict[str, Any]:
        ctx_tokens = set(t for t in context_prep['filtered_tokens'] if t != target_clean)
        ctx_lemmas = set(l for l in context_prep['unique_lemmas'] if l != target_clean)

        gloss_tokens = set(synset_details['gloss_tokens'])
        gloss_lemmas = set(synset_details['gloss_lemmas'])
        example_lemmas = set(synset_details['example_lemmas'])
        context_synonyms = set(synonym_expansion['all_synonyms']) - {target_clean}

        rel_tokens = set(normalize_text(h) for h in (synset_details['hypernyms'] + synset_details['hyponyms']))

        direct_matches = list(ctx_tokens.intersection(gloss_tokens))
        lemma_matches = list(ctx_lemmas.intersection(gloss_lemmas))
        example_matches = list(ctx_lemmas.intersection(example_lemmas))
        synonym_matches = list(context_synonyms.intersection(gloss_lemmas))
        hyper_matches = list(ctx_lemmas.intersection(rel_tokens))

        direct_score = float(len(direct_matches))
        lemma_score = float(len(lemma_matches))
        example_score = float(len(example_matches))
        synonym_score = float(len(synonym_matches))
        hyper_score = float(len(hyper_matches))

        final_score = (
            self.weights['alpha_direct'] * direct_score +
            self.weights['beta_lemma'] * lemma_score +
            self.weights['gamma_example'] * example_score +
            self.weights['delta_synonym'] * synonym_score +
            self.weights['epsilon_hyper'] * hyper_score
        )

        all_evidence_words = list(dict.fromkeys(
            direct_matches + lemma_matches + example_matches + synonym_matches + hyper_matches
        ))

        return {
            'direct_matches': direct_matches,
            'direct_score': direct_score,
            'lemma_matches': lemma_matches,
            'lemma_score': lemma_score,
            'example_matches': example_matches,
            'example_score': example_score,
            'synonym_matches': synonym_matches,
            'synonym_score': synonym_score,
            'hyper_matches': hyper_matches,
            'hyper_score': hyper_score,
            'final_score': round(final_score, 4),
            'all_evidence_words': all_evidence_words
        }


# Convenience alias
WSDModel = DictionaryThesaurusWSD
