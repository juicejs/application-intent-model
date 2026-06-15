# Application Intent Model (AIM) v4

Application Intent Model (AIM) is an intent-driven specification language for humans and AI coding agents. It captures product behavior in a form readable enough for product and design discussion and structured enough for implementation, review, repair, and deterministic code generation.

AIM v4 is a **breaking change** from v3.1. v3.1 made AIM Markdown-native and self-bootstrapping; it succeeded at making intent *readable*, but it left AIM's highest-value job — the **linking** between the things a system is made of — almost entirely informal. Real applications are not trees; they are **graphs**. A View exposes an Action that invokes a Contract that reads or mutates a Schema and emits an Event that a Persona can reach. v3.1 expressed those relations in inconsistent prose ("Invoked by Contract: X", "TRIGGER: Contract.Y", "CALL Z"), demoted the traceability chain to "a useful target, not a requirement," and offered no way to traverse, check, or diff the relation graph.

The three structural shifts that drive v4:

1. **Graph-founded model.** The `.aim` Markdown file is understood as a *projection* of an underlying node-and-edge graph. Every heading is an addressable node; every cross-reference is a typed, directed edge. The graph is *derived* by collecting edges across files — it is never authored as a separate artifact, so `.aim` files remain the sole authority.
2. **Typed edge taxonomy.** A single CommonMark-native edge token replaces the prose. Each edge carries a verb from a closed set and points at a canonical node address. This makes the relation graph traversable and checkable: dangling references, orphan nodes, and impact sets fall out for free, and the traceability chain becomes *computable* rather than aspirational.
3. **Intent↔code binding layer.** Intent nodes may bind to their realization sites in code (`file#symbol`, `route:…`, `topic:…`, `table:…`). Drift detection then becomes a **graph-diff** between the declared intent graph and the realized code graph, yielding precise, owner-routed findings.

The design bar for all three is **LLM-parsability** — consistent conventions an LLM follows and traverses reliably, not a rigid grammar requiring a custom parser. AIM remains valid CommonMark that renders on GitHub with no special tooling.

AIM is the authoritative shared artifact between humans and coding agents. Implementation, review, and repair all run against AIM. When implementation and intent disagree, the mismatch is resolved explicitly — either by fixing code or by revising intent.

**Who writes AIM, and when it is worth it.** In practice `.aim` files are authored by an agent (the Architect role, §1.2) from a human's requirements — not hand-written token by token. The typed structure of v4 therefore costs the author nothing and yields a more precise, checkable artifact. This answers the obvious objection — *if an agent writes the spec and an agent writes the code, why not generate the code directly?* The `.aim` file is the **durable, human-reviewable, machine-checkable contract** between intent and generated code: a small spec is something a human can read, correct, and diff — and the Reviewer can check code against — far more cheaply than the code itself, and it persists across sessions where a chat prompt does not. The corollary is a boundary worth stating plainly: AIM pays off when reading the spec is meaningfully easier than reading the code; for trivially small or throwaway work, generating code directly is the right call.

---

## 1. Core Model

A component is identified by a dotted namespace such as `juice.tasks` or `game.snake`. Sub-components extend the namespace: `juice.tasks.create_task` is a sub-component of `juice.tasks`.

Each component has:

- one required **intent file** (a `.aim` file with `facet: intent`)
- zero or more optional **facets**: `schema`, `flow`, `contract`, `persona`, `view`, `event`
- zero or more optional **sub-components** (each is a component in its own right)
- zero or more optional **mapping files** (`facet: mapping`) — capability-to-provider bindings
- zero or more optional **binding files** (`facet: binding`) — intent-to-code realization bindings

The intent file is the canonical entrypoint. All other detail attaches to it directly (embedded), indirectly (sibling facet files), or through sub-components.

### 1.1 What Changed From v3.1

| Concern | v3.1 | v4 |
|---|---|---|
| Underlying model | Namespace tree (parent/child) | Node-and-edge graph; the tree is one edge type |
| Cross-references | Prose mentions, inconsistent forms | One typed edge token: `[verb](aim:<address>)` |
| Traceability chain | "A useful target, not a requirement" | Derived from declared edges; checkable |
| Inverse relations | Authored twice (`### Trigger`, `### Emitted By`) | Declared once at the acting end; inverse derived |
| Code linkage | None | Optional `facet: binding`; drift becomes graph-diff |
| Per-file `version`/`spec` | Contradictory in v3.1 (frontmatter omitted them, but version-inheritance, registry, and diagnostics still required them) | Removed everywhere; version lives only in `AGENTS.md` (and the external catalog) |

### 1.2 Agent Roles

v4 keeps the three mainstream roles that map onto how real software teams already work:

- **Architect** — translates requirements into intent files. Owns the specification. Declares typed edges between nodes and authors binding facets when realization is known.
- **Developer** — implements code and tests from the resolved graph. Emits or updates bindings for the code it writes. Fixes code when drift is found.
- **Reviewer** — diffs the declared graph against the realized code graph and reports drift.

Roles are workflow guidance, not language constructs — they do not appear in `.aim` source files. A single agent may perform multiple roles, and multiple agents may share one role. See [`PROMPT.md`](./PROMPT.md) and [`agents/`](./agents/) for concrete prompt templates.

Repair is a verb, not a separate role. When the Reviewer flags drift, either the Developer fixes the code or the Architect revises the intent. The decision is explicit, not silent.

Normative behavior across all roles:

- The Developer must not invent material behavior absent from intent.
- When detail is missing, preserve documented intent and minimize assumptions.
- Assumptions are surfaced for review or converted into explicit intent updates by the Architect.
- When implementation and intent disagree, the mismatch is resolved — Developer fixes code if implementation is wrong, Architect revises intent if specification is outdated.

### 1.3 Project Authority Model

AIM is Markdown-native by deliberate choice, but that choice creates a risk: AI agents already love to spawn `.md` plans, design notes, decision logs, and PRDs. Without a clear authority boundary, AIM becomes one more `.md` file in the pile instead of the artifact that displaces it. The following rules establish that boundary.

**Authority hierarchy:**

1. **`.aim` files are the sole behavioral authority.** Every requirement, contract, schema, flow, persona, view, event, and **edge** that defines product behavior must live in a `.aim` file. Tools, agents, and reviewers treat `.aim` as the only source of truth for what the system is supposed to do. The derived graph is a *view* of these files, never a competing artifact.

2. **Other `.md` files are explanatory, not authoritative.** `README.md`, `CONTRIBUTING.md`, ADRs, and similar documents may describe, link to, or summarize intent — but they must not define new behavioral requirements. If a behavioral requirement appears only in an `.md` file and not in a `.aim` file, it is **drift**. The Reviewer reports it. The fix is to move the requirement into a `.aim` file.

3. **Anything outside `/aim/` is invisible to authority.** Behavioral content found in `docs/`, top-level `.md` files, code comments treated as spec, or chat history transcripts is not part of the project's behavioral authority. If it matters, it gets moved into `.aim`. If it doesn't, it isn't authoritative. The lone exception is `AGENTS.md` at the project root (see §3.3) — which carries project bootstrap metadata for agents but does not define behavior itself.

**Behavior vs. realization.** A binding (`facet: binding`, §10) records *where* behavior is realized in code. Realization is not behavior. Bindings are authoritative for the intent↔code mapping but never define what the system should do — that always lives in the behavioral facets. This is why bindings are kept in their own files (§10.2): a binding can go stale (code moved) without the intent being wrong.

**Diagnostics:**

- **Hard error** — none for the prose/authority boundary. The Authority Model is enforced socially and by review, not by the parser. Tools cannot reliably distinguish "describes intent" from "defines intent" in arbitrary prose.
- **Informational diagnostic** — reviewers and validators may flag `.md` files that appear to contain behavioral requirements not present in `.aim` files. The recommended remediation is always to move the requirement into a `.aim` file.

**Why this matters:**

The whole point of AIM is to replace `.md` sprawl with a structured behavioral artifact agents can read once and build from. Without the Authority Model, the same agents that spawned 100 `.md` files will spawn 100 `.md` files plus a few `.aim` files. With the Authority Model, every behavioral fact has exactly one home — and drift between sources is impossible because there is only one source.

---

## 2. Graph Model

v4 reinterprets the v3.1 file surface as the projection of a graph. No new file format and no new parser tier: every node already has a heading, and every edge is just a typed cross-reference. This section defines what a node is and how it is addressed; §8 defines edges.

### 2.1 Nodes

A node is any **addressable heading** in the resolved source. There are three ranks, all of which already exist as headings:

| Rank | Markdown | Node-type | Example |
|---|---|---|---|
| Component | `aim:` frontmatter / H1 | `component` | `nemicko.demo.todo` |
| Facet | `## <Facet>: <Name>` | `schema` `view` `contract` `flow` `persona` `event` `trigger` (+ `requirement`) | `## Contract: CreateTodo` |
| Facet sub-block | `### <Sub>` and its list items | `block` (addressable, not separately typed) | `### Ensures` item `[2]` |

Top-level prose sections (`## Summary`, `## Requirements`, `## Tests`, `## Dependencies`) are nodes of type `section`. They are valid anchor targets for drift reports but are **edge-inert** — they are never the endpoint of a typed edge. Only `component` and the facet node-types participate in the edge graph. The node-type is read directly off the facet-heading keyword; there is no inference.

### 2.2 Node Addresses

The canonical address of a node is:

```
<component>#<FacetType>:<Name>[ → ### <Sub> [<index>]]
```

- `<component>` — the dotted namespace from the file's `aim:` field. Present in any stored or derived address (fully qualified). **Elidable** at an inline reference site when the target resolves within the same component, yielding the unqualified form `#<FacetType>:<Name>`.
- `#<FacetType>:<Name>` — the facet heading, verbatim. `FacetType` is capitalized exactly as in the heading (`Contract`, `View`, `Schema`, …).
- `→ ### <Sub> [<index>]` — optional finer pointer into a sub-block list item, 1-based, matching the Reviewer's drift-report convention.

This is the address scheme drift reports already use (`## Contract: CreateTask → ### Ensures [2]`), promoted from a review artifact to the language's identity scheme.

### 2.3 Address Examples

```
nemicko.demo.todo                                          # component node
nemicko.demo.todo#Schema:TodoItem                          # facet node
nemicko.demo.todo#Schema:TodoItem → ### Attributes [3]     # the `title` attribute
nemicko.demo.todo#Contract:CreateTodo
nemicko.demo.todo#Contract:CreateTodo → ### Ensures [2]    # "Emits a TodoCreated event"
nemicko.demo.todo#Flow:ExecuteCreateTodo → ### Steps [3]
nemicko.demo.todo#Persona:StandardUser
nemicko.demo.todo#View:TodoDashboard → ### Actions [1]
nemicko.demo.todo#Event:TodoCreated
```

Within a single-file component, every node shares the one component prefix, so inline references drop it entirely (`#Contract:CreateTodo`).

### 2.4 The Graph Is Derived

There is no graph file. A tool or agent builds the project graph by:

1. **Collecting nodes** — every component/facet/sub-block heading in the resolved source becomes a node keyed by its fully-qualified address.
2. **Collecting edges** — scanning inline edge tokens (§8) and structured `ref(Type.field)` attributes; each yields one directed, typed edge `(from = enclosing facet node, verb, to = resolved address)`.
3. **Validating** each edge against the from→to schema (§8.2) and resolving each target via §11.1.
4. **Adding derived inverse edges** (§8.4) and reconciling them against any authored inverse blocks.

The result lives only in tool/LLM memory or a build artifact. The `.aim` files remain the sole authority (§1.3).

---

## 3. File Format

### 3.1 Extension

All AIM v4 source files use the `.aim` extension. The extension is a brand and discipline marker: a file named `*.aim` is an authoritative AIM artifact, not a generic note. (Legacy v2.2 sources used `.intent`. v3.1 and v4 both use `.aim`; the v3.1→v4 break does **not** change the extension.)

Files are valid CommonMark Markdown with YAML frontmatter. Any Markdown renderer will display them correctly.

### 3.2 Header (YAML Frontmatter)

Every `.aim` file begins with a small YAML frontmatter block:

```yaml
---
aim: juice.tasks.create_task
facet: intent
parent: juice.tasks
---
```

Required fields:

- `aim` — the component namespace (lowercase, dot-separated)
- `facet` — one of `intent | schema | flow | contract | persona | view | event | trigger | mapping | binding`

Optional fields:

- `parent` — the parent component namespace, present on sub-components
- `display` — a human-readable display name (overrides the H1 heading for tooling)
- `tags` — array of free-form tags for discovery

The frontmatter carries **no** per-file `version:` or `spec:` field. The project-wide AIM version and spec URL live in **`AGENTS.md` at the project root** (see §3.3) — a single source of truth that eliminates redundancy and drift between files. There is no per-file version anywhere in v4.

### 3.3 `AGENTS.md` — Project Bootstrap

Every AIM project carries an `AGENTS.md` file at its root. This is the universal entry point any coding agent (Claude, Cursor, Aider, Gemini, etc.) reads first when entering the project — it predates AIM as a convention and is now the de facto standard across the AI coding ecosystem.

**Required structure:**

```markdown
---
aim_version: 4
aim_root: ./aim/
spec: https://intentmodel.dev/spec.md
---

# Agents

This project uses the **Application Intent Model (AIM) v4** for behavioral specification.

[...prose explaining roles, conventions, project specifics...]
```

The frontmatter on `AGENTS.md` carries:

- `aim_version` — the AIM language version this project targets (e.g. `4`)
- `aim_root` — where `.aim` files live (default `./aim/`)
- `spec` — the canonical specification URL for the declared version

The prose body explains AIM to a cold-start agent in natural language: what the roles are, where `.aim` files live, what conventions apply, that `.aim` files are a projection of a node-and-edge graph, and that bindings live under `aim/bindings/`. Anything an agent needs to know about working in this project — both AIM and non-AIM — belongs here.

**Why this works:**

1. **Cold-start universally solved.** Any agent that follows the `AGENTS.md` convention finds AIM automatically. No AIM-aware tooling required for the first read.
2. **One source of truth for version.** Bumping AIM versions is a one-line edit, not a project-wide search-and-replace. Because no `.aim` file carries a version, there is nothing else to update.
3. **No per-file boilerplate.** `.aim` files carry only what's unique to them (namespace + facet); shared facts live once in `AGENTS.md`.
4. **Tool interop for free.** Cursor, Copilot, Anthropic tooling, and others that already read `AGENTS.md` pick up AIM context without integration work.

### 3.4 Local Spec Cache

Many agents operate without network access (sandboxed environments, CI runners, offline editing, restricted enterprise networks). To support them, AIM tooling installs a local copy of the spec under `/aim/specs/`.

**Layout:**

```
/aim/
  specs/
    spec.md          # the AIM specification (mirrored from spec: URL)
  mappings/          # required-alias mappings
  bindings/          # intent-to-code realization bindings
  <component>/       # one directory per component
```

**Required installer behavior:**

1. On first project setup (performed by an agent or tooling), fetch the spec from the URL declared in `AGENTS.md` and write it to `/aim/specs/spec.md`.
2. When the project adopts a new AIM version, the installer overwrites the local `spec.md` with the new version.
3. The local spec file is a verbatim mirror of the URL content. Tools must not modify it.

**Agent spec-resolution order:**

1. **`AGENTS.md`** — read the project's frontmatter to determine the `spec` URL (the `aim_version` provides language context but the URL is the source of truth). If `AGENTS.md` declares no `aim_version`/`spec`, refuse to proceed — operating against an unknown specification is unsafe.
2. **Local cache** — read `/aim/specs/spec.md` if present. Always works, even offline.
3. **URL fallback** — fetch the `spec` URL declared in `AGENTS.md`.
4. **Hard error** — if none of these resolve, refuse to proceed.

**Reserved names under `/aim/`:**

These directory names are reserved and must not be used as component namespaces:

- `aim/specs/` — cached specifications (`.md` files)
- `aim/mappings/` — capability-to-provider bindings (`.aim` files, `facet: mapping`)
- `aim/bindings/` — intent-to-code realization bindings (`.aim` files, `facet: binding`)

Any other directory under `/aim/` that contains a `<name>.aim` file is a component.

### 3.5 Body (Markdown)

The body of the file is Markdown. Structure is conveyed by heading levels:

- **H1** — the component's display name (exactly one per file)
- **H2** — top-level sections (`## Summary`, `## Requirements`, `## Tests`, `## Subcomponents`, `## Dependencies`) and facet blocks (`## Schema: Task`, `## Contract: CreateTask`, etc.)
- **H3** — facet sub-blocks (`### Attributes`, `### Input`, `### Ensures`, `### Steps`, etc.)
- **Bulleted lists** — for requirements, tests, steps, attributes, and any enumeration
- **Fenced code blocks** — for attribute definitions, type expressions, and code samples

### 3.6 Heading Conventions

Facet headings use the form `## <FacetType>: <Name>`:

```markdown
## Schema: Task
## Contract: CreateTask
## Flow: AssignTask
## Persona: TaskOwner
## View: TaskDashboard
## Event: TaskCreated
## Trigger: NightlySweep
```

Binding-facet files use `## Bind: <FacetType> <Name>` headings (see §10.2):

```markdown
## Bind: Contract CreateTask
```

Top-level section headings use the bare form:

```markdown
## Summary
## Requirements
## Tests
## Subcomponents
## Dependencies
```

The facet heading text is the node's address within the file (§2.2). Every facet heading MUST be immediately followed by an explicit `### Summary` sub-block, with the single exception of a `Persona` acting only as a role/access declaration (§7.8). This keeps node boundaries deterministic.

### 3.7 Attribute Syntax

Attributes inside `### Attributes` blocks use a fenced code block with a simple line format:

````markdown
### Attributes

```aim-attrs
title: string required min(1) max(200)
description: string optional
ownerId: string required ref(User.id)
status: enum(open, completed, archived) required
createdAt: datetime required
```
````

Format per line: `<name>: <type> <modifier>*`

Modifiers: `required`, `optional`, `min(n)`, `max(n)`, `ref(<Type>.<field>)`, `enum(a, b, c)`, `default(<value>)`.

`ref(<Type>.<field>)` is a **typed graph edge** (`refs`, §8.2): it links a schema attribute to another schema's attribute and is collected into the graph alongside inline edge tokens.

### 3.8 Allowed Markdown Features

`.aim` files use CommonMark Markdown, but the spec constrains which features are allowed where. The rule:

- **Structured spec blocks** — facet sub-blocks like `### Requirements`, `### Tests`, `### Steps`, `### Attributes`, `### Input`, `### Ensures`, `### Returns`, `### Actions`, `### Access` — use only the patterns the spec defines (bullets, fenced `aim-attrs` blocks, and the inline edge token `[verb](aim:…)`). These blocks have parseable semantics; alternative forms create parsing ambiguity.
- **Free-form prose sections** — `## Summary`, descriptive paragraphs between facet blocks, the body of `AGENTS.md` — follow standard CommonMark without restriction.

| Feature | In structured blocks | In prose |
|---|---|---|
| Bulleted lists | ✓ (required form) | ✓ |
| Edge token `[verb](aim:…)` | ✓ (typed cross-reference) | ✓ |
| Tables | ✗ | ✓ |
| Blockquotes | ✗ | ✓ |
| Task lists (`- [ ]`) | ✗ | ✓ |
| Footnotes | ✗ | ✓ |
| Bold, italic, inline links | ✓ (inside list items) | ✓ |
| Inline code (backticks) | ✓ | ✓ |
| Fenced code blocks | ✓ (only `aim-attrs` in `### Attributes`; arbitrary elsewhere) | ✓ |
| Raw HTML | ✗ | ✗ |

The edge token is a standard CommonMark inline link whose destination uses the `aim:` URI scheme (§8.1). It renders as a clickable link on GitHub and is therefore allowed inside structured blocks, where it carries the cross-reference semantics.

**Task lists deserve specific mention.** Markdown's `- [ ]` syntax is forbidden in `## Requirements`, `## Tests`, and other structured blocks even though it looks like a bullet list. The `.aim` file is *intent*, not *status*. Implementation and verification status live in a drift report under `/aim/work/` produced by the Reviewer — see §1.3 (Authority Model) and the Reviewer's drift-report convention in [`agents/aim-reviewer.md`](agents/aim-reviewer.md). Putting status into intent makes the spec lie when code changes and the checkbox doesn't.

**Raw HTML is banned everywhere** because it breaks parsers and circumvents the Markdown-native discipline.

---

## 4. Project Layout

### 4.1 Sub-Component-First Default

AIM decomposes real applications into focused sub-components. Each sub-component is a real component with its own intent file, its own namespace, and its own facets. The parent component serves as an index plus a home for cross-cutting requirements and shared facets.

Reasons this is the default:

- LLMs reason better over small focused files than large ones
- Multiple agents can work on different sub-components in parallel without merge conflicts
- Diffs are meaningful when each file has a single concern
- Synthesis maps cleanly to small focused code modules

The namespace hierarchy is the `extends` edge of the graph (parent ← child); it is one relation among many, not the model's organizing principle.

### 4.2 Canonical Layout

```
/aim/
  juice.tasks/
    juice.tasks.aim                  # parent: index + shared
    juice.tasks.schema.aim           # shared schemas (Task, User refs)
    create_task/
      juice.tasks.create_task.aim
      juice.tasks.create_task.contract.aim
    assign_task/
      juice.tasks.assign_task.aim
    complete_task/
      juice.tasks.complete_task.aim
  mappings/
    juice.tasks/
      juice.tasks.mapping.aim
  bindings/
    juice.tasks/
      juice.tasks.binding.aim
```

Rules:

- Each component lives in a directory named after its namespace.
- The intent file filename matches `<component>.aim`.
- Facet filenames match `<component>.<facet>.aim`.
- Sub-components live in nested directories under the parent.
- Mappings live under `/aim/mappings/<component>/`; bindings under `/aim/bindings/<component>/`.
- Generic filenames (`aim.aim`, `schema.aim`, `binding.aim`) are invalid.

### 4.3 When To Collapse Into A Single File

A component should stay in a single `.aim` file (no sub-components, facets embedded inline) only when **all** of the following hold:

- Total content fits comfortably in a single screen of reading.
- There is one clear behavior, not a set of distinct features.
- No facet needs independent ownership or review.

Otherwise, split. Split is the default; single-file is the exception.

### 4.4 Path Identity

The header `aim:` field is authoritative for identity. The directory and filename must agree with the header — tools treat path/header mismatch as a hard error. This lets paths function as a fast sanity check without competing with the header as the source of truth.

---

## 5. Sub-Components

### 5.1 Definition

A sub-component is a component whose namespace extends a parent component's namespace by exactly one segment:

- Parent: `juice.tasks`
- Child:  `juice.tasks.create_task`

The child declares the parent in its frontmatter:

```yaml
---
aim: juice.tasks.create_task
facet: intent
parent: juice.tasks
---
```

A sub-component is a real component: it has its own intent file, its own facets, and is independently addressable. The `parent:` relation is the graph's `extends` edge.

### 5.2 Parent As Index

The parent component's intent file serves two purposes:

1. **Index of sub-components** — either auto-discovered from sibling directories or explicitly listed.
2. **Home for cross-cutting concerns** — shared requirements, shared schemas, shared personas, shared events that apply across all sub-components.

Example parent intent:

```markdown
---
aim: juice.tasks
facet: intent
---

# Tasks

A task management subsystem. Users create, assign, and complete tasks tied to projects.

## Summary

The tasks subsystem owns the full task lifecycle: creation, assignment, state transitions, and archival. All sub-components share the `Task` schema and emit events on the `tasks.*` channel.

## Requirements

- Every task belongs to exactly one owner.
- State transitions are auditable.
- Soft-delete is preferred over hard-delete.

## Subcomponents

- [create_task](./create_task/juice.tasks.create_task.aim) — create a new task
- [assign_task](./assign_task/juice.tasks.assign_task.aim) — assign a task to a user
- [complete_task](./complete_task/juice.tasks.complete_task.aim) — mark a task completed

## Schema: Task

### Summary

The shared task record used by all sub-components.

### Attributes

```aim-attrs
id: string required
title: string required min(1) max(200)
description: string optional
ownerId: string required ref(User.id)
status: enum(open, in_progress, completed, archived) required
createdAt: datetime required
updatedAt: datetime required
```
```

### 5.3 Sub-Component Discovery

By default, sub-components are **auto-discovered**: any sibling directory containing a `<namespace>.aim` file with a matching `parent:` field is treated as a sub-component of the parent.

The parent may override discovery with an explicit `## Subcomponents` block. When the explicit list is present:

- listed sub-components must exist on disk
- discovered sub-components not in the list emit a hard error (ambiguous authority)
- the explicit list is authoritative for the order in which sub-components are presented to agents and tooling

### 5.4 Upward Facet Resolution

A sub-component may reference facets defined in the parent without qualification. The complete precedence rules are defined once in §11.1 — sub-components add one detail: the **parent chain** step walks the namespace upward (parent → grandparent → root) until a match is found or the chain ends.

Tools emit an informational diagnostic when a sub-component defines a facet that shadows one already defined in a parent. This is usually a sign that either the shared definition should move up, or the sub-component name should be more specific.

### 5.5 Nesting Depth

Sub-components may nest, but the spec recommends a maximum effective depth of **three levels** (e.g. `app.module.feature.sub_feature`). Beyond this, comprehension drops and traceability becomes hard to follow. Tools should warn when nesting exceeds three levels.

There is no version inheritance in v4: `.aim` files carry no version, so a sub-component is automatically consistent with its parent. (This removes the v3.1 "version inheritance" rule entirely.)

---

## 6. Intent Envelope

### 6.1 Minimum Valid Intent File

```markdown
---
aim: demo.todo
facet: intent
---

# Todo

## Summary

A simple personal todo tracker.

## Requirements

- User can add, complete, and delete todos.
```

Hard minimum for validity:

- Valid frontmatter with required fields (`aim`, `facet`).
- Exactly one H1 heading.
- A `## Summary` section with at least one paragraph **or** an H1 followed by a paragraph that serves as the summary.
- A `## Requirements` section with at least one bullet.

Recommended:

- `## Tests` section with observable behavior bullets.
- One or more facets when the component has stable interfaces.

### 6.2 Extended Intent Example (Sub-Component)

```markdown
---
aim: juice.tasks.create_task
facet: intent
parent: juice.tasks
---

# CreateTask

## Summary

Create a new task on behalf of the authenticated user. The task starts in the `open` state and is owned by the creator.

## Requirements

- A task must have a non-empty title (1–200 characters).
- A description is optional.
- The creating user becomes the owner.
- The task is persisted with status `open`.
- A `tasks.created` event is emitted on successful creation.

## Tests

- Creating a task with an empty title fails with a validation error.
- A newly created task is visible in the owner's task list.
- A `tasks.created` event is emitted with the new task's id.

## Contract: CreateTask

### Summary

Create a task on behalf of the current user.

### Input

```aim-attrs
title: string required min(1) max(200)
description: string optional max(2000)
```

### Authz

- Caller must be authenticated.

### Ensures

- A new Task record is persisted with status="open" — [mutates](aim:#Schema:Task).
- ownerId is set to the current user's id.
- A `tasks.created` event is emitted — [emits](aim:juice.tasks#Event:TaskCreated).

### Returns

- The newly created Task record.
```

Note: `Task` and `User` are not defined in this file — they resolve upward to the parent component `juice.tasks` (§11.1).

---

## 7. Precision Facets

The six behavioral facets are unchanged in meaning from v3.1. What changes is how their cross-references are written: prose mentions become typed edge tokens (§8), and the inverse blocks `### Trigger` and `### Emitted By` are removed because they are derivable. v4 adds a seventh facet — **Trigger** (§7.7) — for non-actor entry points such as schedules and webhooks.

### 7.1 Schema

Data at rest, structural types, and constraints.

```markdown
## Schema: Task

### Summary

A persisted task record owned by exactly one user.

### Attributes

```aim-attrs
id: string required
title: string required min(1) max(200)
ownerId: string required ref(User.id)
status: enum(open, completed, archived) required
```

### Constraints

- `ownerId` must reference an existing User.
- `status` transitions follow: open → completed → archived.

### Immutable

- `id`, `createdAt`, `ownerId`
```

### 7.2 Contract

Externally observable guarantees and obligations.

```markdown
## Contract: CreateTask

### Summary

Create a task on behalf of the current user.

### Input

```aim-attrs
title: string required
description: string optional
```

### Authz

- Caller must be authenticated.

### Expects

- Title is non-empty after trimming.

### Ensures

- A new Task record is persisted with status="open" — [mutates](aim:#Schema:Task).
- A `tasks.created` event is emitted — [emits](aim:#Event:TaskCreated).

### Returns

- The newly created Task record.
```

### 7.3 Flow

Operational sequencing, branching, retries, and error handling.

```markdown
## Flow: CreateTask

### Summary

Persists a new task and emits the creation event.

### Steps

1. Validate input against the contract.
2. Persist the task — [mutates](aim:#Schema:Task).
3. Emit the creation event — [emits](aim:#Event:TaskCreated).
4. Return the persisted task.

### On Error

- Storage failures: surface as `PersistenceError` and emit no event.
- Event bus failures: persisted task is retained; emission is retried via outbox.
```

The flow's trigger (which contract invokes it) is **not** authored here — it is derived from the `invokes` edge declared at the contract or view that calls the flow (§8.4).

### 7.4 Persona

Actor identity, role semantics, and view access.

```markdown
## Persona: TaskOwner

### Role

- Authenticated user who owns one or more tasks.

### Access

- [accesses](aim:#View:TaskDashboard)
- May invoke [invokes](aim:#Contract:CreateTask), [invokes](aim:#Contract:CompleteTask)
```

### 7.5 View

Shared interface surfaces and user-visible actions.

```markdown
## View: TaskDashboard

### Summary

The owner's primary task list view.

### Display

- A list of [reads](aim:#Schema:Task) records grouped by due date.
- Completed tasks collapsed by default.

### Actions

- Create task — opens the creation form and [exposes](aim:#Contract:CreateTask).
- Complete task — [exposes](aim:#Contract:CompleteTask).
- Archive task — [exposes](aim:#Contract:ArchiveTask).
```

### 7.6 Event

Asynchronous payloads, emissions, and routing.

```markdown
## Event: TaskCreated

### Summary

Emitted when a new task is persisted.

### Payload

```aim-attrs
taskId: string required
ownerId: string required
createdAt: datetime required
```

### Routing

- Channel: `tasks.created`
- Durable: true
```

The event's emitters (`### Emitted By`) are **not** authored here — they are derived from the `emits` edges declared at the contracts/flows that emit the event (§8.4).

### 7.7 Trigger

Non-actor entry points: schedules, webhooks, and external origins that initiate behavior without a Persona or View. A Trigger is the source of a `triggers` edge into a Flow or Contract — which gives a cron job or inbound webhook a place in the graph, and gives the flow it starts a legitimate inbound edge (so it is not flagged as an orphan).

```markdown
## Trigger: NightlySweep

### Summary

Runs the stale-ticket sweep every night.

### Kind

- schedule

### Schedule

- cron: `0 2 * * *`

### Fires

- [triggers](aim:#Flow:EscalateStale)
```

A webhook or external origin sets `### Kind` to `webhook` / `external` and describes the source in prose instead of `### Schedule`. **Externally-originated events** need no special construct: model the origin as a Trigger that `triggers` an ingest Flow, and let that Flow `emits` the internal Event — the event then has a real emitter. Note: the `## Trigger:` *facet* defined here (an entry-point node) is distinct from v3.1's removed `### Trigger` *inverse block* (§8.3).

### 7.8 Summary Rule

Every facet block must carry an explicit `### Summary` sub-block immediately following the facet heading. `Persona` may omit the summary when it acts only as a role/access declaration.

---

## 8. Graph Edges

This section defines the typed edges that connect nodes. An edge is declared once, inline, at the node that *acts* — and the graph (§2.4) is derived by collecting edges across the project.

### 8.1 The Edge Token

A typed cross-reference is a standard CommonMark inline link whose link text is an edge **verb** and whose destination is an `aim:` URI carrying a node address:

```
[verb](aim:<address>)
```

- It renders on GitHub as a clickable link reading the verb (e.g. "invokes").
- It is LLM- and regex-parsable: `\[(\w+)\]\(aim:([^)]+)\)`.
- It is valid CommonMark with no raw HTML, honoring §3.8.

An **authoring shorthand** is permitted for same-component references: the verb followed by a backticked address, `invokes` `` `#Contract:CreateTask` ``. Tools normalize the shorthand to the canonical link form when deriving the graph. The shorthand is the smallest possible delta from what v3.1 authors already typed (`` `Contract: CreateTask` ``): prepend the verb, switch to the address form.

The **`from` node** of an edge is the nearest enclosing facet node of the line the token sits on (the Contract / Flow / View / Persona whose block contains it). The **`to` node** is the resolved address.

For a cross-component reference, the address is fully qualified:

```
- [invokes](aim:company.storage#Contract:PersistTask)
```

This subsumes the *use site* of a v3.1 `## Dependencies → Imports` alias: the import still declares the alias (§9), but the call site now points at a real node address, so a dangling import becomes checkable.

### 8.2 Closed Verb Taxonomy

There are ten **declared** verbs and two **derived** inverses. Each declared verb has a fixed from→to node-type schema. A verb used between disallowed node-types is a **hard error**.

| Verb | from | to | Meaning | Kind |
|---|---|---|---|---|
| `exposes` | view | contract | a View action surfaces a Contract to users | declared |
| `invokes` | flow, view, contract | contract, flow | runtime call into another behavioral unit | declared |
| `reads` | contract, flow, view | schema | reads a persisted entity | declared |
| `mutates` | contract, flow | schema | creates / updates / deletes an entity | declared |
| `emits` | flow, contract | event | produces an event | declared |
| `subscribes` | flow, contract, component | event | consumes an event | declared |
| `accesses` | persona | view, component | a persona may reach a view, or a whole screen/route component | declared |
| `navigates` | view | view | UI navigation between surfaces | declared |
| `triggers` | trigger | contract, flow | a schedule, webhook, or external origin initiates a behavioral unit | declared |
| `refs` | schema attr | schema attr | data-level foreign reference (the `ref()` modifier) | declared |
| `triggered-by` | flow, contract | contract / view / trigger | inverse of `invokes`/`exposes`/`triggers` | derived |
| `emitted-by` | event | flow / contract | inverse of `emits` | derived |

`requires` is **not** a graph verb — it stays as `## Dependencies → Requires` (a capability alias resolved by a mapping, §9). `extends` is **not** a graph verb — it is the `parent:` frontmatter relation (§5.1). **Render/layout composition** — a screen displaying another view inline (a dashboard laying out widget-panels) — is **not** a graph verb either: a UI piece has fluid granularity (`### Display` prose in its host view when simple, a promoted sub-intent owning its own facets once it earns them, §16.9), and the inline arrangement is realization expressed in code and bindings (§1.3), not an intent edge.

An `accesses` edge may target a **View** (access to one surface) **or** a **component** (route/screen-level access — the persona may reach that whole feature). Use the component form for role-gated screens that aggregate several views; `[accesses](aim:app.profile)` is valid and means "this persona may reach the profile screen."

### 8.3 Declared vs Derived

- **Declared once, at the acting end.** The node that performs the verb owns the edge: a View declares `exposes`/`navigates`/`reads`, a Flow declares `invokes`/`emits`/`reads`/`mutates`, a Persona declares `accesses`/`invokes`, a Contract declares `emits`/`mutates`/`invokes`, a Trigger declares `triggers`, a Schema attribute declares `refs`.
- **Inverse views are derived, never authored.** The v3.1 blocks `### Trigger` ("Invoked by Contract: X") on a Flow and `### Emitted By` on an Event are inverse projections of `invokes`/`emits` edges. v4 removes them from authored source. A tool may render them as read-only views.

This is the structural fix for v3.1's "three inconsistent expressions" problem: there is now exactly one authoritative direction per relation, so the forward and backward statements can never fall out of sync.

### 8.4 Inverse Derivation

For every declared `invokes`/`exposes` edge `A → B`, the graph contains a derived `triggered-by` edge `B → A`. For every declared `emits` edge `A → E`, the graph contains a derived `emitted-by` edge `E → A`. Derived edges are computed during graph derivation (§2.4 step 4) and are available to tooling and reviewers exactly like declared edges, but they never appear in source.

If an author writes a `### Trigger` or `### Emitted By` block anyway (e.g. migrated content not yet cleaned up), tools reconcile it against the derived set and emit an informational "redundant inverse, possibly stale" diagnostic on mismatch.

### 8.5 Before / After

The `View: TodoDashboard` facet from the canonical example, v3.1 prose vs v4 graph projection:

**v3.1:**

```markdown
### Actions

- Submitting the "New Task" form → invokes `Contract: CreateTodo`.
- Tapping the checkbox on a PENDING task → invokes `Contract: CompleteTodo`.
```

**v4:**

```markdown
### Actions

- Submitting the "New Task" form — [exposes](aim:#Contract:CreateTodo)
- Tapping the checkbox on a PENDING task — [exposes](aim:#Contract:CompleteTodo)
```

Both forms render on GitHub. The v4 form additionally yields two first-class edges `View:TodoDashboard → exposes → Contract:CreateTodo|CompleteTodo`, so renaming a contract dangles the edge (hard error), an orphan check confirms every contract is exposed, and the impact set of either contract now formally includes the view. The free prose ("Submitting the New Task form") survives as the human label; only the edge is now machine-recognizable.

---

## 9. Dependencies, Requirements, And Mappings

### 9.1 Dependencies Block

External providers and required capabilities are declared in a `## Dependencies` block:

```markdown
## Dependencies

### Imports

- `company.storage.Contract` as Storage
- `company.events.EventBus` as EventBus

### Requires

- Identity as AssigneeUsers
```

- **Imports** reference concrete provider surfaces from other components. An import declares an alias; the *use site* is a cross-component edge token (§8.1) whose address names the real node.
- **Requires** declares required capabilities by alias (the `requires` relation). The alias is resolved via a mapping file.

### 9.2 Requirement Surfaces

Required capabilities may be documented inline with a `## Requirement: <Alias>` block:

```markdown
## Requirement: AssigneeUsers

### Summary

Capability required to resolve user identities.

### Operations

- `ResolveUser(id) -> UserRecord`
```

### 9.3 Mapping Files

Mappings bind required aliases to concrete providers. They live under `/aim/mappings/<component>/` and use `facet: mapping`.

```markdown
---
aim: juice.tasks
facet: mapping
---

# Tasks Mappings

## Map: AssigneeUsers

### Target

- `company.identity`

### Operation Map

- `AssigneeUsers.ResolveUser` → `company.identity.ResolveUser`
```

Unresolved `Requires` aliases are hard errors at validation time.

**Mappings vs bindings.** A mapping is an **intent→intent** capability binding: it resolves a required-capability alias to a concrete provider *component*. A binding (§10) is an **intent→code** realization binding: it links an intent node to the *source code* that implements it. They are distinct facets with distinct directories (`mappings/` vs `bindings/`) and must not be confused.

---

## 10. Binding Layer

A binding records *where* an intent node is realized in code, so the Reviewer can diff the declared intent graph against the realized code graph (§13). Bindings are optional: a component with no bindings is a valid Level 1/2 component (§11.2). Bindings raise fidelity, exactly as facets do.

### 10.1 Drift As Graph-Diff

Two graphs:

- **Declared graph (D)** — nodes are AIM components/facets; edges are the typed relations of §8. Authored by the Architect; behavioral authority.
- **Realized graph (R)** — nodes are code sites (functions, files, routes, tables, topics); edges are relations recovered from the code (this handler writes that table; this route calls that handler; this handler publishes that topic).

A **binding** connects a node in D to a node in R. Drift detection projects D and R into a common space through the bindings and diffs them.

**Building R is bounded, not global.** A tool does **not** statically analyze the whole codebase to reconstruct R. Bindings localize the work: for each *declared* edge, the Reviewer opens the *bound site* and checks that one claim — "does `src/todos/create.ts#createTodo` actually mutate `Ticket` and emit `TicketCreated`?" That is read-the-bound-file, not map-the-system, and it is **polyglot by default** (an agent reads any language, where a static analyzer needs one parser per language; dynamic code that defeats static analysis can still be reasoned about and flagged). Because R is *inferred* this way, every graph-diff finding carries a **confidence** (§13.3). Tooling that *does* have static analysis MAY supply a precomputed **realized-graph manifest** for deterministic diffing — this spec does not define that manifest's format; it is an ecosystem concern.

### 10.2 Binding Notation And Location

A binding target is a portable **code-locator URI**, written as inline code:

```
src/todos/create.ts#createTodo        # file # symbol  (functions, classes, methods)
src/todos/create.ts                    # file only      (a whole module realizes a node)
src/todos/create.ts#L40-L72            # file # line span (last resort; lines drift fastest)
route:POST /api/todos                  # HTTP endpoint
topic:todos.created                    # message / event channel
table:todo_items                       # database table / model
```

A binding line is a normal Markdown bullet:

```markdown
- binds: `src/todos/create.ts#createTodo` — kind: handler
```

`kind` (`handler | model | component | route | topic | test`) is optional and advisory. One node may declare multiple bindings (a Contract realized by both a route and a handler). Everything after the backticked locator is prose a tool may use but the parser may ignore.

**Where bindings live: a dedicated `facet: binding` file under `/aim/bindings/<component>/`.** Realization is not behavior (§1.3), and code paths drift faster than intent — isolating bindings keeps the behavioral file's diffs meaningful and lets a binding go stale without the intent being wrong. This mirrors how `facet: mapping` separates capability bindings.

```markdown
---
aim: nemicko.demo.todo
facet: binding
---

# TaskManager Bindings

## Bind: Contract CreateTodo

- binds: `src/todos/create.ts#createTodo` — kind: handler
- binds: `route:POST /api/todos` — kind: route

## Bind: Schema TodoItem

- binds: `src/models/todo.ts#TodoItem` — kind: model
- binds: `table:todo_items` — kind: table

## Bind: Event TodoCreated

- binds: `topic:todos.created` — kind: topic
```

**Bindings always live in a `facet: binding` file — there is no inline binding form.** Keeping realization out of the behavioral files is the whole point (§1.3): a code path may rot without making the intent wrong, and a behavioral file never carries a volatile `file#symbol` path. (An early v4 draft allowed an inline `### Realized By` escape hatch for trivial components; it was removed — the lazy path muddied the behavior≠realization boundary, so bindings are separate, full stop.)

### 10.3 Optional-Capability Invariant

- A component with no binding facet is fully valid (Level 1/2). Binding coverage is reported as informational, never a hard error.
- Bindings become load-bearing only at Level 3 graph-diff — which the author opted into by writing the bindings. You are never punished for a binding you did not write.

---

## 11. Resolution And Synthesis

### 11.1 Canonical Resolution Algorithm

This algorithm is **authoritative**. All other sections that describe resolution (notably §5.4 for sub-components and §9.3 for mappings) defer to this order. It resolves both unqualified facet names and full node addresses (§2.2).

For any reference within a component:

1. **Component part.** If the address carries a component prefix, resolve to that exact namespace (which must exist). If absent, the component is the current one.
2. **Facet name**, resolved within the chosen component in this precedence order:
   1. **Embedded** — a facet block in the same intent file.
   2. **Sibling facet file** — `<component>.<facet>.aim` next to the intent file.
   3. **Explicit Imports** — entries under `## Dependencies → Imports` in the current file. Explicit author intent beats implicit parent inheritance.
   4. **Parent chain** — facets defined in the parent component, then the grandparent, and so on up the namespace until a match is found or the chain ends.
   5. **Required alias via mapping** — names declared under `## Dependencies → Requires`, resolved through a mapping file (§9.3).
   6. **Absent** — the name does not resolve. If it was required by another facet or edge, this is a hard error.
3. **Type agreement.** If the reference is an address with a `FacetType` (e.g. `#Contract:X`), the resolved node's type must match. A `#Contract:X` that resolves to a `## Schema: X` is a hard error.
4. **Sub-block part.** If the address carries `→ ### Sub [n]`, resolve within the facet node by heading text and 1-based list index. An out-of-range index is a hard error.

The first match wins. Lower-precedence sources for the same name emit an informational diagnostic ("shadowed by higher-precedence source"). Tools must implement this exact order — there are no implementation-defined variations.

### 11.2 Specification Levels

- **Level 1** — Intent only. Useful for early exploration and simple components.
- **Level 2** — Intent plus some facets and edges. Most production components.
- **Level 3** — Full facet trace **with bindings present**, so the declared graph can be diffed against the realized code graph. Highest fidelity for implementation and review.

The level affects expected implementation precision, expected code-generation precision, and strictness of traceability and graph-diff checks. Tools may report a component's level as an informational diagnostic. Level 3 is the precise condition under which an unbound declared node becomes an enforceable finding (§13). Level-3 graph-diff is enforced by the Reviewer verifying each edge at its bound site with a confidence (§10.1, §13.3), or by a supplied realized-graph manifest.

### 11.3 Traceability Chain

The traceability chain is the set of typed declared edges through the behavioral facets:

```
Persona → View → Contract → Flow / Schema / Event
```

- Entry points are a **Persona** (actor, `accesses` a View or screen component) **or** a **Trigger** (schedule/webhook/external, `triggers` a Flow/Contract).
- `Persona` `accesses` `View` (or a whole screen component).
- `View.Actions` `exposes` `Contract`.
- `Contract` `invokes` `Flow`.
- `Contract` and `Flow` `read`/`mutate` `Schema`.
- `Contract`/`Flow` `emits` `Event`.

In v3.1 this chain was prose and "a useful target, not a requirement." In v4 it is **derived from the declared edges** and therefore checkable: a Level-3 component is exactly one whose chain has no orphan nodes and no dangling edges (§13). Intent-only components remain valid; tools emit a reduced-fidelity informational note.

---

## 12. Distribution

AIM components may be packaged and shared, but **distribution is not part of this specification.** Discovery, fetch, and publishing are handled by tooling outside this repository — typically an external, database-backed catalog. This section defines only what makes a package *well-formed* as an AIM artifact and how versions coexist; it does not define a registry-index file format, a CLI, or a publishing flow.

### 12.1 Well-Formed Package

A distributable package has a single root component. It is well-formed when:

- It has exactly one root `facet: intent` file as its entry (sub-components have their own intent files, but only the root is the entry).
- The entry's frontmatter `aim` matches the package's advertised name, and `facet` is `intent`.
- Its declared intra-graph references resolve: every `## Bind:` target and every edge token addressing a node *within the package* names a node that exists. A dangling intra-graph reference is a hard error. (References to a *consumer's* code via binding locators cannot be checked inside the package, since a package ships intent, not the consumer's code.)

A package advertises its release version and its `aim_version` (the language version it conforms to) through the catalog, not through any field inside the `.aim` files — `.aim` files carry no version (§3.2).

### 12.2 Single-Version Projects

A catalog may serve packages of multiple AIM versions side by side. A **working project**, however, is single-version: its `/aim/` tree is wholly one AIM version, because graph-diff requires one consistent model. Installing a package authored against an older version into a newer-version project requires migrating it first (§14) — a project never mixes versions. Installed sources live as local files under `/aim/` so all implementation, review, and code generation run locally.

---

## 13. Tooling Diagnostics

**Conformance and diagnostics are evaluated over the complete derived project graph** — every `.aim` file resolved together (§2.4) — never a single file. A component is "clean" only when the whole graph it participates in is: duplicate entities, dangling references, and orphans are cross-file properties, so judging one file in isolation is never sufficient.

### 13.1 Hard Errors

- Missing or malformed frontmatter.
- Missing required frontmatter fields (`aim`, `facet`).
- Frontmatter `aim` does not match the file path.
- `parent:` declared but no parent intent file exists.
- Missing H1 heading, missing `## Requirements`, or empty `## Requirements`.
- Invalid facet type in heading (e.g. `## Data: X`).
- Duplicate facet definitions with the same name within the effective source.
- Ambiguous sub-component authority (auto-discovered sub-component not in explicit `## Subcomponents` list).
- Unresolved `Requires` aliases with no matching mapping.
- Sub-component facet name collision with a parent facet name (when the parent definition is authoritative).
- Generic filenames (`intent.aim`, `schema.aim`, `mapping.aim`, `binding.aim`).
- **Dangling reference** — an edge token's `to` address resolves to Absent (§11.1). Same class as an unresolved `ref()`.
- **Type-mismatch reference** — an edge target resolves but its node-type ≠ the address's `FacetType`, or the `(verb, from, to)` triple is not in the §8.2 schema.

### 13.2 Informational Diagnostics

- Missing optional `## Tests`.
- Intent-only component (no facets).
- Lower-precedence facet source shadowed by a higher-precedence one.
- Sub-component nesting exceeding three levels.
- Unresolved `Import` alias (not blocking but flagged for repair).
- **Orphan node** — a facet node with no inbound edges of its expected kind: a Contract no View `exposes` and nothing `invokes`/`triggers`; an Event nothing `emits`; a View no Persona `accesses`; a Trigger with no outbound `triggers`. (A Flow or Contract entered via `triggers` or `subscribes` has a valid inbound edge and is not an orphan.)
- **Stale inverse** — an authored `### Trigger`/`### Emitted By` block disagrees with the derived inverse set (§8.4).
- **Probable duplicate entity** — two nodes with the same facet-type and name in components not linked by an import or reference (e.g. `auth#Schema:User` and `billing#Schema:User`). Same name is not proof of same entity, so this is a smell, not a hard error: the remediation is to make one canonical and reference it (§16.8), or to confirm they are genuinely distinct.
- **Over-embedded intent file (monolith)** — an intent file that embeds many facets, especially shared ones used across components, instead of extracting them into sibling facet files or a `<app>.core` component (§16.2, §16.8). The dual of duplication: both fragment maintainability at scale. A smell, not a hard error.

### 13.3 Graph-Diff Findings (Reviewer)

When bindings are present, the Reviewer diffs the declared graph against the realized code graph and produces drift findings. These map onto the Reviewer's existing missing / incorrect / undocumented kinds:

| Finding | Meaning | Severity / owner |
|---|---|---|
| `UNBOUND_NODE` | declared node has no binding | informational at Level 1/2; MISSING at Level 3 |
| `DANGLING_BINDING` | binding points at code that no longer exists | INCORRECT → Developer |
| `MISSING_EDGE` | declared edge has no realized counterpart at the bound site | MISSING → Developer |
| `EDGE_MISMATCH` | edge exists on both sides but endpoints differ | INCORRECT → Developer |
| `UNDECLARED_EDGE` | realized code has an edge with no declared counterpart | UNDOCUMENTED → Architect |
| `AMBIGUOUS_BINDING` | one node binds to conflicting sites, or two nodes bind the same site | ambiguous → user input |

Because R is inferred by reading the bound code (§10.1), **every finding carries a confidence** — `high` (the bound code clearly matches or clearly does not) or `needs-human-check` (dynamic or ambiguous code the Reviewer could not settle). A `clean` drift report (`status: clean`) means the declared and realized graphs are isomorphic through the declared bindings *at the stated confidence* — a materially stronger guarantee than "no prose mismatch found," but only as strong as the confidence attached. The **impact set** (the nodes reachable from a changed node along inbound edges) is not a violation but a reporting capability, and is the headline payoff of the derived graph.

---

## 14. Migration From v3.1

v4 is a breaking change. Migration tooling (outside this specification) converts v3.1 sources to v4 by:

1. **Relabel.** Update `AGENTS.md` frontmatter `aim_version: 3.1` → `4`; update the body's version references. The `.aim` extension does **not** change (unlike the v2.2→v3.1 `.intent`→`.aim` rename).
2. **Strip per-file version/spec.** Remove any lingering `version:`/`spec:` keys from `.aim` frontmatter. Fully automatable.
3. **Prose mentions → typed edges.** v3.1 already expresses the chain in recognizable patterns: backticked facet references inside `### Actions`, `### Ensures`, `### Emitted By`, `### Trigger`, and `CALL X.Y` lines in `### Steps`. A migration pass deterministically pre-extracts edges from these patterns and proposes them; edges implied only by free prose require an LLM-assisted pass with Architect confirmation. **Edges are never silently invented.**
4. **Delete derived inverse blocks.** Remove `### Trigger` and `### Emitted By` once their forward edges are declared (§8.4).
5. **Bindings are not generated by migration.** Migration leaves components at Level 1/2 (valid, §10.3). A separate code-reading pass (Developer- or tool-driven) proposes bindings against actual code afterward, raising a project to Level 3 without migration ever assuming code exists or is correct.

A project's `/aim/` tree must be wholly one AIM version (§12.2). The migration is one-shot per project. Projects still on v2.2 migrate v2.2 → v3.1 first (see the v3.1 spec), then v3.1 → v4.

---

## 15. Conformance Examples

### 15.1 Minimal Valid Component

```markdown
---
aim: demo.snake
facet: intent
---

# Snake

## Summary

A single-player snake game.

## Requirements

- The snake grows when it eats food.
- Wall and self-collision end the run.
```

### 15.2 Component With Sub-Components

```
/aim/game.snake/
  game.snake.aim              # parent: shared schemas, index
  game.snake.schema.aim       # shared SnakeState, FoodPellet
  tick/
    game.snake.tick.aim
  collision/
    game.snake.collision.aim
  score/
    game.snake.score.aim
```

### 15.3 Invalid

- Frontmatter missing `aim:` or `facet:` field.
- `## Data: Foo` heading (invalid facet type).
- Sub-component file with `parent: juice.tasks` but no parent intent file exists.
- Two `## Schema: Task` blocks in the same effective source.
- Project missing `AGENTS.md` with declared `aim_version`.
- A directory named `aim/specs/`, `aim/mappings/`, or `aim/bindings/` used as a component namespace.
- An edge token `[invokes](aim:#Schema:Task)` (invalid: `invokes` cannot target a `schema`).
- An edge token whose target address resolves to no node (dangling reference).

---

## 16. Practical Guidance

### 16.1 Default Authoring Rule

Start by splitting. Create the parent intent with the cross-cutting requirements and shared schemas. Create each feature as a sub-component. Keep each sub-component focused on a single observable behavior. Declare edges inline as you write each facet (a View's actions `expose` contracts; a Flow `mutates` schemas and `emits` events). Collapse into a single file only when the whole component is trivially small.

### 16.2 What Goes In The Parent

The parent intent file is a **lean index**, not a container:

- Cross-cutting requirements that apply system-wide.
- The `## Subcomponents` index.
- Dependencies.

Shared **facets** — schemas, personas, views referenced by multiple components — are authored as their **own files**, never embedded en masse in the parent: a sibling facet file (`<component>.schema.aim`, `<component>.persona.aim`, `<component>.view.aim`) for what's shared within a subtree, or a `<app>.core` component (§16.8) for entities shared *across* top-level components. Embedding many facets into one intent file produces a **monolith** (§13.2) — the dual of the duplication problem, and just as damaging at scale.

### 16.3 What Goes In A Sub-Component

- The intent, requirements, and tests for a single feature.
- Contracts and flows specific to that feature, with their edges.
- Sub-component-specific events.

### 16.4 When To Split A Sub-Component Further

When a sub-component itself has multiple distinct behaviors with their own contracts. Example: a `payments` component might split into `charge`, `refund`, `dispute` sub-components, and `dispute` itself might split into `open_dispute`, `respond_to_dispute`, `resolve_dispute` if each has its own contract. Three nesting levels is the practical maximum.

### 16.5 When To Add Bindings

Add bindings once code exists and you want enforceable drift detection. Bind the stable nodes first (Contracts to handlers/routes, Schemas to models/tables, Events to topics). A binding facet turns the Reviewer's drift report from prose comparison into a graph-diff (§13). Skip bindings while a component is still exploratory — Level 1/2 is valid.

### 16.6 Closed-Loop Workflow

1. Requirements → intent (sub-components first, parent as index), with typed edges declared inline.
2. Intent → implementation, reading the resolved graph; Developer emits bindings for the code it writes.
3. Implementation → graph-diff validation against the declared graph through the bindings.
4. Validation failures → code repair or intent revision, routed by the finding's owner.
5. New requirements → new sub-component or revised parent; new edges declared at the acting nodes.

The intent is the contract. Code follows intent. When they diverge, one of them is wrong and the divergence is resolved explicitly.

### 16.7 Triggers, Schedules, And Orchestration

- **Non-actor entry points** — cron jobs, schedules, polling loops, webhooks, external systems — are modeled with a `## Trigger:` facet (§7.7) and a `triggers` edge into the Flow or Contract they start. This is what gives a nightly job or an inbound webhook a place in the graph; without it, the flow it starts would look like an orphan.
- **External events** need no new machinery: model the origin as a Trigger that `triggers` an ingest Flow, and let that Flow `emits` the internal Event. The event then has a real emitter and subscribers attach as usual.
- **Sagas and long-running orchestration** are expressible with existing verbs: the orchestrator Flow `invokes` each step, `mutates` a saga-state Schema to track progress, and `emits`/`subscribes` compensation Events. AIM captures the *intent* of the orchestration, not the durable-timer/signal semantics of a workflow engine — those remain an implementation detail bound to code.

### 16.8 Shared Entities And Canonicalization

The fastest way a large project rots is duplication: the same `User` (as a `Schema` and as a `Persona`), the same `Money`, the same `Status` reborn in file after file as each component is authored in isolation — and then the copies drift and contradict. Two rules keep the graph single-sourced:

- **Resolve-or-reference, never regenerate.** Before defining a `Schema`, `Persona`, or any entity, the Architect **searches the project graph** for an existing node of that kind and name. If one exists, reference it (a `## Dependencies → Imports` alias plus the edge) instead of defining a new one. The derived graph is a queryable index precisely so this lookup is cheap — use it. Agents default to *generating*; the discipline is to *look first*.
- **Give cross-cutting entities one canonical home.** A parent holds what's shared within its subtree (§16.2). For entities shared *across* sibling top-level components (`auth`, `tasks`, `billing` all needing `User`), designate one shared component — by convention `<app>.core` — as the single definition site, and have the others import from it. One `User`, many references.

Tooling supports this from both ends: the **probable-duplicate diagnostic** (§13.2) surfaces same-type-same-name nodes that are not reference-linked, and the derived graph lets you list every definition of an entity to spot drift. Detection plus discipline is what keeps identity from fragmenting as the system grows — and it is only possible *because* the graph turns "every entity in the project" into something you can query.

Beware the **opposite trap**: do not dodge duplication by embedding every entity in one file. That just trades duplication for a monolith — equally damaging, and a real failure mode in practice (an agent told to avoid duplicate `User`s will happily cram all 20 schemas into one parent). The rule is *both*: don't duplicate **and** don't monolith. Shared facets live in their own files and the parent stays a lean index (§16.2); a canonical entity that consumers cannot reach by upward resolution must be importable (put it in an ancestor or `<app>.core`, not a sibling).

### 16.9 UI Composition And Fluid Granularity

A UI piece — a tab, a panel, a widget — has **fluid granularity**, exactly like any other capability. It is not a fixed kind of node in the model; what it *is* depends on how much behavior it carries, and it moves between forms by the **promote** transform (§17):

- **Trivial / behavior-less** — a static or host-fed panel with no contract, schema, or action of its own is **not a node**. It is a bullet in the host `## View:`'s `### Display`. Modeling it as its own facet adds a node the graph cannot check — nothing to dangle, nothing to impact — and earns it a false orphan diagnostic (§13.2).
- **Carries its own behavior** — once the piece acquires its own data, operations, or surface (the §4.3 test — a fetch contract, a schema, an action), it is **promoted** into its own sub-intent (§5, §17.2) that owns those facets. It rejoins the hierarchy through `extends` (the `parent:` relation) and connects to its host through the view edges that already exist: the host `## View:` `reads` the piece's schema, `exposes` or `invokes` its contract, or `navigates` to it when it is a separate destination rather than an inline part.

**Composition itself is not an intent relation.** That a host screen *lays out* a constituent view inline — as opposed to navigating to it or invoking its behavior — is realization: it lives in code and, where it matters, bindings (§1.3, §8.2). The intent graph models the piece's *behavior* and *reachability*, never its placement on the screen. This is the line §16.7 draws for orchestration: AIM captures intent, not rendering mechanics.

**Worked example — the promote boundary.**

*Simple.* An `AdminDashboard` shows a current-conditions panel. The reading is host-supplied; the panel has no behavior of its own. It is one line in the dashboard's `### Display`:

```markdown
## View: AdminDashboard

### Summary

The operator's control surface.

### Display

- System counters and a current-conditions panel.
```

*Grown.* The panel now fetches live weather and persists a reading — it has acquired a contract and a schema, crossing the §4.3 line. It is **promoted** to its own sub-intent, which owns the behavior:

````markdown
---
aim: app.admin.weather
facet: intent
parent: app.admin
---

# Weather

## Summary

Current-conditions data for the operator console.

## Requirements

- The console can fetch and display the latest weather reading.

## Contract: FetchWeather

### Summary

Fetch the latest reading for the operator's locale.

### Ensures

- Returns the latest reading — [reads](aim:#Schema:WeatherReading).

## Schema: WeatherReading

### Summary

A single current-conditions reading.

### Attributes

```aim-attrs
tempC: number required
condition: string required
observedAt: datetime required
```
````

The dashboard surfaces that behavior with edges it already has — no composition verb required:

```markdown
## View: AdminDashboard

### Display

- System counters and a current-conditions panel from the latest [reads](aim:app.admin.weather#Schema:WeatherReading), refreshed via [exposes](aim:app.admin.weather#Contract:FetchWeather).
```

The promote boundary is the §4.3 test: display-only ⇒ prose in the host; owns data or operations ⇒ its own sub-intent. A promoted piece that is *only* ever embedded usually should **not** declare its own `## View:` — its surface is the host's — so it owns `Contract`/`Schema` and raises no orphan. If it genuinely needs its own reusable surface, the informational orphan diagnostic (§13.2) is the correct nudge: either a Persona `accesses` it, or its surface really belongs to the host.

---

## 17. Intent Evolution

The static rules (§2–§13) define what a *well-formed* model looks like at rest. This section defines how a model *changes* while staying well-formed — the dynamics those rules imply but do not state.

### 17.1 One Root Unit, Two Authoring Operations

The root unit of authoring is the **intent** — a component or sub-component, each with its own intent file (§1, §5). Facets and typed edges are how an intent is *expressed*; they are never the unit an author works in. Everything an author does to a model is one of exactly two operations:

- **EXTEND** an existing intent — add or refine its facets and the edges among them.
- **ADD** a new intent — a new sub-component or capability (§5).

These two operations are the surface a requirements author — often a non-developer, working through the Architect role (§1.2) — designs at; the facet, edge, and binding detail they expand into is where the Developer and Reviewer work. An author does not "move a node" or "rename a schema" as a primitive act; those are *transforms* (§17.2) the system performs to keep the model well-formed as the two operations push against the decomposition rules (§4.3).

### 17.2 Validity-Preserving Transforms

When an EXTEND or ADD would leave the model ill-formed — an intent grown past "one clear behavior" (§4.3), a node living in the wrong namespace, two nodes that are the same concept — the system reshapes the graph with a **transform**. A transform is not new syntax and not an author primitive: it is an operation **defined by the pre/post invariants of §17.3**, producing a spec-valid state from a spec-valid state. Tools and the Architect agent apply transforms; authors express intent.

| Transform | What it does | Typically triggered by |
|---|---|---|
| **promote** | a capability grown inside an intent splits out into its own sub-intent (§5) | an EXTEND that crosses the §4.3 "one clear behavior" line |
| **split** | one intent doing two things becomes two sibling sub-intents under an index parent | a component with multiple distinct behaviors (§16.4) |
| **re-home / move** | a node moves to the intent whose namespace it belongs to | a node whose address namespace does not match where it is used |
| **merge** | two nodes that are the same concept collapse into one canonical node | a probable-duplicate diagnostic (§13.2) confirmed as a true duplicate |
| **rename** | a node's name — and therefore its address — changes | a clearer name, or a collision |

Each transform changes one or more node **addresses** `<component>#<FacetType>:<Name>` (§2.2). `promote` is the bridge between the two operations: an EXTEND that trips §4.3 *resolves structurally into an ADD* — the new capability becomes its own sub-intent rather than more facets piled on the parent (§16.2).

### 17.3 Transform Invariants (Normative)

Because a transform changes addresses, it MUST re-establish every part of the model that addresses anchor. A transform that violates any of the following yields an ill-formed model and MUST NOT be applied as-is:

1. **No dangling edges; legal triples preserved.** Every typed edge whose `to` address targets a moved or renamed node MUST be re-pointed to the node's new address. After the transform the graph MUST contain zero dangling references (§13.1) introduced by the change, and every re-pointed edge MUST still satisfy its `(verb, from, to)` schema (§8.2). Edges are declared at the acting end (§8.3), so inbound edges live in *other* nodes' blocks and MUST be found across the whole project graph (§13), not just the moved file.

2. **Elided outbound addresses MUST be re-qualified on a cross-component move.** A node's own outbound edges travel with it, but any written in the elided unqualified form `#<FacetType>:<Name>` (§2.2) resolve against the *new* component after a move. Where that would change the target, the transform MUST re-qualify the address to its original fully-qualified target so the edge's meaning is preserved.

3. **The parent index MUST be updated.** `promote`, `split`, and a cross-parent `move` change the set of sub-components; each affected parent's `## Subcomponents` index (§5.2) MUST be updated to match what is on disk, or auto-discovery (§5.3) diverges from the explicit list — a hard error.

4. **Path/header identity MUST be re-established.** A node that becomes, or moves into, its own component MUST have its directory, filename, and `aim:`/`parent:` frontmatter brought back into agreement (§4.4); a path/header mismatch is a hard error.

5. **Bindings follow the node.** Any `## Bind:` entry (§10.2) for a moved or renamed node MUST move to the binding file of the node's new component, with its `## Bind: <FacetType> <Name>` heading updated to the new name. The **code locator is unchanged** — the code did not move, only the intent address did. This is precisely why bindings are separate files (§1.3): an intent transform reshapes addresses without touching code.

6. **`merge` is author-confirmed and collapses, never silently unifies.** Because same-name is not proof of same-entity (§13.2), `merge` MUST be confirmed by the Architect. On merge the duplicate node is removed, one node is designated canonical (§16.8), and every edge that targeted either node is re-pointed at the canonical node under invariant 1.

### 17.4 A Transform Is a Graph-Diff

A transform yields a **structured graph-diff** — nodes added / removed / moved, edges re-routed, bindings relocated — of exactly the kind the Reviewer already computes (§2.4, §13.3). This is the payoff of the derived graph: reshaping intent is a *traceable diff*, not an opaque rewrite. The Reviewer reports the diff; the Developer applies the corresponding code moves (a `rename` that changes a Contract's address tells the Developer, through the bindings, precisely which handlers and routes are implicated). The **impact set** (§13.3) of a transform is computable before it is applied.

### 17.5 Choosing the Transform (SHOULD)

- **When EXTENDING, watch the §4.3 line.** If an addition is a distinct capability with its own data, operations, and surfaces, **promote** it into a sub-intent rather than piling facets onto the parent (§16.2 — the parent stays a lean index). Adding facets to an already-multi-behavior intent is how monoliths form (§13.2).
- **Re-home when the namespace doesn't fit.** If a node's address namespace does not match where it is used, **move** it to the intent it belongs to rather than referencing it across an unnatural boundary.
- **Merge duplicates into a canonical home.** When the probable-duplicate diagnostic (§13.2) flags a true duplicate, **merge** to one canonical node (§16.8) — do not let the copies drift.
- **A UI piece that earns behavior promotes.** A view fragment (tab, panel, widget) that acquires its own data or operations crosses the §4.3 line and is **promoted** into a sub-intent (§16.9) rather than remaining inline `### Display` prose.

**Worked example — an EXTEND that promotes.** A CRM has `crm.customer_management`, one intent covering customer CRUD. New requirement: "add customer notes, with edit history." Notes are a distinct capability — their own `Note` schema, their own create/edit/list contracts, their own surface. Piling a `## Schema: Note`, three contracts, and a notes view onto the parent would push it past §4.3, so the EXTEND **promotes** into a new sub-intent:

```
/aim/crm.customer_management/
  crm.customer_management.aim                    # parent index — ## Subcomponents now lists customer_notes
  customer_notes/
    crm.customer_management.customer_notes.aim   # new sub-intent: Note schema, contracts, view
```

The customer-detail view's reference to the notes surface is declared as a cross-reference to the promoted address; the parent's `## Subcomponents` index gains a `customer_notes` line (invariant 3).

**Worked example — a split.** A flat `crm.customers` intent has accreted both per-customer CRUD *and* customer-group management — two distinct behaviors. **split** turns it into two sibling sub-intents under an index parent:

```
/aim/crm.customers/
  crm.customers.aim              # was the flat file; now a lean index (§16.2)
  records/
    crm.customers.records.aim    # per-customer CRUD
  groups/
    crm.customers.groups.aim     # customer-group management
```

Every edge that pointed into the old flat file is re-pointed to whichever sub-intent now owns the target (invariant 1); shared schemas stay in the parent or move to a sibling facet file (§16.2); bindings for the moved contracts relocate to the new components' binding files with code locators unchanged (invariant 5).

### 17.6 Diagnostics

Intent Evolution adds **no new diagnostics**. A transform is correct exactly when the resulting graph raises no new hard error (§13.1) and no new orphan / shadow / duplicate / monolith smell (§13.2) attributable to the change. The invariants of §17.3 are the conditions under which that holds — which is the point: the static checks the spec already defines are the acceptance test for every transform.
