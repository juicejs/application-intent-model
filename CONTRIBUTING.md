# Contributing

This repository is the **AIM language specification** and its reference material — nothing else. Tooling, the package catalog, and publishing live in separate repositories.

## What lives here

- `specification.md` — the authoritative AIM v4 language spec
- `examples/` — conformance example `.aim` files
- `agents/`, `brain/`, `PROMPT.md` — role personas and prompt templates
- `AGENTS.md` — the reference project-bootstrap file

## Proposing spec changes

1. Open an issue describing the problem the change solves.
2. For accepted changes, edit `specification.md`. Keep section cross-references (`§N.M`) consistent, and update the `## 1.1 What Changed` table when the change is breaking.
3. If the change affects authoring, update the personas (`agents/`, `brain/`) and `PROMPT.md` to match.
4. Add or update a conformance example under `examples/` so the change is demonstrated.
5. Open a pull request.

## Examples

Examples must be valid against the current spec: correct frontmatter (`aim`, `facet`), typed edges that resolve, no orphan nodes or dangling references. Keep them small and focused — one component per example.
