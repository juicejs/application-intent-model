# Application Intent Model (AIM) v4.1

AIM is an intent-driven specification language and coordination layer for humans and AI coding agents. It captures product behavior in structured `.aim` files that agents read once, build from, review against, and repair over time — replacing the sprawl of PRDs, design notes, and plan files that agents otherwise generate.

**This repository is the specification itself** — the language, its reference examples, and the role prompts. Tooling, the package catalog, and publishing live in separate repositories.

---

## Why AIM

- **Ground agents in explicit, versioned intent** instead of loose chat context that evaporates between sessions.
- **A reviewable contract between intent and code.** `.aim` files are normally agent-authored, but a small spec is something a human can read, correct, and diff — and a Reviewer can check code against — far more cheaply than the generated code itself.
- **A relation graph, not just a tree.** v4 treats every `.aim` file as a projection of a node-and-edge graph: a View *exposes* a Contract, a Flow *mutates* a Schema and *emits* an Event. That graph is derived, traversable, and checkable.
- **Drift as graph-diff.** With optional intent↔code bindings, review becomes a diff between the declared graph and the realized code graph.

AIM pays off when reading the spec is meaningfully easier than reading the code. For trivially small or throwaway work, generating code directly is the right call.

---

## What's new in v4

v4 is a breaking change from v3.1. The three shifts:

1. **Graph-founded model.** The `.aim` Markdown file is a *projection* of an underlying node-and-edge graph. Every heading is an addressable node.
2. **Typed edge taxonomy.** One CommonMark-native token — `[verb](aim:<address>)` — replaces v3.1's inconsistent prose cross-references. Dangling references, orphan nodes, and impact sets fall out for free, and the traceability chain becomes *computable* rather than aspirational.
3. **Intent↔code binding layer.** Optional `facet: binding` files map intent nodes to their realization sites in code, turning drift detection into a graph-diff.

Migrating from v3.1: see Section 14 of [specification.md](./specification.md).

---

## File format at a glance

```markdown
---
aim: nemicko.demo.todo
facet: intent
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
- [examples/nemicko.demo.todo.aim](./examples/nemicko.demo.todo.aim) — a complete component in a single file.
- [examples/helpdesk/](./examples/helpdesk/) — a multi-file app (sub-components, a mapping, and a binding file) whose graph spans files, exercising **every** facet and all ten edge verbs. Start with its [README](./examples/helpdesk/README.md) for the rendered graph.

---

## The roles

1. **Architect** writes `.aim` files from requirements and declares the graph.
2. **Developer** generates code and tests from the resolved graph, and keeps bindings current.
3. **Reviewer** diffs code against the declared graph and reports drift — explicitly routed to a code fix (Developer) or an intent revision (Architect).

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
- **[agents/](./agents/)** — Architect, Developer, Reviewer persona files.
- **[brain/](./brain/)** — the shared and per-role operating-brain instructions.
- **[examples/](./examples/)** — conformance examples: a single-file component and the multi-file [helpdesk](./examples/helpdesk/) app.
- **[GEMINI.md](./GEMINI.md)** + **[gemini-extension.json](./gemini-extension.json)** — Gemini CLI extension: core mandates and manifest exposing the three roles as `@aim-architect` / `@aim-developer` / `@aim-reviewer`.

---

Current spec: **AIM v4.1**  
Built by **[Juice d.o.o.](https://juice.com.hr)** · MIT License
