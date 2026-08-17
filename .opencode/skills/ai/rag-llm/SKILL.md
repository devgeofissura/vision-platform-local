---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: rag-llm
description: Design and build Retrieval-Augmented Generation (RAG) systems over private documents. Use when building chatbots that answer from your own docs/PDFs/DBs, question-answering over data, knowledge bases, embeddings, vector databases, chunking, retrieval, reranking or evaluating LLM answers grounded in sources.
category: ai
version: 0.1.0
author: devtiagoabreu
tags: [rag, llm, embeddings, vector-database, retrieval, chunking, qa]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.10+ or a JS/TS runtime (Node 18+)
  - An LLM provider API key (OpenAI, Anthropic, Groq, Gemini, DeepSeek...)
  - An embedding model (OpenAI `text-embedding-3`, local `sentence-transformers`, etc.)
  - A vector store (pgvector, Qdrant, Chroma, Pinecone, Weaviate)
provides:
  - End-to-end RAG architecture and pipeline
  - Chunking strategies for different document types
  - Embedding and vector store integration patterns
  - Retrieval, reranking and query strategies
  - Grounded answer generation and hallucination checks
  - Evaluation harness for RAG quality
difficulty: advanced
frameworks: [langchain, llama-index, pgvector, qdrant]
languages: [python, typescript]
---

# RAG / LLM (Retrieval-Augmented Generation)

## Overview

A RAG system answers questions using **your documents** by retrieving relevant
chunks and feeding them to an LLM as context. The quality of the answer is
bounded by the quality of **retrieval** — not by the prompt. Get ingestion,
chunking, and retrieval right before tuning the generation prompt.

## Prerequisites

- Python 3.10+ or a JS/TS runtime (Node 18+)
- An LLM provider API key (OpenAI, Anthropic, Groq, Gemini, DeepSeek...)
- An embedding model (OpenAI `text-embedding-3`, local `sentence-transformers`, etc.)
- A vector store (pgvector, Qdrant, Chroma, Pinecone, Weaviate)

## Architecture

```
Documents → Ingest → Chunks → Embeddings → Vector DB
                                             ↓
User question → (rewrite/expand) → embed → retrieve top-k → rerank
                                             ↓
                    LLM prompt (question + context + sources)
                                             ↓
                       Answer + citations (grounded)
```

## 1. Ingestion Pipeline

Three stages, each with its own failure mode:

| Stage | What it does | Failure mode |
|-------|--------------|--------------|
| Parse | Extract clean text from PDF/DOCX/HTML/MD | Tables, scans, images lost |
| Chunk | Split text into retrievable units | Splits meaning mid-sentence |
| Embed | Convert chunks to vectors | Bad model, wrong dims, no batching |

### Parsing

- PDFs: `pypdf`/`pdfplumber` (text), `marker`/`unstructured` (tables + layout). PDFs that render as images need OCR first (`pytesseract`).
- DOCX: `python-docx`. HTML/Markdown: strip tags/markup, keep headings (they're chunk boundaries).
- Preserve **metadata** per chunk: `source`, `page`, `section`, `updated_at`. It powers citations and filters.

### Chunking strategies

| Strategy | Best for | Notes |
|----------|----------|-------|
| Fixed-size (500–1000 tokens, ~10–20% overlap) | Generic prose | Simplest; can cut meaning |
| By heading/section | Docs, manuals, regulations | Semantic units; recommend |
| Sentence windows (overlap by N sentences) | Q&A style | Keeps context around each sentence |
| Recursive character split (langchain/text-splitter) | Mixed docs | Balances sizes with separators |

**Rules of thumb:**
- Chunk to the size your model "thinks in" — 300–800 tokens is a good default for dense technical docs.
- Overlap 10–20% of the chunk so boundary concepts survive.
- Keep headings attached to the body they introduce (`Header + body` chunking).
- Never chunk inside tables or code blocks if you can avoid it — treat them as atomic units.

## 2. Embeddings

- Store and compare **one embedding model** consistently. Mixing models (e.g. `text-embedding-3-small` vs `bge`) produces garbage similarity scores.
- Normalize embeddings (L2) and use **cosine similarity** or dot product.
- Batch embeddings (e.g. 100–1000 per request) and respect provider rate limits with retry/backoff.
- Large corpora: consider **hybrid search** — combine dense embeddings with lexical (BM25 / full-text) using `Reciprocal Rank Fusion`. Lexical search nails exact terms/IDs/codes that embeddings blur.

## 3. Vector Store

Choose based on stack and scale:

| Store | When to use |
|-------|-------------|
| **pgvector** | Already on Postgres (e.g. Neon, Supabase). Single DB, transactional, joins with app tables. |
| **Qdrant** | Dedicated vector DB, filters + payloads, self-hosted or cloud. |
| **Chroma** | Local prototyping, small corpora, zero infra. |
| **Pinecone/Weaviate** | Managed, large scale, advanced filtering. |

### pgvector example (SQL)

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE doc_chunks (
    id          BIGSERIAL PRIMARY KEY,
    source      TEXT NOT NULL,
    section     TEXT,
    page        INT,
    content     TEXT NOT NULL,
    embedding   vector(1536)
);

CREATE INDEX ON doc_chunks USING hnsw (embedding vector_cosine_ops);
```

```python
import psycopg

rows = [(chunk.content, source, page, emb) for chunk, emb in zip(chunks, embeddings)]
with psycopg.connect(CONN_URI) as conn:
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO doc_chunks (content, source, section, page, embedding) "
            "VALUES (%s, %s, %s, %s, %s)",
            [(c, src, sec, pg, emb) for c, src, sec, pg, emb in rows],
        )
```

### Similarity search

```sql
SELECT content, source, page,
       1 - (embedding <=> %s::vector) AS similarity
FROM doc_chunks
ORDER BY embedding <=> %s::vector
LIMIT 8;
```

Use `<=>` (cosine distance). Filter by metadata *before* ranking when possible (tenant, date range, category) to keep results relevant.

## 4. Retrieval Strategy

- **Query understanding:** rewrite the user question before embedding — expand abbreviations, add context ("last month" → "2026-07"), detect the language of the docs.
- **Multi-query:** generate 3–5 paraphrases, retrieve for each, dedupe. Cheap recall boost.
- **Hybrid + RRF:** merge dense + BM25 ranks.
- **Metadata filters:** pre-filter by source/tenant/date when the domain implies it (e.g. "orders of customer X").
- **Rerank:** a cross-encoder (e.g. `bge-reranker` / `cohere-rerank`) re-scores top ~20 candidates → keeps ~5. Biggest quality lever after good chunking.

## 5. Generation (grounded answers)

Use a prompt that forces source attribution and forbids inventing facts:

```python
SYSTEM_PROMPT = """You are an assistant that answers ONLY from the provided
context. Rules:
1. Answer strictly from the context. If the context lacks the answer, say
   "não encontrado no material" and stop.
2. Cite sources as [1], [2] matching the context items you used.
3. Never invent numbers, names, or procedures."""
```

```python
def answer(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[{i+1}] ({c['source']}, p.{c.get('page', '?')})\n{c['content']}"
        for i, c in enumerate(chunks)
    )
    return llm.chat([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION: {question}"},
    ])
```

**Hallucination guardrails:**
- Require citations; verify each cited chunk actually contains the claim.
- Add a "confidence" or "found in context?" gate for low-recall answers.
- Never put retrieval inside a loop that silently swallows empty results — if top-1 similarity is below a threshold, answer "not found".

## 6. Evaluation (do this from day one)

Keep a small golden set of ~50–100 `(question, expected_chunks, ideal_answer)`.

| Metric | What it measures | How |
|--------|------------------|-----|
| Retrieval Recall@k | Does the right chunk appear? | ground-truth chunk id in top-k |
| Hit rate / MRR | Does the answer get to the right doc | rank of the gold chunk |
| Answer faithfulness | Does the answer stick to context? | LLM-as-judge / NLI |
| Answer relevance | Does it answer the question? | LLM-as-judge |

Track these over every change (chunk size, model, top-k) so improvements are measured, not vibes.

## 7. Production Concerns

- **Security:** never put customer/tenant data in the prompt unless authorized; filter at retrieval, not after generation; log what was retrieved for audit.
- **Cost/latency:** cache repeated questions; embed on write (once), not on every read; cap context size.
- **Freshness:** re-ingest changed documents; keep `updated_at` and rebuild embeddings incrementally.
- **Multi-provider fallback:** route between providers (OpenAI/Anthropic/Groq/Gemini/DeepSeek) with automatic fallback on failure — see the `llm-multi-provider` skill.

## Examples

### Example 1: End-to-end with pgvector (Python)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-small")  # bom para pt-BR

def embed(texts):
    return model.encode(texts, normalize_embeddings=True).tolist()

def ingest(docs):
    for doc in docs:
        chunks = chunk_by_heading(doc)          # seu chunker
        embs = embed([c.content for c in chunks])
        insert_chunks(chunks, embs)             # INSERT no pgvector

def retrieve(question, top_k=8):
    qv = embed([question])[0]
    return pg_search(qv, top_k)
```

### Example 2: n8n/Node.js integration hint

For automation platforms (n8n), expose the retrieval as a small HTTP endpoint
(`POST /search`) so workflows call it instead of embedding logic in the graph.

## Notes

- RAG quality ≈ retrieval quality. Measure Recall@k before blaming the LLM.
- Chunk with the document structure, not against it.
- Keep embeddings and vector DB versioned with the ingestion code.
- For small/technical domains, hybrid search (BM25 + embeddings) usually beats pure dense.

## References

- [pgvector](https://github.com/pgvector/pgvector)
- [Hugging Face Sentence Transformers](https://www.sbert.net/)
- [LangChain](https://python.langchain.com/docs/)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [Reciprocal Rank Fusion (Cornell)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
