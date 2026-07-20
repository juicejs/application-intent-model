---
aim_version: 5.1
aim_root: ./aim/
spec: https://intentmodel.dev/spec.md
---

# Agents

This project uses the **Agentic Intent Model (AIM) v5.1** to specify its intent. Read this file before doing any work — it is the cold-start entry point for every AI agent that enters the project.

## How to read this project

- **Behavioral truth lives in `.aim` files** under `/aim/`. These are the only files that define what the system is supposed to do.
- **Each `.aim` file is a projection of a node-and-edge graph.** Headings are nodes (`## Contract: CreateTask`); cross-references are typed edges written as `[verb](aim:<address>)` — a View `exposes` a Contract, a Flow `emits` an Event, and so on. Non-actor entry points (cron, webhooks, external systems) are `## Trigger:` nodes that `triggers` a flow/contract. Tooling derives the graph by collecting these edges; nothing maintains a separate graph file.
- **The AIM specification** is the authoritative grammar reference. Read it before parsing or writing any `.aim` file:
  1. Try the local cache first: `/aim/specs/spec.md`
  2. Fall back to the canonical URL: <https://intentmodel.dev/spec.md>
  3. If neither resolves, refuse to proceed — operating against an unknown specification is unsafe.
- **`.md` files (including this one) are explanatory, never authoritative.** They describe, link, and onboard, but they do not define behavior. Any behavioral requirement found in a `.md` file but not in a `.aim` file is **drift** that should be moved into intent.

## Project layout

```
.
├── AGENTS.md              # this file — agent onboarding
├── aim/
│   ├── specs/spec.md      # cached AIM specification (reference)
│   └── <intent>/       # one directory per intent
│       ├── <intent>.aim
│       ├── <intent>.mapping.aim   # capability-to-provider bindings (kind: mapping)
│       └── <intent>.binding.aim   # deprecated binding sidecar — bindings are inline `### Bindings` since v5.1
└── ...                    # your application code
```

Reserved directory name under `/aim/`: `specs/`. Everything else is an intent namespace. Mapping and binding facets co-locate with their intent — they are not separate top-level directories.

## Operating modes

AIM is operated through **capabilities**, not a menu of agents a human picks. You are one assistant: read the request and enter the right mode yourself — never ask which role to use. The modes differ only in what each may write (spec §1.2):

- **Architect** (writes intent) — designs the graph of facets + typed edges and serializes it as `.aim` files. Runs *forward* from requirements, or *reverse* to recover intent from a system that already exists (the **Encoder**, §17, whose output is marked `provenance: inferred` and awaits human confirmation). Owns the specification; revises intent when drift is caused by changed requirements.
- **Realizer / Developer** (writes code) — makes reality match the model: generates code and tests, wires automations, performs the process. Fixes the realization when drift is its fault.
- **Reviewer** (writes nothing) — compares reality against intent and reports drift, routing each finding to the Realizer or the Architect. **Runs cold and read-only** — an agent that could also fix what it judges rubber-stamps its own work; review and repair never share a turn.

Repair is a verb, not a mode — drift is resolved explicitly by the Realizer (realization fix) or the Architect (intent revision), never silently normalized. When the task is ambiguous, ask one short clarifying question, then proceed — never make the human name a role.

Detailed per-mode prompts: [PROMPT.md](./PROMPT.md). Mode brains: [brain/](./brain/). Persona files: [agents/](./agents/).

## Authoring discipline

- **Decomposition first.** Decompose intents into focused child intents by default. Collapse to a single file only when the intent is genuinely small (one feature, one screen of content).
- **Add facets only when they increase useful precision.** Start with the intent envelope (Summary + Requirements + Tests). Add Record, Contract, Flow, Persona, View, Event only where the user has given you enough detail to populate them meaningfully.
- **Never invent material behavior absent from intent.** When detail is missing, preserve documented intent and minimize assumptions. Surface ambiguity rather than guess.
- **Never silently normalize drift.** When implementation and intent diverge, resolve the mismatch explicitly.
- **Reuse, don't regenerate.** Before defining a shared entity (a `Record` or `Persona` like `User`), search the graph for an existing one and reference it instead of redefining. Cross-cutting entities shared across intents belong in one canonical home (e.g. `<app>.core`) — duplicate definitions across files are how the model breaks at scale.
- **Keep the parent lean; extract shared facets.** A parent intent file is an index, not a container — author shared schemas/personas/views as their own files (or in `<app>.core`). Don't dodge duplication by cramming everything into one file; a monolith is the dual failure.
- **Evolve by transform, not rewrite.** Every change to the model is one of two operations — EXTEND an existing intent or ADD a new one. When an EXTEND outgrows one clear behavior, *promote* the new capability into its own child intent; re-home, merge, split, or rename as needed. Each move re-points inbound edges, updates the parent's `## Children`, and relocates bindings (locator unchanged — the realization did not move) — a traceable graph-diff, not a rewrite.
- **UI pieces have fluid granularity.** A tab/panel/widget is `### Display` prose in its host view when simple, and promotes into its own child intent once it grows a contract or schema. There is no composition edge — a host connects to a promoted piece through the existing view edges.

## Project conventions

<!--
Add project-specific conventions here:
- Testing requirements
- Code style
- Deployment notes
- Stack choices
- Anything else an agent should know before working in this repo
-->
