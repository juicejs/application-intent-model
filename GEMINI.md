# AIM v3.1 Core Mandates

These mandates are foundational. All agents working in this project MUST adhere to these rules without exception.

## 1. Required reading

Before executing any command or writing any file, read the v3.1 specification.

**Bootstrap order:**

1. Read `AGENTS.md` at the project root — its frontmatter declares `aim_version` and the canonical `spec:` URL.
2. Read `/aim/specs/spec.md` (local cache) if present.
3. Fall back to the URL declared in `AGENTS.md`.
4. If none resolve, refuse to proceed.

This `GEMINI.md` provides operating rules and role dispatch. The specification provides the complete language rules. **You need both.**

## 2. File format and extension

- **Extension:** Every AIM artifact MUST end in `.aim`.
- **Format:** Markdown body with YAML frontmatter. Renders as Markdown anywhere.
- **Frontmatter:** Every file starts with a YAML block containing `aim` and `facet` (and `parent` if it's a sub-component). The project-wide `aim_version` and `spec:` URL live once in `AGENTS.md` at the project root, not per file.
- **Identity:** The `aim` namespace MUST match the filename and directory path.

## 3. Syntax rules

- **Headings:** `# <Name>` for component, `## Summary`/`## Requirements`/`## Tests`/`## Subcomponents`/`## Dependencies` for sections, `## Schema: <Name>`/`## Contract: <Name>`/etc. for facets, `### Attributes`/`### Input`/etc. for sub-blocks.
- **Lists:** Standard Markdown bullets.
- **Attributes:** Fenced `aim-attrs` code blocks with `name: type modifiers` lines.
- **No v2.2 DSL.** `INTENT Name { ... }`, `SUMMARY:`, `REQUIREMENTS {` block syntax is invalid in v3.1.

## 4. Layout

- Parent component: `/aim/<component>/<component>.aim`
- Sub-component: `/aim/<component>/<feature>/<component>.<feature>.aim`
- Facet file: `/aim/<component>/<component>.<facet>.aim`
- Mapping: `/aim/mappings/<component>/<component>.mapping.aim`

Sub-component-first is the default. Collapse to a single file only when the component is genuinely small.

## 5. Role dispatch

- **@aim-architect**: Requirements → Intent. Writes `.aim` files.
- **@aim-developer**: Intent → Code/Tests. Also handles code-side repair when the Reviewer flags drift caused by buggy code.
- **@aim-reviewer**: Code → Drift Report. Identifies whether each finding belongs in code or intent.

Repair is a verb, not a role. The Developer fixes code; the Architect revises intent. Never silently normalize drift.

Package installation is a CLI command (`sinth fetch <package>`), not a separate role.

## 6. Required minimum for any `.aim` file

1. Valid YAML frontmatter with all required fields (`aim`, `facet`, `version`, `spec`).
2. Exactly one H1 heading.
3. A non-empty `## Requirements` section.
4. `version` matches parent (for sub-components).
5. File path matches the `aim` namespace.

## 7. Fail-safes before writing any `.aim` file

1. Frontmatter present and complete with `aim:` and `facet:` (per-file `version:` and `spec:` are no longer used — they live in `AGENTS.md`).
2. Filename ends in `.aim` (never `.md`, `.yml`, `.yaml`, `.json`).
3. Body is valid Markdown — no v2.2 DSL blocks.
4. Sub-component files declare `parent:` matching an existing parent intent file.
5. Generic filenames (`intent.aim`, `schema.aim`) are hard errors.
6. Every requirement traces to user-provided intent. Never invent behavior.

---

For the full language specification, fetch <https://intentmodel.dev/spec.md>.
