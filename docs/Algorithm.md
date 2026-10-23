# EduSense — Algorithm & Mathematical Formulations

## 1. Algorithm Overview
EduSense implements a modified Lesk algorithm enhanced with dictionary lemmatization, example sentence token overlap, thesaurus synonym expansion, and hypernym domain hierarchy scoring.

---

## 2. Mathematical Equations

### A. Context Extraction Window
Given transcript tokens $T = [t_1, t_2, \dots, t_N]$ and target word index $k$:
$$C = [t_{\max(1, k-W)}, \dots, t_{k-1}, t_{k+1}, \dots, t_{\min(N, k+W)}]$$

### B. Preprocessed Sets
- Transcript Context Tokens: $C_{\text{tok}}$
- Transcript Context Lemmas (excluding target word $w$): $C_{\text{lem}}$
- Candidate Gloss Tokens for sense $s$: $G_{s,\text{tok}}$
- Candidate Gloss Lemmas for sense $s$: $G_{s,\text{lem}}$
- Candidate Example Sentence Lemmas for sense $s$: $E_{s,\text{lem}}$
- Context Synonym Expansion: $S_{\text{context}} = \bigcup_{c \in C_{\text{lem}}} \text{Synonyms}(c)$
- Candidate Hypernym/Hyponym Tokens for sense $s$: $H_{s,\text{tok}}$

### C. Multi-Factor Overlap Scores
1. Direct Exact Token Match:
   $$\text{Score}_{\text{direct}}(s) = |C_{\text{tok}} \cap G_{s,\text{tok}}|$$

2. Lemma Gloss Match:
   $$\text{Score}_{\text{lemma}}(s) = |C_{\text{lem}} \cap G_{s,\text{lem}}|$$

3. Example Sentence Match:
   $$\text{Score}_{\text{example}}(s) = |C_{\text{lem}} \cap E_{s,\text{lem}}|$$

4. Thesaurus Synonym Match:
   $$\text{Score}_{\text{synonym}}(s) = |(S_{\text{context}} \setminus \{w\}) \cap G_{s,\text{lem}}|$$

5. Hypernym Hierarchy Match:
   $$\text{Score}_{\text{hyper}}(s) = |C_{\text{lem}} \cap H_{s,\text{tok}}|$$

### D. Final Weighted Score Formulation
$$\text{Final Score}(s) = \alpha \cdot \text{Score}_{\text{direct}}(s) + \beta \cdot \text{Score}_{\text{lemma}}(s) + \gamma \cdot \text{Score}_{\text{example}}(s) + \delta \cdot \text{Score}_{\text{synonym}}(s) + \epsilon \cdot \text{Score}_{\text{hyper}}(s)$$

Default Weight Parameters:
- $\alpha = 1.5$
- $\beta = 1.2$
- $\gamma = 1.0$
- $\delta = 0.7$
- $\epsilon = 0.5$

### E. Relative Confidence
$$\text{Relative Confidence}(s^*) = \frac{\text{Final Score}(s^*)}{\sum_{s \in \text{Synsets}(w)} \text{Final Score}(s)}$$
where $s^* = \arg\max_{s} \text{Final Score}(s)$.

---

## 3. Pseudocode

```python
function DisambiguateWord(transcript, target_word, window_size=10):
    tokens = Tokenize(Normalize(transcript))
    target_indices = FindOccurrences(tokens, target_word)
    context_tokens = ExtractWindow(tokens, target_indices[0], window_size)
    context_prep = Preprocess(context_tokens, preserve=target_word)
    
    inferred_pos = InferPOS(context_tokens, target_word)
    candidate_synsets = GetWordNetSynsets(target_word, pos=inferred_pos)
    
    context_synonyms = GetSynonymExpansions(context_prep.unique_lemmas)
    
    scored_candidates = []
    for synset in candidate_synsets:
        details = ExtractSynsetDetails(synset)
        scores = ComputeOverlapScores(context_prep, details, context_synonyms, weights)
        scored_candidates.append((synset, scores))
        
    SortDescendingByScore(scored_candidates)
    top_sense = scored_candidates[0]
    confidence = ComputeRelativeConfidence(scored_candidates)
    
    return PredictedSense(top_sense, confidence, BuildExplanation(top_sense))
```
