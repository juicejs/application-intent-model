---
aim_version: 3.0
aim_root: ./aim/
spec: https://intentmodel.dev/spec/3.0.md
---

# Agents

This project uses the **Application Intent Model (AIM) v3.0** to specify product behavior. Read this file before doing any work — it is the cold-start entry point for every AI coding agent that enters the project.

## How to read this project

- **Behavioral truth lives in `.aim` files** under `/aim/`. These are the only files that define what the system is supposed to do.
- **The AIM specification** is the authoritative grammar reference. Read it before parsing or writing any `.aim` file:
  1. Try the local cache first: `/aim/specs/3.0.md`
  2. Fall back to the canonical URL: <https://intentmodel.dev/spec/3.0.md>
  3. If neither resolves, refuse to proceed — operating against an unknown specification is unsafe.
- **`.md` files (including this one) are explanatory, never authoritative.** They describe, link, and onboard, but they do not define behavior. Any behavioral requirement found in a `.md` file but not in a `.aim` file is **drift** that should be moved into intent.

## Project layout

```
.
├── AGENTS.md              # this file — agent onboarding
├── aim/
│   ├── specs/3.0.md       # cached AIM specification (reference)
│   ├── work/              # non-authoritative agent scratchpads
│   ├── mappings/          # capability-to-provider bindings
│   └── <component>/       # one directory per component
│       └── <component>.aim
└── ...                    # your application code
```

Reserved directory names under `/aim/`: `specs/`, `work/`, `mappings/`. Everything else is a component namespace.

## Operating roles

AIM defines three mainstream roles. Any agent can take any role; the role is workflow guidance, not a language construct.

- **Architect** — translates requirements into `.aim` files. Owns the specification. When drift is caused by changed requirements, the Architect revises intent.
- **Developer** — generates code and tests from intent. When drift is caused by buggy implementation, the Developer fixes code.
- **Reviewer** — compares code against intent and reports drift. Identifies whether each finding belongs to the Developer or the Architect. Does not fix code or revise intent directly.

Repair is a verb, not a role — drift is resolved explicitly by Developer (code fix) or Architect (intent revision), never silently normalized.

Detailed prompts for each role: [PROMPT.md](./PROMPT.md). Persona files: [agents/](./agents/).

## Authoring discipline

- **Sub-component first.** Decompose components into focused sub-components by default. Collapse to a single file only when the component is genuinely small (one feature, one screen of content).
- **Add facets only when they increase useful precision.** Start with the intent envelope (Summary + Requirements + Tests). Add Schema, Contract, Flow, Persona, View, Event only where the user has given you enough detail to populate them meaningfully.
- **Never invent material behavior absent from intent.** When detail is missing, preserve documented intent and minimize assumptions. Surface ambiguity rather than guess.
- **Never silently normalize drift.** When implementation and intent diverge, resolve the mismatch explicitly.

## Project conventions

<!--
Add project-specific conventions here:
- Testing requirements
- Code style
- Deployment notes
- Stack choices
- Anything else an agent should know before working in this repo
-->
