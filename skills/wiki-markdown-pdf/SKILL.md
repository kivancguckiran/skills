---
name: wiki-markdown-pdf
description: Build styled PDFs from Markdown files in wiki, corpus, lesson, document, and publication-draft projects. Use when the user asks to create, rebuild, export, render, or fix a PDF from Markdown using repository CSS, Pandoc, and a headless browser, or asks to add a reusable Markdown-to-PDF workflow.
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
4. If no script exists, adapt `scripts/build_pdf.sh` into the target repo and add a CSS file under the local output folder or `tools/pdf-style.css`.
5. Verify dependencies before running:
   - `pandoc`
   - Chrome or Chromium, or `CHROME_BIN` pointing to a compatible browser
   - expected CSS file
6. Build only requested files unless the user asks for a full batch.
7. Report output PDF paths and any skipped Markdown files.

## Inputs

Collect:

- Markdown file path or batch pattern
- desired output path, if not beside the source
- style/CSS path, if the repo does not already define one
- browser binary path when the default cannot be detected

## Local Patterns

Read `references/repo-patterns.md` when choosing between repository-local PDF script patterns and the generic wiki behavior.

## Validation

After build:

- confirm each PDF exists and is non-empty
- confirm skipped files were intentionally skipped
- inspect the first page with a PDF/image tool or screenshot when visual quality matters

If `pandoc`, the browser binary, or CSS is missing, report the missing prerequisite instead of inventing a PDF path.
