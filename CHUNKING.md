# Chunking design

Documents are split on **Markdown headers** first. Long sections use a sliding word window (~400 words, 50 overlap).

## Why not fixed-size chunks?

| Fixed-size problem | Header-aware fix |
|--------------------|------------------|
| Splits mid-concept | Keeps one section = one topic |
| Bad citations | Chunk maps to a real doc section |
| Lost context | Section header stored in metadata |

## Metadata per chunk

Each chunk includes: `tool`, `document_title`, `section_header`, `source_url`, `content`.

## Config

Tune in `config/settings.yaml` under `chunking:`.

Implementation: `src/chunking/splitter.py`

## Interview line

> "Naive fixed-length chunking breaks related ideas apart. Header-aware chunking keeps concepts together, which improves retrieval precision because the reranker gets coherent single-topic passages."

More context → [WEEK1_SUMMARY.md](WEEK1_SUMMARY.md)
