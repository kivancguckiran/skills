#!/bin/bash
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 /abs/path/source.pdf START-END /abs/path/output.pdf" >&2
  exit 1
fi

SOURCE_PDF="$1"
PAGE_RANGE="$2"
OUTPUT_PDF="$3"

if [ ! -f "$SOURCE_PDF" ]; then
  echo "Source PDF not found: $SOURCE_PDF" >&2
  exit 1
fi

if ! command -v qpdf >/dev/null 2>&1; then
  echo "qpdf is required but not installed." >&2
  exit 1
fi

if ! command -v pdfinfo >/dev/null 2>&1; then
  echo "pdfinfo is required but not installed." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT_PDF")"

qpdf --empty --pages "$SOURCE_PDF" "$PAGE_RANGE" -- "$OUTPUT_PDF"
pdfinfo "$OUTPUT_PDF"
