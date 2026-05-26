# AIM v3.0 Core Mandates

These mandates are foundational. All agents working in this project MUST adhere to these rules without exception.

## 1. Required reading

Before executing any command or writing any file, fetch and fully internalize the v3.0 specification:

```
https://intentmodel.dev/spec/3.0
```

This `GEMINI.md` provides operating rules and role dispatch. The specification provides the complete language rules. **You need both.**

## 2. File format and extension

- **Extension:** Every AIM artifact MUST end in `.intent`.
- **Format:** Markdown body with YAML frontmatter. Renders as Markdown anywhere.
- **Frontmatter:** Every file starts with a YAML block containing `aim`, `facet`, `version: 3.0`, `spec: https://intentmodel.dev/spec/3.0`, and `parent` if it's a sub-component.
- **Identity:** The `aim` namespace MUST match the filename and directory path.

## 3. Syntax rules

- **Headings:** `# <Name>` for component, `## Summary`/`## Requirements`/`## Tests`/`## Subcomponents`/`## Dependencies` for sections, `## Schema: <Name>`/`## Contract: <Name>`/etc. for facets, `### Attributes`/`### Input`/etc. for sub-blocks.
- **Lists:** Standard Markdown bullets.
- **Attributes:** Fenced `aim-attrs` code blocks with `name: type modifiers` lines.
- **No v2.2 DSL.** `INTENT Name { ... }`, `SUMMARY:`, `REQUIREMENTS {` block syntax is invalid in v3.0.

## 4. Layout

- Parent component: `/intent/<component>/<component>.intent`
- Sub-component: `/intent/<component>/<feature>/<component>.<feature>.intent`
- Facet file: `/intent/<component>/<component>.<facet>.intent`
- Mapping: `/intent/mappings/<component>/<component>.mapping.intent`

Sub-component-first is the default. Collapse to a single file only when the component is genuinely small.

## 5. Role dispatch

- **@aim-architect**: Requirements → Intent. Writes `.intent` files.
- **@aim-developer**: Intent → Code/Tests. Also handles code-side repair when the Reviewer flags drift caused by buggy code.
- **@aim-reviewer**: Code → Drift Report. Identifies whether each finding belongs in code or intent.

Repair is a verb, not a role. The Developer fixes code; the Architect revises intent. Never silently normalize drift.

Package installation is a CLI command (`sinth fetch <package>`), not a separate role.

## 6. Required minimum for any `.intent` file

1. Valid YAML frontmatter with all required fields (`aim`, `facet`, `version`, `spec`).
2. Exactly one H1 heading.
3. A non-empty `## Requirements` section.
4. `version` matches parent (for sub-components).
5. File path matches the `aim` namespace.

## 7. Fail-safes before writing any `.intent` file

1. Frontmatter present and complete with `spec: https://intentmodel.dev/spec/3.0`.
2. Filename ends in `.intent` (never `.md`, `.yml`, `.yaml`, `.json`).
3. Body is valid Markdown — no v2.2 DSL blocks.
4. Sub-component files declare `parent:` matching an existing parent intent file.
5. Generic filenames (`intent.intent`, `schema.intent`) are hard errors.
6. Every requirement traces to user-provided intent. Never invent behavior.

---

For the full language specification, fetch <https://intentmodel.dev/spec/3.0>.
