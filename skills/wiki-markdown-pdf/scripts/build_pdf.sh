#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STYLE="${PDF_STYLE:-$ROOT_DIR/tools/pdf-style.css}"
CHROME="${CHROME_BIN:-}"

usage() {
  echo "Usage: scripts/build_pdf.sh [-o output.pdf] [-s style.css] file.md [file2.md ...]" >&2
}

out_override=""
while getopts ":o:s:h" opt; do
  case "$opt" in
    o) out_override="$OPTARG" ;;
    s) STYLE="$OPTARG" ;;
    h) usage; exit 0 ;;
    :) echo "Missing argument: -$OPTARG" >&2; usage; exit 2 ;;
    \?) echo "Unknown option: -$OPTARG" >&2; usage; exit 2 ;;
  esac
done
shift $((OPTIND - 1))

if [[ "$#" -lt 1 ]]; then usage; exit 2; fi
if [[ -n "$out_override" && "$#" -ne 1 ]]; then
  echo "-o can only be used with one Markdown file." >&2
  exit 2
fi
command -v pandoc >/dev/null 2>&1 || { echo "pandoc not found." >&2; exit 1; }
if [[ -z "$CHROME" ]]; then
  if command -v google-chrome >/dev/null 2>&1; then
    CHROME="$(command -v google-chrome)"
  elif command -v chromium >/dev/null 2>&1; then
    CHROME="$(command -v chromium)"
  elif [[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
    CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  fi
fi
[[ -n "$CHROME" && -x "$CHROME" ]] || { echo "Chrome/Chromium not found. Set CHROME_BIN." >&2; exit 1; }
[[ -f "$STYLE" ]] || { echo "PDF style not found: $STYLE" >&2; exit 1; }

cd "$ROOT_DIR"
for md in "$@"; do
  [[ -f "$md" ]] || { echo "Skipped, missing file: $md" >&2; continue; }
  [[ "$md" == *.md ]] || { echo "Skipped, not Markdown: $md" >&2; continue; }
  out="${out_override:-${md%.md}.pdf}"
  html_base="$(mktemp "${TMPDIR:-/tmp}/wiki-pdf.XXXXXX")"
  html="${html_base}.html"
  pandoc "$md" -s --embed-resources --css="$STYLE" -o "$html"
  "$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
    --print-to-pdf="$ROOT_DIR/$out" "file://$html" >/dev/null
  rm -f "$html"
  echo "PDF written: $out"
done
