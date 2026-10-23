# EduSense — Dictionary and Thesaurus-Based Word Sense Disambiguation for Educational Transcripts

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![NLTK](https://img.shields.io/badge/NLTK-WordNet-green)
![Flask](https://img.shields.io/badge/Flask-Web_App-black)
![License](https://img.shields.io/badge/Academic-MT--AIML_Problem_13-purple)

---

## 📌 Problem Overview & Objective

Educational lecture audio transcripts contain polysemous academic vocabulary (e.g. *bank*, *plant*, *cell*, *memory*, *power*, *tree*). The same word carries fundamentally different meanings across subjects like Geology, Economics, Biology, Physics, and Computer Science.

**EduSense** is a transparent, explainable Natural Language Processing (NLP) system built for **MT-AIML Problem 13**. It disambiguates target words in lecture transcripts using **NLTK WordNet**, context gloss overlap, example sentence matching, and thesaurus synonym expansion—**without relying on external LLM APIs**.

---

## 🚀 Key Features

1. **Pure Algorithmic WSD Engine**:
   - Implements multi-factor weighted gloss-context overlap.
   - Evaluates direct exact token overlap, lemma overlap, example sentence overlap, thesaurus synonym expansion, and hypernym domain hierarchy.
   - Strictly excludes black-box LLM APIs to demonstrate core NLP principles.

2. **Transparent Text Preprocessing Pipeline**:
   - Lowercasing, tokenization, stop-word removal, POS tagging, and NLTK `WordNetLemmatizer`.
   - Real-time step-by-step pipeline view in web interface.

3. **Configurable Context Windowing**:
   - Allows users to dynamically set context window size ($\pm 5$ to $\pm 25$ words).
   - Handles target word occurrences and highlights target words in extracted context excerpts.

4. **Explainable AI (XAI) & Relative Confidence**:
   - Displays exact matched evidence tokens (direct words, lemma gloss words, example words, synonym matches).
   - Calculates transparent relative confidence scores.

5. **Empirical Benchmark & Baseline Comparison**:
   - Includes a 25-sample labeled educational dataset (`data/annotated/evaluation_dataset.csv`).
   - Evaluates custom engine against NLTK's built-in Simplified Lesk baseline.
   - Interactive Chart.js charts for accuracy and prediction status breakdowns.

---

## 📐 Mathematical Formulation

For a target word $w$ with surrounding context $C$, and candidate synset $s$ with gloss definition $G_s$, examples $E_s$, and thesaurus synonyms $S_{\text{context}}$:

$$\text{Final Score}(s) = \alpha \cdot \text{DirectOverlap}(C, G_s) + \beta \cdot \text{LemmaOverlap}(C_{\text{lemma}}, G_{s,\text{lemma}}) + \gamma \cdot \text{ExampleOverlap}(C_{\text{lemma}}, E_{s,\text{lemma}}) + \delta \cdot \text{ThesaurusOverlap}(S_{\text{context}}, G_{s,\text{lemma}}) + \epsilon \cdot \text{HypernymOverlap}(C_{\text{lemma}}, H_s)$$

Default Weights: $\alpha=1.5, \beta=1.2, \gamma=1.0, \delta=0.7, \epsilon=0.5$.

$$\text{Relative Confidence} = \frac{\text{Top Candidate Score}}{\sum_{s \in \text{Candidates}} \text{Score}(s)}$$

---

## 🛠️ Required Deliverable Structure

EduSense strictly satisfies the academic deliverable structure specified in the MT-AIML Mini Project guidelines:

```
project-folder/
├── docs/
│   ├── Architecture_and_Methodology.pdf  # Theoretical concepts, mathematical formulas, and design
│   ├── Architecture_and_Methodology.md
│   ├── Evaluation_Report.pdf             # Empirical results, metric tables, charts, failure analysis
│   ├── Evaluation_Report.md
│   └── Final_Presentation_Outline_and_Speaker_Notes.md
│
├── src/
│   ├── preprocessing.py                  # Sentence segmentation, Tokenization, Lemmatization, Stopwords
│   ├── models.py                         # POS tagger + DictionaryThesaurusWSD (single source of truth for the algorithm)
│   ├── pipeline.py                       # Execution pipeline / evaluation runner
│   ├── context_extractor.py              # Configurable context windowing (±5 to ±25 words)
│   ├── wordnet_engine.py                 # NLTK WordNet synset querying & thesaurus expansion
│   ├── wsd_engine.py                     # Thin functional wrapper over models.py (used by Flask app/tests)
│   ├── baseline.py                       # NLTK Simplified Lesk baseline model
│   └── utils.py                          # Offline NLTK resource downloader & safety validator
│
├── data/
│   ├── raw_transcripts/                  # Sample speech-to-text educational inputs across domains
│   │   ├── lecture_geology_river_bank.txt
│   │   ├── lecture_economics_banking.txt
│   │   ├── lecture_biology_cell_nucleus.txt
│   │   └── lecture_cs_memory_stack.txt
│   └── annotated/                        # Gold standard benchmark datasets
│       └── evaluation_dataset.csv        # 25 Validated educational test sentences across 18 words
│
├── templates/                            # Web Interface HTML Templates (Bootstrap 5)
│   ├── base.html                         # Master layout with navigation
│   ├── index.html                        # Dashboard with dynamic metric cards
│   ├── analyzer.html                     # Interactive WSD Analyzer with slider & sample presets
│   ├── results.html                      # Disambiguation output, XAI evidence badges, and rankings
│   ├── evaluation.html                   # Benchmark comparison dashboard with Chart.js
│   └── about.html                        # Methodology, architecture & viva examination guide
│
├── static/                               # Static Web Assets (CSS/JS)
│   ├── css/style.css                     # Dark glassmorphism academic theme
│   └── js/app.js                         # Dynamic slider sync & sample loaders
│
├── tests/                                # 18 Unit Tests (pytest / unittest)
│   ├── test_app.py                       # Flask route & REST API integration tests
│   ├── test_context.py                   # Context extraction & windowing tests
│   ├── test_evaluation.py                # Benchmark evaluation suite tests
│   ├── test_preprocessing.py             # Preprocessing & lemmatization tests
│   └── test_wsd.py                       # Disambiguation & ranking logic tests
│
├── Problem_13_MT_AIML_WSD_Om_Kumbhare.pptx # 16-Slide Final PowerPoint Presentation
├── build_ppt.py                          # Presentation generator script
├── build_pdfs.py                         # PDF document compiler (ReportLab)
├── render.yaml                           # Render Cloud Blueprint Specification
├── Procfile                              # Production Gunicorn process runner for Render
├── requirements.txt                      # Dependencies (nltk, flask, gunicorn, scikit-learn, etc.)
└── README.md                             # Execution instructions and project overview
```

---

## ☁️ Deploying to Render (Cloud Hosting)

The application is 100% prepared for instant, free deployment on [Render](https://render.com):

### Option A: Via GitHub Repository (Recommended)
1. Push this local Git repository to your GitHub account:
   ```bash
   git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
   git branch -M main
   git push -u origin main
   ```
2. Log in to [dashboard.render.com](https://dashboard.render.com).
3. Click **New +** $\rightarrow$ **Web Service** $\rightarrow$ Select your GitHub repository.
4. Render will automatically detect `render.yaml` and `Procfile`.
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt && python -c "from src.utils import ensure_nltk_resources; ensure_nltk_resources()"`
   - **Start Command**: `gunicorn app:app`
5. Click **Create Web Service**. Your app will deploy to a permanent public URL (e.g. `https://edusense-wsd.onrender.com`) that you can present from any mobile phone, tablet, or laptop!

---

## 💻 Installation & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify & Download NLTK Corpora
```bash
python -c "from src.utils import ensure_nltk_resources; ensure_nltk_resources()"
```

### 3. Run Unit Tests
```bash
python -m pytest tests/
```

### 4. Run the Pipeline (benchmark + raw transcript demo)
```bash
python -m src.pipeline
```

### 5. Launch Flask Web Application
```bash
python app.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 📊 Empirical Evaluation Benchmark Results

Evaluated on `data/annotated/evaluation_dataset.csv` (25 Educational Transcripts):

| Method / Metric | Custom EduSense WSD | NLTK Simplified Lesk Baseline |
| :--- | :---: | :---: |
| **Accuracy (%)** | **56.0%** | 40.0% |
| **Correct Predictions** | **14 / 25** | 10 / 25 |
| **Macro Precision / Recall / F1** | 40.3 / 45.2 / 41.9 | N/A |
| **Avg Senses / Word** | 6.2 | 6.2 |
| **Avg Relative Confidence** | 42.1% | N/A |
| **Domain Scope** | Multi-subject (Science, CS, Finance, Physics) | General |

*Note: EduSense outperforms the Lesk baseline by +16.0% due to thesaurus synonym expansion, POS filtering, and hypernym hierarchy matching.*

---

## 🎓 Viva Q&A Summary

- **Q: Why avoid LLM APIs?**
  *A: Academic mini-projects must evaluate fundamental NLP concepts (lexical semantics, vector overlap, gloss matching). Black-box LLMs conceal algorithm mechanics.*
- **Q: What is the main innovation over Lesk?**
  *A: Context synonym expansion via WordNet thesaurus sets, target self-match exclusion, POS-guided candidate filtering, and hypernym domain hierarchy scoring.*

---

## 📜 References

1. Lesk, M. (1986). *Automatic sense disambiguation using machine readable dictionaries: how to tell a pine cone from an ice cream cone*. ACM SIGDOC.
2. Miller, G. A. (1995). *WordNet: a lexical database for English*. Communications of the ACM.
3. Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing (3rd ed. draft)*.
