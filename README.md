# Application Intent Model (AIM) v3.0

AIM is an intent-driven specification language and coordination layer for humans and AI coding agents. It replaces the sprawl of `.md` PRDs, design notes, and plan files that agents otherwise generate — capturing product behavior in structured `.aim` files that agents read once, build from, review against, and repair over time.

---

## Why AIM

- **Eliminate hallucinations.** Ground AI agents in explicit, versioned specifications instead of loose chat context.
- **Deterministic code generation.** Build production-ready code traceable to every requirement.
- **Automated review.** Detect when code drifts from intent and decide explicitly: fix code, or revise intent.
- **Self-bootstrapping.** Every `.aim` file carries a `spec:` URL — any agent (Claude, Cursor, Gemini, Aider) can fetch the spec on first encounter and immediately understand the format. No plugin required.

---

## What's new in v3.0

v3.0 is a breaking change from v2.2. The shifts:

1. **Markdown-native syntax.** Files are valid Markdown with YAML frontmatter — renders on GitHub, in any IDE, and in any LLM context with no special tooling.
2. **Self-describing headers.** Every file carries a `spec:` URL so cold-start agents can fetch the spec and self-bootstrap.
3. **Sub-component-first authoring.** Complex applications are decomposed into focused sub-components by default. The parent intent acts as an index plus a home for shared facets.
4. **Three mainstream roles.** Architect, Developer, Reviewer — matching real software teams instead of formal-methods jargon.

Migrating from v2.2: see Section 11 of [specification.md](./specification.md).

---

## File format at a glance

```markdown
---
aim: juice.tasks.create_task
facet: intent
parent: juice.tasks
---

# CreateTask

## Summary

Create a new task on behalf of the authenticated user.

## Requirements

- Title must be 1–200 characters.
- Owner is the creating user.
- A `tasks.created` event is emitted on success.

## Contract: CreateTask

### Input

```aim-attrs
title: string required min(1) max(200)
description: string optional
```

### Ensures

- A new Task record is persisted with status="open".
- A `tasks.created` event is emitted.
```

---

## Layout

```
/aim/
  juice.tasks/
    juice.tasks.aim              # parent: index + shared schemas
    juice.tasks.schema.aim       # shared Task schema
    create_task/
      juice.tasks.create_task.aim
    assign_task/
      juice.tasks.assign_task.aim
  mappings/
    juice.tasks/
      juice.tasks.mapping.aim
```

Each sub-component is a real component with its own intent file and namespace. The parent indexes them and holds shared facets.

---

## The workflow

1. **Architect** writes intent files from requirements.
2. **Developer** generates code and tests from intent.
3. **Reviewer** compares code against intent and reports drift.
4. **Repair** is explicit: code fix (Developer) or intent revision (Architect) — never silent normalization.

---

## Render `.aim` files as Markdown on GitHub

Drop a `.gitattributes` file at your repo root:

```gitattributes
*.aim linguist-language=Markdown
*.aim linguist-detectable=true
```

GitHub will render `.aim` files as Markdown with full frontmatter, headings, and lists.

---

## Reference

- **[AGENTS.md](./AGENTS.md)** — project bootstrap for AI coding agents (cold-start entry point).
- **[specification.md](./specification.md)** — the authoritative v3.0 language spec.
- **[PROMPT.md](./PROMPT.md)** — role-based prompts for any AI assistant (Claude, Cursor, Aider, Gemini).
- **[agents/](./agents/)** — Architect, Developer, Reviewer persona files.
- **[Registry](./registry/)** — community catalog of reusable intent packages.

---

## Repository layout

- `agents/` — Architect, Developer, Reviewer persona definitions.
- `skills/` — Autonomous skills for code-generation workflows.
- `registry/` — Component package catalog.
- `site/` — The [intentmodel.dev](https://intentmodel.dev) website source.

---

## Gemini CLI extension

AIM ships as a first-class Gemini CLI extension. Three personas, one command:

```bash
gemini extensions install application-intent-model
```

Then invoke from your terminal:

- `@aim-architect`: "I want to build a 2FA login flow."
- `@aim-developer`: "build [component] in React"
- `@aim-reviewer`: "review [component]" (produces a drift report)

Package fetching is a CLI command (`sinth fetch <package>`), not a separate agent.

---

Current spec: **AIM v3.0**  
Built by **[Juice d.o.o.](https://juice.com.hr)**
