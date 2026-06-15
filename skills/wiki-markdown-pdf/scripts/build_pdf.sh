#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-}"

usage() {
  echo "Usage: scripts/build_pdf.sh [-o output.pdf] file.md [file2.md ...]" >&2
  echo "Builds styled PDFs directly with Python/reportlab; no Chrome is required." >&2
}

if [[ -z "$PYTHON_BIN" ]]; then
  for candidate in \
    "/Users/kivancguckiran/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" \
    python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      PYTHON_BIN="$(command -v "$candidate")"
      break
    elif [[ -x "$candidate" ]]; then
      PYTHON_BIN="$candidate"
      break
    fi
  done
fi

[[ -n "$PYTHON_BIN" ]] || { echo "python3 not found. Set PYTHON_BIN." >&2; exit 1; }
"$PYTHON_BIN" -c "import reportlab" >/dev/null 2>&1 || {
  echo "Python package not found: reportlab. Use the Codex bundled Python or install reportlab." >&2
  echo "Current PYTHON_BIN: $PYTHON_BIN" >&2
  exit 1
}

out_override=""
while getopts ":o:s:h" opt; do
  case "$opt" in
    o) out_override="$OPTARG" ;;
    s) echo "Warning: -s is ignored by the browser-free ReportLab renderer." >&2 ;;
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

cd "$ROOT_DIR"
if [[ -n "$out_override" ]]; then
  "$PYTHON_BIN" "$ROOT_DIR/scripts/markdown_to_pdf.py" -o "$out_override" "$@"
else
  "$PYTHON_BIN" "$ROOT_DIR/scripts/markdown_to_pdf.py" "$@"
fi
