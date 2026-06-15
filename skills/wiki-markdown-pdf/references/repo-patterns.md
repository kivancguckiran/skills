# Repo Patterns

## Wiki Or Corpus Project

- General PDF script: `scripts/build_wiki_pdf.sh`
- Lesson/document PDF wrapper: a repo-local wrapper such as `scripts/build_lesson_pdf.sh`
- Default style: `tools/pdf-style.css`
- Local lesson/document style: a folder-local `pdf-style.css` when the repo has one
- Example:
  ```sh
  scripts/build_wiki_pdf.sh -o output.pdf path/to/file.md
  scripts/build_lesson_pdf.sh path/to/lesson-or-document.md
  ```

## Document Collection

- Document script: `scripts/build_document_pdf.sh`
- Batch script: `scripts/build_all_document_pdfs.sh`
- Default style: `documents/pdf-style.css`
- Output path mirrors Markdown path: `documents/name.md` -> `documents/name.pdf`

## Generic Markdown Project

Use the bundled `scripts/build_pdf.sh` pattern:

- Place `scripts/build_pdf.sh` and `scripts/markdown_to_pdf.py` under repo `scripts/`.
- Prefer the browser-free ReportLab renderer for new projects.
- Keep output beside source Markdown by default.

## Common Failures

- `PYTHON_BIN` points to a Python without `reportlab`.
- The Codex bundled Python path differs on another machine; set `PYTHON_BIN` explicitly.
- Running from the wrong repo root.
- Complex Markdown extensions are not supported by the simple renderer. For those files, preprocess to simpler Markdown or use the repo's existing Pandoc workflow.
- Images are not yet rendered by the simple script; use an existing repo workflow if image fidelity is required.
