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

- Place script under repo `scripts/`.
- Place CSS at `tools/pdf-style.css` unless a more local output style already exists.
- Keep output beside source Markdown by default.

## Common Failures

- Chrome missing or not executable.
- `pandoc` missing.
- CSS path wrong after moving the script.
- Running from the wrong repo root.
