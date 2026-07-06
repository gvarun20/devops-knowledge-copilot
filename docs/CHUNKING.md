# Header-aware chunking

Documents are split on Markdown headers first. Long sections are split with a sliding word window (400 words, 50 overlap).

**Why:** fixed-size chunks break related ideas. Header splits keep one topic per chunk and improve citation accuracy.

Each chunk stores: `tool`, `document_title`, `section_header`, `source_url`, `content`.
