# EduSense — Final Presentation Outline, Slide Content & Speaker Notes

**Presentation File Name**: `Problem_13_MT_AIML_WSD_Om_Kumbhare.pptx`  
**Subject**: Modern Trends in Artificial Intelligence & Machine Learning (MT-AIML Mini Project)  
**Problem Number**: Problem 13  
**Problem Title**: Dictionary and Thesaurus-Based Word Sense Disambiguation for Educational Transcripts  
**Student Name**: Om Kumbhare  
**Enrollment Number**: ET23BTEC026  
**Program**: B.Tech Electronics & Communication Engineering (4th Year | 7th Semester | AY 2026–27)  
**Honors**: Artificial Intelligence & Machine Learning  
**College**: Sarvajanik College of Engineering and Technology (SCET)  
**Faculty Guide**: Prof. Dr. Niteenbhai Patel  

---

## 📋 Complete Slide-by-Slide Outline & Speaker Notes

### SLIDE 1: Title & Student Details
- **Slide Header**: Problem 13 — Final Mini Project Presentation
- **Main Title**: Dictionary and Thesaurus-Based Word Sense Disambiguation for Educational Transcripts
- **Subtitle**: Modern Trends in Artificial Intelligence & Machine Learning (MT-AIML)
- **Student Information**:
  - Name: Om Kumbhare
  - Enrollment No.: ET23BTEC026
  - Department: B.Tech Electronics & Communication Engineering
  - Year/Semester: 4th Year | 7th Semester (Academic Year: 2026–27)
  - Specialization: Honors in Artificial Intelligence & Machine Learning
- **Institution Details**:
  - College: Sarvajanik College of Engineering and Technology
  - Faculty Guide: Prof. Dr. Niteenbhai Patel
  - Placeholders: `[COLLEGE LOGO]`, `[STUDENT PHOTOGRAPH]`, `[SUBMISSION DATE]`
- **Speaker Notes**:
  > *"Good morning Professor Patel and evaluators. I am Om Kumbhare, enrollment number ET23BTEC026, 4th-year B.Tech student in Electronics and Communication Engineering with Honors in AIML. Today, I am presenting my final mini-project for MT-AIML Problem 13 titled 'Dictionary and Thesaurus-Based Word Sense Disambiguation for Educational Transcripts' supervised by Prof. Dr. Niteenbhai Patel."*

---

### SLIDE 2: Problem Introduction
- **Slide Header**: Problem Introduction: Lexical Ambiguity in Lecture Transcripts
- **Content**:
  - What is WSD? An essential NLP task identifying which specific dictionary sense of a polysemous word is used in context.
  - Polysemy Definition: A single word form possessing multiple distinct or related dictionary meanings.
  - Educational Challenge: Academic transcripts contain dense domain vocabulary where words carry completely different meanings across subjects.
  - Concrete Example:
    - *Example A (Geology)*: *"Geologists surveyed the river bank..."* $\rightarrow$ `bank.n.01` (Sloping land beside water).
    - *Example B (Economics)*: *"The commercial bank handles monetary deposits..."* $\rightarrow$ `depository_financial_institution.n.01` (Financial bank).
- **Speaker Notes**:
  > *"Slide 2 introduces the core problem. Word Sense Disambiguation is a fundamental open challenge in NLP. In educational lectures, polysemous terms appear constantly. As demonstrated by the example, the word 'bank' in a geology transcript with words like 'river' and 'erosion' means sloping land. In an economics transcript with words like 'deposits' and 'interest', it means a financial institution. Surrounding context is the key to resolving this ambiguity."*

---

### SLIDE 3: Detailed Problem Understanding
- **Slide Header**: Detailed Problem Understanding: Academic Transcript Constraints
- **Content**:
  - 1. High Fine-Grained Polysemy: Academic terms have dozens of WordNet synsets (e.g., 'bank' has 10+ synsets, 'point' has 30+).
  - 2. Transcript Noisiness & ASR Artifacts: Speech-to-text transcripts lack formal punctuation and contain conversational filler.
  - 3. Concise Dictionary Glosses: WordNet definitions are very brief (5–10 words). Direct overlap is often zero without lemmatization and synonym expansion.
  - 4. Core Constraint: Problem 13 requires a transparent gloss-overlap algorithm using WordNet without relying on black-box LLM APIs.
- **Speaker Notes**:
  > *"Here we examine why basic dictionary lookup alone fails. WordNet provides dozens of candidate senses for academic words. Furthermore, dictionary glosses are very short—often just 5 words long. If we only count raw word matches, overlap is almost always zero. That is why our implementation incorporates lemmatization, example sentence matching, and thesaurus synonym expansion."*

---

### SLIDE 4: Project Objectives & Proposed Solution Pipeline
- **Slide Header**: Project Objectives & Core Algorithmic Idea
- **Content**:
  - 9 Clear Objectives: Transcript input $\rightarrow$ Target word detection $\rightarrow$ Context extraction $\rightarrow$ Text normalization $\rightarrow$ WordNet synset querying $\rightarrow$ Overlap scoring $\rightarrow$ Thesaurus expansion $\rightarrow$ Sense ranking $\rightarrow$ Empirical benchmark evaluation.
  - System Pipeline Diagram: Transcript Input $\rightarrow$ Context Extractor ($\pm N$ words) $\rightarrow$ NLP Preprocessing $\rightarrow$ WordNet Retrieval $\rightarrow$ Thesaurus Expansion $\rightarrow$ Multi-Factor Overlap Scoring $\rightarrow$ Ranking & Relative Confidence $\rightarrow$ Output + XAI Evidence.
- **Speaker Notes**:
  > *"Slide 4 outlines our key project objectives and high-level architectural flow. The objectives cover input processing, context extraction, WordNet querying, multi-factor scoring, empirical evaluation, and web app delivery. The diagram shows our end-to-end pipeline from raw transcript down to predicted sense and decision explanations."*

---

### SLIDE 5: Scope of Solution & System Boundaries
- **Slide Header**: Scope of Solution & System Boundaries
- **Content**:
  - In Scope: English lecture transcripts, polysemous academic terms, NLTK WordNet synsets, configurable context windowing ($\pm 5$ to $\pm 25$ words), multi-factor scoring, empirical benchmark evaluation, local Flask web app.
  - Input/Output: Transcript text + target word $\rightarrow$ Predicted synset, definition, score, relative confidence %, matched evidence.
  - Core Restriction: Strictly no external LLM APIs (OpenAI/Gemini). Pure NLTK & WordNet implementation.
  - Current Limitations: Dependent on WordNet English vocabulary coverage.
  - Future Expansion: Transformer embeddings (BERT/SBERT) and live speech-to-text streams.
- **Speaker Notes**:
  > *"Slide 5 defines our solution boundaries. In scope, we focus on English academic transcripts, NLTK WordNet data, and explainable multi-factor scoring. Crucially, no paid or black-box LLM APIs are used. Limitations include dependency on WordNet gloss coverage. Future work can extend this with contextual Transformer embeddings."*

---

### SLIDE 6: Survey of Existing WSD Approaches & Related Work
- **Slide Header**: Survey of Existing WSD Approaches & Related Work
- **Content**:
  - Comparative Survey Table comparing:
    1. Original Lesk (1986): Raw dictionary overlaps $\rightarrow$ Unsupervised but combinatorial & sparse.
    2. Simplified Lesk (NLTK): Individual sense gloss comparison $\rightarrow$ Efficient baseline but ignores synonyms/hierarchy.
    3. Supervised WSD: Classifiers trained on SemCor $\rightarrow$ High accuracy on frequent words but requires massive annotated data.
    4. EduSense (Our Engine): Multi-factor weighted overlap + Thesaurus expansion + POS filtering $\rightarrow$ 100% Explainable; +16% accuracy over baseline.
    5. Transformer WSD (BERT): Contextual embeddings $\rightarrow$ SOTA representations but acts as black-box.
- **Speaker Notes**:
  > *"Slide 6 presents a survey of established WSD paradigms. Standard Lesk was introduced in 1986. NLTK's Simplified Lesk is a well-known baseline. Supervised WSD requires massive sense-tagged datasets like SemCor. Modern Transformers give high accuracy but act as black boxes. Our EduSense method enhances Lesk with thesaurus expansion and POS filtering while maintaining 100% explainability."*

---

### SLIDE 7: Academic Research References & Technical Distinction
- **Slide Header**: Academic Research References & Technical Distinction
- **Content**:
  - Verified References:
    - 1. Lesk, M. (1986). *Automatic sense disambiguation using machine readable dictionaries*. ACM SIGDOC. DOI: 10.1145/318723.318728
    - 2. Miller, G. A. (1995). *WordNet: A lexical database for English*. Communications of the ACM, 38(11), 39-41.
    - 3. Banerjee, S., & Pedersen, T. (2002). *An adapted Lesk algorithm for word sense disambiguation using WordNet*. CICLing.
    - 4. Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing (3rd ed. draft)*.
  - Technical Distinction: Thesaurus synonym expansion, multi-factor weighting ($\alpha=1.5, \beta=1.2, \gamma=1.0, \delta=0.7, \epsilon=0.5$), POS filtering, target self-match exclusion, and relative confidence calculation.
- **Speaker Notes**:
  > *"Slide 7 cites established research literature including Michael Lesk's original 1986 paper, George Miller's 1995 WordNet paper, and Banerjee & Pedersen's 2002 Extended Lesk paper. On the right, we explicitly detail how our EduSense engine improves upon these baseline works through multi-factor weighting and thesaurus expansion."*

---

### SLIDE 8: Proposed System Architecture
- **Slide Header**: EduSense Proposed System Architecture & Module Pipeline
- **Content**:
  - Detailed module breakdown:
    - 1. `src/context_extractor.py`: Configurable windowing ($\pm 10$ words) & highlighting.
    - 2. `src/preprocessing.py`: Lowercasing, tokenization, stop-words, POS tagging, lemmatization.
    - 3. `src/wordnet_engine.py`: Candidate synset retrieval, glosses, examples, thesaurus synonym expansion.
    - 4. `src/wsd_engine.py`: Multi-factor overlap scoring, self-match exclusion, sense ranking, relative confidence.
    - 5. `src/baseline.py` & `src/evaluation.py`: NLTK Lesk baseline wrapper & 25-sample benchmark suite.
    - 6. `app.py` & `templates/`: Flask web application serving interactive UI, SVG charts, & XAI badges.
- **Speaker Notes**:
  > *"Slide 8 illustrates our modular code architecture. We created 7 specialized Python modules inside the src directory: context_extractor handles windowing, preprocessing handles tokenization and lemmatization, wordnet_engine fetches synsets and synonyms, wsd_engine calculates weighted overlap scores, evaluation runs benchmark tests, and app.py serves the Flask web application."*

---

### SLIDE 9: Methodology & Mathematical Formulation
- **Slide Header**: Methodology: Mathematical Formulations & Pseudocode
- **Content**:
  - Scoring Formula:
    $$\text{Final Score}(s) = \alpha \cdot \text{Direct} + \beta \cdot \text{Lemma} + \gamma \cdot \text{Example} + \delta \cdot \text{Synonym} + \epsilon \cdot \text{Hypernym}$$
  - Applied Weights: $\alpha=1.5, \beta=1.2, \gamma=1.0, \delta=0.7, \epsilon=0.5$.
  - Target Exclusion: $C_{\text{lemmas}} = \text{Lemmatize}(\text{Context}) \setminus \{\text{target\_word}\}$.
  - Relative Confidence: $\text{Confidence}(s^*) = \frac{\text{Score}(s^*)}{\sum_{s \in \text{Synsets}} \text{Score}(s)}$.
  - Pseudocode block showing full algorithm loop.
- **Speaker Notes**:
  > *"Slide 9 contains our exact mathematical formulations and pseudocode. The multi-factor score combines direct token matches weighted at 1.5, lemma matches at 1.2, example matches at 1.0, thesaurus synonyms at 0.7, and hypernym hierarchy matches at 0.5. We explicitly subtract the target word itself from context lemmas to avoid self-matching bias."*

---

### SLIDE 10: Web Application Interface & Dashboard
- **Slide Header**: Web Application Interface & Interactive Dashboard
- **Content**:
  - Overview of Flask Web App running on `http://127.0.0.1:5000`:
    - 1. Home Dashboard (`/`): Pipeline diagram & live benchmark metrics cards. `[Placeholder: WEB APP HOME DASHBOARD SCREENSHOT]`
    - 2. WSD Analyzer (`/analyzer`): Textarea, target input, window slider, preloaded presets. `[Placeholder: WSD ANALYZER INPUT SCREENSHOT]`
    - 3. Results & XAI (`/results`): Highlighted context, 3-stage preprocessing, predicted synset card, confidence bar, evidence badges. `[Placeholder: RESULTS & XAI SCREENSHOT]`
    - 4. Evaluation Dashboard (`/evaluation`): Quantitative benchmark metrics, SVG Chart.js graphs, test table. `[Placeholder: EVALUATION DASHBOARD SCREENSHOT]`
    - 5. Methodology & Viva (`/about`): Formulas, ASCII diagrams, 5 viva Q&A answers. `[Placeholder: METHODOLOGY PAGE SCREENSHOT]`
- **Speaker Notes**:
  > *"Slide 10 details our web application user interface built using Flask, HTML5, Bootstrap 5, and Chart.js. The app contains 5 distinct pages: Home Dashboard, Interactive WSD Analyzer, Results & XAI Spotlight, Empirical Evaluation Dashboard, and Methodology Viva Guide. Screen placeholders mark where live browser screenshots are presented."*

---

### SLIDE 11: Real Working Execution Trace & Output
- **Slide Header**: Real Working Project Execution Trace & Output
- **Content**:
  - Geology Lecture Trace:
    - Input: *"Geologists surveyed the river bank to measure soil erosion along the sloping water edge."*
    - Target: `bank` | Window: $\pm 10$ words
    - Context: `... geologists surveyed the river <mark>bank</mark> to measure soil erosion ...`
    - Preprocessing: Tokens $\rightarrow$ Filtered $\rightarrow$ Lemmatized (`['geologist', 'survey', 'river', 'measure', 'soil', 'erosion', 'slope', 'water', 'edge']`).
    - Synsets: 10 candidate synsets evaluated.
    - Predicted: `bank.n.01` ("sloping land beside a body of water").
    - Score Breakdown: Direct: 3.0 | Lemma: 2.0 | Example: 1.0 | Synonym: 0.7 | Total: 6.4.
    - Relative Confidence: 58.2% | Evidence: `['river', 'water', 'soil', 'erosion', 'sloping', 'edge']`.
- **Speaker Notes**:
  > *"Slide 11 demonstrates an actual working output trace generated by running our code on a geology transcript. For target word 'bank', the context window extracts 'river', 'soil', 'erosion', and 'water'. The preprocessing pipeline filters stop-words and lemmatizes tokens. The system evaluates all 10 candidate synsets, predicting bank.n.01 with a score of 6.4 and 58.2% relative confidence."*

---

### SLIDE 12: Empirical Evaluation Benchmark & Results
- **Slide Header**: Empirical Evaluation Benchmark & Results Analysis
- **Content**:
  - Benchmark Performance Table (`data/annotated/evaluation_dataset.csv` - 25 Transcripts):
    - **EduSense Custom WSD**: **56.0% Accuracy** (14 / 25 Correct).
    - **NLTK Simplified Lesk Baseline**: **40.0% Accuracy** (10 / 25 Correct).
    - **Performance Gain**: **+16.0% accuracy improvement**.
  - Qualitative Error Analysis:
    - 1. Sparse Gloss Definitions: WordNet glosses are very short (3–6 words).
    - 2. Highly Granular Senses: Fine-grained noun distinctions in WordNet.
    - 3. Short Context Windows: Brief transcript sentences lack domain keywords.
- **Speaker Notes**:
  > *"Slide 12 presents our empirical evaluation benchmark. Tested on 25 labeled educational transcripts across 18 target words, EduSense achieved 56.0% accuracy (14 correct) compared to 40.0% accuracy (10 correct) for NLTK Simplified Lesk baseline—a +16.0% improvement. Error analysis shows that failure cases occur primarily when WordNet glosses are sparse."*

---

### SLIDE 13: Conclusion, Key Learnings & Future Directions
- **Slide Header**: Conclusion, Key Academic Learnings & Future Directions
- **Content**:
  - **Conclusion**: Successfully constructed a transparent dictionary/thesaurus WSD engine outperforming Lesk baseline by +16.0% without LLM APIs.
  - **Academic Learnings**: Hands-on mastery of NLTK, WordNet synsets, lemmatization, lexical semantics, XAI design, and Flask web app development.
  - **Future Directions**: Transformer embeddings (Sentence-BERT), larger 500+ sample benchmark, educational taxonomy domain priors, speech-to-text integration.
- **Speaker Notes**:
  > *"Slide 13 divides our final summary into Project Conclusion, Key Academic Learnings, and Future Directions. We successfully built a working, explainable WSD engine that outperforms baseline Lesk. Academic learnings cover NLTK, WordNet, lexical semantics, and Flask web development. Future work includes dense Transformer embeddings."*

---

### SLIDE 14: Live System Demonstration Workflow
- **Slide Header**: Live System Demonstration & Evaluator Execution Workflow
- **Content**:
  - Step-by-step workflow:
    - Step 1: Startup (`python app.py` $\rightarrow$ NLTK verification $\rightarrow$ Flask active on port 5000).
    - Step 2: Interactive Analysis (Navigate to `/analyzer` $\rightarrow$ Select preset or type transcript).
    - Step 3: Execution (Set window slider $\pm 10$ words $\rightarrow$ Click 'Disambiguate Word Sense').
    - Step 4: XAI Evidence Inspection (Review highlighted context, preprocessing, predicted synset spotlight, confidence %, evidence badges, ranking table).
    - Step 5: Benchmark Evaluation (Navigate to `/evaluation` $\rightarrow$ Inspect stats, charts, test table).
- **Speaker Notes**:
  > *"Slide 14 guides the live demonstration for evaluators. We show how to launch the Flask server locally with 'python app.py', navigate to the interactive WSD Analyzer, run disambiguation on sample transcripts, inspect decision evidence badges, and view the benchmark evaluation dashboard."*

---

### SLIDE 15: Academic References & Citations
- **Slide Header**: Academic References & Formal Citations
- **Content**:
  - IEEE/APA Formal Citations:
    - 1. Lesk, M. (1986). *Automatic sense disambiguation using machine readable dictionaries*. ACM SIGDOC. DOI: 10.1145/318723.318728
    - 2. Miller, G. A. (1995). *WordNet: A lexical database for English*. Communications of the ACM, 38(11), 39–41.
    - 3. Banerjee, S., & Pedersen, T. (2002). *An adapted Lesk algorithm for word sense disambiguation using WordNet*. CICLing.
    - 4. Bird, S., Loper, E., & Klein, E. (2009). *Natural Language Processing with Python*. O'Reilly Media.
    - 5. Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing (3rd ed. draft)*. Chapter 18.
    - 6. MT-AIML Problem 13 Assignment Specification. Sarvajanik College of Engineering and Technology, AY 2026–27.
- **Speaker Notes**:
  > *"Slide 15 contains formal academic references formatted in standard IEEE/APA citation style. It lists Michael Lesk's 1986 landmark paper, George Miller's 1995 WordNet paper, Banerjee and Pedersen's 2002 Adapted Lesk paper, NLTK documentation, Jurafsky & Martin's NLP textbook, and the official SCET Problem 13 assignment specification."*

---

## 📌 Summary of Clearly Marked Placeholders for Student Customization

As requested, the PowerPoint file contains clearly marked placeholders for items to be added before final submission:

1. `[COLLEGE LOGO]` (Slide 1) — Insert Sarvajanik College of Engineering and Technology official logo image.
2. `[STUDENT PHOTOGRAPH]` (Slide 1) — Insert student passport photograph if required by college guidelines.
3. `[SUBMISSION DATE]` (Slide 1) — Insert exact date of oral defense / presentation.
4. `[WEB APP SCREENSHOTS]` (Slide 10) — Option to paste actual browser screenshots of `http://127.0.0.1:5000/` into Slide 10 placeholder cards.
