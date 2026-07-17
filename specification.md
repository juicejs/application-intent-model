# Agentic Intent Model (AIM) v5

Agentic Intent Model (AIM) is a specification language for humans and AI agents. It makes the **intent** of a system durable and computable — from an application's behavior to a complete business process or an organization's commitments. The model remains readable enough for the people who own the intent, while being structured enough for agents to realize it, review it, repair it, and verify reality against it. Software was AIM's first domain and remains its most fully worked example; nothing in the language is specific to it (§18).

**The central proposition.** Every consequential system has two forms: what its owners intend and what actually happens. For an application, reality is code, configuration, data, interfaces, and runtime behavior. For an organization, reality also includes people, approvals, operating procedures, automations, external systems, deadlines, and evidence of work performed. AIM gives both forms a shared structure. It connects purpose and requirements to the contracts, flows, views, events, roles, and resources that fulfill them, then binds those commitments to the places where they are realized.

The result is more than documentation. It is a navigable chain from **why** a system exists, through **what** it promises and **how** those promises are fulfilled, to **where** each part exists in reality. That chain makes drift computable. In an application, drift may be behavior implemented without intent, intent with no implementation, or a stale binding after code moves. Across a company, drift may be a policy no process enforces, an approval people routinely bypass, an automation that no longer fulfills its obligation, a manual step with no accountable performer, or a stated commitment with no capability that satisfies it. The same graph and review loop expose all of these as mismatches between declared intent and observed reality.

AIM v4 was a **breaking change** from v3.1. v3.1 made AIM Markdown-native and self-bootstrapping; it succeeded at making intent *readable*, but it left AIM's highest-value job — the **linking** between the things a system is made of — almost entirely informal. Real applications are not trees; they are **graphs**. A View exposes an Action that invokes a Contract that reads or mutates a Schema and emits an Event that a Persona can reach. v3.1 expressed those relations in inconsistent prose ("Invoked by Contract: X", "TRIGGER: Contract.Y", "CALL Z"), demoted the traceability chain to "a useful target, not a requirement," and offered no way to traverse, check, or diff the relation graph.

The three structural shifts of the v4 break — still the spine of the language:

1. **Graph-founded model.** The `.aim` Markdown file is understood as a *projection* of an underlying node-and-edge graph. Every heading is an addressable node; every cross-reference is a typed, directed edge. The graph is *derived* by collecting edges across files — it is never authored as a separate artifact, so `.aim` files remain the sole authority.
2. **Typed edge taxonomy.** A single CommonMark-native edge token replaces the prose. Each edge carries a verb from a closed set and points at a canonical node address. This makes the relation graph traversable and checkable: dangling references, orphan nodes, and impact sets fall out for free, and the traceability chain becomes *computable* rather than aspirational.
3. **Intent↔realization binding layer.** Intent nodes may bind to their realization sites — in code (`file#symbol`, `route:…`, `table:…`), in operations (`system:…`, `agent:…`, `workflow:…`). Drift detection then becomes a **graph-diff** between the declared intent graph and the realized graph recovered from reality, yielding precise, owner-routed findings.

v5 keeps that foundation intact and generalizes it: the unit is named the **intent**, the tree reads parent/children (§2.1), and nothing in the language is specific to software (§13.3, §18).

The design bar for all three is **LLM-parsability** — consistent conventions an LLM follows and traverses reliably, not a rigid grammar requiring a custom parser. AIM remains valid CommonMark that renders on GitHub with no special tooling.

AIM is the authoritative shared artifact between humans and agents. Realization, review, and repair all run against AIM. When reality and intent disagree, the mismatch is resolved explicitly — either by fixing the realization or by revising intent.

**Where AIM is going, and why the drift machinery exists.** AIM's destination is intent as source: the model is what humans maintain, and the realization — code, automations, agent behavior — is synthesized or performed from it, the same inversion every prior abstraction jump made, from assembly to compilers. Today that is not yet safe: synthesis is stochastic, humans still change reality directly, and most systems predate their model (§17). The binding layer, graph-diff, and repair loop (§10, §12) are the trust-building apparatus for exactly this transitional period — every clean report is evidence that intent → reality is reliable for that intent. The success criterion of that machinery is to make itself progressively unnecessary: for an intent that is fully confirmed, Level 3, and repeatedly clean, regeneration replaces repair, and its binding file quietly changes meaning from review tool to build manifest. Readers and agents should treat this as the interpretive key for the rest of the document: the behavioral facets and the edge graph are the destination; the drift machinery is the road.

**Who writes AIM, and when it is worth it.** In practice `.aim` files are authored by an agent (the Architect role, §1.2) from a human's narration — not hand-written token by token. The typed structure therefore costs the author nothing and yields a more precise, checkable artifact. This answers the obvious objection — *if an agent writes the model and an agent produces the realization, why not act directly?* The `.aim` file is the **durable, human-reviewable, machine-checkable contract** between intent and reality: a small model is something a human can read, correct, and diff — and a Reviewer can check reality against — far more cheaply than inspecting the realization itself, and it persists across sessions where a chat prompt does not. The corollary is a boundary worth stating plainly: AIM pays off when reading the model is meaningfully easier than inspecting the realization; for trivially small or throwaway work, acting directly is the right call.

---

## 1. Core Model

An intent is identified by a dotted namespace such as `juice.tasks` or `game.snake`. Child intents extend the namespace: `juice.tasks.create_task` is a child of `juice.tasks`.

Each intent has:

- one required **intent file** (a `.aim` file with `kind: intent`)
- zero or more optional **facets**: `schema`, `flow`, `contract`, `persona`, `view`, `event`
- zero or more optional **child intents** (each is an intent in its own right)
- zero or more optional **mapping files** (`kind: mapping`) — capability-to-provider bindings
- zero or more optional **binding files** (`kind: binding`) — intent-to-realization bindings

The intent file is the canonical entrypoint. All other detail attaches to it directly (embedded), indirectly (sibling facet files), or through child intents.

### 1.1 What Changed From v3.1 (The v4 Break)

| Concern | v3.1 | v4 |
|---|---|---|
| Underlying model | Namespace tree (parent/child) | Node-and-edge graph; the tree is one edge type |
| Cross-references | Prose mentions, inconsistent forms | One typed edge token: `[verb](aim:<address>)` |
| Traceability chain | "A useful target, not a requirement" | Derived from declared edges; checkable |
| Inverse relations | Authored twice (`### Trigger`, `### Emitted By`) | Declared once at the acting end; inverse derived |
| Code linkage | None | Optional `kind: binding`; drift becomes graph-diff |
| Per-file `version`/`spec` | Contradictory in v3.1 (frontmatter omitted them, but version-inheritance, registry, and diagnostics still required them) | Removed everywhere; version lives only in `AGENTS.md` (and the external catalog) |

### 1.2 Roles And Capabilities

AIM is operated through three **capabilities**, each defined by what it may write — not by a roster of agents a human must choose between. In software they read as architect, developer, reviewer; in operations, as process designer, operators and automations, audit. They are **operating modes, not a menu**: one agent may hold all three, and a mature tool classifies the human's request and enters the right mode itself rather than asking which role to use.

| Capability | Writes intent (`.aim`) | Writes realization | Certifies match |
|---|---|---|---|
| **Architect** | ✓ | — | — |
| **Realizer** (Developer) | — | ✓ | — |
| **Reviewer** | — | — | ✓ (writes nothing) |

- **Architect** — **designs the intent graph**: translates a human's narration into intents, their facets, and the typed edges among them. The `.aim` files are the graph's serialization (§2), not the design itself — an Architect who writes facets without edges has not architected, only documented. Owns the model; authors binding facets when realization is known. The Architect works in two **directions**: *forward*, designing intent from requirements, and *reverse*, recovering intent from a system that already exists (**Encoding**, §17). The reverse direction is the same capability with one difference — its output carries `provenance: inferred` (§17.2) and awaits human confirmation, because it is read off reality rather than authored. Direction and provenance are variations of authoring, not a separate role.
- **Realizer** — makes reality match the model: a development team implementing code and tests, an ops team wiring automations, an agent performing a process. Emits or updates bindings for what it realizes. Fixes the realization when drift is found. (In the software domain this role is conventionally called the **Developer**, and the shipped prompt templates use that name.) A realization is either an **artifact** produced once (code, a configuration) or a **performance** repeated per instance (a process executed by people or agents). In the performed case realization work happens at execution time, so the performer wears this role — an agent executing a process is a Realizer, and the conduct rules below bind it: that is precisely what forbids it from improvising behavior the model does not state.
- **Reviewer** — diffs the declared graph against the realized graph recovered from reality (code, configuration, execution logs — §10.1) and reports drift, writing nothing.

**Verification must be independent.** The Reviewer capability MUST run in a context that cannot write what it judges — a cold evaluation with read-only access to the model and the realization. An agent that both produces a realization and certifies it against intent will pass its own work; drift detection is only meaningful when something with no stake in the output re-derives the graph and diffs it. Independence is a property of the *context and its permissions*, not of the model in use: the same agent re-invoked cold and denied write access is a valid Reviewer; that agent continuing in the session that just wrote the code is not.

Roles are workflow guidance, not language constructs — they do not appear in `.aim` source files. A single agent may hold multiple capabilities and multiple agents may share one; the only separation that is normative is Reviewer independence, above. See [`PROMPT.md`](./PROMPT.md) and [`agents/`](./agents/) for concrete prompt templates for the software domain.

Repair is a verb, not a separate role. When the Reviewer flags drift, either the Realizer fixes the realization or the Architect revises the intent. The decision is explicit, not silent.

Normative behavior across all roles:

- The Realizer must not invent material behavior absent from intent.
- When detail is missing, preserve documented intent and minimize assumptions.
- Assumptions are surfaced for review or converted into explicit intent updates by the Architect.
- When reality and intent disagree, the mismatch is resolved — the Realizer fixes the realization if it is wrong, the Architect revises intent if the model is outdated.

**Architect: validate before present.** Before presenting a proposal to the user or committing an EXTEND or ADD (§16.1), the Architect MUST derive the graph (§2.4) over the *proposed* state and **repair every hard error (§12.1) it can resolve autonomously** — a dangling edge left by a rename, an out-of-sync `## Children` index, a path/header mismatch, an illegal `(verb, from, to)` triple. Only diagnostics that genuinely need a human decision are surfaced: a confirmed-duplicate `merge` (§16.3 invariant 6), an unresolved canonical-home choice (§15.8), or an ambiguous binding (§12.3). A proposal presented with unrepaired hard errors is **non-conforming Architect behavior** — the graph must be well-formed before a human is asked to review it.

### 1.3 Project Authority Model

AIM is Markdown-native by deliberate choice, but that choice creates a risk: AI agents already love to spawn `.md` plans, design notes, decision logs, and PRDs. Without a clear authority boundary, AIM becomes one more `.md` file in the pile instead of the artifact that displaces it. The following rules establish that boundary.

**Authority hierarchy:**

1. **`.aim` files are the sole behavioral authority.** Every requirement, contract, schema, flow, persona, view, event, and **edge** that defines the system's behavior must live in a `.aim` file. Tools, agents, and reviewers treat `.aim` as the only source of truth for what the system is supposed to do. The derived graph is a *view* of these files, never a competing artifact.

2. **Other `.md` files are explanatory, not authoritative.** `README.md`, `CONTRIBUTING.md`, ADRs, and similar documents may describe, link to, or summarize intent — but they must not define new behavioral requirements. If a behavioral requirement appears only in an `.md` file and not in a `.aim` file, it is **drift**. The Reviewer reports it. The fix is to move the requirement into a `.aim` file.

3. **Anything outside `/aim/` is invisible to authority.** Behavioral content found in `docs/`, top-level `.md` files, code comments treated as spec, or chat history transcripts is not part of the project's behavioral authority. If it matters, it gets moved into `.aim`. If it doesn't, it isn't authoritative. The lone exception is `AGENTS.md` at the project root (see §3.3) — which carries project bootstrap metadata for agents but does not define behavior itself.

**Behavior vs. realization.** A binding (`kind: binding`, §10) records *where* behavior is realized in code. Realization is not behavior. Bindings are authoritative for the intent↔code mapping but never define what the system should do — that always lives in the behavioral facets. This is why bindings are kept in their own files (§10.2): a binding can go stale (code moved) without the intent being wrong.

**The system vs. the work on the system.** AIM describes the *system under specification* — its commitments, actors, data, and events. Facts about *producing and maintaining that description* — who authored a file, what review state it is in, when and by whom it changed — are **meta-level** facts. The test for any proposed field, block, or marker: *would the fact survive replacing the entire team and toolchain while the specified system stays identical?* If it would not, it is meta-level. Several existing rules are instances of this one rule: roles are workflow guidance, not language constructs (§1.2); implementation status is banned from behavioral content (§3.8 — intent, not status); work artifacts are point-in-time and non-authoritative (§16.4, §17.4); enforcement mechanics and report formats are tooling concerns this spec does not define (§10.1). Evolution history and change governance belong to the project's storage and collaboration environment — a version-control system, a product database, a reviewed file share — and AIM requires nothing of that environment: the spec defines what the files *mean*, never how they are versioned, reviewed, or approved. Meta facts that must travel *with* the files — authority and accountability — use the spec-defined frontmatter fields (`provenance`, `owner`, `status`, `approved_by`, §3.2); further project-specific keys are permitted and carry no spec semantics. Meta facts never appear in the **body**: no status markers in requirements, no changelogs, no review annotations in behavioral content. The boundary excludes only the meta level: actors *of the specified system* are object-level and fully in-model — a `Persona` is a commitment about who the system serves, never a statement about who maintains its spec. A business process specified in AIM therefore legitimately models its workers, approvals, and execution evidence as Personas, Contracts, and Events, while the question of who edits those `.aim` files stays outside the language.

**Diagnostics:**

- **Hard error** — none for the prose/authority boundary. The Authority Model is enforced socially and by review, not by the parser. Tools cannot reliably distinguish "describes intent" from "defines intent" in arbitrary prose.
- **Informational diagnostic** — reviewers and validators may flag `.md` files that appear to contain behavioral requirements not present in `.aim` files. The recommended remediation is always to move the requirement into a `.aim` file.

**Why this matters:**

The whole point of AIM is to replace `.md` sprawl with a structured behavioral artifact agents can read once and build from. Without the Authority Model, the same agents that spawned 100 `.md` files will spawn 100 `.md` files plus a few `.aim` files. With the Authority Model, every behavioral fact has exactly one home — and drift between sources is impossible because there is only one source.

---

## 2. Graph Model

v4 reinterpreted the v3.1 file surface as the projection of a graph. No new file format and no new parser tier: every node already has a heading, and every edge is just a typed cross-reference. This section defines what a node is and how it is addressed; §8 defines edges.

**Why a graph, and what kind.** An application's intent is not a document; it is a set of commitments and the relations among them. A facet is a **unit of intent**; a typed edge is **relational intent** — `[exposes](aim:#Contract:CreateTodo)` is itself a normative statement ("this surface shall offer this operation to users"), carrying the same authority as any requirement bullet. The graph is therefore **normative, not descriptive**. A code-analysis graph is derived from source and cannot disagree with it — it has no concept of *wrong*, only of structure. The intent graph is *authored*, so it can be wrong, unrealized, or drifted-from — and that capacity for disagreement is the point: drift (§10, §12) is only a meaningful concept because the declared graph is authoritative over what the system *should* do, independent of what the code *does*.

**Why prose could not hold it.** Prose and headings are trees; application behavior is a graph. Serializing a graph into a tree forces every relation that crosses the hierarchy to be stated twice — once at each end ("Invoked by Contract: X" on the flow, "CALL X" in the steps) — and duplicated statements inevitably drift apart. v3.1's "three inconsistent expressions" problem (§8.3) was the structural symptom, not sloppy authoring. v4 re-normalized this: every relation is declared once, at the acting end, and inverse views are derived, never authored. The resulting division of labor is exact — **prose carries semantics** (what a commitment means, and why), **the graph carries structure** (how commitments compose into a system). Each holds precisely what the other cannot.

**Who reads which projection.** The model carries two structures for two audiences, superimposed in the same files. The **tree** — namespaces, `## Children`, headings — is the *human* projection: hierarchy gives progressive disclosure (a handful of children per level, drill down), and the parent–child edge carries explanation — descending answers *how*, ascending answers *why*. Humans navigate, review, and understand the model through the tree. The **graph** — the typed edges — is the *machine* substrate: complete, queryable, and never meant to be read whole. Humans consume the graph only as **answers**: an impact set, a satisfies-coverage report, a calendar of every Trigger, one role's operations. Tools SHOULD surface the graph as such views and queries, and SHOULD NOT require a human to comprehend the global graph — no human can, and the design never asks them to. A `.aim` file is both projections at once: its headings are the tree, its edge tokens are the graph, and each reader takes their half (§18). And the two structures are independent by design: the tree may nest intents to whatever depth they earn (§5.5 — every level re-earns the shape rules), while the typed edges form **one global graph** that crosses tree levels and intent boundaries freely (§8.1) — tree position never limits what an edge may connect; it only decides who owns the node.

The split rests on a hard asymmetry: a human can hold a tree in mind; no one holds a graph. That makes the tree not a convenience view but the model's **entire human interface** — and its *shape* a first-class quality property. Every intent SHOULD read as a short table of contents for the level below; an intent that degenerates into a flat bag of technical nodes has failed its audience even while the graph beneath it validates perfectly. The noun-cluster diagnostic (§12.2) and the `promote` transform (§16.2) exist to restore the ladder.

### 2.1 Nodes

A node is any **addressable heading** in the resolved source. There are three ranks, all of which already exist as headings:

| Rank | Markdown | Node-type | Example |
|---|---|---|---|
| Intent | `aim:` frontmatter / H1 | `intent` | `nemicko.demo.todo` |
| Facet | `## <Facet>: <Name>` | `schema` `view` `contract` `flow` `persona` `event` `trigger` (+ `capability` — the `## Capability:` surface, §9.2; **not** a `## Requirements` list item) | `## Contract: CreateTodo` |
| Facet sub-block | `### <Sub>` and its list items | `block` (addressable, not separately typed) | `### Ensures` item `[2]` |

Top-level prose sections (`## Summary`, `## Requirements`, `## Tests`, `## Dependencies`) are nodes of type `section`. They are valid anchor targets for drift reports but are **edge-inert** as sections — a section heading is never itself the endpoint of a typed edge. Only `intent` and the facet node-types participate in the edge graph, with two defined sub-block exceptions: a **schema attribute** participates solely as an endpoint of a `refs` edge (§3.7, §8.2), and a **`## Requirements` list item** participates solely as the target of a `satisfies` edge (§8.2). Both are addressable sub-blocks, not separately typed nodes; no other sub-block is ever an edge endpoint, and `## Requirements` as a *section* stays edge-inert (only its individual items are `satisfies` targets). The node-type is read directly off the facet-heading keyword; there is no inference.

Intents form a **tree**: hierarchy is a *property*, not a kind. There is exactly one intent node-type — an intent with a `parent:` (§3.2, §5) is the same kind of node as the root, and a node's tree position never changes what it is: the tree is a projection (§2.4). The relational vocabulary this spec uses for tree position is **parent**, **child** (plural **children**), **root intent**, **leaf**, and **siblings**.

### 2.2 Node Addresses

The canonical address of a node is:

```
<intent>#<FacetType>:<Name>[ → ### <Sub> [<index>]]
```

- `<intent>` — the dotted namespace from the file's `aim:` field. Present in any stored or derived address (fully qualified). **Elidable** at an inline reference site when the target resolves within the same intent, yielding the unqualified form `#<FacetType>:<Name>`.
- `#<FacetType>:<Name>` — the facet heading, verbatim. `FacetType` is capitalized exactly as in the heading (`Contract`, `View`, `Schema`, …). Because facet names are constrained to `[A-Za-z][A-Za-z0-9_]*` (§3.6), the address is always a valid CommonMark link destination with no percent-encoding.
- `→ ### <Sub> [<index>]` — optional finer pointer into a sub-block list item, 1-based, matching the Reviewer's drift-report convention.

This is the address scheme drift reports already use (`## Contract: CreateTask → ### Ensures [2]`), promoted from a review artifact to the language's identity scheme.

**Sub-block addresses are point-in-time, not durable.** A `→ ### <Sub> [<index>]` (or `→ ## Requirements [<index>]`) pointer is 1-based and positional: inserting or reordering a list item silently re-points every later index, so such an address is valid only relative to a *specific revision* of the file. Authored `.aim` source therefore MUST NOT use a sub-block address as an edge target — typed edges (§8) target facet-level nodes only (`#<FacetType>:<Name>`). Sub-block addresses appear only in point-in-time work artifacts (drift reports and change records under `/aim/work/`), which SHOULD additionally record the item's text as a **content anchor** so the reference re-resolves after the list shifts.

The one sub-block target permitted in authored source is a `## Requirements` list item referenced by a `satisfies` edge (§8.2), and it comes in two forms with different durability. A **positional** reference (`#Requirements[3]`) inherits the point-in-time fragility above: inserting or reordering requirement bullets is a `rename`-class transform (§16.2), and every inbound positional `satisfies` edge MUST be re-pointed under §16.3 invariant 1 — an edit made without tooling silently re-points them, which is why positional references are the casual form, not the durable one. A **labeled** reference (`#Requirements[NET14]`, §8.2) targets a requirement by its stable label and survives any reordering — once `satisfies` edges exist, labels SHOULD be used.

### 2.3 Address Examples

```
nemicko.demo.todo                                          # intent node
nemicko.demo.todo#Schema:TodoItem                          # facet node
nemicko.demo.todo#Schema:TodoItem → ### Attributes [3]     # the `title` attribute
nemicko.demo.todo#Contract:CreateTodo
nemicko.demo.todo#Contract:CreateTodo → ### Ensures [2]    # "Emits a TodoCreated event"
nemicko.demo.todo#Flow:ExecuteCreateTodo → ### Steps [3]
nemicko.demo.todo#Persona:StandardUser
nemicko.demo.todo#View:TodoDashboard → ### Actions [1]
nemicko.demo.todo#Event:TodoCreated
```

Within a single-file intent, every node shares the one intent prefix, so inline references drop it entirely (`#Contract:CreateTodo`).

### 2.4 The Graph Is Derived

There is no graph file. A tool or agent builds the project graph by:

1. **Collecting nodes** — every intent/facet/sub-block heading in the resolved source becomes a node keyed by its fully-qualified address.
2. **Collecting edges** — scanning inline edge tokens (§8) and structured `ref(Type.field)` attributes; each yields one directed, typed edge `(from = enclosing facet node, verb, to = resolved address)`.
3. **Validating** each edge against the from→to schema (§8.2) and resolving each target via §11.1.
4. **Adding derived inverse edges** (§8.4) and reconciling them against any authored inverse blocks.

The result lives only in tool/LLM memory or a build artifact. The `.aim` files remain the sole authority (§1.3).

---

## 3. File Format

### 3.1 Extension

All AIM source files use the `.aim` extension. The extension is a brand and discipline marker: a file named `*.aim` is an authoritative AIM artifact, not a generic note. (Legacy v2.2 sources used `.intent`. Every version since v3.1 uses `.aim`; neither the v3.1→v4 nor the v4→v5 break changed the extension.)

Files are valid CommonMark Markdown with YAML frontmatter. Any Markdown renderer will display them correctly.

### 3.2 Header (YAML Frontmatter)

Every `.aim` file begins with a small YAML frontmatter block:

```yaml
---
aim: juice.tasks.create_task
kind: intent
parent: juice.tasks
---
```

Required fields:

- `aim` — the intent namespace (lowercase, dot-separated)
- `kind` — the file role: one of `intent | schema | flow | contract | persona | view | event | trigger | mapping | binding`

Optional fields:

- `parent` — the parent intent namespace, present on child intents
- `display` — a human-readable display name (overrides the H1 heading for tooling)
- `tags` — array of free-form tags for discovery
- `provenance` — `inferred` on a file produced by re-encoding existing code and not yet human-accepted (§17). Absent (the default) or `confirmed` means authored/accepted intent. This is the only field that qualifies a file's authority.
- `owner` — the identity accountable for this file's intent (free-form — a name or an email). Tools use it as the routing target for findings (§12.3). Accountability metadata only; it never affects the file's authority.
- `status` — the authoring lifecycle of the **specification**: `draft | review | approved | deprecated`. This is the state of the intent, never of the implementation — implementation status remains banned from `.aim` files (§3.8) and lives in the drift report. Absent means unspecified.
- `approved_by` — the identity that ratified the current content, optionally paired with `approved_at` (a date). This records the *who* of a §17.2 acceptance — or of ordinary review — in any environment, including after export to bare files.

**Frontmatter is an open set with reserved keys.** Keys this spec does not define are permitted: conforming tools MUST ignore keys they do not recognize (an informational diagnostic at most, §12.2), and project-specific keys MUST NOT redefine the spec-defined keys. Two consistency rules bind the defined keys: `provenance: inferred` combined with `status: approved` or a present `approved_by` is a contradiction (informational diagnostic, §12.2) — accepting an inferred file flips `provenance` and records `approved_by` in the same act — and `provenance` remains the only field that qualifies a file's *authority* (§17.3); `owner`, `status`, and `approved_by` are accountability and lifecycle metadata and never change how tools treat the file's content. The boundary all these fields sit on — what belongs to the system versus what belongs to the work on the system — is defined in §1.3.

The frontmatter carries **no** per-file `version:` or `spec:` field. The project-wide AIM version and spec URL live in **`AGENTS.md` at the project root** (see §3.3) — a single source of truth that eliminates redundancy and drift between files. There is no per-file version anywhere in the language.

### 3.3 `AGENTS.md` — Project Bootstrap

Every AIM project carries an `AGENTS.md` file at its root. This is the universal entry point any agent (Claude, Cursor, Aider, Gemini, etc.) reads first when entering the project — the convention originated with coding agents, predates AIM, and is now the de facto standard across the agent ecosystem.

**Required structure:**

```markdown
---
aim_version: 5
aim_root: ./aim/
spec: https://intentmodel.dev/spec.md
---

# Agents

This project uses the **Agentic Intent Model (AIM) v5** for behavioral specification.

[...prose explaining roles, conventions, project specifics...]
```

The frontmatter on `AGENTS.md` carries:

- `aim_version` — the AIM language version this project targets (e.g. `5`)
- `aim_root` — where `.aim` files live (default `./aim/`)
- `spec` — the canonical specification URL for the declared version

The prose body explains AIM to a cold-start agent in natural language: what the roles are, where `.aim` files live, what conventions apply, that `.aim` files are a projection of a node-and-edge graph, and that mapping and binding facets live alongside their intent. Anything an agent needs to know about working in this project — both AIM and non-AIM — belongs here.

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
  <intent>/       # one directory per intent (mapping/binding facets live inside it)
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

The `aim/specs/` directory name is reserved for cached specifications (`.md` files) and must not be used as an intent namespace. Mapping and binding facets are **not** separate top-level directories — they are `kind: mapping` / `kind: binding` files that live inside their intent's own directory (§4.2, §9.3, §10.2).

Any other directory under `/aim/` that contains a `<name>.aim` file is an intent.

### 3.5 Body (Markdown)

The body of the file is Markdown. Structure is conveyed by heading levels:

- **H1** — the intent's display name (exactly one per file)
- **H2** — top-level sections (`## Summary`, `## Requirements`, `## Tests`, `## Children`, `## Dependencies`) and facet blocks (`## Schema: Task`, `## Contract: CreateTask`, etc.)
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

Binding-facet files use `## Bind: <FacetType>:<Name>` headings — the payload after `Bind:` is exactly the bound node's in-intent address minus the leading `#` (see §10.2):

```markdown
## Bind: Contract:CreateTask
```

Top-level section headings use the bare form:

```markdown
## Summary
## Requirements
## Tests
## Children
## Dependencies
```

Tooling MUST accept `## Subintents` and `## Subcomponents` — the headings earlier versions wrote — as deprecated aliases for `## Children`.

The facet heading text is the node's address within the file (§2.2). Every facet heading MUST be immediately followed by an explicit `### Summary` sub-block, with the single exception of a `Persona` acting only as a role/access declaration (§7.8). This keeps node boundaries deterministic.

**Facet name grammar.** A facet `<Name>` MUST match `[A-Za-z][A-Za-z0-9_]*` (PascalCase recommended) — no spaces, no punctuation. A heading whose name violates the pattern (`## Schema: Todo Item`) is a hard error (§12.1). This constraint is what lets a name sit verbatim inside an `aim:` link destination and a `## Bind:` heading as a valid CommonMark link target without percent-encoding (§2.2).

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

Modifiers: `required`, `optional`, `min(n)`, `max(n)`, `ref(<Type>.<field>)`, `ref(<intent>#<Type>.<field>)`, `enum(a, b, c)`, `default(<value>)`.

`ref(<Type>.<field>)` is a **typed graph edge** (`refs`, §8.2): it links a schema attribute to another schema's attribute and is collected into the graph alongside inline edge tokens.

**Resolving `ref()`.** The `<Type>` resolves as an unqualified facet name of type `Schema` through the canonical resolution algorithm (§11.1); if it resolves in more than one intent along the resolution path, first-match-wins per §11.1 (a shadow diagnostic fires on the losing sources). To pin a specific provider, use the qualified form `ref(<intent>#<Type>.<field>)`. It is a hard error (§12.1) if `<Type>` does not resolve to a Schema, or if `<field>` does not exist as an attribute on the resolved schema.

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

**Task lists deserve specific mention.** Markdown's `- [ ]` syntax is forbidden in `## Requirements`, `## Tests`, and other structured blocks even though it looks like a bullet list. The `.aim` file is *intent*, not *status*. Implementation and verification status live in a drift report under `/aim/work/` produced by the Reviewer — see §1.3 (Authority Model) and the Reviewer's drift-report convention in [`agents/aim-reviewer.md`](agents/aim-reviewer.md). Putting status into intent makes the spec lie when code changes and the checkbox doesn't. The frontmatter `status:` field (§3.2) is unaffected by this rule: it tracks the *specification's* own authoring lifecycle, never the implementation's.

**Raw HTML is banned everywhere** because it breaks parsers and circumvents the Markdown-native discipline.

---

## 4. Project Layout

### 4.1 Decomposition-First Default

AIM decomposes real applications into focused child intents. Each child is a real intent with its own intent file, its own namespace, and its own facets. The parent intent serves as an index plus a home for cross-cutting requirements and shared facets.

Reasons this is the default:

- LLMs reason better over small focused files than large ones
- Multiple agents can work on different children in parallel without merge conflicts
- Diffs are meaningful when each file has a single concern
- Synthesis maps cleanly to small focused code modules

The namespace hierarchy is the `extends` edge of the graph (parent ← child); it is one relation among many, not the model's organizing principle.

### 4.2 Canonical Layout

```
/aim/
  juice.tasks/
    juice.tasks.aim                  # parent: index + shared
    juice.tasks.schema.aim           # shared schemas (Task, User refs)
    juice.tasks.mapping.aim          # capability mappings (kind: mapping)
    juice.tasks.binding.aim          # code bindings (kind: binding)
    create_task/
      juice.tasks.create_task.aim
      juice.tasks.create_task.contract.aim
    assign_task/
      juice.tasks.assign_task.aim
    complete_task/
      juice.tasks.complete_task.aim
```

Rules:

- Each intent lives in a directory named after its namespace.
- The intent file filename matches `<intent>.aim`.
- Sidecar filenames match `<intent>.<kind>.aim` — facet files (schema, contract, …) and the mapping/binding files alike, all co-located with their intent.
- Child intents live in nested directories under the parent.
- Mapping and binding facets belong to the child they realize: a facet for `juice.tasks.create_task` lives in the `create_task/` directory, not the parent's.
- Generic filenames (`aim.aim`, `schema.aim`, `binding.aim`) are invalid.

### 4.3 When To Collapse Into A Single File

An intent should stay in a single `.aim` file (no children, facets embedded inline) only when **all** of the following hold:

- Total content fits comfortably in a single screen of reading.
- There is one clear behavior, not a set of distinct features.
- No facet needs independent ownership or review.

Otherwise, split. Split is the default; single-file is the exception.

### 4.4 Path Identity

The header `aim:` field is authoritative for identity. The directory and filename must agree with the header — tools treat path/header mismatch as a hard error. This lets paths function as a fast sanity check without competing with the header as the source of truth.

### 4.5 One Version Per Project

A working project is **single-version**: its `/aim/` tree conforms wholly to one AIM language version, because graph derivation and conformance require one consistent model. Bringing in intents authored against an older version means migrating them first (§13) — a project never mixes versions.

---

## 5. The Intent Tree

### 5.1 Definition

A child intent is an intent whose namespace extends its parent's namespace by exactly one segment:

- Parent: `juice.tasks`
- Child:  `juice.tasks.create_task`

The child declares the parent in its frontmatter:

```yaml
---
aim: juice.tasks.create_task
kind: intent
parent: juice.tasks
---
```

A child is a real intent: it has its own intent file, its own facets, and is independently addressable. The `parent:` relation is the graph's `extends` edge.

**The constraint is on the name, never the count.** "Exactly one segment" defines the shape of a single parent→child *edge* — it does not limit fan-out or depth. A parent has as many children as its capabilities demand (3–9 per level is the healthy band, §5.5), and a child nests further the moment its own behaviors earn children of their own (§15.4). One segment per edge; any number of edges.

Why one segment: it keeps the namespace an honest tree coordinate. The parent chain and the namespace walk are the same walk (§5.4, §11.1); no level can exist without its own intent file and Summary; and discovery (§5.3) stays mechanical. A grouping that wants to skip a level is either a real intermediate intent or a compound leaf name (`admin_reports`) — never an unnamed level.

### 5.2 Parent As Index

The parent intent's intent file serves two purposes:

1. **Index of children** — either auto-discovered from sibling directories or explicitly listed.
2. **Home for cross-cutting concerns** — shared requirements, shared schemas, shared personas, shared events that apply across all children.

Example parent intent:

````markdown
---
aim: juice.tasks
kind: intent
---

# Tasks

A task management subsystem. Users create, assign, and complete tasks tied to projects.

## Summary

The tasks subsystem owns the full task lifecycle: creation, assignment, state transitions, and archival. All child intents share the `Task` schema and emit events on the `tasks.*` channel.

## Requirements

- Every task belongs to exactly one owner.
- State transitions are auditable.
- Soft-delete is preferred over hard-delete.

## Children

- [create_task](./create_task/juice.tasks.create_task.aim) — create a new task
- [assign_task](./assign_task/juice.tasks.assign_task.aim) — assign a task to a user
- [complete_task](./complete_task/juice.tasks.complete_task.aim) — mark a task completed

## Schema: Task

### Summary

The shared task record used by all children.

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
````

### 5.3 Child Discovery

By default, children are **auto-discovered**: any sibling directory containing a `<namespace>.aim` file with a matching `parent:` field is treated as a child of the parent.

The parent may override discovery with an explicit `## Children` block. When the explicit list is present:

- listed children must exist on disk
- discovered children not in the list emit a hard error (ambiguous authority)
- the explicit list is authoritative for the order in which children are presented to agents and tooling

### 5.4 Upward Facet Resolution

A child intent may reference facets defined in the parent without qualification. The complete precedence rules are defined once in §11.1 — children add one detail: the **parent chain** step walks the namespace upward (parent → grandparent → root) until a match is found or the chain ends.

Tools emit an informational diagnostic when a child defines a facet that shadows one already defined in a parent. This is usually a sign that either the shared definition should move up, or the child's name should be more specific.

### 5.5 Tree Shape

**Breadth:** 3–9 children per level is the healthy band. A parent's children should read as a short table of contents for the level below — that is the tree's job as the human projection (§2). One child is a smell (§15.2 — no single-child parents); a dozen or more means an intermediate level wants to exist or siblings want merging.

**Depth:** depth is **earned level by level, never capped**. Every level must itself hold the breadth band and read as a table of contents for the level below; depth follows from scale alone — a focused tool may need one level, a whole-organization model (§18) many. The stopping rule is content, never a count: decomposition stops where an intent holds **one clear behavior** (§4.3) — while an intent's Summary still says "and", it needs children. Level count is never a reason to stop, and never a reason to split. What tools flag is not absolute depth but *accidental* depth: a chain of single-child levels (§15.2), or a level outside the breadth band. A dotted address grown unreadable is usually breadth debt surfacing as depth, not a depth problem itself.

There is no version inheritance: `.aim` files carry no version, so a child is automatically consistent with its parent. (v4 removed the v3.1 "version inheritance" rule entirely.)

---

## 6. Intent Envelope

### 6.1 Minimum Valid Intent File

```markdown
---
aim: demo.todo
kind: intent
---

# Todo

## Summary

A simple personal todo tracker.

## Requirements

- User can add, complete, and delete todos.
```

Hard minimum for validity:

- Valid frontmatter with required fields (`aim`, `kind`).
- Exactly one H1 heading.
- A `## Summary` section with at least one paragraph **or** an H1 followed by a paragraph that serves as the summary.
- A `## Requirements` section with at least one bullet.

Recommended:

- `## Tests` section with observable behavior bullets.
- One or more facets when the intent has stable interfaces.

### 6.2 Extended Intent Example (Child Intent)

````markdown
---
aim: juice.tasks.create_task
kind: intent
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
````

Note: `Task` and `User` are not defined in this file — they resolve upward to the parent intent `juice.tasks` (§11.1).

---

## 7. Precision Facets

The six behavioral facets are unchanged in meaning from v3.1. What changes is how their cross-references are written: prose mentions become typed edge tokens (§8), and the inverse blocks `### Trigger` and `### Emitted By` are removed because they are derivable. v4 added the seventh facet — **Trigger** (§7.7) — for non-actor entry points such as schedules and webhooks.

### 7.1 Schema

Data at rest, structural types, and constraints.

````markdown
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
````

### 7.2 Contract

Externally observable guarantees and obligations.

````markdown
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
````

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

When a guarantee cannot be cheaply and completely verified from its outcome, a Flow's `### Steps` take on a second job: they are the normative **proxy verifier** for that guarantee (§15.10).

### 7.4 Persona

Actor identity, role semantics, and view access.

```markdown
## Persona: TaskOwner

### Role

- Authenticated user who owns one or more tasks.

### Access

- [accesses](aim:#View:TaskDashboard)
- Create and complete tasks — [invokes](aim:#Contract:CreateTask), [invokes](aim:#Contract:CompleteTask)
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

````markdown
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
````

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

**Deadlines and calendar rhythms.** Time commitments — SLAs, escalation windows, expiries, recurring obligations — are all this one construct: a Trigger with `### Kind` `deadline` (event-anchored) or `schedule` (calendar-recurring). Its `### Schedule` lines take one of two forms, each with an optional informal *unless-clause* naming what disarms the timer:

- **Event-anchored:** `<n> <unit> after [Event:<Name>]` with units `minutes | hours | days | business-days | weeks` — e.g. `5 business-days after [Event:ContractSigned] — unless [Event:KickoffScheduled]`.
- **Calendar-recurring:** `monthly on the <n>th` / `weekly on <weekday>` / `yearly on <date>`, alongside the machine-precise `cron:` form — e.g. `monthly on the 8th — unless [Event:ReportReceived] for the period`.

**The unless-clause is informal prose and therefore not conformance-checkable** — a tool arms and disarms timers from the realization; nothing evaluates the clause text. When disarm verification matters, the disarming condition SHOULD be an **Event** emitted by the fulfilling operation, and the clause SHOULD name it (`— unless [Event:KickoffScheduled]`): the disarm condition then references a node the graph can check — the Event exists and has an emitter (§12.2) — while a clause naming anything else remains documentation.

Which operating calendar `business-days` names is realization, bound to whatever arms the timer — the duration and its anchor are the intent. Recurring patterns compose from this construct alone: an SLA is a deadline firing an escalation, an escalation ladder is chained deadline Triggers, an expiry is a deadline firing a revocation.

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

An **authoring shorthand** is permitted for same-intent references: the verb followed by a backticked address, `invokes` `` `#Contract:CreateTask` ``. Tools normalize the shorthand to the canonical link form when deriving the graph. The shorthand is the smallest possible delta from what v3.1 authors already typed (`` `Contract: CreateTask` ``): prepend the verb, switch to the address form.

**Normalization is in-memory only.** Normalizing the shorthand to the canonical link form happens *during graph derivation*; a tool MUST NOT rewrite authored source as a side effect of deriving the graph (consistent with the §1.3 authority model — the author owns the file). Both the shorthand and the canonical link form are valid on disk indefinitely, and every conforming parser MUST accept both. A formatter or linter MAY offer canonicalization to the link form as an explicit, user-invoked operation, never as an automatic rewrite.

**Prose convention.** The recommended style for an edge token inside a list item is *human label — [verb](aim:…)*: a plain-language label, an em-dash, then the token. The prose SHOULD NOT restate the verb the link text already carries (write `Create task — [exposes](aim:#Contract:CreateTask)`, not `Create task exposes [exposes](aim:…)`). A bare token with no label (`- [accesses](aim:#View:TaskDashboard)`) is equally valid where no label adds meaning.

The **`from` node** of an edge is the nearest enclosing facet node of the line the token sits on (the Contract / Flow / View / Persona whose block contains it). The **`to` node** is the resolved address.

For a cross-intent reference, the address is fully qualified:

```
- [invokes](aim:company.storage#Contract:PersistTask)
```

This subsumes the *use site* of a v3.1 `## Dependencies → Imports` alias: the import still declares the alias (§9), but the call site now points at a real node address, so a dangling import becomes checkable.

### 8.2 Closed Verb Taxonomy

There are eleven **declared** verbs and three **derived** inverses. Each declared verb has a fixed from→to node-type schema. A verb used between disallowed node-types is a **hard error**.

| Verb | from | to | Meaning | Kind |
|---|---|---|---|---|
| `exposes` | view | contract | a View action surfaces a Contract to users | declared |
| `invokes` | flow, view, contract, persona | contract, flow | a call into another behavioral unit — from a Persona: the actor performs the operation directly (§7.4) | declared |
| `reads` | contract, flow, view | schema | reads a persisted entity | declared |
| `mutates` | contract, flow | schema | creates / updates / deletes an entity | declared |
| `emits` | flow, contract | event | produces an event | declared |
| `subscribes` | flow, contract, intent | event | consumes an event | declared |
| `accesses` | persona | view, intent | a persona may reach a view, or a whole screen/route intent | declared |
| `navigates` | view | view | UI navigation between surfaces | declared |
| `triggers` | trigger | contract, flow | a schedule, webhook, or external origin initiates a behavioral unit | declared |
| `refs` | schema attr | schema attr | data-level foreign reference (the `ref()` modifier) | declared |
| `satisfies` | contract, flow, view, trigger | requirement item | a behavioral unit (or a deadline Trigger enforcing a time policy) realizes a `## Requirements` item | declared |
| `triggered-by` | flow, contract | contract / view / trigger / persona | inverse of `invokes`/`exposes`/`triggers` — a persona appears here when it invokes the unit directly (§7.4) | derived |
| `emitted-by` | event | flow / contract | inverse of `emits` | derived |
| `satisfied-by` | requirement item | contract / flow / view / trigger | inverse of `satisfies` | derived |

`requires` is **not** a graph verb — it stays as `## Dependencies → Requires` (a capability alias resolved by a mapping, §9). `extends` is **not** a graph verb — it is the `parent:` frontmatter relation (§5.1). **Render/layout composition** — a screen displaying another view inline (a dashboard laying out widget-panels) — is **not** a graph verb either: a UI piece has fluid granularity (`### Display` prose in its host view when simple, a promoted child intent owning its own facets once it earns them, §15.9), and the inline arrangement is realization expressed in code and bindings (§1.3), not an intent edge.

An `accesses` edge may target a **View** (access to one surface) **or** a **intent** (route/screen-level access — the persona may reach that whole feature). Use the intent form for role-gated screens that aggregate several views; `[accesses](aim:app.profile)` is valid and means "this persona may reach the profile screen."

**`exposes` vs `invokes` from a View.** Both are legal view→contract edges, and the choice carries meaning. Use **`exposes`** when the contract is reached through a *user-initiated action* on the view — a button, a form submit, a gesture. Use **`invokes`** when the view calls the contract *programmatically*, with no user initiation — an on-load data fetch, a poll, a prefetch. Either inbound edge counts as the contract being "reached" for the orphan check (§12.2); the distinction records whether the behavior is user-driven, which matters for reading intent and for realization.

**`subscribes` from a `intent`.** Almost every `subscribes` edge is declared at the consuming Flow or Contract. A `intent`-level `subscribes` is a deliberate early-stage exception: it declares that an intent consumes an event *without yet naming the internal handler* — `[subscribes](aim:#Event:TicketResolved)` written at the intent root. It is valid at Level 1/2; at Level 3 it SHOULD be refined to a flow- or contract-level edge once the handler exists (an informational diagnostic flags an intent-level `subscribes` that survives into a Level-3 intent, §12.2).

**`satisfies` and its target.** `satisfies` is the one edge that reaches a sub-block target: its `to` is a `## Requirements` list item, not a facet node. It is declared at the acting unit — the Contract, Flow, or View that realizes the requirement, or the deadline Trigger that enforces a time policy (§7.7). The token URI form is `aim:[<intent>]#Requirements[<key>]`: the reserved section address carries **no** `FacetType:` colon, which is exactly what distinguishes it from the facet form `#<FacetType>:<Name>` and keeps it a valid CommonMark link destination (§2.2, §3.6). The `<key>` takes two forms, discriminated by grammar:

- **Positional** — a 1-based integer: `[satisfies](aim:#Requirements[2])`. Valid everywhere, but fragile: reordering bullets re-points it (§2.2, §16.3 invariant 1). The casual form for small models.
- **Labeled** — a name matching the facet-name grammar (§3.6): `[satisfies](aim:#Requirements[NET14])`. A requirement declares its label by opening the bullet with a bolded name and an em-dash:

  ```markdown
  ## Requirements

  - **NET14** — The invoice is issued within one business day of signature, net-14.
  - **COUNTERSIGN** — No work is scheduled before the contract is countersigned.
  - Requesters see only their own tickets.        (unlabeled — positional only)
  ```

  A labeled reference survives any insertion or reordering; the label is part of the requirement's identity, so *renaming a label* is the `rename`-class transform instead. Labels MUST be unique within their intent's `## Requirements` and SHOULD be used once `satisfies` edges exist; labeled and unlabeled bullets may coexist, and an unlabeled bullet remains addressable by position.

Cross-intent targets are fully qualified either way: `aim:app.tasks#Requirements[NET14]`. This makes "which behavior satisfies this requirement?" a graph query, and the derived inverse `satisfied-by` (§8.4) makes the reverse computable.

`satisfies` targets **only** a `## Requirements` list item. It never targets a `## Capability:` surface (§9.2) — that is a facet node resolved by a mapping, not a requirement statement; `[satisfies](aim:#Capability:AssigneeUsers)` is a hard error (type mismatch, §12.1). *(v4 named this surface `## Requirement:`; v5 renamed it to end the collision with `## Requirements` items — §13.3.)*

### 8.3 Declared vs Derived

- **Declared once, at the acting end.** The node that performs the verb owns the edge: a View declares `exposes`/`navigates`/`reads`, a Flow declares `invokes`/`emits`/`reads`/`mutates`, a Persona declares `accesses`/`invokes`, a Contract declares `emits`/`mutates`/`invokes`, a Trigger declares `triggers`, a Schema attribute declares `refs`.
- **Inverse views are derived, never authored.** The v3.1 blocks `### Trigger` ("Invoked by Contract: X") on a Flow and `### Emitted By` on an Event are inverse projections of `invokes`/`emits` edges. v4 removed them from authored source. A tool may render them as read-only views.

This is the structural fix for v3.1's "three inconsistent expressions" problem: there is now exactly one authoritative direction per relation, so the forward and backward statements can never fall out of sync.

### 8.4 Inverse Derivation

For every declared `invokes`/`exposes` edge `A → B`, the graph contains a derived `triggered-by` edge `B → A`. For every declared `emits` edge `A → E`, the graph contains a derived `emitted-by` edge `E → A`. For every declared `satisfies` edge `A → R` (R a `## Requirements` item), the graph contains a derived `satisfied-by` edge `R → A`. Derived edges are computed during graph derivation (§2.4 step 4) and are available to tooling and reviewers exactly like declared edges, but they never appear in source.

If an author writes a `### Trigger` or `### Emitted By` block anyway (e.g. migrated content not yet cleaned up), tools reconcile it against the derived set and emit an informational "redundant inverse, possibly stale" diagnostic on mismatch.

### 8.5 Before / After

The `View: TodoDashboard` facet from the canonical example, v3.1 prose vs the graph form (v4 onward):

**v3.1:**

```markdown
### Actions

- Submitting the "New Task" form → invokes `Contract: CreateTodo`.
- Tapping the checkbox on a PENDING task → invokes `Contract: CompleteTodo`.
```

**Graph form:**

```markdown
### Actions

- Submitting the "New Task" form — [exposes](aim:#Contract:CreateTodo)
- Tapping the checkbox on a PENDING task — [exposes](aim:#Contract:CompleteTodo)
```

Both forms render on GitHub. The graph form additionally yields two first-class edges `View:TodoDashboard → exposes → Contract:CreateTodo|CompleteTodo`, so renaming a contract dangles the edge (hard error), an orphan check confirms every contract is exposed, and the impact set of either contract now formally includes the view. The free prose ("Submitting the New Task form") survives as the human label; only the edge is now machine-recognizable.

### 8.6 Extending The Verb Set

The taxonomy is closed on purpose: every verb an author must learn taxes every author, and a verb that means "relates to" is prose with extra syntax. Pressure to add verbs is permanent; this policy is the gate. A verb is admitted into a future version only when **all** of the following hold:

1. **It is a relational commitment** between existing node types — not an attribute (belongs in `aim-attrs`), not sequencing (belongs in a Flow's `### Steps`), not composition or layout (realization, §15.9), not accountability metadata (prose in `### Role`/`### Authz`).
2. **It is not expressible today** — no existing verb plus prose carries the meaning without losing checkability. (`satisfies` passed this test: requirement linkage was uncheckable prose; `performs` fails it: it is `invokes` from a persona.)
3. **It pays rent** — at least one question becomes computable, or one diagnostic becomes possible, *only* with the new verb. A verb that no validator, query, or reviewer check ever consumes is decoration.
4. **It has demonstrated need** — real models worked around its absence (in prose, in convention) before it is canonized. Verbs are admitted from evidence, never from anticipation.
5. **It is fully specified on arrival** — a fixed `(verb, from, to)` schema, its derived inverse (or the explicit statement that none is derived), and its diagnostics.

Two standing rules bound the process: **verbs are forever** — removing or renaming one is a breaking change to every model in existence, so the default answer is no; and **one verb, one meaning** — no aliases, no domain-specific synonyms (a domain may *read* a verb in its own vocabulary, never spell it differently).

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

- **Imports** reference concrete provider surfaces from other intents. An import declares an alias; the *use site* is a cross-intent edge token (§8.1) whose address names the real node.
- **Requires** declares required capabilities by alias (the `requires` relation). The alias is resolved via a mapping file.

### 9.2 Capability Surfaces

Required capabilities may be documented inline with a `## Capability: <Alias>` block:

```markdown
## Capability: AssigneeUsers

### Summary

Capability required to resolve user identities.

### Operations

- `ResolveUser(id) -> UserRecord`
```

### 9.3 Mapping Files

Mappings bind required aliases to concrete providers. A mapping is a `kind: mapping` file that co-locates with its intent, exactly like any other facet (§4.2).

```markdown
---
aim: juice.tasks
kind: mapping
---

# Tasks Mappings

## Map: AssigneeUsers

### Target

- `company.identity`

### Operation Map

- `AssigneeUsers.ResolveUser` → `company.identity.ResolveUser`
```

Unresolved `Requires` aliases are hard errors at validation time.

**Mappings vs bindings.** A mapping is an **intent→intent** capability binding: it resolves a required-capability alias to a concrete provider *intent*. A binding (§10) is an **intent→code** realization binding: it links an intent node to the *source code* that implements it. They are distinct facets (`kind: mapping` vs `kind: binding`) — both co-locate with their intent, and must not be confused with each other.

---

## 10. Binding Layer

A binding records *where* an intent node is realized — in code, in a system configuration, in an automation, in an agent — so the Reviewer can diff the declared intent graph against the realized graph (§12). Bindings are optional: an intent with no bindings is a valid Level 1/2 intent (§11.2). Bindings raise fidelity, exactly as facets do.

### 10.1 Drift As Graph-Diff

Two graphs:

- **Declared graph (D)** — nodes are AIM intents/facets; edges are the typed relations of §8. Authored by the Architect; behavioral authority.
- **Realized graph (R)** — nodes are realization sites (functions, routes, tables, SaaS workflows, agent skills); edges are relations recovered from the realization — code, system configuration, or execution logs (this handler writes that table; this automation fires on that event; these log entries show the step performed).

A **binding** connects a node in D to a node in R. Drift detection projects D and R into a common space through the bindings and diffs them.

**Building R is bounded, not global.** A tool does **not** statically analyze the whole codebase to reconstruct R. Bindings localize the work: for each *declared* edge, the Reviewer opens the *bound site* and checks that one claim — "does `src/todos/create.ts#createTodo` actually mutate `Ticket` and emit `TicketCreated`?" That is read-the-bound-file, not map-the-system, and it is **polyglot by default** (an agent reads any language, where a static analyzer needs one parser per language; dynamic code that defeats static analysis can still be reasoned about and flagged). Because R is *inferred* this way, every graph-diff finding carries a **confidence** (§12.3). Tooling that *does* have static analysis MAY supply a precomputed **realized-graph manifest** for deterministic diffing — this spec does not define that manifest's format; it is an ecosystem concern.

**What graph-diff verifies — and what it cannot.** Graph-diff verifies *structure*: that each declared edge has a realized counterpart at its bound site. The *semantic* content of a guarantee — what an `### Ensures` bullet claims — is verified by reading the bound code, and the finding carries a confidence (§12.3). A third class of guarantee is not cheaply and completely verifiable from output or code at all — judgment-shaped claims ("the summary is accurate," "the review was performed diligently"). For those, the declared *procedure* stands in as the verifier: see §15.10 (proxy verification).

### 10.2 Binding Notation And Location

A binding target is a portable **locator URI**, written as inline code. The scheme set is **open**: the generic form is `<scheme>:<opaque-locator>`, this specification registers the code family, and other domains register theirs (a process model binds to `system:`, `workflow:`, `form:`, `agent:`, `queue:`, `calendar:` locators). Unknown schemes are valid; a tool that cannot check a scheme reports the binding as unverifiable, never as an error. The code family:

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
- binds: `src/todos/create.ts#createTodo` — as: handler
```

`as` (`handler | model | component | route | topic | test`) is optional and advisory. One node may declare multiple bindings (a Contract realized by both a route and a handler). Everything after the backticked locator is prose a tool may use but the parser may ignore.

Each bound node gets one `## Bind: <FacetType>:<Name>` heading — the same `<FacetType>:<Name>` that addresses the node in its intent (§2.2, §3.6), so a binding heading is mechanically the node's in-intent address minus the leading `#`. The `binds:` bullets under it list that node's code locators.

**Where bindings live: a dedicated `kind: binding` file that co-locates with its intent (§4.2).** Realization is not behavior (§1.3), and realization drifts faster than intent — keeping bindings in their *own file* is what keeps the behavioral file's diffs meaningful and lets a binding go stale without the intent being wrong. The isolation that matters is the *file/facet* boundary, not a separate directory tree: an intent owns all its facets — schema, contract, mapping, binding — in one place, so a split or rename (§16) moves one coherent unit instead of reconciling parallel trees. This mirrors how `kind: mapping` co-locates capability bindings.

```markdown
---
aim: nemicko.demo.todo
kind: binding
---

# TaskManager Bindings

## Bind: Contract:CreateTodo

- binds: `src/todos/create.ts#createTodo` — as: handler
- binds: `route:POST /api/todos` — as: route

## Bind: Schema:TodoItem

- binds: `src/models/todo.ts#TodoItem` — as: model
- binds: `table:todo_items` — as: table

## Bind: Event:TodoCreated

- binds: `topic:todos.created` — as: topic
```

**Bindings always live in a `kind: binding` file — there is no inline binding form.** Keeping realization out of the behavioral files is the whole point (§1.3): a code path may rot without making the intent wrong, and a behavioral file never carries a volatile `file#symbol` path. (An early v4 draft allowed an inline `### Realized By` escape hatch for trivial intents; it was removed — the lazy path muddied the behavior≠realization boundary, so bindings are separate, full stop.)

### 10.3 Optional-Capability Invariant

- An intent with no binding facet is fully valid (Level 1/2). Binding coverage is reported as informational, never a hard error.
- Bindings become load-bearing only at Level 3 graph-diff — which the author opted into by writing the bindings. You are never punished for a binding you did not write.

---

## 11. Resolution And Synthesis

### 11.1 Canonical Resolution Algorithm

This algorithm is **authoritative**. All other sections that describe resolution (notably §5.4 for child intents and §9.3 for mappings) defer to this order. It resolves both unqualified facet names and full node addresses (§2.2).

For any reference within an intent:

1. **Intent part.** If the address carries an intent prefix, resolve to that exact namespace (which must exist). If absent, the intent is the current one.
2. **Facet name**, resolved within the chosen intent in this precedence order:
   1. **Embedded** — a facet block in the same intent file.
   2. **Sibling facet file** — `<intent>.<kind>.aim` next to the intent file.
   3. **Explicit Imports** — entries under `## Dependencies → Imports` in the current file. Explicit author intent beats implicit parent inheritance.
   4. **Parent chain** — facets defined in the parent intent, then the grandparent, and so on up the namespace until a match is found or the chain ends.
   5. **Required alias via mapping** — names declared under `## Dependencies → Requires`, resolved through a mapping file (§9.3).
   6. **Absent** — the name does not resolve. If it was required by another facet or edge, this is a hard error.
3. **Type agreement.** If the reference is an address with a `FacetType` (e.g. `#Contract:X`), the resolved node's type must match. A `#Contract:X` that resolves to a `## Schema: X` is a hard error.
4. **Sub-block part.** If the address carries `→ ### Sub [n]`, resolve within the facet node by heading text and 1-based list index. The reserved requirement-item form `#Requirements[<key>]` (§8.2) resolves against the resolved intent's top-level `## Requirements` section: a numeric `<key>` by 1-based list index, a named `<key>` by matching a bullet's declared **label** (`- **<Label>** — …`). An out-of-range index, an unknown label, or a duplicate label in the section is a hard error.

The first match wins. Lower-precedence sources for the same name emit an informational diagnostic ("shadowed by higher-precedence source"). Tools must implement this exact order — there are no implementation-defined variations.

### 11.2 Specification Levels

- **Level 1** — Intent only. Useful for early exploration and simple intents.
- **Level 2** — Intent plus some facets and edges. Most production intents.
- **Level 3** — Full facet trace **with bindings present**, so the declared graph can be diffed against the realized graph. Highest fidelity for implementation and review.

The level affects expected implementation precision, expected code-generation precision, and strictness of traceability and graph-diff checks. Tools may report an intent's level as an informational diagnostic. Level 3 is the precise condition under which an unbound declared node becomes an enforceable finding (§12). Level-3 graph-diff is enforced by the Reviewer verifying each edge at its bound site with a confidence (§10.1, §12.3), or by a supplied realized-graph manifest.

### 11.3 Traceability Chain

The traceability chain is the set of typed declared edges through the behavioral facets:

```
Requirement → Contract / Flow / View → … → Flow / Schema / Event
Persona → View → Contract → Flow / Schema / Event
```

- The **root** of the chain is a **`## Requirements` item**: a behavioral unit `satisfies` it (§8.2), so following `satisfied-by` from a requirement reaches the behavior that realizes it, and a requirement with no inbound `satisfies` is an unrealized-requirement gap (§12.2). This closes the loop from stated requirement to running behavior.
- Entry points are a **Persona** (actor, `accesses` a View or screen intent) **or** a **Trigger** (schedule/webhook/external, `triggers` a Flow/Contract).
- `Persona` `accesses` `View` (or a whole screen intent).
- `View.Actions` `exposes` `Contract`.
- `Contract` `invokes` `Flow`.
- `Contract` and `Flow` `read`/`mutate` `Schema`.
- `Contract`/`Flow` `emits` `Event`.

In v3.1 this chain was prose and "a useful target, not a requirement." Since v4 it is **derived from the declared edges** and therefore checkable: a Level-3 intent is exactly one whose chain has no orphan nodes and no dangling edges (§12). Intent-only intents remain valid; tools emit a reduced-fidelity informational note.

---

## 12. Tooling Diagnostics

**Conformance and diagnostics are evaluated over the complete derived project graph** — every `.aim` file resolved together (§2.4) — never a single file. An intent is "clean" only when the whole graph it participates in is: duplicate entities, dangling references, and orphans are cross-file properties, so judging one file in isolation is never sufficient.

### 12.1 Hard Errors

- Missing or malformed frontmatter.
- Missing required frontmatter fields (`aim`, `kind`).
- Frontmatter `aim` does not match the file path.
- `parent:` declared but no parent intent file exists.
- Missing H1 heading, missing `## Requirements`, or empty `## Requirements`.
- Invalid facet type in heading (e.g. `## Data: X`).
- Facet name violating the `[A-Za-z][A-Za-z0-9_]*` grammar (e.g. `## Schema: Todo Item`) (§3.6).
- Duplicate facet definitions with the same name within the effective source.
- Ambiguous child-intent authority (auto-discovered child not in explicit `## Children` list).
- Unresolved `Requires` aliases with no matching mapping.
- Child-intent facet name collision with a parent facet name (when the parent definition is authoritative).
- Generic filenames (`intent.aim`, `schema.aim`, `mapping.aim`, `binding.aim`).
- **Dangling reference** — an edge token's `to` address resolves to Absent (§11.1). Same class as an unresolved `ref()` (`<Type>` resolves to no Schema).
- **Unresolved `ref()` field** — a `ref(<Type>.<field>)` whose `<Type>` resolves to a Schema but whose `<field>` is not an attribute of that schema (§3.7).
- **Unresolvable requirement target** — a `satisfies` key that is out of range (positional), matches no declared label (labeled), or a `## Requirements` section declaring the same label twice (§8.2, §11.1).
- **Type-mismatch reference** — an edge target resolves but its node-type ≠ the address's `FacetType`, or the `(verb, from, to)` triple is not in the §8.2 schema.

### 12.2 Informational Diagnostics

- Missing optional `## Tests`.
- Intent-only intent (no facets).
- Lower-precedence facet source shadowed by a higher-precedence one.
- Tree-shape smell (§5.5): a level outside the 3–9 breadth band, or a chain of single-child parents (§15.2).
- Unresolved `Import` alias (not blocking but flagged for repair).
- **Orphan node** — a facet node with no inbound edges of its expected kind: a Contract no View `exposes` and nothing `invokes`/`triggers`; an Event nothing `emits`; a View no Persona `accesses`; a Trigger with no outbound `triggers`. (A Flow or Contract entered via `triggers` or `subscribes` has a valid inbound edge and is not an orphan.) A **View is not an orphan** if (a) a Persona `accesses` it directly, **or** (b) a Persona `accesses` its intent or any ancestor intent — an intent-level `accesses` (§8.2) grants reachability to every View in that subtree.
- **Unrefined intent subscription** — a `intent`-level `subscribes` edge (§8.2) that survives into a Level-3 intent without being refined to a flow- or contract-level edge. Valid at Level 1/2; informational at Level 3.
- **Unrealized requirement** — a `## Requirements` list item with no inbound `satisfies` edge (§8.2): no declared behavior claims to realize it. Informational at Level 1/2; at Level 3 tools MAY promote it to a finding, since a full facet trace with no behavior for a stated requirement is a real gap.
- **Positional `satisfies` reference** — a `satisfies` edge targeting a requirement by index rather than by label (§8.2). Fragile under reordering; labels are the durable form.
- **Unconfirmed provenance** — a `provenance: inferred` file (§17) not yet human-accepted. A project's confirmation coverage (fraction of nodes confirmed) is reported as an informational metric, never a hard error.
- **Provenance/lifecycle contradiction** — `provenance: inferred` combined with `status: approved` or a present `approved_by` (§3.2). Accepting an inferred file flips `provenance` and records `approved_by` in the same act.
- **Unrecognized frontmatter key** — a frontmatter key this spec does not define (§3.2). Project-specific keys are permitted and ignored by conforming tools; the note exists for visibility only.
- **Stale inverse** — an authored `### Trigger`/`### Emitted By` block disagrees with the derived inverse set (§8.4).
- **Probable duplicate entity** — two nodes with the same facet-type and name in intents not linked by an import or reference (e.g. `auth#Schema:User` and `billing#Schema:User`). Same name is not proof of same entity, so this is a smell, not a hard error: the remediation is to make one canonical and reference it (§15.8), or to confirm they are genuinely distinct.
- **Over-embedded intent file (monolith)** — an intent file that embeds many facets, especially shared ones used across intents, instead of extracting them into sibling facet files or a `<app>.core` intent (§15.2, §15.8). The dual of duplication: both fragment maintainability at scale. A smell, not a hard error.
- **Noun-cluster (a child intent wanting to exist)** — inside a *mixed* intent, one noun has claimed a Schema plus several like-named Contracts/Flows (often a View too) while the intent's other facets serve different concerns — a `Note` schema with add/edit/list-note contracts and a notes view lying flat in `customer_management` next to customer CRUD. The cluster is a cohesive capability that accreted past the §4.3 line without any single change crossing it, and the tree has stopped telling its story (§2). Remediation is the **promote** transform (§16.2, §16.5): move the cluster — existing facets included — into its own child intent. Detection is heuristic and tools MAY tune it (a reasonable default: a Schema whose name recurs across three or more sibling Contracts/Flows, with at least two unrelated content facets remaining). It MUST NOT fire on an intent that holds *only* the cluster — that intent is already focused, and wrapping it would mint a single-child parent (§15.2). A smell, not a hard error.

### 12.3 Graph-Diff Findings (Reviewer)

When bindings are present, the Reviewer diffs the declared graph against the realized graph and produces drift findings. These map onto the Reviewer's existing missing / incorrect / undocumented kinds:

| Finding | Meaning | Severity / owner |
|---|---|---|
| `UNBOUND_NODE` | declared node has no binding | informational at Level 1/2; MISSING at Level 3 |
| `DANGLING_BINDING` | binding points at a realization site that no longer exists | INCORRECT → Realizer |
| `MISSING_EDGE` | declared edge has no realized counterpart at the bound site | MISSING → Realizer |
| `EDGE_MISMATCH` | edge exists on both sides but endpoints differ | INCORRECT → Realizer |
| `UNDECLARED_EDGE` | realized code has an edge with no declared counterpart | UNDOCUMENTED → Architect |
| `AMBIGUOUS_BINDING` | one node binds to conflicting sites, or two nodes bind the same site | ambiguous → user input |

Because R is inferred by reading the bound code (§10.1), **every finding carries a confidence** — `high` (the bound code clearly matches or clearly does not) or `needs-human-check` (dynamic or ambiguous code the Reviewer could not settle). A `clean` drift report (`status: clean`) means every declared edge was **reviewed as realized** at its bound site, and no undeclared behavior was found at those sites, *at the stated confidence* — not a proof of isomorphism. It is a materially stronger guarantee than "no prose mismatch found," but exactly as strong as the confidence attached and no stronger: R was examined at the bound sites, not reconstructed globally. For a proxy-verified guarantee (§15.10), confidence attaches to *procedure-conformance*, never to the outcome. The **impact set** (the nodes reachable from a changed node along inbound edges) is not a violation but a reporting capability, and is the headline payoff of the derived graph.

---

## 13. Migration

### 13.1 From v3.1

v4 is a breaking change. Migration tooling (outside this specification) converts v3.1 sources to v4 by:

1. **Relabel.** Update `AGENTS.md` frontmatter `aim_version: 3.1` → `5`; update the body's version references. The `.aim` extension does **not** change (unlike the v2.2→v3.1 `.intent`→`.aim` rename).
2. **Strip per-file version/spec.** Remove any lingering `version:`/`spec:` keys from `.aim` frontmatter. Fully automatable.
3. **Prose mentions → typed edges.** v3.1 already expresses the chain in recognizable patterns: backticked facet references inside `### Actions`, `### Ensures`, `### Emitted By`, `### Trigger`, and `CALL X.Y` lines in `### Steps`. A migration pass deterministically pre-extracts edges from these patterns and proposes them; edges implied only by free prose require an LLM-assisted pass with Architect confirmation. **Edges are never silently invented.**
4. **Delete derived inverse blocks.** Remove `### Trigger` and `### Emitted By` once their forward edges are declared (§8.4).
5. **Bindings are not generated by migration.** Migration leaves intents at Level 1/2 (valid, §10.3). A separate code-reading pass (Realizer- or tool-driven) proposes bindings against actual code afterward, raising a project to Level 3 without migration ever assuming code exists or is correct.

A project's `/aim/` tree must be wholly one AIM version (§4.5). The migration is one-shot per project. Projects still on v2.2 migrate v2.2 → v3.1 first (see the v3.1 spec), then v3.1 → v4 → v5 (§13.2, §13.3).

### 13.2 From v4.0 To v4.1

v4.1 is the July 2026 amendment wave. Most of it is additive — the `satisfies` verb and `satisfied-by` inverse (§8.2, §8.4), re-encoding with provenance (§17), the normative-graph rationale (§2), graph-first authoring guidance (§1.2, §15.1) — and requires no migration. Three changes are breaking for on-disk v4.0 projects, all mechanical:

1. **Co-locate mapping and binding facets.** Move each `aim/mappings/<intent>/<intent>.mapping.aim` and `aim/bindings/<intent>/<intent>.binding.aim` into the intent's own directory; delete the emptied `aim/mappings/` and `aim/bindings/` trees, which are now invalid (§4.2, §14.3).
2. **Colon in binding headings.** `## Bind: <FacetType> <Name>` → `## Bind: <FacetType>:<Name>` (§3.6, §10.2).
3. **Facet name grammar.** Facet names must match `[A-Za-z][A-Za-z0-9_]*` (§3.6); rename any facet whose name contains spaces or punctuation, re-pointing inbound edges per §16.3 invariant 1.

Relabel `AGENTS.md` to `aim_version: 5` and refresh the local spec cache (§3.4). Adoption of the additive features (`satisfies` edges, `provenance:`) is encouraged but not required for conformance.

This section covers migration *within* AIM (an older model version to the current one). Producing intent from a codebase that was **never** authored in AIM — reading code to infer the graph — is the reverse direction, defined in §17 (Re-Encoding).


### 13.3 From v4.x To v5

v5 is the **generalization release**: the language that specified software now specifies any system of commitments — an application, a business process, an organization (§18). Most of the wave is additive; four changes are breaking, all mechanical:

1. **Frontmatter key `facet:` → `kind:`.** The old key named the file's *role*, colliding with "facet" the node concept (§2.1). Sed-able: `facet: intent` → `kind: intent` across the tree. Tools SHOULD dual-read (`kind` falling back to `facet`) through the transition.
2. **`## Requirement:` → `## Capability:`** (§9.2). Ends the near-collision with `## Requirements` items that `satisfies` targets (§8.2).
3. **Binding advisory suffix `— kind:` → `— as:`** (§10.2), freeing `kind` for the frontmatter key.
4. **The core unit is named what it is: *intent*.** Since v3.1 the unit was called the *component* — software heritage in a language named the Intent Model. v5 names it the **intent** everywhere: the tree is intents all the way down (§2.1, §5), the parent index heading `## Subcomponents` → `## Children` (the old spellings remain deprecated aliases, §3.6), the node-type `component` → `intent`, addresses read `<intent>#<FacetType>:<Name>`.

Identity and structure: the language was renamed **Agentic Intent Model** (formerly *Application* Intent Model); the roles generalized to Architect / **Realizer** / Reviewer (§1.2); the Distribution section was removed (single-version rule now §4.5) and later sections renumbered accordingly.

Additive in the same wave, no migration required: labeled requirement targets (`#Requirements[NET14]`, §8.2); event-anchored and calendar-recurring Trigger schedules with `deadline` kind (§7.7); the open binding locator scheme set (§10.2); realized graphs recovered from configuration and execution logs, not only code (§10.1); `invokes` from a Persona and `satisfies` from a Trigger (§8.2); re-encoding generalized to any existing system, including elicitation with testimony provenance (§17); purpose-rooted organization models (§18); the verb-set extension policy (§8.6); governance frontmatter keys and the open frontmatter set (§3.2); proxy verification (§15.10).

Relabel `AGENTS.md` to `aim_version: 5`, apply the three renames, refresh the local spec cache (§3.4) — nothing else changes on disk.

---

## 14. Conformance Examples

### 14.1 Minimal Valid Intent

```markdown
---
aim: demo.snake
kind: intent
---

# Snake

## Summary

A single-player snake game.

## Requirements

- The snake grows when it eats food.
- Wall and self-collision end the run.
```

### 14.2 Intent With Children

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

### 14.3 Invalid

- Frontmatter missing `aim:` or `kind:` field.
- `## Data: Foo` heading (invalid facet type).
- Child intent file with `parent: juice.tasks` but no parent intent file exists.
- Two `## Schema: Task` blocks in the same effective source.
- Project missing `AGENTS.md` with declared `aim_version`.
- A directory named `aim/specs/` used as an intent namespace.
- A `kind: binding` or `kind: mapping` file placed in a separate `aim/bindings/` or `aim/mappings/` tree instead of co-located with its intent.
- An edge token `[invokes](aim:#Schema:Task)` (invalid: `invokes` cannot target a `schema`).
- An edge token `[satisfies](aim:#Capability:AssigneeUsers)` (invalid: `satisfies` targets a `## Requirements` list item, never a `## Capability:` surface, §8.2, §9.2).
- An edge token whose target address resolves to no node (dangling reference).

---

## 15. Practical Guidance

### 15.1 Default Authoring Rule

**Architect the graph, then serialize it.** From the requirements, identify the nodes — who acts (Personas), what they reach (Views), what they do (Contracts), how it runs (Flows), what it changes (Schemas), what it announces (Events, Triggers) — and the typed relations among them: who `accesses` what, what `exposes`/`invokes` what, what `mutates`/`reads` what, what `emits` and who `subscribes`, what `satisfies` which requirement. That graph **is** the design; the files merely record it.

Then write it down. Start by splitting: create the parent intent with the cross-cutting requirements and shared schemas, and each feature as a child intent. Keep each child focused on a single observable behavior. Declare the edges inline at the acting nodes as you serialize each facet. Collapse into a single file only when the whole intent is trivially small.

The test of a finished intent is graph-shaped, not prose-shaped: every requirement reachable via `satisfied-by`, every contract reachable from a persona or trigger, every event with an emitter — a connected graph, not a stack of well-written facets (§11.3, §12.2).

### 15.2 What Goes In The Parent

The parent intent file is a **lean index**, not a container:

- Cross-cutting requirements that apply system-wide.
- The `## Children` index.
- Dependencies.

Shared **facets** — schemas, personas, views referenced by multiple intents — are authored as their **own files**, never embedded en masse in the parent: a sibling facet file (`<intent>.schema.aim`, `<intent>.persona.aim`, `<intent>.view.aim`) for what's shared within a subtree, or a `<app>.core` intent (§15.8) for entities shared *across* top-level intents. Embedding many facets into one intent file produces a **monolith** (§12.2) — the dual of the duplication problem, and just as damaging at scale.

### 15.3 What Goes In A Child Intent

- The intent, requirements, and tests for a single feature.
- Contracts and flows specific to that feature, with their edges.
- Child-specific events.

### 15.4 When To Split A Child Further

When a child itself has multiple distinct behaviors with their own contracts. Example: a `payments` intent might split into `charge`, `refund`, `dispute` children, and `dispute` itself might split into `open_dispute`, `respond_to_dispute`, `resolve_dispute` if each has its own contract. Split as long as each new level re-earns the shape rules (§5.5) — and no further.

The signal is often a **noun-cluster** (§12.2) rather than a planned decision: one noun quietly claims a schema plus several like-named contracts inside a mixed intent. Promote the whole cluster — existing facets included — the next time a change touches it (§16.5).

### 15.5 When To Add Bindings

Add bindings once code exists and you want enforceable drift detection. Bind the stable nodes first (Contracts to handlers/routes, Schemas to models/tables, Events to topics). A binding facet turns the Reviewer's drift report from prose comparison into a graph-diff (§12). Skip bindings while an intent is still exploratory — Level 1/2 is valid.

### 15.6 Closed-Loop Workflow

1. Requirements → **graph**: nodes (facets) and typed edges, serialized as intents (children first, parent as index), edges declared inline at the acting nodes.
2. Intent → realization, reading the resolved graph; the Realizer emits bindings for what it realizes.
3. Implementation → graph-diff validation against the declared graph through the bindings.
4. Validation failures → code repair or intent revision, routed by the finding's owner.
5. New requirements → new child intent or revised parent; new edges declared at the acting nodes.

The intent is the contract. Code follows intent. When they diverge, one of them is wrong and the divergence is resolved explicitly.

### 15.7 Triggers, Schedules, And Orchestration

- **Non-actor entry points** — cron jobs, schedules, polling loops, webhooks, external systems — are modeled with a `## Trigger:` facet (§7.7) and a `triggers` edge into the Flow or Contract they start. This is what gives a nightly job or an inbound webhook a place in the graph; without it, the flow it starts would look like an orphan.
- **External events** need no new machinery: model the origin as a Trigger that `triggers` an ingest Flow, and let that Flow `emits` the internal Event. The event then has a real emitter and subscribers attach as usual.
- **Sagas and long-running orchestration** are expressible with existing verbs: the orchestrator Flow `invokes` each step, `mutates` a saga-state Schema to track progress, and `emits`/`subscribes` compensation Events. AIM captures the *intent* of the orchestration, not the durable-timer/signal semantics of a workflow engine — those remain an implementation detail bound to code.

### 15.8 Shared Entities And Canonicalization

The fastest way a large project rots is duplication: the same `User` (as a `Schema` and as a `Persona`), the same `Money`, the same `Status` reborn in file after file as each intent is authored in isolation — and then the copies drift and contradict. Two rules keep the graph single-sourced:

- **Resolve-or-reference, never regenerate.** Before defining a `Schema`, `Persona`, or any entity, the Architect **searches the project graph** for an existing node of that kind and name. If one exists, reference it (a `## Dependencies → Imports` alias plus the edge) instead of defining a new one. The derived graph is a queryable index precisely so this lookup is cheap — use it. Agents default to *generating*; the discipline is to *look first*.
- **Give cross-cutting entities one canonical home.** A parent holds what's shared within its subtree (§15.2). For entities shared *across* sibling top-level intents (`auth`, `tasks`, `billing` all needing `User`), designate one shared intent — by convention `<app>.core` — as the single definition site, and have the others import from it. One `User`, many references.

Tooling supports this from both ends: the **probable-duplicate diagnostic** (§12.2) surfaces same-type-same-name nodes that are not reference-linked, and the derived graph lets you list every definition of an entity to spot drift. Detection plus discipline is what keeps identity from fragmenting as the system grows — and it is only possible *because* the graph turns "every entity in the project" into something you can query.

Beware the **opposite trap**: do not dodge duplication by embedding every entity in one file. That just trades duplication for a monolith — equally damaging, and a real failure mode in practice (an agent told to avoid duplicate `User`s will happily cram all 20 schemas into one parent). The rule is *both*: don't duplicate **and** don't monolith. Shared facets live in their own files and the parent stays a lean index (§15.2); a canonical entity that consumers cannot reach by upward resolution must be importable (put it in an ancestor or `<app>.core`, not a sibling).

### 15.9 UI Composition And Fluid Granularity

A UI piece — a tab, a panel, a widget — has **fluid granularity**, exactly like any other capability. It is not a fixed kind of node in the model; what it *is* depends on how much behavior it carries, and it moves between forms by the **promote** transform (§16):

- **Trivial / behavior-less** — a static or host-fed panel with no contract, schema, or action of its own is **not a node**. It is a bullet in the host `## View:`'s `### Display`. Modeling it as its own facet adds a node the graph cannot check — nothing to dangle, nothing to impact — and earns it a false orphan diagnostic (§12.2).
- **Carries its own behavior** — once the piece acquires its own data, operations, or surface (the §4.3 test — a fetch contract, a schema, an action), it is **promoted** into its own child intent (§5, §16.2) that owns those facets. It rejoins the hierarchy through `extends` (the `parent:` relation) and connects to its host through the view edges that already exist: the host `## View:` `reads` the piece's schema, `exposes` or `invokes` its contract, or `navigates` to it when it is a separate destination rather than an inline part.

**Composition itself is not an intent relation.** That a host screen *lays out* a constituent view inline — as opposed to navigating to it or invoking its behavior — is realization: it lives in code and, where it matters, bindings (§1.3, §8.2). The intent graph models the piece's *behavior* and *reachability*, never its placement on the screen. This is the line §15.7 draws for orchestration: AIM captures intent, not rendering mechanics.

**Worked example — the promote boundary.**

*Simple.* An `AdminDashboard` shows a current-conditions panel. The reading is host-supplied; the panel has no behavior of its own. It is one line in the dashboard's `### Display`:

```markdown
## View: AdminDashboard

### Summary

The operator's control surface.

### Display

- System counters and a current-conditions panel.
```

*Grown.* The panel now fetches live weather and persists a reading — it has acquired a contract and a schema, crossing the §4.3 line. It is **promoted** to its own child intent, which owns the behavior:

````markdown
---
aim: app.admin.weather
kind: intent
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

The promote boundary is the §4.3 test: display-only ⇒ prose in the host; owns data or operations ⇒ its own child intent. A promoted piece that is *only* ever embedded usually should **not** declare its own `## View:` — its surface is the host's — so it owns `Contract`/`Schema` and raises no orphan. If it genuinely needs its own reusable surface, the informational orphan diagnostic (§12.2) is the correct nudge: either a Persona `accesses` it, or its surface really belongs to the host.

### 15.10 Proxy Verification — When The Outcome Cannot Be Checked

Every guarantee is verified in one of two modes, and the choice is the Architect's:

- **Output-verified — the default.** The guarantee is checked against its result: the realized code, the persisted record, the emitted event. When a postcondition is cheaply and completely checkable, declare it in `### Ensures` and let the Reviewer verify the outcome (§10.1, §12.3). Do **not** also prescribe the procedure: a procedure spec for an outcome-checkable guarantee adds no verification power, goes stale, and needlessly constrains the realization.
- **Procedure-verified — the proxy.** When a guarantee cannot be cheaply and completely verified from its output — judgment steps, qualitative claims, generated content whose correctness no automated check can settle — declare the *procedure* as a `## Flow:` and let its `### Steps` stand in as the verifier: since the outcome cannot be checked, conformance to the procedure trusted to produce good outcomes is checked instead. The Contract `invokes` the Flow; no new syntax is involved. The Flow's Steps are then **normative**: realization must follow them, and the Reviewer checks that they are followed, not (only) what came out.

Most real guarantees are partially checkable — the record exists, the deadline was met, the required sections are present, but is the content *right*? The modes therefore compose per guarantee, not per facet: verify what the output exposes through `### Ensures`, and let a Flow cover only the unverifiable remainder.

**Confidence attribution (normative).** A proxy check yields confidence about the *procedure*, never the *outcome*. A finding that the Steps are realized and followed is procedure-conformance and MUST NOT be reported as outcome-verification; a proxy-verified guarantee never earns outcome confidence `high` (§12.3). The misclassification risk runs in one direction only: treating an outcome-checkable guarantee as proxy-verified merely wastes specification effort, but treating an unverifiable outcome as output-checkable produces green reports over silent failures — false assurance. When in doubt, verify the output; write the procedure only where the output cannot answer.

---

## 16. Intent Evolution

The static rules (§2–§12) define what a *well-formed* model looks like at rest. This section defines how a model *changes* while staying well-formed — the dynamics those rules imply but do not state.

### 16.1 One Root Unit, Two Authoring Operations

The root unit of authoring is the **intent** — root or nested (a **child intent**), each with its own envelope file (§1, §5). Facets and typed edges are how an intent is *expressed*; they are never the unit an author works in. Everything an author does to a model is one of exactly two operations:

- **EXTEND** an existing intent — add or refine its facets and the edges among them.
- **ADD** a new intent — a new child intent or capability (§5).

These two operations are the surface a requirements author — often a non-developer, working through the Architect role (§1.2) — designs at; the facet, edge, and binding detail they expand into is where the Realizer and Reviewer work. An author does not "move a node" or "rename a schema" as a primitive act; those are *transforms* (§16.2) the system performs to keep the model well-formed as the two operations push against the decomposition rules (§4.3).

### 16.2 Validity-Preserving Transforms

When an EXTEND or ADD would leave the model ill-formed — an intent grown past "one clear behavior" (§4.3), a node living in the wrong namespace, two nodes that are the same concept — the system reshapes the graph with a **transform**. A transform is not new syntax and not an author primitive: it is an operation **defined by the pre/post invariants of §16.3**, producing a spec-valid state from a spec-valid state. Tools and the Architect agent apply transforms; authors express intent.

| Transform | What it does | Typically triggered by |
|---|---|---|
| **promote** | a capability grown inside an intent splits out into its own child intent (§5) | an EXTEND that crosses the §4.3 "one clear behavior" line |
| **split** | one intent doing two things becomes two siblings under an index parent | an intent with multiple distinct behaviors (§15.4) |
| **re-home / move** | a node moves to the intent whose namespace it belongs to | a node whose address namespace does not match where it is used |
| **merge** | two nodes that are the same concept collapse into one canonical node | a probable-duplicate diagnostic (§12.2) confirmed as a true duplicate |
| **rename** | a node's name — and therefore its address — changes | a clearer name, or a collision |

Each transform changes one or more node **addresses** `<intent>#<FacetType>:<Name>` (§2.2). `promote` is the bridge between the two operations: an EXTEND that trips §4.3 *resolves structurally into an ADD* — the new capability becomes its own child intent rather than more facets piled on the parent (§15.2).

### 16.3 Transform Invariants (Normative)

A transform reshapes **addresses, never commitments**: after re-pointing (and, for `merge`, de-duplication) the model states the same requirements, the same behavior, the same relations — only structure and naming have moved. Because a transform changes addresses, it MUST re-establish every part of the model that addresses anchor. A transform that violates any of the following yields an ill-formed model and MUST NOT be applied as-is:

1. **No dangling edges; legal triples preserved.** Every typed edge whose `to` address targets a moved or renamed node MUST be re-pointed to the node's new address. After the transform the graph MUST contain zero dangling references (§12.1) introduced by the change, and every re-pointed edge MUST still satisfy its `(verb, from, to)` schema (§8.2). Edges are declared at the acting end (§8.3), so inbound edges live in *other* nodes' blocks and MUST be found across the whole project graph (§12), not just the moved file.

2. **Elided outbound addresses MUST be re-qualified on a cross-intent move.** A node's own outbound edges travel with it, but any written in the elided unqualified form `#<FacetType>:<Name>` (§2.2) resolve against the *new* intent after a move. Where that would change the target, the transform MUST re-qualify the address to its original fully-qualified target so the edge's meaning is preserved.

3. **The parent index MUST be updated.** `promote`, `split`, and a cross-parent `move` change the set of children; each affected parent's `## Children` index (§5.2) MUST be updated to match what is on disk, or auto-discovery (§5.3) diverges from the explicit list — a hard error.

4. **Path/header identity MUST be re-established.** A node that becomes, or moves into, its own intent MUST have its directory, filename, and `aim:`/`parent:` frontmatter brought back into agreement (§4.4); a path/header mismatch is a hard error.

5. **Bindings follow the node.** Any `## Bind:` entry (§10.2) for a moved or renamed node MUST move to the binding file of the node's new intent, with its `## Bind: <FacetType>:<Name>` heading updated to the new name. The **locator is unchanged** — the realization did not move, only the intent address did. This is precisely why bindings are separate files (§1.3): an intent transform reshapes addresses without touching code.

6. **`merge` is author-confirmed and collapses, never silently unifies.** Because same-name is not proof of same-entity (§12.2), `merge` MUST be confirmed by the Architect. On merge the duplicate node is removed, one node is designated canonical (§15.8), and every edge that targeted either node is re-pointed at the canonical node under invariant 1.

### 16.4 A Transform Is a Graph-Diff

A transform yields a **structured graph-diff** — nodes added / removed / moved, edges re-routed, bindings relocated — of exactly the kind the Reviewer already computes (§2.4, §12.3). This is the payoff of the derived graph: reshaping intent is a *traceable diff*, not an opaque rewrite. The Reviewer reports the diff; the Realizer applies the corresponding realization moves (a `rename` that changes a Contract's address tells the Realizer, through the bindings, precisely which handlers, routes, or automations are implicated). The **impact set** (§12.3) of a transform is computable before it is applied.

Because the transform knows *exactly* what changed at the intent level, this diff MAY be **persisted as a change record** under `/aim/work/` — the forward companion to the Reviewer's drift report. A drift report is *reverse*: it discovers unknown drift by re-deriving the realized graph and diffing it against intent. A change record is *forward*: the `.aim` files have already been reshaped, and the record simply *describes* that known delta — renames, moves, re-pointed edges, relocated bindings — so the Realizer can propagate it to the realization as a targeted update (rename this symbol, move that module, re-point this binding to the same locator, §16.3) instead of reconstructing and diffing the whole realized graph. It also carries the handoff across sessions. A change record is a **non-authoritative** work artifact (§1.3): it never *defines* intent — the post-transform `.aim` files already did, and remain the sole authority — it only records what changed, and on any disagreement the files win and the Realizer falls back to a full graph-diff. It is point-in-time and archived after it is applied, exactly like a drift report; its on-disk format is a tooling concern this spec does not define (as with the drift report and the realized-graph manifest, §10.1).

### 16.5 Choosing the Transform (SHOULD)

- **When EXTENDING, watch the §4.3 line.** If an addition is a distinct capability with its own data, operations, and surfaces, **promote** it into a child intent rather than piling facets onto the parent (§15.2 — the parent stays a lean index). Adding facets to an already-multi-behavior intent is how monoliths form (§12.2).
- **Clusters accrete; promote them whole.** The §4.3 line is usually crossed *gradually*: no single EXTEND introduces "a distinct capability," but change by change one noun accumulates a Schema, several Contracts, a View — until a cohesive capability lies flat inside a mixed intent (the noun-cluster smell, §12.2). The next EXTEND that touches the cluster is the moment to **promote** it, and the promotion takes the *existing* facets along with the new ones. Preservation discipline is never a reason to leave a cluster flat: a transform changes addresses, never commitments (§16.3) — moving a node removes nothing.
- **Re-home when the namespace doesn't fit.** If a node's address namespace does not match where it is used, **move** it to the intent it belongs to rather than referencing it across an unnatural boundary.
- **Merge duplicates into a canonical home.** When the probable-duplicate diagnostic (§12.2) flags a true duplicate, **merge** to one canonical node (§15.8) — do not let the copies drift.
- **A UI piece that earns behavior promotes.** A view fragment (tab, panel, widget) that acquires its own data or operations crosses the §4.3 line and is **promoted** into a child intent (§15.9) rather than remaining inline `### Display` prose.

**Worked example — an EXTEND that promotes.** A CRM has `crm.customer_management`, one intent covering customer CRUD. New requirement: "add customer notes, with edit history." Notes are a distinct capability — their own `Note` schema, their own create/edit/list contracts, their own surface. Piling a `## Schema: Note`, three contracts, and a notes view onto the parent would push it past §4.3, so the EXTEND **promotes** into a new child intent:

```
/aim/crm.customer_management/
  crm.customer_management.aim                    # parent index — ## Children now lists customer_notes
  customer_notes/
    crm.customer_management.customer_notes.aim   # new child intent: Note schema, contracts, view
```

The customer-detail view's reference to the notes surface is declared as a cross-reference to the promoted address; the parent's `## Children` index gains a `customer_notes` line (invariant 3).

**Worked example — a split.** A flat `crm.customers` intent has accreted both per-customer CRUD *and* customer-group management — two distinct behaviors. **split** turns it into two siblings under an index parent:

```
/aim/crm.customers/
  crm.customers.aim              # was the flat file; now a lean index (§15.2)
  records/
    crm.customers.records.aim    # per-customer CRUD
  groups/
    crm.customers.groups.aim     # customer-group management
```

Every edge that pointed into the old flat file is re-pointed to whichever child now owns the target (invariant 1); shared schemas stay in the parent or move to a sibling facet file (§15.2); bindings for the moved contracts relocate to the new intents' binding files with locators unchanged (invariant 5).

### 16.6 Diagnostics

Intent Evolution adds **no new diagnostics**. A transform is correct exactly when the resulting graph raises no new hard error (§12.1) and no new orphan / shadow / duplicate / monolith smell (§12.2) attributable to the change. The invariants of §16.3 are the conditions under which that holds — which is the point: the static checks the spec already defines are the acceptance test for every transform.

---

## 17. Re-Encoding Existing Systems (Reality → Intent)

§13 defines migration *within* the model (v3.1 → v4 → v5). This section defines the other direction: producing `.aim` intent from a **system that already exists** and was never authored in AIM — a codebase, a running process, an organization's way of working. Re-encoding is a primary workflow, and it is the Reviewer's machinery (§10.1, §12.3) run in reverse — instead of diffing a declared graph against reality, the agent *reads reality and infers the declared graph*. Without spec support the inferred intent has no provenance, and the authority model (§1.3) silently degrades from "authored truth" to "a guess a tool made." This section keeps that boundary explicit.

### 17.1 Definition And Sources

Re-encoding produces `.aim` files from evidence of how a system actually is. The producing agent acts as **Architect and Realizer simultaneously** (§1.2): it authors the intent (facets, typed edges) and, because it has just examined the realization, emits the bindings for it in the same pass. Evidence comes in two kinds, and they carry different weight:

- **Artifacts** — code, system configurations, automations, templates, execution logs. Readable, re-checkable; an inference from an artifact cites its source the way a binding cites a locator.
- **Elicitation** — human testimony: interviews, walkthroughs, the narration of the person who runs the process. Testimony is how intent that lives only in heads enters the model — and it is *testimony*, not evidence: the encoding report records **who said so and when**, an elicited claim defaults to `needs-human-check` until its source (or their principal) confirms, and an asserted-but-unevidenced rule ("we always get sign-off first") is kept **and** flagged with the confirming question, never silently trusted or dropped.

Expect elicited descriptions to generalize; the exceptions ("except when sales expedites") are not noise but the substance — captured in `### On Error` or as their own operations, and asked about explicitly.

### 17.2 Provenance

Every re-encoded facet node carries a provenance state:

- **`inferred`** — agent-derived from artifacts or testimony, not yet human-accepted.
- **`confirmed`** — a human has reviewed and accepted it.

The mechanism is the `provenance:` frontmatter field (§3.2): a re-encoded file is written `provenance: inferred` and the field is removed (or set to `confirmed`) on acceptance. **An absent field means `confirmed`** — authored intent is trusted by default, so hand-written files need no annotation. Per-node provenance (finer than per-file) is an optional tooling refinement; **per-file is the spec-level requirement.**

### 17.3 Authority Of Inferred Intent

`inferred` intent is **provisionally authoritative** for tooling: graph derivation, resolution, and diagnostics all treat it as real intent, so the graph is usable the moment it is encoded. But it MUST be visually and reportably distinguished from confirmed intent wherever intent is presented, and a project's **confirmation coverage** (fraction of nodes confirmed) is an informational metric (§12.2), never a hard error. Inferred intent is a strong draft, not yet ratified truth.

### 17.4 Confidence

Inferred nodes and edges carry the same confidence vocabulary as graph-diff findings (§12.3): `high` (an artifact clearly evidences it) or `needs-human-check` (ambiguous artifacts, or elicited testimony awaiting its source's confirmation). Where recorded, confidence lives in the **encoding report** — a point-in-time work artifact under `/aim/work/`, the forward companion to the drift report and change record (§16.4) — **not** in the `.aim` file. The `.aim` file carries provenance; the work artifact carries confidence.

### 17.5 Bindings Come Free

The encoding agent examined the realization to infer each node, so it already knows the realization site. It therefore **MUST emit a binding** (§10.2) for every inferred node **that has one** — a Contract, Schema, Event, Trigger, or View realized at an identifiable site (a symbol, a route, a SaaS workflow, an agent skill). Nodes with no realization site are exempt: a **Persona** is a role, not a location, and a step known only from testimony is a **manual step** — legitimately unbound. Modulo those exemptions, a re-encoded intent lands at **Level 3** immediately (§11.2). This is the payoff of the direction — re-encoding is the one workflow where bindings are a byproduct rather than extra work, so drift-checking is available from the first pass.

### 17.6 Scope Discipline

Encoding is **bounded per intent**, mirroring §10.1's bounded construction of the realized graph — the agent examines one intent's realization, not the whole system, per pass. An agent MAY draft an entire intent tree in one sweep, but **confirmation is granted per intent**: a human ratifies one coherent unit at a time.

### 17.7 Duplicates

Re-encoding at scale surfaces §15.8 cases — the same entity (`User`, `Money`, `Status`) independently inferred in several intents. The **probable-duplicate diagnostic** (§12.2) applies unchanged, and the remediation is `merge` (§16.2) with Architect confirmation (§16.3 invariant 6). Encoding agents SHOULD **resolve-or-reference** (§15.8) against already-encoded intents before defining a new entity, so duplication is avoided during encoding rather than cleaned up after.

---

## 18. Purpose-Rooted Models: Mapping An Organization

Nothing in this language is specific to software. A facet is a unit of commitment and the graph is normative (§2) — and organizations run on commitments as much as programs do. The same model that holds an application can hold a complete business process, a department's obligations, or an entire company. This section is the guideline for mapping something that large.

**An organization is a system of realized intent.** Its realization is not a single artifact: it is the combined behavior of people, software, automations, policies, vendors, records, and recurring work. AIM models that whole without forcing every part to become software. A manual approval can remain a human-performed Flow step; a SaaS workflow can be a bound realization; an internal application can own a subtree of intents; and an external deadline can enter through a Trigger. They remain connected because each is described in terms of the commitment it fulfills rather than the medium that performs it.

**Model the process end to end.** A process boundary follows the commitment, not the boundary of a team or application. For example, "convert an accepted proposal into collected revenue" may begin with a salesperson, cross an e-signature provider, create work in a delivery system, require human time approval, generate an invoice through accounting software, and end when a payment Event satisfies the original commercial requirement. Modeling only one application would preserve local behavior while losing the organizational outcome. Modeling the complete intent exposes the handoffs, dependencies, deadlines, evidence, and failure paths across the whole chain.

**Organizational drift is observable.** Once the end-to-end intent is bound to its realization sites, review can detect more than implementation defects: a required approval with no evidence, a policy contradicted by the operational Flow, a handoff that depends on undocumented human knowledge, a deadline with no Trigger, an application behavior no longer serving a business commitment, or a root requirement with no satisfying capability. These findings are routed to the owner of the relevant intent; they are repaired either by changing reality or by explicitly revising what the organization intends.

**The root is a purpose.** Model an organization as one project whose root intent states *why it exists* — its Summary is the mission in plain words, and its `## Requirements` are the existential commitments ("every delivered hour is attributable to an engagement and billed", "no work begins before countersignature"). The root also serves as the canonical home (§15.8) for the organization's shared entities: the personas everyone references, the artifacts every process touches.

**The tree is a why/how ladder.** Each child intent exists to fulfill commitments of its parent; each level down answers *how*, each level up answers *why*. Wire that justification with `satisfies`: a child's contracts and flows carry `[satisfies](aim:<root-or-ancestor>#Requirements[<Label>])` edges into the commitments that justify their existence — and at organizational scale, **label the requirements** (§8.2): an org model lives for years, its requirement lists get edited by many hands, and labeled references are the form that survives it. Tree completeness then stops being rhetorical and becomes checkable — an unrealized requirement at the root (§12.2) means *a stated purpose that nothing in the organization actually does*.

**Siblings may be different kinds of thing.** A company tree legitimately mixes a software application, a billing process, and a compliance obligation as siblings — the language does not distinguish; only the reading differs. The cross-kind edges are where the value concentrates: a process step that `reads` an application's View, an application Event a process `subscribes` to. Those edges are the organization's integration map, and a process step with no edge into any system and no binding is, precisely, the digitalization backlog.

**Content leads; structure follows.** Two authoring motions are valid, and they are the same rule seen from both ends: bottom-up, enumerate commitments and actors flat and let the clusters name the children (§15.1 — the graph is the design); or top-down, narrate the purpose and grow children by asking "how do we fulfill this?". The failure mode is deciding *structure before content* — organizing children before the commitments they would own exist. Structure decisions are deliberately cheap (§16 transforms reshape the tree while the graph survives unchanged); missing commitments are the only expensive omission.

**Do not mirror the org chart.** Reporting lines are not commitment ownership. Divisions and departments make wrapper levels that own nothing — the hierarchy belongs in the model as **Personas and `### Authz`** ("Accountant may…", "CFO approves…"), never as namespace segments. Decompose by *capability* (what is promised), not by *hierarchy* (who reports to whom); capability trees run wider and flatter than the org chart they replace — they still nest as deep as the capabilities themselves demand (§5.5).

**Humans keep the tree; machines keep the graph.** Reviewing an organization model means reading its tree and prose — the front pages, the ladder of why and how. The graph underneath is consumed as answers (§2): what breaks if this parameter changes, which policies nothing enforces, what the whole company owes this month. No one is ever asked to see the organization as a graph — and everyone benefits that the machine does.
