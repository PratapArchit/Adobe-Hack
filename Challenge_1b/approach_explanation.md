# Approach Explanation for Round 1B Solution

## **Objective**
The task is to extract contextually relevant sections and subsections from multiple PDFs based on a given persona and a "job-to-be-done" statement, then produce a structured JSON output containing:
- Metadata
- Ranked extracted sections
- Refined subsection summaries

The solution must work offline, be lightweight, and run efficiently under hackathon constraints.

---

## **Methodology**

### **1. Input Understanding**
The input JSON provides:
- A persona (role)
- A job-to-be-done description
- A set of documents (PDFs)

From this, we extract **actions**, **keywords**, and **boost terms** using **NLTK**:
- **Actions**: Verbs and verb phrases (e.g., "prepare menu")
- **Keywords**: Nouns and adjectives (e.g., "vegetarian", "gluten-free")
- **Boost Terms**: Combined list to enhance scoring
We also infer **avoid terms** using WordNet antonyms (e.g., "vegetarian" → avoid "meat").

---

### **2. PDF Parsing**
We use **PyMuPDF** for reliable text extraction. Sections and subsections are identified using a heuristic:
- Headings ≤ 12 words, not full sentences, uppercase or capitalized
- Context-aware title generation:
  - If the heading is generic (e.g., "Introduction"), attach the parent heading or key keywords for clarity
- Subsections are smaller content blocks under these sections

---

### **3. Context-Aware Ranking**
For each section and subsection:
- Compute embeddings using **SentenceTransformers (MiniLM)** (downloaded offline)
- Rank using:
  - **Semantic similarity** to extracted query embeddings
  - **Direct relevance** to the full job text
  - **Title relevance** and **keyword match score**
  - Penalty for **avoid terms**

Scoring Formula:
final_score = 0.3 * query_sim + 0.3 * job_sim + 0.2 * title_relevance + 0.2 * keyword_match - penalty


---

### **4. Summarization**
For subsections, we generate concise summaries:
- Normalize text (remove ligatures, bullets, symbols)
- Select top 2–3 sentences based on boost term overlap

---

### **5. Output Structure**
The final JSON includes:
- **Metadata**: persona, job, documents
- **Extracted Sections**: ranked by importance
- **Subsection Analysis**: refined summaries with context

---

## **Why This Approach?**
- **Lightweight**: NLTK + SentenceTransformers (MiniLM) < 200MB
- **Offline**: Models and resources pre-downloaded
- **Universal**: No hardcoding for domain-specific terms
- **Context-Aware**: Combines persona, job intent, and content semantics

---
