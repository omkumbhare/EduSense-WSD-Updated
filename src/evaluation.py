"""
Evaluation Benchmark Engine for EduSense.
Evaluates the custom Dictionary/Thesaurus WSD engine against NLTK Simplified Lesk baseline
on the labeled educational dataset (data/annotated/evaluation_dataset.csv).
Computes quantitative performance metrics, confidence distributions, and failure analyses.
"""

import os
import pandas as pd
from typing import Dict, Any, List
from src.wsd_engine import disambiguate_word
from src.baseline import run_nltk_lesk


def _macro_prf(results: List[Dict[str, Any]]):
    """Macro-averaged precision / recall / F1 (%) over gold synset classes."""
    labels = sorted({r['gold_synset'] for r in results} | {r['custom_predicted'] for r in results})
    ps, rs, fs = [], [], []
    for lab in labels:
        tp = sum(1 for r in results if r['gold_synset'] == lab and r['custom_predicted'] == lab)
        fp = sum(1 for r in results if r['gold_synset'] != lab and r['custom_predicted'] == lab)
        fn = sum(1 for r in results if r['gold_synset'] == lab and r['custom_predicted'] != lab)
        p = tp / (tp + fp) if tp + fp else 0.0
        r_ = tp / (tp + fn) if tp + fn else 0.0
        f = 2 * p * r_ / (p + r_) if p + r_ else 0.0
        ps.append(p); rs.append(r_); fs.append(f)
    n = len(labels) or 1
    return round(100 * sum(ps) / n, 2), round(100 * sum(rs) / n, 2), round(100 * sum(fs) / n, 2)


def run_evaluation_benchmark(dataset_path: str = "data/annotated/evaluation_dataset.csv") -> Dict[str, Any]:
    """
    Runs evaluation benchmark over labeled test dataset.

    Returns comprehensive metrics dictionary:
    - total_samples: int
    - custom_correct: int
    - custom_accuracy: float (%)
    - baseline_correct: int
    - baseline_accuracy: float (%)
    - avg_candidate_senses: float
    - avg_confidence: float
    - avg_overlap_score: float
    - detailed_results: List[Dict]
    - failure_cases: List[Dict]
    - metric_comparison_table: List[Dict]
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Evaluation dataset file not found at: {dataset_path}")

    df = pd.read_csv(dataset_path)

    total_samples = len(df)
    custom_correct = 0
    baseline_correct = 0

    total_candidates = 0
    total_confidence = 0.0
    total_overlap_score = 0.0

    detailed_results = []
    failure_cases = []

    for _, row in df.iterrows():
        sample_id = int(row['id'])
        sentence = str(row['sentence'])
        target_word = str(row['target_word']).strip()
        gold_synset = str(row['gold_synset']).strip()
        gold_def = str(row['gold_definition']).strip()

        # Run Custom WSD Engine
        custom_res = disambiguate_word(
            transcript=sentence,
            target_word=target_word,
            window_size=10
        )

        # Run NLTK Lesk Baseline
        baseline_res = run_nltk_lesk(
            transcript=sentence,
            target_word=target_word
        )

        custom_predicted = custom_res['predicted_sense']['synset_name'] if custom_res.get('success') else None
        baseline_predicted = baseline_res.get('predicted_synset')

        custom_is_correct = (custom_predicted == gold_synset)
        baseline_is_correct = (baseline_predicted == gold_synset)

        if custom_is_correct:
            custom_correct += 1
        if baseline_is_correct:
            baseline_correct += 1

        cand_count = custom_res.get('candidate_count', 0) if custom_res.get('success') else 0
        conf = custom_res.get('relative_confidence', 0.0) if custom_res.get('success') else 0.0
        score = custom_res['predicted_sense']['final_score'] if custom_res.get('success') else 0.0

        total_candidates += cand_count
        total_confidence += conf
        total_overlap_score += score

        result_item = {
            'id': sample_id,
            'sentence': sentence,
            'target_word': target_word,
            'gold_synset': gold_synset,
            'gold_definition': gold_def,
            'custom_predicted': custom_predicted or "Failed",
            'custom_definition': custom_res['predicted_sense']['definition'] if custom_res.get('success') else "N/A",
            'custom_correct': custom_is_correct,
            'baseline_predicted': baseline_predicted or "None",
            'baseline_correct': baseline_is_correct,
            'candidate_count': cand_count,
            'score': score,
            'confidence': conf,
            'evidence_words': custom_res['explanation']['matched_direct_words'] + custom_res['explanation']['matched_lemma_words'] if custom_res.get('success') else []
        }
        detailed_results.append(result_item)

        if not custom_is_correct:
            failure_cases.append({
                'id': sample_id,
                'sentence': sentence,
                'target_word': target_word,
                'gold_synset': gold_synset,
                'predicted_synset': custom_predicted,
                'reason': "Low context-gloss vocabulary overlap or multiple overlapping senses in WordNet."
            })

    custom_accuracy = round((custom_correct / total_samples) * 100.0, 2) if total_samples > 0 else 0.0
    baseline_accuracy = round((baseline_correct / total_samples) * 100.0, 2) if total_samples > 0 else 0.0

    avg_candidates = round(total_candidates / total_samples, 2) if total_samples > 0 else 0.0
    avg_confidence = round(total_confidence / total_samples, 4) if total_samples > 0 else 0.0
    avg_overlap_score = round(total_overlap_score / total_samples, 2) if total_samples > 0 else 0.0

    # Macro Precision / Recall approximation across target words
    precision, recall, f1_score = _macro_prf(detailed_results)

    return {
        'total_samples': total_samples,
        'custom_correct': custom_correct,
        'custom_incorrect': total_samples - custom_correct,
        'custom_accuracy': custom_accuracy,
        'baseline_correct': baseline_correct,
        'baseline_incorrect': total_samples - baseline_correct,
        'baseline_accuracy': baseline_accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'avg_candidate_senses': avg_candidates,
        'avg_confidence': avg_confidence,
        'avg_overlap_score': avg_overlap_score,
        'detailed_results': detailed_results,
        'failure_cases': failure_cases,
        'chart_data': {
            'methods': ['EduSense Custom WSD (Dictionary + Thesaurus)', 'NLTK Simplified Lesk Baseline'],
            'accuracies': [custom_accuracy, baseline_accuracy],
            'correct_counts': [custom_correct, baseline_correct],
            'incorrect_counts': [total_samples - custom_correct, total_samples - baseline_correct]
        }
    }
