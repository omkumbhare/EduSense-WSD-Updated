# EduSense — Architecture & Methodology Specification

## 1. Problem Definition
Educational transcripts frequently contain domain-specific academic vocabulary with multiple dictionary senses (polysemy). Determining whether "bank" refers to a river bank (Geology) or a financial institution (Economics) requires analyzing the surrounding lexical context against formal dictionary glosses.

---

## 2. System Architecture

```
Educational Lecture Transcript Input
               │
               ▼
   ┌──────────────────────┐
   │ Text Preprocessing   │ ──► Lowercasing, Tokenization, Stopwords, Lemmatization
   └──────────┬───────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Context Extractor    │ ──► Windowing (±10 words around target occurrence)
   └──────────┬───────────┘
              │
              ▼
   ┌──────────────────────┐
   │ WordNet Interface    │ ──► Candidates, Definitions, Examples, Hypernyms
   └──────────┬───────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Thesaurus Expansion  │ ──► Context Word Synonyms via WordNet Lemmas
   └──────────┬───────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Overlap Scoring      │ ──► Weighted Direct, Lemma, Example, Synonym & Hypernym
   └──────────┬───────────┘
              │
              ▼
   ┌──────────────────────┐
   │ Sense Ranking & XAI  │ ──► Rank Candidates, Relative Confidence & Evidence
   └──────────┬───────────┘
              │
              ▼
   Disambiguated Output & UI Display
```

---

## 3. Subsystem Methodology

### A. Preprocessing Module (`src/preprocessing.py`)
- **Lowercasing**: Standardizes case sensitivity.
- **Tokenization**: NLTK `word_tokenize` breaking sentences into lexical units.
- **Stop-word Filtering**: Removes function words (e.g., *the*, *is*, *at*) using NLTK English stopwords.
- **POS Tagging & Lemmatization**: Uses Penn Treebank tags mapped to WordNet POS categories to reduce inflected forms to dictionary base forms.

### B. Context Extractor (`src/context_extractor.py`)
- Extracts a configurable window size $W$ (default $\pm 10$ words) centered at target occurrence $k$.
- Generates HTML `<mark>` tags around target occurrences for visual highlight display.

### C. WordNet & Thesaurus Engine (`src/wordnet_engine.py`)
- Retrieves candidate synsets $S = \{s_1, s_2, \dots, s_n\}$ for target word $w$.
- For each context lemma $c \in C_{\text{lemma}}$, fetches top synonym lemmas from WordNet synsets to form expanded vocabulary $S_{\text{context}}$.

### D. Scoring & Ranking Engine (`src/wsd_engine.py`)
- Computes direct token match, lemma gloss match, example sentence match, synonym match, and hypernym match.
- Normalizes scores and ranks candidate senses in descending order.
