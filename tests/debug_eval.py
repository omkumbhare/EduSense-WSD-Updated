from src.evaluation import run_evaluation_benchmark

res = run_evaluation_benchmark()
print(f"Total: {res['total_samples']} | Custom Correct: {res['custom_correct']} ({res['custom_accuracy']}%) | Baseline Correct: {res['baseline_correct']} ({res['baseline_accuracy']}%)")
print("-" * 80)
for item in res['detailed_results']:
    status = "OK" if item['custom_correct'] else "FAIL"
    print(f"ID {item['id']:02d} [{status}] Target: '{item['target_word']}'")
    print(f"  Sentence: {item['sentence']}")
    print(f"  Gold: {item['gold_synset']} | Pred: {item['custom_predicted']} | Score: {item['score']}")
    if not item['custom_correct']:
        print(f"  Evidence matched: {item['evidence_words']}")
    print("-" * 80)
