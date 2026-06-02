---
name: pdf-page-extract
description: Extract page ranges from an existing PDF into a new PDF without converting formats. Use when the user wants PDF-to-PDF splitting, page extraction, or a smaller PDF made from specific pages of a source PDF, especially for books, scans, or source documents where the original page images/layout must be preserved.
---

# PDF Page Extract

Use this skill when the task is to keep the original PDF pages intact and only cut out the relevant page range.

Do not use this skill when the user wants OCR, text cleanup, Markdown conversion, image editing, page reflow, or a new designed PDF. Use it only for preserving original PDF pages.

## Workflow

1. Confirm the source PDF path.
2. Determine the exact physical PDF page range to extract.
3. Prefer `qpdf` for the final PDF-to-PDF split.
4. Verify the output with `pdfinfo`.
5. Save the result with a clear name near the working files unless the user requests another location.

## Inputs

Collect:

- source PDF path
- physical PDF page range, or enough content markers to find it
- output PDF path or naming preference
- whether non-contiguous pages are allowed

## Find The Right Pages

- If the user already gives exact PDF page numbers, use them directly.
- If the user gives logical content markers like beyit numbers, story names, or headings, locate the matching physical PDF pages first.
- Prefer fast text-location tools before extracting:
  - `pdftotext source.pdf - | rg 'needle'`
  - `pdftotext -f START -l END source.pdf - | rg 'needle'`
- Narrow the page window iteratively until the start and end pages are clear.
- Distinguish between:
  - Logical/book numbering inside the page image
  - Physical PDF page numbers used by `qpdf`

## Extract Pages

Use `qpdf` for the actual split:

```bash
qpdf --empty --pages /abs/path/source.pdf START-END -- /abs/path/output.pdf
```

Examples:

```bash
qpdf --empty --pages /work/source.pdf 264-275 -- /work/extracted-pages.pdf
qpdf --empty --pages /work/book.pdf 10,12,18-22 -- /work/selected-pages.pdf
```

If the page range is large or uncertain, verify the boundary pages before saving the final file.

## Verify Output

After extraction, run:

```bash
pdfinfo /abs/path/output.pdf
```

Check at least:

- page count matches the intended range
- output file is non-empty
- source page size was preserved

## Script

If repeated extraction is useful, use the bundled helper:

```bash
scripts/extract_pdf_pages.sh /abs/path/source.pdf START-END /abs/path/output.pdf
```

The helper:

- validates arguments
- creates the output directory if needed
- runs `qpdf`
- verifies with `pdfinfo`

## Output Naming

- Prefer descriptive names tied to the content, such as `muaviye-iblis-orijinal-sayfalar.pdf`.
- If the user asks for only the relevant original pages, do not create markdown, docx, or OCR-derived PDFs.
- Keep the output as PDF-to-PDF unless the user explicitly asks for another format.

## Dependencies

Required tools:

- `qpdf`
- `pdfinfo` from Poppler

If either tool is missing, state the missing dependency and do not fabricate an extraction result.
