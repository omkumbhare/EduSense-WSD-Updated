# EduSense — Presentation Content & Slide Outline (13 Slides)

---

### Slide 1: Title & Project Details
- **Title**: EduSense — Dictionary and Thesaurus-Based Word Sense Disambiguation for Educational Transcripts
- **Subtitle**: MT-AIML Mini-Project | Problem 13
- **Technology**: Python, NLTK WordNet, Flask, Bootstrap 5, Chart.js
- **Presenter**: Student Name / Roll Number

---

### Slide 2: Problem Introduction
- **Context**: Educational lecture transcripts contain polysemous academic vocabulary.
- **Challenge**: The same word (e.g. *bank*, *plant*, *cell*) carries completely different meanings across Geology, Economics, Biology, and Computer Science.
- **Goal**: Build a transparent, explainable NLP engine to automatically identify the exact WordNet sense from surrounding lecture context.

---

### Slide 3: Problem Understanding & Polysemy
- **Polysemy Definition**: A single word form with multiple related or distinct dictionary senses.
- **Examples in Lectures**:
  - *"River bank erosion"* (Geology) vs *"Commercial bank deposit"* (Economics)
  - *"Manufacturing plant"* (Engineering) vs *"Photosynthetic plant"* (Botany)
  - *"Biological cell nucleus"* (Biology) vs *"RAM memory cell"* (CS)

---

### Slide 4: Need for WSD in Educational Systems
- Automated transcript indexing and academic search engines.
- AI lecture summarization and automated flashcard generation.
- Accessibility for Non-Native English Speakers studying STEM subjects.

---

### Slide 5: Scope of Solution
- Pure algorithmic WSD based on WordNet lexical database.
- Explicitly **NO LLM APIs** (OpenAI / Gemini) used for WSD decision.
- Transparent explainable decision logic suitable for college evaluator demonstration.
- Runnable local web application with interactive dashboard.

---

### Slide 6: Literature Survey & Existing Solutions
- **Lesk Algorithm (1986)**: Overlap between context and dictionary definitions.
- **Simplified Lesk (NLTK)**: Standard baseline.
- **Limitation of Standard Lesk**: Fails when exact definition words do not appear in short contexts.
- **EduSense Innovation**: Adds Thesaurus Synonym Expansion, POS filtering, Example matching, and Hypernym hierarchy.

---

### Slide 7: Proposed System Overview
- End-to-end WSD processing pipeline:
  1. Transcript & Target Word Input
  2. Context Extraction (±10 words window)
  3. Preprocessing (Lowercasing, Stopwords, POS, Lemmatization)
  4. WordNet Synset & Gloss Retrieval
  5. Thesaurus Synonym Expansion
  6. Multi-Factor Overlap Scoring
  7. Sense Ranking & Relative Confidence
  8. Decision Explanation Dashboard

---

### Slide 8: System Architecture & Workflow
- **Frontend**: HTML5, Bootstrap 5 dark theme, Chart.js visualizations.
- **Backend Controller**: Flask (`app.py`).
- **Core NLP Modules**: `preprocessing.py`, `context_extractor.py`, `wordnet_engine.py`, `wsd_engine.py`, `evaluation.py`.

---

### Slide 9: Mathematical Formulation & Scoring
- Multi-Factor Overlap Formula:
  $$\text{Final Score}(s) = \alpha \cdot \text{Direct} + \beta \cdot \text{Lemma} + \gamma \cdot \text{Example} + \delta \cdot \text{Synonym} + \epsilon \cdot \text{Hypernym}$$
- Weights: $\alpha=1.5, \beta=1.2, \gamma=1.0, \delta=0.7, \epsilon=0.5$.
- Relative Confidence:
  $$\text{Confidence} = \frac{\text{Top Score}}{\sum \text{Scores}}$$

---

### Slide 10: Web Application Interface & XAI
- **Interactive WSD Analyzer**: Real-time transcript input, target selection, context window slider, preloaded presets.
- **Explainable AI (XAI)**: Displays exact matched evidence badges (direct words, gloss lemmas, example words, thesaurus synonyms).
- **Candidate Sense Ranking Table**: Displays all candidate WordNet senses with individual component scores.

---

### Slide 11: Benchmark Results & Comparison
- **Dataset**: 25 Labeled Educational Transcripts across 18 target words (`data/annotated/evaluation_dataset.csv`).
- **EduSense Custom WSD**: **56.0% Accuracy** (14 / 25 correct).
- **NLTK Lesk Baseline**: **40.0% Accuracy** (10 / 25 correct).
- **Performance Gain**: **+16.0% improvement** due to thesaurus expansion and hypernym hierarchy scoring.

---

### Slide 12: Conclusion, Learnings & Future Scope
- **Conclusion**: Proved that transparent dictionary/thesaurus context matching effectively disambiguates academic terms without black-box APIs.
- **Learnings**: Lexical semantics, WordNet structure, NLTK pipelines, evaluation methodologies.
- **Future Scope**: Integration of domain-specific educational ontologies and sentence transformer embeddings.

---

### Slide 13: Demonstration & Q&A
- Live web app demonstration (`python app.py`).
- Interactive evaluator questions & answers.
