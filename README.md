# Agentic Intent Model (AIM) v5

*Formerly "Application Intent Model" — renamed when the language generalized beyond software.*

AIM is a specification language for humans and AI agents. It captures the **intent** of a system — an application's behavior, a business process, an organization's commitments — in structured `.aim` files that agents read once, realize, review against, and repair over time — replacing the sprawl of PRDs, SOPs, design notes, and plan files that otherwise hold intent hostage in prose. Software was AIM's first domain and remains its most worked example; nothing in the language is specific to it.

**This repository is the specification itself** — the language, its reference examples, and the role prompts. Tooling, the package catalog, and publishing live in separate repositories.

---

## Why AIM

- **Ground agents in explicit, versioned intent** instead of loose chat context that evaporates between sessions.
- **A reviewable contract between intent and reality.** `.aim` files are normally agent-authored from a human's narration, but a small model is something a human can read, correct, and diff — and a Reviewer can check reality against (code, configurations, execution logs) — far more cheaply than inspecting the realization itself.
- **A relation graph, not just a tree.** v4 treats every `.aim` file as a projection of a node-and-edge graph: a View *exposes* a Contract, a Flow *mutates* a Schema and *emits* an Event. That graph is derived, traversable, and checkable.
- **Drift as graph-diff.** With optional intent↔realization bindings, review becomes a diff between the declared graph and the realized graph — recovered from code for software, from logs and configurations for processes.

AIM pays off when reading the model is meaningfully easier than inspecting the realization. For trivially small or throwaway work, acting directly is the right call.

---

## What's new in v4

v4 is a breaking change from v3.1. The three shifts:

1. **Graph-founded model.** The `.aim` Markdown file is a *projection* of an underlying node-and-edge graph. Every heading is an addressable node.
2. **Typed edge taxonomy.** One CommonMark-native token — `[verb](aim:<address>)` — replaces v3.1's inconsistent prose cross-references. Dangling references, orphan nodes, and impact sets fall out for free, and the traceability chain becomes *computable* rather than aspirational.
3. **Intent↔realization binding layer.** Optional `kind: binding` files map intent nodes to their realization sites — in code, in systems, in automations — turning drift detection into a graph-diff.

Migrating from v3.1: see Section 13 of [specification.md](./specification.md).

---

## File format at a glance

```markdown
---
aim: nemicko.demo.todo
kind: intent
---

# TaskManager

## Summary

A personal task manager.

## Requirements

- Users can create and complete tasks.

## View: TodoDashboard

### Summary

The owner's task-list surface.

### Actions

- Submitting the "New Task" form — [exposes](aim:#Contract:CreateTodo)
```

The `[exposes](aim:#Contract:CreateTodo)` token is a typed edge: `View → exposes → Contract:CreateTodo`. Collect every such token across a project and you have the relation graph.

Two worked examples ship with the spec:
- [examples/nemicko.demo.todo.aim](./examples/nemicko.demo.todo.aim) — a complete intent in a single file.
- [examples/helpdesk/](./examples/helpdesk/) — a multi-file app (sub-intents, a mapping, and a binding file) whose graph spans files, exercising **every** facet and the closed verb set end to end. Start with its [README](./examples/helpdesk/README.md) for the rendered graph.

---

## The roles

1. **Architect** designs the intent graph from a human's narration and serializes it as `.aim` files.
2. **Realizer** makes reality match the model — a development team, an automation, an agent performing a process — and keeps bindings current. (In software this role is the **Developer**, and the shipped prompt templates use that name.)
3. **Reviewer** diffs reality against the declared graph and reports drift — explicitly routed to a realization fix (Realizer) or an intent revision (Architect).

---

## Render `.aim` files as Markdown on GitHub

Drop a `.gitattributes` file at your repo root:

```gitattributes
*.aim linguist-language=Markdown
*.aim linguist-detectable=true
```

GitHub will render `.aim` files as Markdown — frontmatter, headings, lists, and the edge tokens as clickable links.

---

## Repository contents

- **[specification.md](./specification.md)** — the authoritative AIM v4 language spec.
- **[AGENTS.md](./AGENTS.md)** — the reference project-bootstrap file (cold-start entry point for any AI coding agent).
- **[PROMPT.md](./PROMPT.md)** — role-based prompts for any AI assistant.
- **[agents/](./agents/)** — Architect, Developer, Reviewer, and Encoder persona files.
- **[brain/](./brain/)** — the shared and per-role operating-brain instructions.
- **[examples/](./examples/)** — conformance examples: a single-file intent and the multi-file [helpdesk](./examples/helpdesk/) app.
- **[GEMINI.md](./GEMINI.md)** + **[gemini-extension.json](./gemini-extension.json)** — Gemini CLI extension: core mandates and manifest exposing the roles as `@aim-architect` / `@aim-developer` / `@aim-reviewer` / `@aim-encoder`.

---

Current spec: **AIM v5**  
Built by **[Juice d.o.o.](https://juice.com.hr)** · MIT License
