---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: doc-to-markdown
description: Convert PDF, Office, image, audio and web documents into clean Markdown for LLM pipelines using Microsoft MarkItDown
category: documentation
version: 0.1.0
author: devtiagoabreu
tags: [markdown, conversion, documentation, llm, markitdown, pdf, office]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.9+ and pip
  - markitdown package (pip install markitdown)
provides:
  - Markdown conversion from PDF, DOCX, PPTX, XLSX, images, audio and web pages
  - Token-efficient Markdown optimized for LLM consumption
---

# Doc to Markdown (MarkItDown)

## Overview

This skill converts unstructured documents into clean, token-efficient Markdown
that is ready to feed into LLM pipelines. It uses
[Microsoft MarkItDown](https://github.com/microsoft/markitdown), the universal
document converter behind GitHub Copilot and Azure AI Foundry. MarkItDown
prioritizes document structure (headings, lists, tables, links) over visual
fidelity, producing Markdown that LLMs naturally understand with minimal token
waste.

Use this skill whenever you need to bring content from PDFs, Word, PowerPoint,
Excel, images (via OCR), audio (via speech-to-text) or web pages into a
conversation with an AI assistant.

## Prerequisites

- Python 3.9 or higher with pip
- Internet access on first install of the package
- Optional extras for specific formats (see [Installing format extras](#4-installing-format-extras))

## Usage Instructions

### 1. Installing MarkItDown

```bash
pip install markitdown
```

Verify the install:

```bash
markitdown --help
```

### 2. Converting a document to Markdown

The CLI converts any supported file to Markdown on stdout:

```bash
# PDF
markitdown path/to/report.pdf > report.md

# Word document
markitdown path/to/proposal.docx > proposal.md

# PowerPoint
markitdown path/to/slides.pptx > slides.md

# Excel spreadsheet
markitdown path/to/data.xlsx > data.md

# HTML page
markitdown https://example.com/page.html > page.md

# Image (OCR)
markitdown path/to/scan.png > scan.md
```

### 3. Using the Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("path/to/document.pdf")
print(result.text_content)
```

### 4. Installing format extras

MarkItDown uses optional dependencies per format. Install only what you need:

```bash
pip install 'markitdown[all]'     # everything
pip install 'markitdown[pdf]'     # PDF only
pip install 'markitdown[docx]'    # Word only
pip install 'markitdown[pptx]'    # PowerPoint only
pip install 'markitdown[xlsx]'    # Excel only
pip install 'markitdown[outlook]' # Outlook messages
pip install 'markitdown[az-doc-intel]'  # Azure Document Intelligence
```

### 5. Best practices for LLM consumption

- Convert only the sections that matter; the result is meant to be read by an
  LLM, not rendered by a browser.
- For scanned PDFs/images, prefer OCR-capable paths (Azure Document
  Intelligence) when accuracy matters.
- Review the output for table and heading fidelity before sending to the model.
- Store the converted `.md` files next to the originals so the conversion is
  done once and reused across sessions (saves tokens).

## Examples

### Example 1: Convert a research paper to Markdown

```bash
pip install 'markitdown[pdf]'
markitdown ~/Downloads/paper.pdf > ~/Downloads/paper.md
head -50 ~/Downloads/paper.md
```

### Example 2: Batch-convert an Office folder

```bash
mkdir -p ./md
for file in ./docs/*.docx; do
  name=$(basename "$file" .docx)
  markitdown "$file" > "./md/$name.md"
done
```

### Example 3: Convert a web page for a quick summary

```bash
markitdown https://opencode.ai/docs > opencode-docs.md
```

## References

- [MarkItDown repository](https://github.com/microsoft/markitdown)
- [MarkItDown PyPI](https://pypi.org/project/markitdown/)

## Notes

- MarkItDown is a general conversion tool; format-specific accuracy varies.
- The Azure Document Intelligence extension adds OCR and layout analysis for
  scanned documents (requires an Azure endpoint).
- Do not feed documents containing secrets into a conversion without reviewing
  the output first.
