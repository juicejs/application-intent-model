# AIM v4 Core Mandates

These mandates are foundational. All agents working in this project MUST adhere to these rules without exception.

## 1. Required reading

Before executing any command or writing any file, read the v4 specification.

**Bootstrap order:**

1. Read `AGENTS.md` at the project root — its frontmatter declares `aim_version` and the canonical `spec:` URL.
2. Read `/aim/specs/spec.md` (local cache) if present.
3. Fall back to the URL declared in `AGENTS.md`.
4. If none resolve, refuse to proceed.

This `GEMINI.md` provides operating rules and role dispatch. The specification provides the complete language rules. **You need both.**

## 2. The graph model

An `.aim` file is a **projection of a node-and-edge graph.** Every heading is an addressable node (`## Contract: CreateTask`); cross-references are typed edges. The graph is *derived* by collecting edges across files — never authored as a separate artifact, so `.aim` files stay the sole authority.

## 3. File format and extension

- **Extension:** Every AIM artifact MUST end in `.aim`.
- **Format:** Markdown body with YAML frontmatter. Renders as Markdown anywhere.
- **Frontmatter:** Every file starts with a YAML block containing `aim` and `facet` (and `parent` if it's a sub-component). The project-wide `aim_version` and `spec:` URL live once in `AGENTS.md` — there is **no per-file `version` or `spec`.**
- **Facet values:** `intent | schema | flow | contract | persona | view | event | trigger | mapping | binding`.
- **Identity:** The `aim` namespace MUST match the filename and directory path.

## 4. Syntax rules

- **Headings:** `# <Name>` for component; `## Summary`/`## Requirements`/`## Tests`/`## Subcomponents`/`## Dependencies` for sections; `## Schema: <Name>`/`## Contract: <Name>`/etc. for facets (each followed by `### Summary`); `### Attributes`/`### Input`/etc. for sub-blocks; `## Bind: <FacetType> <Name>` in a `facet: binding` file.
- **Lists:** Standard Markdown bullets.
- **Attributes:** Fenced `aim-attrs` code blocks with `name: type modifiers` lines. `ref(Type.field)` is the data-level `refs` edge.
- **Typed edges:** A cross-reference is `[verb](aim:<address>)`, declared at the node that acts. Verbs: `exposes`, `invokes`, `reads`, `mutates`, `emits`, `subscribes`, `accesses`, `navigates`, `triggers`, `refs`. (`triggers` is declared on a `## Trigger:` node — cron / webhook / external entry points.) Never author `### Trigger`/`### Emitted By` inverse blocks — those are derived. There is **no composition verb**: a screen rendering another view inline is realization (code/bindings), not an edge — a host connects to a promoted widget through the existing view edges (§16.9).
- **No v2.2 DSL.** `INTENT Name { ... }`, `SUMMARY:`, block syntax is invalid.

## 5. Layout

- Parent component: `/aim/<component>/<component>.aim`
- Sub-component: `/aim/<component>/<feature>/<component>.<feature>.aim`
- Facet file: `/aim/<component>/<component>.<facet>.aim`
- Mapping: `/aim/mappings/<component>/<component>.mapping.aim`
- Binding (optional, intent→code): `/aim/bindings/<component>/<component>.binding.aim`

Sub-component-first is the default. Collapse to a single file only when the component is genuinely small. Author shared facets (schemas/personas/views) as their own files or in `<app>.core`; the parent intent file is a lean index, not a container — don't dodge duplication by building a monolith.

UI pieces have **fluid granularity**: a tab/panel/widget is `### Display` prose until it earns a contract/schema, then it promotes to its own sub-intent (§16.9). Reshape an existing model by **transform** (promote / split / re-home / merge / rename), which re-points edges, updates `## Subcomponents`, and relocates bindings (code locator unchanged) — a traceable graph-diff, not a rewrite (§17).

## 6. Role dispatch

- **@aim-architect**: Requirements → Intent. Writes `.aim` files and declares the graph (typed edges, optional bindings).
- **@aim-developer**: Intent → Code/Tests. Builds from the resolved graph, keeps bindings current, and handles code-side repair when the Reviewer flags drift caused by buggy code.
- **@aim-reviewer**: Code → Drift Report. Diffs the declared graph against the realized code graph (graph-diff when bindings exist); routes each finding to code or intent.

Repair is a verb, not a role. The Developer fixes code; the Architect revises intent. Never silently normalize drift. Distribution (discovery, fetch, publishing) is handled by external tooling, not an agent role.

## 7. Required minimum for any `.aim` file

1. Valid YAML frontmatter with the required fields (`aim`, `facet`).
2. Exactly one H1 heading.
3. A non-empty `## Requirements` section.
4. File path matches the `aim` namespace.

## 8. Fail-safes before writing any `.aim` file

1. Frontmatter present with `aim:` and `facet:` (per-file `version:`/`spec:` are not used — they live in `AGENTS.md`).
2. Filename ends in `.aim` (never `.md`, `.yml`, `.yaml`, `.json`).
3. Body is valid Markdown — no v2.2 DSL blocks.
4. Sub-component files declare `parent:` matching an existing parent intent file.
5. Generic filenames (`intent.aim`, `schema.aim`, `binding.aim`) are hard errors.
6. Every `[verb](aim:…)` edge targets an existing node with a verb legal for the from/to node-types.
7. Every requirement and edge traces to user-provided intent. Never invent behavior.
8. Reuse, don't regenerate — search the graph for an existing `Schema`/`Persona`/entity before defining one; reference it (Imports + edge) instead. Cross-cutting entities live in one canonical home (`<app>.core`).

---

For the full language specification, fetch <https://intentmodel.dev/spec.md>.
