"""
Execution Pipeline & Evaluation Runner for EduSense.
Fulfills required deliverable: src/pipeline.py
Provides end-to-end WSD execution pipeline and benchmark evaluation runner.
"""

import os
from typing import Dict, Any, Optional
from src.models import DictionaryThesaurusWSD
from src.evaluation import run_evaluation_benchmark
from src.preprocessing import segment_sentences, normalize_text


class WSDPipeline:
    """
    End-to-end WSD execution pipeline for educational transcripts.
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.model = DictionaryThesaurusWSD(weights=weights)

    def run(
        self,
        transcript: str,
        target_word: str,
        window_size: int = 10,
        occurrence_index: int = 0
    ) -> Dict[str, Any]:
        """
        Executes complete WSD pipeline on an educational transcript.
        """
        return self.model.disambiguate(
            transcript=transcript,
            target_word=target_word,
            window_size=window_size,
            occurrence_index=occurrence_index
        )

    def run_on_transcript_file(self, path: str, target_words, window_size: int = 10) -> list:
        """
        Segments a raw lecture transcript into sentences and disambiguates every
        occurrence of each target word (data/raw_transcripts/*.txt).
        """
        with open(path, encoding="utf-8") as f:
            text = f.read()
        out = []
        for sent in segment_sentences(text):
            for tw in target_words:
                if tw.lower() in normalize_text(sent).split() or tw.lower() in normalize_text(sent):
                    res = self.run(sent, tw, window_size=window_size)
                    if res.get("success"):
                        ps = res["predicted_sense"]
                        out.append({
                            "file": os.path.basename(path), "word": tw, "sentence": sent,
                            "synset": ps["synset_name"], "definition": ps["definition"],
                            "confidence": res["relative_confidence"],
                        })
        return out

    @staticmethod
    def evaluate(dataset_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Runs empirical benchmark evaluation over labeled dataset.
        Defaults to the gold-standard file data/annotated/evaluation_dataset.csv.
        """
        if not dataset_path:
            dataset_path = "data/annotated/evaluation_dataset.csv"

        return run_evaluation_benchmark(dataset_path=dataset_path)


# CLI execution runner
if __name__ == "__main__":
    import glob
    pipeline = WSDPipeline()

    print("=== Benchmark evaluation (data/annotated) ===")
    results = pipeline.evaluate()
    print(f"Total Samples      : {results['total_samples']}")
    print(f"Custom WSD Accuracy: {results['custom_accuracy']}%")
    print(f"NLTK Lesk Accuracy : {results['baseline_accuracy']}%")
    print(f"Macro P / R / F1   : {results['precision']} / {results['recall']} / {results['f1_score']}")

    print("\n=== Raw transcript demo (data/raw_transcripts) ===")
    demo_words = ["bank", "cell", "memory", "stack", "nucleus", "plant"]
    for f in sorted(glob.glob("data/raw_transcripts/*.txt")):
        for r in pipeline.run_on_transcript_file(f, demo_words)[:3]:
            print(f"[{r['file']}] {r['word']} -> {r['synset']} ({r['confidence']:.2f})")
