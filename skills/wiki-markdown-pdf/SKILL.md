---
name: wiki-markdown-pdf
description: Build styled PDFs from Markdown files in wiki, corpus, lesson, document, and publication-draft projects. Use when the user asks to create, rebuild, export, render, or fix a PDF from Markdown using a simple browser-free ReportLab workflow, repository PDF scripts, or a reusable Markdown-to-PDF workflow.
---

# Wiki Markdown PDF

Use this skill to turn repository Markdown outputs into styled PDFs without rediscovering the local pattern.

Do not use this skill for extracting original PDF pages, editing existing PDFs, or designing a presentation-style document from scratch.

## Workflow

1. Find the nearest repo root and local `AGENTS.md`.
2. Check whether the repo already has a PDF script:
   - `scripts/build_wiki_pdf.sh`
   - `scripts/build_lesson_pdf.sh`
   - `scripts/build_document_pdf.sh`
   - `scripts/build_all_document_pdfs.sh`
3. Prefer the repo script over bundled templates.
4. If no script exists, adapt `scripts/build_pdf.sh` and `scripts/markdown_to_pdf.py` into the target repo. This path uses Python/reportlab directly and does not require Chrome, Pandoc, LaTeX, or CSS.
5. Verify dependencies before running:
   - the Codex bundled Python, or `PYTHON_BIN` pointing to a Python with `reportlab`
   - a readable Markdown file
6. Build only requested files unless the user asks for a full batch.
7. Report output PDF paths and any skipped Markdown files.

## Inputs

Collect:

- Markdown file path or batch pattern
- desired output path, if not beside the source
- `PYTHON_BIN`, only when the bundled Python is unavailable or the project must use a different runtime

## Local Patterns

Read `references/repo-patterns.md` when choosing between repository-local PDF script patterns and the generic wiki behavior.

## Styling Baseline

Use the ReportLab renderer for the default path. It supports:

- A4 page size, margins, and page numbers
- Turkish glyph support through bundled Noto/DejaVu fonts when available
- heading hierarchy, paragraphs, bullet lists, block quotes, fenced code blocks, and pipe tables
- stable table borders, spacing, and code block wrapping

Use a browser/Pandoc/CSS workflow only when the user explicitly needs HTML/CSS fidelity or an existing repo script already provides that workflow.

## Validation

After build:

- confirm each PDF exists and is non-empty
- confirm skipped files were intentionally skipped
- inspect the first page with a PDF/image tool or screenshot when visual quality matters
- inspect one page containing a table, image, long heading, or code block when the source has those elements
- if text is clipped or tables overflow, adjust `scripts/markdown_to_pdf.py` styles and rebuild before reporting completion

If Python or `reportlab` is missing, report the missing prerequisite and the exact `PYTHON_BIN` checked instead of inventing a PDF path.
