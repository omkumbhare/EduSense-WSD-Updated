# EduSense — Benchmark Evaluation Report

## 1. Experimental Setup
- **Dataset**: `data/annotated/evaluation_dataset.csv`
- **Total Test Samples**: 25 Educational Transcripts across 18 polysemous target words.
- **Domains Covered**: Geology, Economics, Biology, Industrial Engineering, Optics Physics, Computer Science, Geometry, Psychology, Chemistry.
- **Baseline**: NLTK Simplified Lesk algorithm (`nltk.wsd.lesk`).
- **Evaluation Criteria**: Accuracy (exact synset match with gold label) plus macro-averaged Precision / Recall / F1 over gold synset classes.

---

## 2. Quantitative Benchmark Results

| Model / Algorithm | Correct Predictions | Total Samples | Accuracy (%) | Avg Relative Confidence |
| :--- | :---: | :---: | :---: | :---: |
| **EduSense Custom WSD** | **14** | **25** | **56.0%** | **42.1%** |
| **NLTK Simplified Lesk Baseline** | **10** | **25** | **40.0%** | N/A |

**Macro Precision / Recall / F1 (EduSense):** 40.3% / 45.2% / 41.9%

### Performance Delta:
EduSense achieved a **+16.0% accuracy improvement** over the NLTK Simplified Lesk baseline.

---

## 3. Key Success Factors
1. **Thesaurus Synonym Expansion**: Matches semantic paraphrases in transcript context (e.g. *monetary* matching *financial* in banking context).
2. **POS-Guided Filtering**: Prevents misclassifying noun target words into verb candidate senses.
3. **Hypernym Hierarchy Overlap**: Captures domain-level concepts like *organism* for biology plants and *region* for physics fields.
4. **Target Self-Match Exclusion**: Eliminates artificial bias toward candidate senses whose gloss happens to repeat the target lemma.

---

## 4. Qualitative Failure Analysis

### Example 1: `memory.n.02` vs `memory.n.05`
- **Sentence**: *"Psychology class discussed human short term memory retention and cognitive recall techniques."*
- **Gold Synset**: `memory.n.02` ("cognitive processes whereby past experience is remembered")
- **Predicted Synset**: `memory.n.05` ("the power of retaining and recalling past experience")
- **Root Cause**: WordNet contains nearly identical overlapping definitions for cognitive memory. Both senses score high; `memory.n.05` gloss contained exact lemma match for *psychology*.

### Example 2: `plant.n.02` (Biology Plant)
- **Sentence**: *"The biology professor explained how the plant absorbs light and water from the soil to perform photosynthesis."*
- **Gold Synset**: `plant.n.02` ("(botany) a living organism lacking the power of locomotion")
- **Root Cause**: WordNet's gloss for `plant.n.02` is very concise (8 words). Without explicit occurrence of the word *botany* or *locomotion* in the sentence, gloss overlap score was 0.0.

---

## 5. Conclusion & Recommendations
Transparent dictionary gloss overlap provides a strong, interpretable baseline for educational transcript WSD without requiring expensive GPU inference or LLM APIs. Future work can incorporate domain-specific educational ontology weights and contextual embedding similarity.


---

## Known Failure Case (raw transcript demo)
In `lecture_biology_cell_nucleus.txt`, *nucleus* is resolved to `lens_nucleus.n.01` instead of the biological `nucleus.n.01`. Cause: the sentence context shares equal-weight gloss overlap with several senses (score ties), and WordNet gloss vocabulary is sparse. Ties are now broken by WordNet sense order (frequency-ranked), which resolves most such ties but not this one.
