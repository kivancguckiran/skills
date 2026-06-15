#!/usr/bin/env python3
import argparse
import os
import re
import sys
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


FONT_CANDIDATES = [
    os.environ.get("PDF_FONT"),
    "/Users/kivancguckiran/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype/NotoSans-Regular.ttf",
    "/Users/kivancguckiran/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/fonts/DejaVuSans.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]

BOLD_FONT_CANDIDATES = [
    os.environ.get("PDF_BOLD_FONT"),
    "/Users/kivancguckiran/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype/NotoSans-Bold.ttf",
]


def register_font(name, candidates, fallback):
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            pdfmetrics.registerFont(TTFont(name, candidate))
            return name
    return fallback


BODY_FONT = register_font("DocBody", FONT_CANDIDATES, "Helvetica")
BOLD_FONT = register_font("DocBold", BOLD_FONT_CANDIDATES, BODY_FONT)
MONO_FONT = "Courier"


def inline_markup(text):
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier" backColor="#eef2f7">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", rf'<font name="{BOLD_FONT}">\1</font>', text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return text


def make_styles():
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName=BODY_FONT,
            fontSize=10.6,
            leading=16,
            textColor=colors.HexColor("#1f2933"),
            spaceAfter=7,
            alignment=TA_LEFT,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName=BOLD_FONT,
            fontSize=22,
            leading=27,
            textColor=colors.HexColor("#111827"),
            spaceBefore=0,
            spaceAfter=14,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName=BOLD_FONT,
            fontSize=15.5,
            leading=20,
            textColor=colors.HexColor("#111827"),
            spaceBefore=12,
            spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName=BOLD_FONT,
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#111827"),
            spaceBefore=10,
            spaceAfter=6,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName=MONO_FONT,
            fontSize=8.8,
            leading=12,
            textColor=colors.HexColor("#102a43"),
            backColor=colors.HexColor("#f6f8fb"),
            borderColor=colors.HexColor("#d8dee8"),
            borderWidth=0.6,
            borderPadding=7,
            spaceAfter=9,
        ),
        "quote": ParagraphStyle(
            "quote",
            parent=base["BodyText"],
            fontName=BODY_FONT,
            fontSize=10,
            leading=15,
            leftIndent=10,
            borderColor=colors.HexColor("#9aa8b8"),
            borderWidth=0,
            borderPadding=7,
            backColor=colors.HexColor("#f5f7fa"),
            textColor=colors.HexColor("#394b59"),
            spaceAfter=8,
        ),
    }


def flush_paragraph(story, parts, styles):
    if parts:
        story.append(Paragraph(inline_markup(" ".join(parts).strip()), styles["body"]))
        parts.clear()


def parse_table(lines, start):
    rows = []
    i = start
    while i < len(lines) and "|" in lines[i]:
        raw = lines[i].strip()
        if raw.startswith("|"):
            raw = raw[1:]
        if raw.endswith("|"):
            raw = raw[:-1]
        cells = [cell.strip() for cell in raw.split("|")]
        rows.append(cells)
        i += 1
    if len(rows) >= 2 and all(re.fullmatch(r":?-{3,}:?", c or "") for c in rows[1]):
        return rows[:1] + rows[2:], i
    return None, start


def add_table(story, rows, styles):
    data = [[Paragraph(inline_markup(cell), styles["body"]) for cell in row] for row in rows]
    table = Table(data, hAlign="LEFT", repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf2f7")),
                ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8dee8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(KeepTogether([table, Spacer(1, 8)]))


def build_story(markdown, styles):
    lines = markdown.splitlines()
    story = []
    para = []
    list_items = []
    i = 0

    def flush_list():
        if list_items:
            story.append(
                ListFlowable(
                    [ListItem(Paragraph(inline_markup(item), styles["body"])) for item in list_items],
                    bulletType="bullet",
                    leftIndent=16,
                )
            )
            story.append(Spacer(1, 4))
            list_items.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph(story, para, styles)
            flush_list()
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            story.append(Preformatted("\n".join(code), styles["code"]))
            i += 1
            continue

        table_rows, next_i = parse_table(lines, i)
        if table_rows:
            flush_paragraph(story, para, styles)
            flush_list()
            add_table(story, table_rows, styles)
            i = next_i
            continue

        if not stripped:
            flush_paragraph(story, para, styles)
            flush_list()
            i += 1
            continue

        if stripped == "---":
            flush_paragraph(story, para, styles)
            flush_list()
            story.append(PageBreak())
            i += 1
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush_paragraph(story, para, styles)
            flush_list()
            style = f"h{len(heading.group(1))}"
            story.append(Paragraph(inline_markup(heading.group(2)), styles[style]))
            i += 1
            continue

        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        if bullet:
            flush_paragraph(story, para, styles)
            list_items.append(bullet.group(1))
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph(story, para, styles)
            flush_list()
            story.append(Paragraph(inline_markup(stripped.lstrip("> ")), styles["quote"]))
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_paragraph(story, para, styles)
    flush_list()
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(BODY_FONT, 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def build_pdf(markdown_path, output_path):
    styles = make_styles()
    text = Path(markdown_path).read_text(encoding="utf-8")
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=22 * mm,
        title=Path(markdown_path).stem,
    )
    doc.build(build_story(text, styles), onFirstPage=footer, onLaterPages=footer)


def main():
    parser = argparse.ArgumentParser(description="Build a styled PDF from simple Markdown without a browser.")
    parser.add_argument("markdown", nargs="+")
    parser.add_argument("-o", "--output", help="Output PDF path. Only valid with one Markdown file.")
    args = parser.parse_args()

    if args.output and len(args.markdown) != 1:
        parser.error("-o/--output can only be used with one Markdown file")

    for md in args.markdown:
        markdown_path = Path(md)
        if not markdown_path.is_file():
            print(f"Skipped, missing file: {md}", file=sys.stderr)
            continue
        if markdown_path.suffix.lower() != ".md":
            print(f"Skipped, not Markdown: {md}", file=sys.stderr)
            continue
        output_path = Path(args.output) if args.output else markdown_path.with_suffix(".pdf")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        build_pdf(markdown_path, output_path)
        print(f"PDF written: {output_path}")


if __name__ == "__main__":
    main()
