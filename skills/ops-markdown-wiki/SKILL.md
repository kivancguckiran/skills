---
name: ops-markdown-wiki
description: Maintain operational Markdown wiki/vault systems with indexes, append-only logs, tasks, recurring follow-ups, source notes, Obsidian links, and optional static dashboard data. Use when the user asks to note, log, track, update, summarize, or organize real-world operations in Markdown knowledge bases across projects, teams, labs, services, or personal systems.
---

# Ops Markdown Wiki

Use this skill for operational Markdown systems where chat notes become durable, linked, auditable records.

Do not use it for polished essays, source interpretation, code-only changes, or private secrets. If the note contains credentials or sensitive personal data, preserve only the minimum safe reference required by the local system.

## Workflow

1. Read the nearest `AGENTS.md`, then `README.md` or the vault index.
2. Identify whether the request is a question, new record, status update, recurring follow-up, source intake, comment/decision request, or dashboard update.
3. Read only the relevant current files before editing:
   - root `index.md` or `00-giris/index.md`
   - append-only `log.md` or `90-loglar/log.md`
   - the affected task, follow-up, area, source, experiment, project, or query page
   - static dashboard data such as `site/data.js` only when the local guide requires it
4. Preserve user changes and append to logs instead of rewriting history.
5. If information is missing, record it explicitly using the local vocabulary, such as unknown, unclear, to follow up, no owner, or date unclear; do not invent facts.
6. Update all linked surfaces touched by the same operational fact: primary record, area/project page, index summary, log, and dashboard data when applicable.
7. Keep user-facing content in the repository language unless a title, quote, command, or package name requires another language.

## Inputs

Before editing, identify:

- the operation, project, person/team, or asset being updated
- whether this is a new fact, changed status, decision, question, or follow-up
- all linked surfaces that must stay consistent
- date, owner, and next action, if known

## Record Rules

- Use local status and priority vocabularies when present.
- Prefer short, scannable Markdown sections and tables.
- Use Obsidian links when the repo uses them.
- For new pages, follow existing file naming, frontmatter, and folder conventions.
- Keep raw sources in raw/source folders; write durable summaries into wiki pages.
- Do not expose repo process chatter in reader-facing notes.
- Do not turn uncertain information into a fact; mark uncertainty explicitly.
- Do not rewrite append-only logs except to fix a mechanical error in the entry being created.

## Log Rules

Treat logs as append-only. New entries usually go at the top unless the local guide says otherwise.

Common heading format:

```md
## [YYYY-MM-DD] type | Short title
```

Common log types: daily note, task, follow-up, source, comment, decision, operation, experiment, synthesis, maintenance. Use local slugs when the repo defines them.

## Validation

- If a static site or dashboard is affected and the repo has a build script, run the local build.
- For pure Markdown updates, verify changed links and required index/log updates manually unless the repo provides a lint or build command.

## Output

Report the records updated, any follow-up created, and any missing fact that remains unknown.
