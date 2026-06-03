# RAG Pipeline Evaluator

> Most people build RAG apps. Almost nobody builds tools to **evaluate** them. This project does exactly that.

A benchmarking dashboard that takes any document, automatically generates a ground truth Q&A dataset, runs it through a RAG pipeline, and scores the pipeline on **Faithfulness** and **Relevancy** — giving you concrete, measurable proof of how well your retrieval system actually works.

---

## The Problem This Solves

Most RAG pipelines are never properly evaluated. Developers build them, test with a few manual questions, and ship. But there is a big difference between a pipeline that *seems* to work and one that *actually* works under measurement.

This tool automates that measurement process end to end.

---

## Live Demo

Upload any `.txt` or `.pdf` document, hit **Run Evaluation**, and get a full report in under 2 minutes.

---

## How It Works

```
User uploads document
        │
        ▼
┌─────────────────────────┐
│   Document Chunking     │  ← SentenceSplitter (chunk_size=512)
│   + Embedding           │  ← BAAI/bge-small-en-v1.5 (local, free)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   ChromaDB Vector Store │  ← Stores embedded chunks in memory
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Dataset Generator     │  ← Auto-generates Q&A pairs from chunks
│   (Ground Truth)        │     using Groq LLaMA 3.3 70B
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Evaluation Engine     │  ← Runs each question through pipeline
│                         │     Scores on Faithfulness + Relevancy
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Dashboard Report      │  ← Visual scores + per-question breakdown
└─────────────────────────┘
```

---

## Metrics Explained

| Metric | What It Measures |
|---|---|
| **Faithfulness** | Is the answer grounded in the retrieved context, or is the model hallucinating? |
| **Relevancy** | Does the answer actually address the question that was asked? |
| **Overall Score** | Average of Faithfulness and Relevancy |

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq API (LLaMA 3.3 70B Versatile) — free tier |
| Embeddings | HuggingFace `BAAI/bge-small-en-v1.5` — runs locally, no API needed |
| Vector Store | ChromaDB — in-memory, no setup required |
| RAG Framework | LlamaIndex |
| Evaluation | LlamaIndex `FaithfulnessEvaluator` + `RelevancyEvaluator` |
| Dashboard | Streamlit with custom CSS |

---

## Project Structure

```
rag-evaluator/
│
├── app/
│   ├── __init__.py
│   ├── config.py             # API key loading
│   ├── pipeline.py           # RAG pipeline (chunking, embedding, indexing)
│   ├── dataset_generator.py  # Auto Q&A generation from documents
│   ├── evaluator.py          # Faithfulness + Relevancy scoring
│   └── report.py             # Score aggregation and report formatting
│
├── data/
│   └── sample_docs/          # Default sample documents
│
├── notebooks/                # Experimentation notebooks
├── main.py                   # Streamlit dashboard entry point
├── .env.example              # Environment variable template
├── requirements.txt          # Python dependencies
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Pandey002/rag-evaluator.git
cd rag-evaluator
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Run the app

```bash
streamlit run main.py
```

Open `http://localhost:8501` in your browser.

---

## Usage

1. Upload a `.txt` or `.pdf` document using the upload widget
2. Click **Run Evaluation**
3. Wait 1 to 2 minutes while the pipeline:
   - Chunks and embeds your document
   - Generates questions automatically
   - Evaluates each question for faithfulness and relevancy
4. View your scores and per-question breakdown

---

## Sample Output

```json
{
  "total_questions": 8,
  "faithfulness_score": "100.0%",
  "relevancy_score": "100.0%",
  "overall_score": "100.0%"
}
```

---

## Key Design Decisions

**Why local embeddings?**
Using `BAAI/bge-small-en-v1.5` via HuggingFace instead of a paid embedding API means zero cost and zero rate limits for the embedding step. Only LLM calls go to Groq.

**Why auto-generate the dataset?**
Most evaluation tools require you to manually write test questions. This tool generates them automatically from the document itself using an LLM, making evaluation possible without any manual effort.

**Why ChromaDB EphemeralClient?**
For a benchmarking tool, persistent storage is not needed. Every evaluation run starts fresh which ensures clean, unbiased results.

---

## What I Learned Building This

- The difference between a RAG pipeline that *works* and one that *works well* comes down to evaluation
- Chunk size has a huge impact on retrieval quality
- Faithfulness and relevancy are two completely different failure modes — a pipeline can be relevant but hallucinate, or be faithful but answer the wrong question
- Building evaluation infrastructure is harder and more valuable than building the RAG app itself

---

## Roadmap

- [ ] Add Hit Rate and MRR metrics
- [ ] Compare two pipeline configurations side by side
- [ ] Export report as PDF or JSON
- [ ] Add latency tracking per query
- [ ] Support for more document types (DOCX, CSV)

---

## Part of Advanced RAG Portfolio

This project is one of three built as part of an Advanced RAG portfolio, directly applying concepts from the **Activeloop Advanced RAG certification**.

Other projects in the series:
- Financial Report Comparator
- RAG Powered Code Review Assistant

---
