---
name: rag-system-design
description: Design a RAG system end-to-end (ingestion, chunking, embeddings, retrieval, generation, evaluation)
category: ai
version: 0.1.0
author: devtiagoabreu
tags: [rag, llm, embeddings, vector-database, retrieval, system-design]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: documents
    description: Document types and volume (PDFs, DOCX, HTML, DB rows, scale)
  - name: use_case
    description: Question-answering, chatbot, support copilot, internal search
  - name: stack
    description: Preferred stack (Python/TS, pgvector/Qdrant, providers)
---

# RAG System Design

## Objective

Produce a concrete, buildable RAG architecture for the given documents and
use case — covering ingestion, chunking, retrieval, generation, and
evaluation — before any code is written.

## Instructions

### Context

You are a senior AI engineer. Design for the actual constraints: document
types, scale, languages (pt-BR support matters for embeddings), latency, and
cost. Retrieval quality is the priority.

### Task

1. Clarify document types, volume, update frequency, and language mix
2. Recommend chunking strategy per document type (with rationale)
3. Recommend an embedding model and vector store (fit to the stack)
4. Define the retrieval strategy (hybrid search, reranking, filters)
5. Define the generation prompt with citations and no-invention rules
6. Define an evaluation plan (golden set, Recall@k, faithfulness)
7. List the build order (milestones) and risks

### Criteria

1. **Fit:** choices match the stack and scale stated
2. **Measurable:** evaluation plan exists from day one
3. **Safe:** answers are grounded and attributed
4. **Buildable:** clear milestones, each independently testable

## Usage Example

```
Design a RAG system for the following:

Documents: {{documents}}
Use case: {{use_case}}
Stack: {{stack}}

Please provide:
1. Recommended chunking strategy and embedding model
2. Vector store choice with rationale
3. Retrieval strategy (hybrid? rerank? metadata filters?)
4. Generation prompt that enforces grounding and citations
5. Evaluation plan with concrete metrics
6. Ordered build milestones
```

## Variations

### Variation 1: Chatbot over PDFs (pt-BR)

```
Design a RAG for a support chatbot answering from ~500 PDF manuals in pt-BR,
served through WhatsApp (Evolution API) and a web widget. Prioritize:
- multilingual-capable embeddings for pt-BR
- chunking that preserves table structure
- fast retrieval (P99 < 800ms)
- a way to audit which source answered
```

### Variation 2: Hybrid search tradeoffs

```
Compare dense-only vs hybrid (BM25 + embeddings + RRF) retrieval for a
technical product catalog with exact product codes. When is lexical search
better than semantic, and how should we fuse and rerank?
```

## References

- [RAG skill](../skills/ai/rag-llm/SKILL.md)
- [pgvector](https://github.com/pgvector/pgvector)
- [LlamaIndex](https://docs.llamaindex.ai/)
