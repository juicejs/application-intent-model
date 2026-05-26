# Application Intent Model (AIM) v3.0

Application Intent Model (AIM) is an intent-driven specification language for humans and AI coding agents. It captures product behavior in a form readable enough for product and design discussion and structured enough for implementation, review, repair, and deterministic code generation.

AIM v3.0 is a **breaking change** from v2.2. The motivation is to make AIM the single authoritative artifact that AI coding agents read and write — replacing the ad hoc sprawl of PRDs, design notes, READMEs, and plan files that agents otherwise generate. The three structural shifts that drive v3.0:

1. **Markdown-native syntax.** Files are now valid Markdown so they render on GitHub, in IDEs, and in any LLM context with no special tooling.
2. **Self-describing headers.** Every file carries a `spec:` URL so an agent encountering AIM for the first time can fetch the specification and self-bootstrap.
3. **Sub-component-first authoring.** Real applications are decomposed into small, focused sub-components by default. The "single file first" default of v2.2 is inverted: split as the norm, collapse only when the component is genuinely small.

AIM is the authoritative shared artifact between humans and coding agents. Implementation, review, and repair all run against AIM. When implementation and intent disagree, the mismatch is resolved explicitly — either by fixing code or by revising intent.

---

## 1. Core Model

A component is identified by a dotted namespace such as `juice.tasks` or `game.snake`. Sub-components extend the namespace: `juice.tasks.create_task` is a sub-component of `juice.tasks`.

Each component has:

- one required **intent file** (a `.intent` file with `facet: intent`)
- zero or more optional **facets**: `schema`, `flow`, `contract`, `persona`, `view`, `event`
- zero or more optional **sub-components** (each is a component in its own right)
- zero or more optional **mapping files** (`facet: mapping`)

The intent file is the canonical entrypoint. All other detail attaches to it directly (embedded), indirectly (sibling facet files), or through sub-components.

### 1.1 What Changed From v2.2

| Concern | v2.2 | v3.0 |
|---|---|---|
| File syntax | Custom DSL with braces and uppercase keywords | Markdown with YAML frontmatter |
| Header | Single line: `AIM: name#facet@x.y` | YAML frontmatter with `spec:` URL |
| Authoring default | Single file first, split when it hurts | Split by default, collapse when trivial |
| Sub-components | Not modeled | First-class with parent/child resolution |
| Cold-start discovery | Requires AIM-aware tooling | Any agent can fetch `spec:` URL |

### 1.2 Agent Roles

v3.0 uses three mainstream roles that map onto how real software teams already work:

- **Architect** — translates requirements into intent files. Owns the specification.
- **Developer** — implements code and tests from intent. Fixes code when drift is found.
- **Reviewer** — checks implementation against intent and reports drift.

Roles are workflow guidance, not language constructs — they do not appear in `.intent` source files. A single agent may perform multiple roles, and multiple agents may share one role. See [`PROMPT.md`](./PROMPT.md) and [`agents/`](./agents/) for concrete prompt templates.

Repair is a verb, not a separate role. When the Reviewer flags drift, either the Developer fixes the code or the Architect revises the intent. The decision is explicit, not silent.

Normative behavior across all roles:

- The Developer must not invent material behavior absent from intent.
- When detail is missing, preserve documented intent and minimize assumptions.
- Assumptions are surfaced for review or converted into explicit intent updates by the Architect.
- When implementation and intent disagree, the mismatch is resolved — Developer fixes code if implementation is wrong, Architect revises intent if specification is outdated.

---

## 2. File Format

### 2.1 Extension

All AIM source files use the `.intent` extension. The extension is retained from v2.2 as an identity marker: a file named `*.intent` is an authoritative AIM artifact, not a generic note.

Files are valid CommonMark Markdown with YAML frontmatter. Any Markdown renderer will display them correctly.

### 2.2 Header (YAML Frontmatter)

Every `.intent` file must begin with a YAML frontmatter block:

```yaml
---
aim: juice.tasks.create_task
facet: intent
version: 3.0
spec: https://intentmodel.dev/spec/3.0
parent: juice.tasks
---
```

Required fields:

- `aim` — the component namespace (lowercase, dot-separated)
- `facet` — one of `intent | schema | flow | contract | persona | view | event | mapping`
- `version` — the AIM language version this file conforms to (e.g. `3.0`)
- `spec` — a stable URL pointing to the language specification for `version`

Optional fields:

- `parent` — the parent component namespace, present on sub-components
- `display` — a human-readable display name (overrides the H1 heading for tooling)
- `tags` — array of free-form tags for discovery

### 2.3 Why `spec:` Is Required

The `spec:` field exists so an AI coding agent with no prior AIM knowledge can self-bootstrap. On encountering a `.intent` file, the agent fetches the URL, reads the spec, and immediately understands the structure of the file in front of it. No plugin, extension, skill, or prompt customization required.

The URL must be **version-stable**. `https://intentmodel.dev/spec/3.0` must continue to serve the v3.0 spec indefinitely, even after later versions exist.

### 2.4 Body (Markdown)

The body of the file is Markdown. Structure is conveyed by heading levels:

- **H1** — the component's display name (exactly one per file)
- **H2** — top-level sections (`## Summary`, `## Requirements`, `## Tests`, `## Subcomponents`, `## Dependencies`) and facet blocks (`## Schema: Task`, `## Contract: CreateTask`, etc.)
- **H3** — facet sub-blocks (`### Attributes`, `### Input`, `### Ensures`, `### Steps`, etc.)
- **Bulleted lists** — for requirements, tests, steps, attributes, and any enumeration
- **Fenced code blocks** — for attribute definitions, type expressions, and code samples

### 2.5 Heading Conventions

Facet headings use the form `## <FacetType>: <Name>`:

```markdown
## Schema: Task
## Contract: CreateTask
## Flow: AssignTask
## Persona: TaskOwner
## View: TaskDashboard
## Event: TaskCreated
```

Top-level section headings use the bare form:

```markdown
## Summary
## Requirements
## Tests
## Subcomponents
## Dependencies
```

The first paragraph immediately following any facet heading is treated as the facet's summary. An explicit `### Summary` sub-block is also permitted when the prose runs longer.

### 2.6 Attribute Syntax

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

Modifiers from v2.2 carry over: `required`, `optional`, `min(n)`, `max(n)`, `ref(<Type>.<field>)`, `enum(a, b, c)`, `default(<value>)`.

---

## 3. Project Layout

### 3.1 Sub-Component-First Default

AIM v3.0 inverts the v2.2 default. Real applications are decomposed into focused sub-components. Each sub-component is a real component with its own intent file, its own namespace, and its own facets. The parent component serves as an index plus a home for cross-cutting requirements and shared facets.

Reasons this is the default in v3.0:

- LLMs reason better over small focused files than large ones
- Multiple agents can work on different sub-components in parallel without merge conflicts
- Diffs are meaningful when each file has a single concern
- Synthesis maps cleanly to small focused code modules

### 3.2 Canonical Layout

```
/intent/
  juice.tasks/
    juice.tasks.intent                  # parent: index + shared
    juice.tasks.schema.intent           # shared schemas (Task, User refs)
    create_task/
      juice.tasks.create_task.intent
      juice.tasks.create_task.contract.intent
    assign_task/
      juice.tasks.assign_task.intent
    complete_task/
      juice.tasks.complete_task.intent
  mappings/
    juice.tasks/
      juice.tasks.mapping.intent
```

Rules:

- Each component lives in a directory named after its namespace.
- The intent file filename matches `<component>.intent`.
- Facet filenames match `<component>.<facet>.intent`.
- Sub-components live in nested directories under the parent.
- Mappings live under `/intent/mappings/<component>/`.
- Generic filenames (`intent.intent`, `schema.intent`) are invalid.

### 3.3 When To Collapse Into A Single File

A component should stay in a single `.intent` file (no sub-components, facets embedded inline) only when **all** of the following hold:

- Total content fits comfortably in a single screen of reading.
- There is one clear behavior, not a set of distinct features.
- No facet needs independent ownership or review.

Otherwise, split. The principle reverses v2.2: split is the default, single-file is the exception.

### 3.4 Path Identity

The header `aim:` field is authoritative for identity. The directory and filename must agree with the header — tools treat path/header mismatch as a hard error. This lets paths function as a fast sanity check without competing with the header as the source of truth.

---

## 4. Sub-Components

### 4.1 Definition

A sub-component is a component whose namespace extends a parent component's namespace by exactly one segment:

- Parent: `juice.tasks`
- Child:  `juice.tasks.create_task`

The child declares the parent in its frontmatter:

```yaml
---
aim: juice.tasks.create_task
facet: intent
version: 3.0
spec: https://intentmodel.dev/spec/3.0
parent: juice.tasks
---
```

A sub-component is a real component: it has its own intent file, its own facets, and is independently addressable.

### 4.2 Parent As Index

The parent component's intent file serves two purposes:

1. **Index of sub-components** — either auto-discovered from sibling directories or explicitly listed.
2. **Home for cross-cutting concerns** — shared requirements, shared schemas, shared personas, shared events that apply across all sub-components.

Example parent intent:

```markdown
---
aim: juice.tasks
facet: intent
version: 3.0
spec: https://intentmodel.dev/spec/3.0
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

- [create_task](./create_task/juice.tasks.create_task.intent) — create a new task
- [assign_task](./assign_task/juice.tasks.assign_task.intent) — assign a task to a user
- [complete_task](./complete_task/juice.tasks.complete_task.intent) — mark a task completed

## Schema: Task

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

### 4.3 Sub-Component Discovery

By default, sub-components are **auto-discovered**: any sibling directory containing a `<namespace>.intent` file with a matching `parent:` field is treated as a sub-component of the parent.

The parent may override discovery with an explicit `## Subcomponents` block. When the explicit list is present:

- listed sub-components must exist on disk
- discovered sub-components not in the list emit a hard error (ambiguous authority)
- the explicit list is authoritative for the order in which sub-components are presented to agents and tooling

### 4.4 Upward Facet Resolution

A sub-component may reference facets defined in the parent without qualification. Resolution proceeds outward from the most local scope:

1. The sub-component's own facets (embedded or in sibling facet files).
2. The sub-component's explicit `## Dependencies` includes.
3. The parent component's facets.
4. The parent's parent (for nested sub-components), and so on up the tree.
5. External components referenced via `## Dependencies`.

A name resolves to the first match encountered. Tools emit an informational diagnostic when a sub-component's facet shadows a parent's facet with the same name (this is usually a sign that the shared definition should move up, or that the sub-component name should be more specific).

### 4.5 Nesting Depth

Sub-components may nest, but the spec recommends a maximum effective depth of **three levels** (e.g. `app.module.feature.sub_feature`). Beyond this, comprehension drops and traceability becomes hard to follow. Tools should warn when nesting exceeds three levels.

### 4.6 Version Inheritance

A sub-component's `version` must match its parent's `version` exactly. The `version` field is replicated in every file for cold-start clarity but is structurally controlled by the parent.

---

## 5. Intent Envelope

### 5.1 Minimum Valid Intent File

```markdown
---
aim: demo.todo
facet: intent
version: 3.0
spec: https://intentmodel.dev/spec/3.0
---

# Todo

## Summary

A simple personal todo tracker.

## Requirements

- User can add, complete, and delete todos.
```

Hard minimum for validity:

- Valid frontmatter with required fields.
- Exactly one H1 heading.
- A `## Summary` section with at least one paragraph **or** an H1 followed by a paragraph that serves as the summary.
- A `## Requirements` section with at least one bullet.

Recommended:

- `## Tests` section with observable behavior bullets.
- One or more facets when the component has stable interfaces.

### 5.2 Extended Intent Example (Sub-Component)

```markdown
---
aim: juice.tasks.create_task
facet: intent
version: 3.0
spec: https://intentmodel.dev/spec/3.0
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

Create a task on behalf of the current user.

### Input

```aim-attrs
title: string required min(1) max(200)
description: string optional max(2000)
```

### Authz

- Caller must be authenticated.

### Ensures

- A new Task record is persisted with status="open".
- ownerId is set to the current user's id.
- A `tasks.created` event is emitted with the new task's id.

### Returns

- The newly created Task record.
```

Note: `Task` and `User` are not defined in this file — they resolve upward to the parent component `juice.tasks`.

---

## 6. Precision Facets

The six facets are unchanged from v2.2. Only the syntax differs.

### 6.1 Schema

Data at rest, structural types, and constraints.

```markdown
## Schema: Task

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

### 6.2 Contract

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

- A new Task record is persisted with status="open".
- A `tasks.created` event is emitted.

### Returns

- The newly created Task record.
```

### 6.3 Flow

Operational sequencing, branching, retries, and error handling.

```markdown
## Flow: CreateTask

### Summary

Persists a new task and emits the creation event.

### Trigger

- Invoked by the `Contract: CreateTask` boundary.

### Steps

1. Validate input against the contract.
2. `CALL` Storage.PersistTask(input).
3. `CALL` EventBus.Emit("tasks.created", task.id).
4. Return the persisted task.

### On Error

- Storage failures: surface as `PersistenceError` and emit no event.
- Event bus failures: persisted task is retained; emission is retried via outbox.
```

### 6.4 Persona

Actor identity, role semantics, and view access.

```markdown
## Persona: TaskOwner

### Role

- Authenticated user who owns one or more tasks.

### Access

- May view `View: TaskDashboard`.
- May invoke `Contract: CreateTask`, `Contract: CompleteTask`.
```

### 6.5 View

Shared interface surfaces and user-visible actions.

```markdown
## View: TaskDashboard

### Summary

The owner's primary task list view.

### Display

- Pending tasks grouped by due date.
- Completed tasks collapsed by default.

### Actions

- CreateTask — opens task creation form.
- CompleteTask — marks the selected task complete.
- ArchiveTask — moves a completed task to archive.
```

### 6.6 Event

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

### Emitted By

- `Flow: CreateTask`

### Routing

- Channel: `tasks.created`
- Durable: true
```

### 6.7 Summary Rule

Every facet block must carry a summary, either as the first paragraph after the facet heading or as an explicit `### Summary` sub-block. `Persona` may omit the summary when it acts only as a role/access declaration.

---

## 7. Dependencies, Requirements, And Mappings

### 7.1 Dependencies Block

External providers and required capabilities are declared in a `## Dependencies` block:

```markdown
## Dependencies

### Imports

- `company.storage.Contract` as Storage
- `company.events.EventBus` as EventBus

### Requires

- Identity as AssigneeUsers
```

- **Imports** reference concrete provider surfaces from other components.
- **Requires** declares required capabilities by alias. The alias is resolved via a mapping file.

### 7.2 Requirement Surfaces

Required capabilities may be documented inline with a `## Requirement: <Alias>` block:

```markdown
## Requirement: AssigneeUsers

### Summary

Capability required to resolve user identities.

### Operations

- `ResolveUser(id) -> UserRecord`
```

### 7.3 Mapping Files

Mappings bind required aliases to concrete providers. They live under `/intent/mappings/<component>/` and use `facet: mapping`.

```markdown
---
aim: juice.tasks
facet: mapping
version: 3.0
spec: https://intentmodel.dev/spec/3.0
---

# Tasks Mappings

## Map: AssigneeUsers

### Target

- `company.identity`

### Operation Map

- `AssigneeUsers.ResolveUser` → `company.identity.ResolveUser`
```

Unresolved `Requires` aliases are hard errors at validation time.

---

## 8. Resolution And Synthesis

### 8.1 Resolution Order

For any facet referenced within a component, content is resolved in this order:

1. Embedded facet block in the same intent file.
2. Sibling facet file (`<component>.<facet>.intent` next to the intent file).
3. Parent component's facets (upward chain).
4. External component referenced via `## Dependencies → Imports`.
5. Absent.

The first match wins. Lower-precedence sources for the same facet name emit an informational diagnostic ("shadowed by higher-precedence source").

### 8.2 Specification Levels

- **Level 1** — Intent only. Useful for early exploration and simple components.
- **Level 2** — Intent plus some facets. Most production components.
- **Level 3** — Intent plus full facet trace (Persona → View → Contract → Flow / Schema / Event). Highest fidelity for implementation and review.

The level affects expected implementation precision, expected code-generation precision, and strictness of traceability checks. Tools may report a component's level as an informational diagnostic.

### 8.3 Traceability Chain

When relevant facets are present:

```
Persona → View → Contract → Flow / Schema / Event
```

- `Persona.Access` references `View`.
- `View.Actions` reference `Contract`.
- `Contract` may reference or imply `Flow`.
- `Contract` and `Flow` may read or mutate `Schema`.
- `Contract.Ensures` may guarantee `Event` emission.

This chain is a useful target, not a requirement. Intent-only components are valid; tools emit a reduced-fidelity informational note.

---

## 9. Registry And Installation

### 9.1 Registry Package Catalog

Remote package discovery uses `registry/index.json`. Each package object must include:

- `name`
- `version`
- `entry` — relative path to the package's root intent file

Package validity:

- `entry` must exist and end with `.intent`.
- The entry's frontmatter `aim` must match the package `name`.
- The entry's `version` must match the package `version`.
- A package directory must contain exactly one root `facet: intent` file (sub-components have their own intent files but only the package root is the entry).

### 9.2 Local Installation

Even when sources are fetched remotely, all implementation, review, and code generation runs against local files under `/intent`. Fetched packages are installed into the canonical layout described in Section 3 so users can edit and rebuild without refetching.

---

## 10. Tooling Diagnostics

### 10.1 Hard Errors

- Missing or malformed frontmatter.
- Missing required frontmatter fields (`aim`, `facet`, `version`, `spec`).
- Frontmatter `aim` does not match the file path.
- `parent:` declared but no parent intent file exists.
- Sub-component `version` differs from parent `version`.
- Missing H1 heading, missing `## Requirements`, or empty `## Requirements`.
- Invalid facet type in heading (e.g. `## Data: X`).
- Duplicate facet definitions with the same name within the effective source.
- Ambiguous sub-component authority (auto-discovered sub-component not in explicit `## Subcomponents` list).
- Unresolved `Requires` aliases with no matching mapping.
- Sub-component facet name collision with a parent facet name (when the parent definition is authoritative).
- Generic filenames (`intent.intent`, `schema.intent`, `mapping.intent`).

### 10.2 Informational Diagnostics

- Missing optional `## Tests`.
- Intent-only component (no facets).
- Lower-precedence facet source shadowed by a higher-precedence one.
- Sub-component nesting exceeding three levels.
- Unresolved `Import` alias (not blocking but flagged for repair).

---

## 11. Migration From v2.2

v3.0 is a breaking change. Tools should ship a `sinth migrate` command that converts v2.2 sources to v3.0:

1. Convert `AIM: <name>#<facet>@2.2` headers to YAML frontmatter with `version: 3.0` and `spec: https://intentmodel.dev/spec/3.0`.
2. Translate `INTENT Name { ... }` → `# Name` + section headings.
3. Translate `SCHEMA Name { ATTRIBUTES { ... } }` → `## Schema: Name` + `### Attributes` + fenced `aim-attrs` block.
4. Translate other facet blocks similarly.
5. Optionally split large intent files into sub-components when natural feature boundaries exist (manual review recommended).

v2.2 and v3.0 sources must not coexist within the same `/intent` tree. The migration is one-shot per project. v2.2 projects also need to rename `/aim/` to `/intent/` as part of migration.

---

## 12. Conformance Examples

### 12.1 Minimal Valid Component

```markdown
---
aim: demo.snake
facet: intent
version: 3.0
spec: https://intentmodel.dev/spec/3.0
---

# Snake

## Summary

A single-player snake game.

## Requirements

- The snake grows when it eats food.
- Wall and self-collision end the run.
```

### 12.2 Component With Sub-Components

```
/intent/game.snake/
  game.snake.intent              # parent: shared schemas, index
  game.snake.schema.intent       # shared SnakeState, FoodPellet
  tick/
    game.snake.tick.intent
  collision/
    game.snake.collision.intent
  score/
    game.snake.score.intent
```

### 12.3 Invalid

- Frontmatter missing `spec:` field.
- `## Data: Foo` heading (invalid facet type).
- Sub-component file with `parent: juice.tasks` but no parent intent file exists.
- Two `## Schema: Task` blocks in the same effective source.
- Sub-component `version: 3.0` under a parent declaring `version: 2.2`.

---

## 13. Practical Guidance

### 13.1 Default Authoring Rule

Start by splitting. Create the parent intent with the cross-cutting requirements and shared schemas. Create each feature as a sub-component. Keep each sub-component focused on a single observable behavior. Collapse into a single file only when the whole component is trivially small (one feature, one screen of content).

This is the opposite of v2.2's "start single, split when it hurts." The shift is intentional: AI code generation works better with many small focused files than with one large one.

### 13.2 What Goes In The Parent

- Shared schemas (entities referenced by multiple sub-components).
- Shared personas and views.
- Cross-cutting requirements that apply system-wide.
- Index of sub-components.

### 13.3 What Goes In A Sub-Component

- The intent, requirements, and tests for a single feature.
- Contracts and flows specific to that feature.
- Sub-component-specific events.

### 13.4 When To Split A Sub-Component Further

When a sub-component itself has multiple distinct behaviors with their own contracts. Example: a `payments` component might split into `charge`, `refund`, `dispute` sub-components, and `dispute` itself might split into `open_dispute`, `respond_to_dispute`, `resolve_dispute` if each has its own contract.

Three nesting levels is the practical maximum.

### 13.5 Closed-Loop Workflow

1. Requirements → intent (sub-components first, parent as index).
2. Intent → implementation, reading the resolved facet set.
3. Implementation → validation against intent.
4. Validation failures → code repair or intent revision.
5. New requirements → new sub-component or revised parent.

The intent is the contract. Code follows intent. When they diverge, one of them is wrong and the divergence is resolved explicitly.
