# Codex Skills

Reusable Codex skills for practical development and Markdown knowledge-work workflows.

This repository intentionally starts with a small public core: skills that are useful across projects without exposing private repository structure or higher-value authoring methods.

## Skills

| Skill | Use when |
| --- | --- |
| `contract-first-monorepo` | Implementing API, schema, migration, backend, and client changes in TypeScript monorepos where one contract must stay consistent across packages. |
| `ops-markdown-wiki` | Turning operational notes into durable Markdown records, append-only logs, linked pages, and dashboard updates. |
| `pdf-page-extract` | Extracting original page ranges from an existing PDF into a new PDF without OCR, reflow, or format conversion. |
| `wiki-markdown-pdf` | Building styled PDFs from Markdown files using repository-local scripts, CSS, Pandoc, and a headless browser. |

## Layout

```text
skills/
  contract-first-monorepo/
    SKILL.md
    agents/openai.yaml
  ops-markdown-wiki/
    SKILL.md
    agents/openai.yaml
  pdf-page-extract/
    SKILL.md
    agents/openai.yaml
    scripts/
  wiki-markdown-pdf/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
```

## Install

Clone this repository and copy the desired skill folder into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/contract-first-monorepo "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Repeat for any other skill you want to install, then restart Codex so the new skills are discovered.

## Claude Code

These skills can also be used by Claude Code directly. Claude Code discovers project skills from:

```text
.claude/skills/<skill-name>/SKILL.md
```

To use one of these skills with Claude Code, copy the whole skill folder into your Claude skills directory:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R skills/wiki-markdown-pdf "$HOME/.claude/skills/"
```

Copy the whole folder, not only `SKILL.md`, because some skills also need bundled `scripts/` and `references/`.

Claude Code does not need an `agents/claude.yaml` sidecar for normal skill discovery. It reads the YAML frontmatter in `SKILL.md`; the existing `agents/openai.yaml` files are Codex/OpenAI-specific interface metadata.

## Requirements

- `pdf-page-extract` requires `qpdf` and `pdfinfo` from Poppler.
- `wiki-markdown-pdf` requires `pandoc` and Chrome or Chromium. Set `CHROME_BIN` if the browser is not auto-detected.
- Other skills are instruction-only and depend on the target repository's own scripts and conventions.

## Notes

- These skills are designed to prefer local repository conventions over hard-coded defaults.
- They avoid private project names, personal paths, credentials, and internal workspace topology.

## License

Licensed under the MIT License. See [LICENSE](LICENSE).
