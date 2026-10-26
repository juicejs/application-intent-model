# Agentic Intent Model (AIM) v6.0

## 1. Core and authority

AIM specifies a system's commitments and their relationships. A realization is either an artifact, such as code or configuration, or a performance repeated for each process instance. AIM specifies what must hold, who may act, and observable obligations; implementation mechanisms belong to the realization. Requirements, criteria, and steps may carry normative prose. Typed edges and structured properties carry relationships and mechanically checkable constraints.

An **intent** is identified by a lowercase dotted namespace, such as `juice.tasks`. It has one required intent file (`kind: intent`), optional embedded or sibling facets, optional children, optional capability mappings, and optional realization bindings. The intent file is its canonical entry point. A child is an intent with the same node type as its parent.

### Authority

- `.aim` files under the project's AIM root are the sole behavioral authority, including their typed edges. The graph is derived from these files and is never a competing authority.
- Other documents may explain or summarize intent but MUST NOT introduce behavioral requirements. Behavior stated only in Markdown notes, chat history, comments, or material outside the AIM root is drift; move it into `.aim` if it is intended to be authoritative. Root `AGENTS.md` provides bootstrap and working instructions, not system behavior.
- Bindings authoritatively locate realizations but never define behavior. Their provenance is separate from the behavioral intent's provenance.
- Facts about authoring, review, change history, implementation status, or maintenance of the specification are metadata. They MUST NOT appear in behavioral bodies. Spec-defined frontmatter carries portable authority and accountability metadata; other metadata belongs in the collaboration/storage environment or project-specific frontmatter. AIM does not prescribe version control, review, or approval storage.
- Actors, approvals, and evidence within the specified system are behavior and may be modeled. A fact is metadata if it would cease to apply when the specification's team and toolchain were replaced while the specified system stayed identical.

The authority boundary is enforced by review, not a parser hard error. Tools MAY report apparent behavioral requirements in non-authoritative documents and recommend moving them into `.aim`.

### Operating capabilities

| Capability | May write |
|---|---|
| Architect | Intent and its relationships; bindings when realization is known |
| Realizer, called Developer in software | Realization and its bindings |
| Reviewer | No model or realization changes; reports drift |

These are operating modes, not language constructs or a required agent roster. One agent may hold multiple capabilities. A Reviewer MUST run cold with read-only access to what it judges; continuing the session that produced the realization is not independent verification. Independence depends on context and permissions, not model identity.

The Realizer MUST NOT invent material behavior absent from intent. Preserve documented intent, minimize assumptions, and surface assumptions for review or explicit intent revision. Resolve a mismatch explicitly: repair reality or revise intent; never silently substitute one for the other.

Before presenting a proposal or committing an extension/addition, the Architect MUST derive the proposed graph and repair every hard error it can resolve autonomously. Surface only decisions requiring the owner, such as canonical ownership, a confirmed duplicate merge, ambiguous bindings, or missing/conflicting performers. Never assign a performer merely to clear a finding. A rewritten requirement requires reconsidering every satisfier; state explicitly when an unchanged satisfier still holds.

## 2. Files and project bootstrap

All AIM source files use `.aim` and consist of YAML frontmatter followed by CommonMark Markdown. Each file has exactly one H1, its display name.

### Frontmatter

Every source file begins with `---`-delimited YAML:

```yaml
---
aim: juice.tasks.create_task
kind: intent
parent: juice.tasks
---
```

| Key | Meaning and values |
|---|---|
| `aim` | Required lowercase, dot-separated intent namespace; authoritative identity |
| `kind` | Required file role: `intent`, a facet kind, `mapping`, or deprecated `binding` |
| `parent` | Parent namespace; present on child intents |
| `display` | Display name overriding H1 for tooling |
| `tags` | Array of free-form discovery tags |
| `nature` | Projection hint: `record`, `persona`, `flow`, `view`, `event`, `trigger`, or `capability`; absent defaults to capability reading |
| `provenance` | `inferred` for unaccepted recovered intent; absent or `confirmed` means authored/accepted intent |
| `owner` | Free-form accountable identity, used to route findings |
| `status` | Specification lifecycle: `draft`, `review`, `approved`, or `deprecated`; absent means unspecified |
| `approved_by` | Identity ratifying current content |
| `approved_at` | Optional ratification date accompanying `approved_by` |

Only `provenance` qualifies authority. `owner`, `status`, and approval fields never change how tools treat content. `provenance: inferred` with `status: approved` or a present `approved_by` produces an informational contradiction diagnostic. Acceptance changes provenance and records the approver in the same act.

`nature` MUST NOT affect resolution, edge legality, or synthesis. Tools MAY infer a projection when it is absent: a top-level Schema without acting edges reads as record; intent-level Role/Access or acting edges reads as persona; top-level Steps reads as flow. Contradiction between declared nature and content is informational; content remains authoritative.

Frontmatter is open: conforming tools MUST ignore unrecognized keys, with at most an informational diagnostic. Project keys MUST NOT redefine spec-defined keys. Source files have no per-file `version` or `spec`; a project declares one language version. **Compatibility:** source valid under AIM v5.13 is valid v6.0 source and is read as it is, without migration. v6.0 adds constructs (`plays`, `cross-owner(...)`, in-state guards, explicit modifier properties) and changes no existing meaning; the 5.13 edge shorthand is read as a deprecated spelling (§7). Tools MAY canonicalize older spellings only under the preservation rules of §3.

### Bootstrap and spec cache

Each project MUST have root `AGENTS.md` with frontmatter:

```yaml
---
aim_version: 6.0
aim_root: ./aim/
spec: <canonical specification URL>
---
```

`aim_root` locates source and defaults to `./aim/`. Its prose explains roles, project conventions, graph serialization, and co-location of mappings/bindings with their intents. It may include other project working instructions.

Agents resolve the specification in this order:

1. Read `AGENTS.md`; require the language declaration and `spec` URL. The URL is authoritative; `aim_version` provides language context.
2. Read `<aim_root>/specs/spec.md` when present.
3. Otherwise fetch the declared URL.
4. Refuse to proceed if the project declaration or specification cannot be resolved.

On setup, tooling fetches the declared specification into `specs/spec.md`. On adopting a new version, it replaces the cache. The cache MUST remain a verbatim mirror; tools MUST NOT edit it. `specs/` is reserved for cached specifications and MUST NOT be an intent namespace. Other directories containing a `<name>.aim` intent file are intent directories.

## 3. Body structure and schema grammar

H2 introduces top-level sections or facets. H3 introduces facet sub-blocks. Facets use `## <FacetType>: <Name>`; top-level sections use bare names such as `## Summary`, `## Requirements`, `## Tests`, `## Children`, and `## Dependencies`. Data-bearing or acting intents may also have top-level Schema, Role, Access, and Steps as defined by their facet rules.

A facet name MUST match `[A-Za-z][A-Za-z0-9_]*`; PascalCase is recommended. Names with spaces or punctuation are hard errors. The facet heading MUST be immediately followed by explicit `### Summary`, except a Persona used only for role/access declaration. Realization bindings are an inline `### Bindings` property; deprecated binding sidecars use `## Bind: <FacetType>:<Name>`.

Tools MUST accept deprecated `## Subintents` and `## Subcomponents` as aliases of `## Children`. `## Schema: <Name>` is the deprecated Record facet spelling; `aim-attrs` is the deprecated `schema` fence spelling. Both remain accepted and SHOULD be migrated without forced rewrites.

### Preservation of meaning vs. canonical formatting

Tools that parse `.aim` files into an intermediate representation and re-serialize them MUST distinguish **preservation of meaning** from **canonical formatting**:

- **Preservation of meaning** requires retaining every intent and facet node, requirement label and text, typed edge, schema attribute and modifier, `## Dependencies` (`### Imports` and `### Requires`), frontmatter authority and lifecycle metadata (`provenance`, `owner`, `status`, `approved_by`, `approved_at`, `tags`, `display`, `nature`), and realization binding (including merging any deprecated `kind: binding` sidecar `## Bind:` entries into inline `### Bindings` before retiring the sidecar).
- **Canonical formatting** normalizes whitespace, heading order, and deprecated spellings (`## Subintents` → `## Children`, `aim-attrs` → `schema`, inline `### Bindings` for `## Bind:`) without altering the derived graph, bindings, or authority metadata. An automated migration MUST NOT run if the intermediate representation drops any of these elements.

### Markdown restrictions

Structured blocks use the specified bullet, `schema` fence, and edge-token forms. Requirements, Tests, Steps, Schema, Payload, Input, Authz, Expects, Ensures, Returns, Decides, Display, Actions, Access, Of, States, Moves, and Bindings are structured blocks. Tables, blockquotes, task lists, and footnotes are forbidden there. Bold, italic, links, and inline code are permitted within list items. Fences in Schema/payload blocks use `schema`; arbitrary fences are permitted elsewhere where the block's defined syntax allows them.

Free prose, including Summary and descriptive paragraphs, permits ordinary CommonMark. Raw HTML is forbidden everywhere. Task lists MUST NOT express implementation or verification status in structured intent; that status belongs in work reports. Frontmatter `status` concerns specification lifecycle only.

### Schema properties

Schemas use a fenced `schema` block, with one attribute per line:

```schema
title: string required min(1) max(200)
code: string required unique
ownerId: string required ref(Member.id) owner
reviewerId: string ref(Member.id) !owner
items: list(ExpenseItem)
```

Grammar: `<name>: <type> <modifier>*`.

| Position | Allowed forms |
|---|---|
| Scalar type | `string`, `number`, `boolean`, `date`, `datetime`, `file` |
| Other type | `enum(a, b, c)`, `list(<type>)` |
| Modifier | `required`, `optional`, `unique`, `min(n)`, `max(n)`, `ref(<Type>.<field>)`, `ref(<intent>#<Type>.<field>)`, `enum(a, b, c)`, `default(<value>)`, `list(<type>)`, `owner`, `!owner` |

`file` is a document value, not a storage or parsing mechanism. An operation invoking a document-reading Capability for a caller's document declares a `file` Input; the Capability reads it and the Contract owns the resulting commitments. A document acquired by an external service does not imply a caller upload. Parsed text and source addresses remain ordinary values.

`unique` declares that no two rows of the Record may hold the same non-empty value for that attribute.

`owner` and `!owner` govern row-level ownership and separation of duties:

- **`owner`** marks the referenced actor (`ref(...)`) to whom the row belongs. On creation, the field is bound to the acting caller's identity. At most one field on a Record may carry `owner`; a plain reference to a person does not imply ownership. A row referencing an owned row through one or more `ref(...)` links inherits that row's ownership restriction. All applicable ownership restrictions MUST hold: by default, a caller may see or mutate a directly or indirectly owned row only when every applicable owner matches the caller's identity. Records with no ownership path are not owner-scoped. A different local Persona, including one linked through `plays`, does not widen scope.
- **`!owner`** restricts an otherwise authorized action: the acting caller MUST differ from every applicable owner of the target row. It may follow a backticked role in `### Authz`, qualify a Contract's `### Input` field identifying the target row, or qualify a Record's reviewer `ref(...)` field. A field-level restriction applies when that Input is supplied or that Record field is written; an Authz restriction applies when acting under that entry. It never grants visibility or mutation rights. To permit action on others' rows while forbidding self-action, declare both an explicit cross-owner grant and `!owner`.

**Explicit cross-owner scope.** `cross-owner(<Record-address>)` is a modifier, not a graph verb. `<Record-address>` is `#Record:<Name>` or `<namespace>#Record:<Name>` without `aim:`, resolved by canonical address resolution from the containing intent. It MUST resolve to a Record. Repeat the modifier to name several Records. It is permitted only:

- After a backticked role on a Contract or Flow's `### Authz` entry. It lifts ownership scope only for that operation's declared `reads` or `mutates` targets named by the modifier, while acting under that entry. It grants no permission beyond the entry's Authz and no scope to invoked operations.
- After a Persona's `[accesses](aim:<View-address>)` edge in `### Access`. It qualifies that edge and lifts ownership scope only for the named Record among that View's declared `reads` targets. It grants no scope to other Views or to operations exposed or invoked by the View; each operation still needs its own authorization and scope.

A grant applies only to rows of its named Record, including that Record's inherited ownership restrictions. It grants no access to related Records, ancestors or descendants, and is not inherited through `ref(...)`, `plays`, Imports, or other graph edges. The named Record MUST be a declared read/mutation target of the operation or a declared read target of the accessed View, respectively.

```markdown
### Authz
- `#Persona:Approver` cross-owner(#Record:Claim) !owner

### Access
- Review claims — [accesses](aim:#View:Claims) cross-owner(#Record:Claim)
```

The first entry permits the Approver to act on others' claims under that operation's rules. The second permits that Persona to see claims across owners in Claims; it does not authorize approval.

`list(<type>)` holds repeated scalars or owned Record parts. A Record-typed list derives a `refs` edge to the Record. `ref(Type.field)` derives a `refs` edge between schema attributes. Resolve the Type as a Record using canonical resolution; its field MUST exist. A non-Record target or missing field is a hard error. The qualified form `ref(<intent>#<Type>.<field>)` selects the namespace from which canonical resolution begins, allowing unrelated Records with the same name (such as `billing#Record:Account` and `identity#Record:Account`) to coexist without collision. Resolution shadows are informational.

## 4. Graph identity and derivation

The graph is normative. Relations are declared once at the acting end; inverse relations are derived. Tree position determines ownership but does not constrain cross-intent or cross-level edges. Tools SHOULD expose useful graph queries and views without requiring people to comprehend the entire graph.

| Node | Source | Identity/type |
|---|---|---|
| Intent | `aim` and H1 | Namespace; `intent` |
| Facet | `## <FacetType>: <Name>` | Heading keyword determines type; no inference |
| Section | Bare top-level section | `section` |
| Sub-block/item | H3 and its list items | Addressable `block`, not an independent facet type |

Sections are valid report anchors but are edge-inert. Typed edges connect intents/facets, with only two sub-block exceptions: schema attributes participate in `refs`; individual top-level Requirements items are targets of `satisfies`. No other sub-block is an edge endpoint.

An intent address is its namespace. A facet address is:

```text
<intent>#<FacetType>:<Name>
```

Store and derive fully qualified addresses. At an inline reference site the namespace may be omitted when resolution is within the same intent, producing `#Contract:CreateTask`. Facet type capitalization and name match the heading verbatim; no percent encoding is required for valid names.

A report may add ` → ### <Sub> [<index>]`, or ` → ## Requirements [<index>]`, to identify a 1-based list item. Such pointers are revision-specific and MUST NOT be authored edge targets. Work artifacts SHOULD include the item's text as a content anchor. Authored `satisfies` targets use `#Requirements[<key>]`: a stable declared label (or a numeric 1-based index in legacy source). Once edges exist, labels SHOULD be used. Inserting or reordering positional requirements is a rename-class transform and MUST re-point all inbound positional edges.

Derive the graph by collecting fully qualified intent/facet/sub-block nodes; collecting inline edge tokens and structured references; resolving targets and validating legal source/verb/target triples; and adding inverses, reconciling any authored inverse blocks. The graph may live in memory or a build artifact, never as an independent source file.

## 5. Layout, tree, and resolution

### Layout and decomposition

Decompose into focused child intents by default. The parent indexes children and owns shared facets and cross-cutting requirements. A single file with embedded facets and no children is appropriate only when all content fits comfortably on one screen, specifies one clear behavior, and no facet needs independent ownership/review.

The intent file is `<intent>.aim`; sibling facet, mapping, and deprecated binding files are `<intent>.<kind>.aim`. All are co-located in the intent directory. A root directory uses its full namespace; each nested child directory uses its added namespace segment. Children occupy nested directories under their parent. A child's mapping/binding files belong alongside that child, never in the parent directory. Generic filenames `aim.aim`, `intent.aim`, `schema.aim`, `mapping.aim`, and `binding.aim` are invalid. Header identity is authoritative; directory and filename MUST agree with it, otherwise a hard error results.

A child namespace extends its parent by exactly one segment and declares `parent`. No intermediate level may be skipped without its own intent file and Summary. The one-segment constraint applies to each edge, not total breadth or depth.

Children are auto-discovered from directories containing intent files whose `parent` matches. An explicit `## Children` list overrides discovery: listed children MUST exist, every discovered child MUST be listed, and the list controls presentation order. Omitted discovered children are hard errors.

Each level SHOULD form a short table of contents, normally 3–9 children. Single-child chains and levels outside this band merit diagnostics. Depth has no absolute cap: each level earns its place, and decomposition stops at one clear behavior. A Summary that still combines distinct behaviors calls for children; depth count alone neither requires nor forbids a split.

### Minimum intent envelope

An intent file requires valid `aim`/`kind` frontmatter, exactly one H1, a Summary containing at least one paragraph (or an H1-following paragraph serving as Summary), and Requirements containing at least one bullet. Observable Tests and precision facets for stable interfaces are recommended.

### Canonical resolution

All references MUST use this algorithm; implementations MUST NOT substitute another precedence order:

1. Select the exact namespace if an intent prefix is present; otherwise select the current intent. A named namespace MUST exist.
2. Resolve the facet name by first match: embedded facet in the intent file; sibling facet file; explicit Imports in the current file; parent, grandparent, and continuing upward; required alias through mapping or Capability binding; absent.
3. If a facet type is specified, require agreement with the resolved node's type. A mismatch is a hard error.
4. Resolve any report sub-block pointer by heading and 1-based item index. Resolve a Requirements key against the chosen intent's top-level Requirements, by numeric position or a bullet label declared as `- **Label** — …`. Missing/out-of-range keys and duplicate labels are hard errors.

A required unresolved name is a hard error. Lower-precedence definitions produce informational shadow diagnostics. Explicit Imports take precedence over inherited parent definitions.

### Levels and traceability

| Level | Specification |
|---|---|
| 1 | Intent only |
| 2 | Intent plus some facets and edges |
| 3 | Full facet trace with bindings, enabling declared/realized graph comparison |

Levels govern expected realization precision and traceability/review strictness. Tools MAY report the level. Intent-only source remains valid with reduced fidelity. At Level 3, unbound declared nodes become enforceable findings; review verifies edges at bound sites with confidence, or uses a supplied realized-graph manifest.

Traceability begins at individual Requirements satisfied by behavior. Behavioral entry points are a Persona accessing a View/screen intent or a Trigger starting a Flow/Contract. Views expose Contracts; Contracts may invoke Flows; Contracts/Flows read or mutate Records and emit Events. Following derived `satisfied-by` reaches a requirement's realizers; no inbound `satisfies` is a coverage gap. Style and State do not join this behavioral chain: Style has no edges; State's structural edges are derived. A complete Level-3 trace has no orphan behavioral nodes or dangling edges.

## 6. Facets

A facet is a node of the graph declared by a heading, `## <FacetType>: <Name>`, with its properties in H3 sub-blocks. AIM 6.0 has ten facets: Record, Contract, Flow, Persona, View, Event, Trigger, Capability, Style and State. Each is specified in its own block below, and every block has the same parts, so a facet can be read, implemented and reviewed on its own.

### 6.0 How a facet is specified

Every facet block has these parts, in this order:

| Part | Says |
|---|---|
| **Purpose** | What the facet commits to, in one paragraph, and what it does not. |
| **Form** | Its heading and every sub-block: required or optional, and the grammar of each. |
| **Example** | One complete facet as it is written in a `.aim` file. |
| **Edges** | The verbs it declares and the verbs that reach it (§7). |
| **Rules** | Its normative rules. |
| **Diagnostics** | The hard errors and informational conditions it owns (§10 holds the cross-cutting ones). |
| **Since** | The version that introduced it and its later additions. |

**Rules every facet shares.** A facet name matches `[A-Za-z][A-Za-z0-9_]*`; PascalCase is recommended (§3). The heading is immediately followed by `### Summary`, except a Persona used only for role and access. Its sub-blocks are its properties: they belong to the node and are not nodes themselves; a schema is a property, not a node. A facet may carry an inline `### Bindings` property (§9). Only State restricts its sub-blocks to the listed ones (§6.10). A facet whose substance outgrows its host may become an intent of its own (§11): Record, Persona and Flow have defined promoted forms, given in their blocks.

**Adding a facet.** A future facet is admitted only when it (1) expresses a commitment no existing facet and property can carry without losing checkability, (2) has demonstrated need in real models, and (3) arrives complete: a block with every part above; its node type; the verbs it declares and receives, added to the closed taxonomy in §7 with their endpoints; any derived structure; its place in traceability (§5) and whether it can be an orphan; its diagnostics; and a statement that existing models stay valid. It arrives with a proposal under `proposals/` that records the evidence. A new sub-block of an existing facet meets the same tests and is added to that facet's block. Renaming or removing a facet is breaking.

### 6.1 Record

**Purpose.** A Record is passive data that operations store, read or process: an order, a claim, a team member. It declares what one row holds and the rules on that data. It never acts; an actor is a Persona.

**Form.**

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | yes | What one row is. |
| `### Schema` | expected | A `schema` fence, one field per line, in the grammar of §3 (types, `required`, `unique`, `min`, `max`, `default`, `enum`, `ref`, `list`, `owner`, `!owner`). |
| `### Constraints` | no | Data constraints, one bullet each. |
| `### Immutable` | no | Fields that never change after the row is created, one bullet each. |

**Example.**

````markdown
## Record: Claim

### Summary

One expense claim an employee submits.

### Schema

```schema
id: string required
ownerId: string required ref(Member.id) owner
amount: number required min(0)
status: enum(Draft, Submitted, Approved) required
note: string
items: list(ClaimLine)
```

### Constraints

- A claim's amount equals the sum of its lines.

### Immutable

- `ownerId`
````

**Edges.** A Record declares no edge verbs. Its schema derives `refs` from each `ref(...)` field and each Record-valued `list(...)` (§3). It receives `reads` and `mutates` from Contracts, Flows and Views, and the derived `governs` from a State.

**Rules.**

- The same schema grammar serves every data property: Contract `### Input`, Event `### Payload` and a promoted entity's top-level `## Schema`.
- Ownership is declared on the schema: `owner` marks the field naming whose row it is, rows referencing an owned row inherit its owner, and `cross-owner(...)` and `!owner` state the exceptions (§3).
- A Record whose data and lifecycle warrant a file becomes an intent: its schema becomes top-level `## Schema`, the intent carries `nature: record`, and its operations co-locate as facets. The intent is the entity and MUST NOT contain a same-named Record facet.
- `## Schema: <Name>` is the deprecated spelling of this facet and is read as a Record.

**Diagnostics.** Hard errors: more than one `owner` field; a `ref(...)` whose Record or field does not resolve (§10). Informational: a Record read but never mutated in the model owes supplied contents (§8); a Record with no fields leaves its rows unstated for whoever realizes it.

**Since.** 3.1 as a facet; named Record in 5.1 (formerly `Schema`); the `owner` modifier by 5.13; inherited ownership, `cross-owner` and `!owner` in 6.0.

### 6.2 Contract

**Purpose.** A Contract is one operation: what a caller supplies, who may perform it, what must hold before, what is guaranteed after, and what it returns. A decision is a Contract that reaches a judgment. A Contract states outcomes, not mechanics.

**Form.**

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | yes | The operation's purpose. |
| `### Input` | no | Caller-supplied fields, in a `schema` fence. |
| `### Authz` | no | Who may perform it: bullets naming roles by backticked address, each optionally followed by `cross-owner(<Record-address>)` and `!owner` (§3). |
| `### Expects` | no | Preconditions, one bullet each. |
| `### Ensures` | no | Postconditions and their edges, one bullet each. |
| `### Returns` | no | Externally returned results, one bullet each. |
| `### Decides` | no | Outcomes of a judgment, one bullet each (below). |

**Example.**

````markdown
## Contract: ApproveClaim

### Summary

An approver approves or returns another person's submitted claim.

### Input

```schema
claimId: string required ref(Claim.id) !owner
```

### Authz

- `#Persona:Approver` cross-owner(#Record:Claim) !owner

### Expects

- The claim is submitted.

### Ensures

- The claim records who decided and when — [mutates](aim:#Record:Claim), [satisfies](aim:#Requirements[FAIR])

### Decides

- **Approved** — every line is supported by a receipt — [emits](aim:#Event:ClaimApproved)
- **Returned** — any line lacks a receipt — [invokes](aim:#Contract:CorrectClaim)
````

**Edges.** Declares `reads`, `mutates`, `emits`, `invokes` (to a Contract, Flow, promoted process or Capability), `subscribes` and `satisfies`, inside Ensures or Decides bullets. Receives `exposes` and `invokes` from Views, `invokes` from Personas, Flows and Contracts, `triggers` from Triggers, and the derived `moved-by` from a State.

**Rules.**

- An operation acquiring outside information MUST declare the Capability it consults with `invokes`; a source named only in prose is insufficient. For a caller's document, the Input declares a `file`; the reading Capability parses it and the Contract owns the resulting records. Acquisition may be a collect operation that invokes the Capability and mutates a Record; later operations read that Record.
- **Decisions.** The Contract (or Flow) that reaches a judgment is the decision; there is no separate decision node. Each `### Decides` bullet is one outcome: a bold label in the facet-name grammar, addressable as `#Contract:<Name> → Decides[<Label>]`; the criteria after the dash, which are normative — the realization MUST decide on them; and the outcome's edges (`emits`, `invokes`, `mutates`, `reads`). The block MUST hold at least two outcomes and asserts that they are mutually exclusive and exhaustive. It derives one exclusivity group for the node; operations that share a step without such a decision are joint work.
- **Every write is held to the model.** However a realization performs a Contract — coded, interpreted or by a runtime engine — every Record mutation it makes MUST satisfy the Record's `### Schema` and `### Immutable`, ownership (`owner`, `!owner`, grants; §3) and every State governing the Record (§6.10), before it commits. When a realization may perform a Contract without interpretation is realization, not language.
- `### Authz` is permission, never performance; who performs the operation is resolved as in §6.4.

**Diagnostics.** Informational: a Contract nothing exposes, invokes, triggers or subscribes (orphan); a Decides block with fewer than two outcomes; an outcome without criteria; an outcome Event nothing subscribes to or anchors a Trigger on; two or more emitted Events whose consumers diverge without a Decides block (ask whether it is a decision); a decision with no basis — no reads, Capability invokes or Input.

**Since.** 3.1; typed edges 4.0; `### Decides` 5.4; Capability consultation 5.6; every write held to the model 6.0.

### 6.3 Flow

**Purpose.** A Flow is one piece of work done in order: its steps, where it branches, and what happens on error. It sequences operations; it does not replace them. Work that happens at different times for different reasons is separate operations, not one Flow.

**Form.**

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | yes | What the work achieves. |
| `### Steps` | expected | A numbered list, one step per item (below). |
| `### On Error` | no | Error handling, one bullet each. |
| `### Input`, `### Authz`, `### Expects`, `### Ensures`, `### Returns`, `### Decides` | no | As on a Contract (§6.2). |

**Example.**

```markdown
## Flow: ReimburseClaim

### Summary

From a submitted claim to the payment.

### Steps

1. The approver reviews the claim — [invokes](aim:#Contract:ApproveClaim)
2. Finance pays it — [invokes](aim:#Contract:PayClaim)
3. The employee is told — [emits](aim:#Event:ClaimPaid)

### On Error

- A failed payment leaves the claim approved and is retried the next day.
```

**Edges.** Declares `invokes`, `reads`, `mutates`, `emits` and `subscribes` in its steps, and `satisfies`. Receives `invokes` and `triggers`; its callers are derived, so a Flow MUST NOT author an inverse `### Trigger` block.

**Rules.**

- **Steps.** One numbered item is one step; position, not the written number, sets the order, and an indented line continues the step above. A step's inline edge tokens are its operations and keep the step's index in the graph. Several `invokes` in one item are one step: exclusive alternatives when they are a deciding Contract's outcomes, otherwise unordered joint work that MAY run concurrently, with the next step as the join that MUST NOT begin until they all complete. A multi-step parallel branch is its own Flow or process, invoked jointly from one step. An item with no edges is a human step and appears in every process projection; an item whose only operations are `reads`, `mutates` or `emits` is work the Flow performs itself. A step's words describe the work and never declare its performer (§6.4). Joint work does not express a race or cancellation: where first-completes-wins is a real commitment, say it in the step's prose and verify the procedure.
- **Decision continuation.** A step invoking a deciding Contract carries the fork. If one outcome continues the procedure, its continuation is the next step and MUST NOT also be declared on that outcome; every other outcome declares its own consequence in its Decides bullet. A correcting outcome may invoke work that invokes the decision again: that cycle is legal while the Steps stay the linear procedure. If no outcome proceeds, the deciding step is the last and every outcome declares its continuation. A correction loop is bounded by a deadline Trigger anchored on the phase's start and disarmed by the confirming Event; a count bound is not expressible.
- **Event continuation.** The next step always follows by position, whatever was emitted. Only `invokes` and `emits` lead along an edge; `reads`, `mutates` and `satisfies` lead nowhere. An emitted Event continues the branch at its subscribers: a subscriber without steps is the next work on that branch; one with steps starts a separate run. An Event nobody subscribes to ends only that branch. A Trigger anchored on an Event arms a timer and continues nothing.
- **Promoted process.** A process with its own operations, records and requirements may become an intent with `nature: flow`: its sequence is a top-level `## Steps` in the same grammar, declared from the intent node, and no same-named Flow restates it. An organization with several processes gives each its own flow-natured intent; a project that is one process uses its root and MUST NOT wrap it in a lone child.
- **Phases.** A large process splits into phases, each a run of consecutive steps producing one artifact; a phase with its own Record and operations becomes a flow-natured child. The root keeps the shared roles, the entry Trigger, cross-cutting requirements, the Children index and an orchestrating sequence that invokes the phases; each phase keeps its steps, operations, Events and Record. A step is declared at its owning level only. References cross phases freely.
- Long-running orchestration uses these constructs: a Flow invokes work, mutates a progress Record, and emits or subscribes to compensation Events. Durable timers and signals are realization.

**Diagnostics.** Informational: an outcome that repeats the next step's operation (redundant continuation); a deciding step followed by further steps with no single proceeding outcome (ambiguous continuation); a sequence with no entry point, a step no entry reaches, a step that cannot reach an end, or a cycle with no decision outcome or deadline Trigger leading out of it.

**Since.** 3.1; structured Steps 5.3; joint work, decision continuation and phases 5.4–5.5; event continuation 5.9.

### 6.4 Persona

**Purpose.** A Persona is an actor: an entity that exists (an employee, a client) or a role played in one intent (the approver of a claim). It declares what the actor reaches and what work it performs. Permission (Authz), reach (access) and performance are three separate facts, and only edges declare them.

**Form.**

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | no | Who the actor is. |
| `### Role` | no | One bullet describing the actor; may carry `[plays](aim:<address>)`. |
| `### Access` | no | Bullets with the Views or intents it `accesses` (each optionally followed by `cross-owner(<Record-address>)`) and the operations it `invokes`. |

**Example.**

```markdown
## Persona: Approver

### Role

- Reviews other people's expense claims — [plays](aim:org#Persona:Employee)

### Access

- Review submitted claims — [accesses](aim:#View:Claims) cross-owner(#Record:Claim)
- [invokes](aim:#Contract:ApproveClaim)
```

**Edges.** Declares `accesses`, `invokes` and `plays`. Receives `plays` from roles that are filled by it; Authz entries name it without an edge.

**Rules.**

- **Who performs the work.** Work is performed by, in order: (1) the Persona that `invokes` it — several invokers are alternatives, any one may act; where a particular actor must act in a particular step, that step invokes an operation only that actor invokes, and joint performance is one step per actor; (2) the Flow itself, for a step whose only operations are `reads`, `mutates` or `emits` — it inherits no Persona; (3) the performer of the nearest enclosing Flow or promoted process, for a human step or an operation with no performer of its own — direct or inherited in turn, the first declaration stops inheritance.
- **These facts stay distinct.** Authz declares permission, never performance: it names roles by backticked address (`#Persona:Approver`, `org#Persona:Employee`), several named roles are alternatives, a name in its prose names nobody, the performer MUST be among the roles it names, and with no named role whoever performs the operation is permitted. Accessing a View that exposes an operation reaches it and commits the Persona to nothing. A Trigger starts work and never performs it. Role prose and step prose assign no work.
- Work owes a performer when it is a step of a Flow or process, is invoked by a step, or is started by a Trigger or a subscription; owed work without one is incomplete. An operation only offered through a View owes none: whoever reaches it may act within its Authz.
- **Roles and shared entities.** An entity shared across processes has one canonical home; a role a process reads stays with that process. Moving shared entities upward MUST NOT merge distinct roles and erase a handoff. Where a local role is filled by a shared Persona, the local role is its own Persona whose `### Role` carries `[plays](aim:<address>)`: it stays a distinct performer in every projection and handoff, takes the shared Persona's identity, and gains no permission or ownership scope by it — its own Authz and access apply. An `## Dependencies → Imports` alias may name the shared entity directly where there is no distinct role; never declare a second canonical entity for the same group.
- A grant after an `accesses` edge widens that View's reads for the named Record only (§3, §6.5).
- **Promoted persona.** A Persona that acquires its own data and operations may become a `nature: persona` intent: its acting face becomes top-level `## Role` and `## Access`, its data a top-level `## Schema`, its operations co-located facets. The intent is the actor and MUST NOT contain a same-named Persona.

**Diagnostics.** Informational: owed work with no performer — distinguishing no performer at all, permission only (Authz without an invoking Persona) and a Trigger only, and asked once per Flow where one declaration answers several steps; a performer outside the roles Authz names; a Persona that performs, reaches, plays and is permitted nothing (give it its part or remove it). The owner answers these; the Architect never assigns a performer to clear one.

**Since.** 3.1; performers from edges 5.9–5.10; `plays` and View grants 6.0.

### 6.5 View

**Purpose.** A View is a surface people use: what it shows, which records it reads, and the actions it offers. It commits to the existence of copy and the names of actions, not to the words of the copy or the pixels of the layout.

**Form.**

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | yes | What the surface is for. |
| `### Display` | no | What it shows, one bullet each, with the `reads` of each. |
| `### Actions` | no | Each action's label and the operation it `exposes` or `invokes`, or the View it `navigates` to. |
| `### Layout` | no | Arrangements the owner stated, one bullet each, in their words. |

**Example.**

```markdown
## View: Claims

### Summary

The claims waiting for a decision.

### Display

- Each submitted claim with its lines and receipts — [reads](aim:#Record:Claim)

### Actions

- Approve or return — [exposes](aim:#Contract:ApproveClaim)

### Layout

- The oldest claim comes first.
```

**Edges.** Declares `reads`, `exposes` (a user action), `invokes` (a programmatic call), `navigates` and `satisfies`. Receives `accesses` from Personas.

**Rules.**

- Display declares that copy exists, not its words: the words are supplied material (§8). Action labels are intent, because they name commitments.
- **Ownership.** A View reading owned rows shows only the caller's own by default, whatever the caller's Persona or `plays` link. Only a `cross-owner(...)` grant on that Persona's access edge to this View widens its reads, and only for the named Record. Authz on an exposed operation does not widen the View, and access to the View widens no operation.
- **Layout** states only what the owner specified — relative position, order, grouping, prominence — and names its subject through the View's Display terms, Action labels or read Records. It declares no edges; a parser MUST NOT compare its prose with other blocks; review judges it. Pixels, grids and stylesheets are realization. Unstated arrangement is the realization's freedom, and a tool's arrangement MUST NOT become Layout unasked.
- **Surface ownership.** A page with an accountable outcome of its own is a child intent once that purpose is understood, before it owns data or operations: its Summary and requirements state the purpose, its sections are View facets, and it MUST NOT add a same-named View restating itself; a Persona may access the intent, covering every View in it. A static piece of a screen is a Display bullet, not a node. A piece that acquires its own data, operations or surface owns those facets — a child intent when they form a capability, or a View beside its siblings. Inline visual composition has no edge.

**Diagnostics.** Informational: a View no Persona reaches, directly or through its intent or an ancestor (orphan); a View with no Style in reach (§6.9); missing supplied copy (§8).

**Since.** 3.1; Layout 5.12; ownership grants 6.0.

### 6.6 Event

**Purpose.** An Event is an announcement that something happened, with its data. It is a fact, never work: the work lives in what subscribes to it.

**Form.**

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | yes | What happened. |
| `### Payload` | no | Its data, in a `schema` fence. |
| `### Routing` | no | Routing properties as bullets, such as `Channel: claims.approved`, `Durable: true`. |

**Example.**

````markdown
## Event: ClaimApproved

### Summary

An approver approved a claim.

### Payload

```schema
claimId: string required ref(Claim.id)
approvedAt: datetime required
```
````

**Edges.** Declares none. Receives `emits` from Contracts and Flows and `subscribes` from Contracts, Flows and intents; Triggers name it as an anchor.

**Rules.**

- Emitters are derived from `emits` edges; an Event MUST NOT author `### Emitted By`.
- An outside announcement enters through a Trigger that `triggers` an ingest Flow, which emits the internal Event, so every Event has an emitter in the model.
- Where an Event leads is §6.3, *Event continuation*.

**Diagnostics.** Informational: an Event nothing emits (orphan); a decision outcome's Event nothing consumes (§6.2).

**Since.** 3.1; derived emitters 4.0.

### 6.7 Trigger

**Purpose.** A Trigger is an entry point that is not an actor: a schedule, a deadline, a webhook or another outside origin. It starts work and never performs it.

**Form.**

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | yes | When and why it fires. |
| `### Kind` | expected | One of `schedule`, `deadline`, `webhook`, `external`. |
| `### Schedule` | for `schedule` and `deadline` | One line: `cron: <expression>`; `<n> <unit> after [Event:<Name>]` with `minutes`, `hours`, `days`, `business-days` or `weeks`; or `monthly on the <n>th`, `weekly on <weekday>`, `yearly on <date>` — the latter forms optionally followed by `— unless [Event:<Name>]`. |
| `### Fires` | expected — without it the Trigger is an orphan | `triggers` edges to what it starts. |

Webhook and external origins describe their source in prose instead of a Schedule.

**Example.**

```markdown
## Trigger: ApprovalDeadline

### Summary

A claim waiting five business days for a decision is escalated.

### Kind

- deadline

### Schedule

- 5 business-days after [Event:ClaimSubmitted] — unless [Event:ClaimApproved]

### Fires

- [triggers](aim:#Contract:EscalateClaim)
```

**Edges.** Declares `triggers` (to a Contract, Flow or promoted process) and `satisfies` (a deadline enforcing a time policy).

**Rules.**

- Schedules, polling, SLAs, escalation windows, expiries and recurring obligations all use this facet: an escalation ladder is chained deadlines, an expiry is a deadline triggering a revocation. Event-anchored timing is `deadline`; calendar recurrence is `schedule`.
- The `unless` clause is prose: nothing evaluates it. Where disarming must be verifiable, it SHOULD name an Event the fulfilling operation emits, so the graph can check that Event and its emitter.
- The calendar behind `business-days` is realization; the duration and its anchor are intent.
- Work a Trigger starts still owes a performer (§6.4).

**Diagnostics.** Informational: a Trigger that fires nothing (orphan); an anchor or `unless` Event that does not resolve (unanchored deadline: declare the Event and its emitter).

**Since.** 4.0; deadline and calendar schedules 5.0.

### 6.8 Capability

**Purpose.** A Capability is the kind of outside service or information source the model relies on — a weather source, an identity provider, an ERP — named by what it offers, never by provider, transport or credentials.

**Form.**

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | yes | The kind of source or service. |
| `### Operations` | no | What it offers, one bullet each, as signatures such as `` `FetchRates(currency) -> rates` ``. |
| `### Bindings` | no | The realization that answers it (§9). |

**Example.**

```markdown
## Capability: ExchangeRates

### Summary

An official source of daily currency exchange rates.

### Operations

- `FetchRates(currency, date) -> rates`
```

**Edges.** Declares none. Receives `invokes` from the operations that consult it; that edge derives no inverse.

**Rules.**

- A consuming operation MUST `invoke` the Capability it consults (§6.2). Document-shaped information is acquired by a collect Contract that invokes the Capability and mutates a Record; later work reads the Record.
- The Capability is required in `## Dependencies → ### Requires` (`- ExchangeRates as Rates`) and resolves through a mapping or its Bindings (§8).
- Unresolved capabilities, with Records read but never mutated in the model and schedules to arm, are what a performed intent needs supplied.

**Diagnostics.** Hard error: a Requires alias that resolves through neither a mapping nor Bindings (§8). Informational: a Capability nothing invokes and no Requires names (unused).

**Since.** 4.0 as a requirement surface; a graph node named Capability since 5.6.

### 6.9 Style

**Purpose.** A Style is how what people see should look, at the grain the owner states it: identity, never stylesheet mechanics.

**Form.**

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | yes | The look in a sentence. |
| `### Palette`, `### Type`, `### Shape`, `### Mark`, `### Layout` | no | Bullets of `<token>: <value>`; a token is one lowercase word from an open vocabulary; a value is the owner's words, an exact value, or both. |

**Example.**

```markdown
## Style: Warm

### Summary

Calm and warm, close to paper.

### Palette

- surface: bone `#fbf9f6`
- ink: charcoal `#26221f`
- accent: orange, the only hue

### Layout

- actions: left-aligned under the content
```

**Edges.** None, in either direction. A Style is never an orphan and is outside behavioral traceability.

**Rules.**

- Authored in its intent's file, never a separate kind. At most one per intent. It applies to every View of that intent and its descendants; the nearest Style wins; no edge selects it.
- Tooling MUST accept any token. A realization MUST use exact values verbatim and elaborate descriptive words consistently, recording its choice. A Summary-only Style is valid; a parser does not judge the grain of values.
- Style Layout sets conventions for every screen wearing it; a View's own Layout wins for that screen.
- A Mark's description is intent; its image is supplied material under `content/assets/`, used verbatim, never inside an `.aim` file.
- A View with no Style in reach is complete: the realization chooses a clean neutral look and records it.
- A recovered look is proposed with provenance and needs the owner's signature. Owner-entered legacy `content/style/` tokens MAY move into a Style without inventing values, keeping words and exact values, recording the move, and leaving the tokens readable as a backup.

**Diagnostics.** Hard error: more than one Style on an intent. Informational: a View with no Style in reach.

**Since.** 5.11; Layout family 5.12.

### 6.10 State

**Purpose.** A State is the complete list of how one enum field of a Record may change: where it starts, where it ends, every move with the operation that makes it, where deletion is allowed, and which operations may change the rest of the record only in certain states.

**Form.** A State has only these sub-blocks:

| Sub-block | Required | Holds |
|---|---|---|
| `### Summary` | yes | How the record moves. |
| `### Of` | yes | One bullet: a backticked `Record:<Name>.<field>` or `<ns>#Record:<Name>.<field>`, resolved upward; the field MUST be a required enum. |
| `### States` | yes | One bullet per enum value, one to one. Names compare case-insensitively with spaces as underscores (`In review` is `in_review`); a different value follows in parentheses (`Waiting (on_hold)`). Exactly one is marked `— initial`; any number `— final`. |
| `### Moves` | yes | One bullet per move or guard: `<From> → <To> — <operations>` (`->` accepted), the operations bracketed Contract or Flow references, local or qualified, comma-separated. The reserved target `deleted` declares deletion; the reserved target `unchanged` declares an in-state guard. |

**Example.**

```markdown
## State: ClaimStatus

### Summary

A claim moves from draft to approved; only a draft may be edited or withdrawn.

### Of

- `Record:Claim.status`

### States

- Draft — initial
- Submitted
- Approved — final

### Moves

- Draft → Submitted — [Contract:SubmitClaim]
- Submitted → Approved — [Contract:ApproveClaim]
- Submitted → Draft — [Contract:CorrectClaim]
- Draft → unchanged — [Contract:EditClaim]
- Draft → deleted — [Contract:WithdrawClaim]
```

**Edges.** A State declares no edge tokens; its moves are structured references. The graph derives `governs` to its Record and `moved-by` to each named operation; these are structure, not verbs. A State is never an orphan and is outside traceability.

**Rules.** For every operation writing the Record:

- A changed value MUST be a declared `<From> → <To>` move, made by an operation the move names; the realization MUST refuse any other change before it commits.
- Creation starts in the initial state, by any creating operation; creation is no move.
- Where `→ deleted` moves exist, deletion is allowed only from their states and by their operations, a final state included; with none, the State says nothing about deletion.
- No move leaves a final state except a declared deletion.
- An in-state guard, `<From> → unchanged — [Contract:X]`, lets X change other fields of the record only while it is in `<From>`. Writing the same state value is no move; an operation named on guards MUST find the record in one of their states, and any other operation follows its own rules. Other fields and related records are otherwise not frozen.
- A legal move grants no permission and changes nothing about the operation's Input, Authz, Expects or Ensures.
- A realization that does not enforce these rules is drift and MUST NOT be described as enforcing the State.
- One State per field across the whole model; separate fields have separate States, never combined ones. A State lives with its Record or in a descendant intent. Moves keep their resolved operations and the roles those operations' Authz admits; a State's impact includes its Record, its operations and every other operation that mutates the Record. References are rewritten when the Record or operations move.
- An enum without a State is only a set of values. A machine MUST NOT be inferred from an enum or from guard prose; a recovered machine is proposed with provenance and needs the owner's signature.

**Diagnostics.** Hard errors: `### Of` missing or not a required Record enum field; states and values differing or repeated; not exactly one initial state; a move endpoint that is no state (`deleted` and `unchanged` only as targets); a move out of a final state other than to `deleted`; a self-move `<From> → <From>`; a move naming no operation, an unresolved one, one that is no Contract or Flow, or one that does not mutate the Record; the same move by the same operation twice; two States over one field; any sub-block other than Summary, Of, States and Moves. Informational: a state no move reaches; a non-final state with no way out; an operation that mutates the Record and is named in no move or guard (often right — it may leave the status alone); a State with no moves.

**Since.** 5.13; in-state guards and several machines per record enforced at run time 6.0.

## 7. Edges

Declare each relation once, at its acting node, with `[verb](aim:<address>)`. This is the edge syntax authors write. The 5.13 same-intent shorthand — a declared verb immediately followed by a backticked same-intent address, as in `invokes` `` `#Contract:CreateTask` `` — is a deprecated spelling: tools MUST read it as that link, authors MUST NOT write it, and a tool that rewrites a file writes the link form. A backticked address not immediately preceded by a declared verb (an Authz role, a Dependencies target) is never an edge. The `from` node is the nearest enclosing facet node, or the intent for a top-level declaration; the `to` node is the resolved address. Cross-intent addresses are fully qualified (`aim:<namespace>#<FacetType>:<Name>`); same-intent addresses may omit the namespace (`aim:#<FacetType>:<Name>`). A prose label before the token is optional; it SHOULD NOT repeat the verb.

### Closed taxonomy

Only these verbs and endpoint types are allowed. A disallowed `(verb, from, to)` triple is a hard error.

| Verb | From | To | Meaning | Kind |
|---|---|---|---|---|
| `exposes` | view | contract | A View action surfaces a Contract to users. | declared |
| `invokes` | flow, view, contract, persona, intent | contract, flow, intent, capability | Calls a behavioral unit; from a Persona or persona-natured intent, performs it directly; to a Capability, consults that source-kind. | declared |
| `reads` | contract, flow, view | record | Reads a persisted Record. | declared |
| `mutates` | contract, flow | record | Creates, updates or deletes a Record. | declared |
| `emits` | flow, contract | event | Produces an Event. | declared |
| `subscribes` | flow, contract, intent | event | Consumes an Event. | declared |
| `accesses` | persona, intent | view, intent | Permits a Persona or promoted persona-intent to reach a surface or screen/route intent. | declared |
| `plays` | persona | persona | Binds a local role Persona to a shared organizational Persona while preserving distinct performer lanes. | declared |
| `navigates` | view | view | UI navigation between surfaces. | declared |
| `triggers` | trigger | contract, flow, intent | A schedule, webhook or external origin initiates a behavioral unit. | declared |
| `refs` | record field | record field | Data foreign reference declared by `ref()`. | declared |
| `satisfies` | contract, flow, view, trigger | requirement item | Realizes a `## Requirements` item; a deadline Trigger may enforce a time policy. | declared |
| `triggered-by` | flow, contract, intent | flow / contract / view / trigger / persona / intent | Inverse of `invokes` / `exposes` / `triggers`. | derived |
| `emitted-by` | event | flow / contract | Inverse of `emits`. | derived |
| `satisfied-by` | requirement item | contract / flow / view / trigger | Inverse of `satisfies`. | derived |

`requires` is the capability-alias relation in Dependencies, not an edge verb. `extends` is the `parent:` relation, not an edge verb. Render/layout composition is not an edge verb.

Use View `exposes` for user-initiated actions and View `invokes` for programmatic calls. Both count as reaching a Contract. `accesses` an intent grants reachability to every View in its subtree. Intent-level `accesses` and `invokes` in a promoted Persona's top-level `## Access` are permanent declarations, not placeholders.

Use `invokes` or `triggers` to an intent for a promoted process with top-level `## Steps`; use the facet address when the callee is a facet. Targeting an intent without Steps is a modeling smell. Capability-targeted `invokes` means consulting an external source-kind; its target must be a required capability of the resolving scope. It derives no `triggered-by`. Intent-level `subscribes` is valid when an internal handler is not yet named; at Level 3 it SHOULD be refined to the consuming Contract or Flow.

`satisfies` targets only a Requirements item, never a Capability. Its address is `aim:[<intent>]#Requirements[<key>]`, without a facet-type colon. A key is either a label matching `[A-Za-z][A-Za-z0-9_-]*` or a 1-based integer. Declare a label at the bullet's start: `- **NET14** — The invoice is payable within fourteen days.` Labels MUST be unique within the intent and SHOULD be used once satisfies edges exist. Labeled and unlabeled bullets may coexist; all remain position-addressable. Inserting or reordering items changes positional targets; renaming a label changes identity and requires a rename transform.

Inverse relations are derived, never authored. Behavioral-unit-targeted `invokes`/`exposes`/`triggers` derive `triggered-by`; `emits` derives `emitted-by`; `satisfies` derives `satisfied-by`. Legacy authored `### Trigger` or `### Emitted By` blocks are reconciled against derived sets, with an informational stale-inverse finding on mismatch.

### Language extension policy

A future verb is admitted only if it (1) expresses a relational commitment between existing node types, (2) cannot already be expressed with existing verbs plus prose without losing checkability, (3) enables a new query or diagnostic, (4) has demonstrated need in real models, and (5) arrives with endpoint types, inverse or explicit absence of one, and diagnostics. Attributes, sequencing, composition and accountability prose belong in their existing constructs. The same tests apply to proposed blocks or attribute families, routing non-relational proposals to those forms. Removing or renaming a verb is breaking; aliases and domain synonyms are forbidden. No additional race/cancellation, delivery, per-View-style or implicit foreign-key-by-naming construct is admitted.

## 8. Dependencies and supplied material

`## Dependencies` contains `### Imports` for concrete provider surfaces and `### Requires` for capability aliases. Requires entries use `- <capability-kind> as <Alias>`, for example `- Identity as AssigneeUsers`. Imports declare file-local aliases, such as ``- `org.Employee` as Traveler``; aliases have no separate identity. Use-site edges name the canonical node. Tools MAY display an alias beside the canonical name, consulting the importing file. Where a process has multiple distinct roles played by the same shared organizational Persona, model each local role as a `Persona` with `[plays](aim:...)` (§6.4) rather than collapsing them through `Imports`.

A required external service or information source is a Capability facet (§6.8), required here by its alias.

Each Requires alias resolves either through a co-located `kind: mapping` file or inline Bindings on its Capability. A mapping has `## Map: <Alias>`, `### Target` with a backticked provider intent bullet, and `### Operation Map` bullets in the form ``- `<Alias>.<Operation>` → `<provider>.<Operation>` ``. It is intent-to-intent. Bindings resolve an external provider with no intent model and remain intent-to-realization. A Capability binding MAY name the Capability operation it realizes after `— as:`. An alias unresolved by either form is a hard validation error.

Supplied material is concrete copy, seed data and media beside the model, never authored into `.aim` and never a new facet, verb or block. A View reading a Record owes displayed data and any stated empty-state message; a Record read but never mutated in-model owes externally supplied contents. Optional starting entries for mutable Records are permitted material but create no owed-material obligation. Visual identity belongs in Style; a mark's words are intent, its image file is supplied material. Action labels remain intent and material MUST NOT duplicate them.

The conventional handoff channels are `records/<Name>/` for seed entries and `content/` for copy/media (`content/assets/` for image assets). Their file shapes are not specified. Consumers MUST use supplied material verbatim and never write it back into the model. Missing material is a question for the owner, never permission to invent content or ship placeholders. Material recovered from an existing realization is a draft for owner confirmation, with the same provenance discipline as inferred intent. Material readiness is derived from the handoff; it never changes specification level or becomes a hard model error. Ecosystem tooling determines owed content slots; placement remains realization unless stated in Layout.

## 9. Bindings and review

A binding connects an intent node to its realization site. Bindings are optional; missing coverage is informational at Level 1/2. Writing bindings opts into Level-3 graph-diff responsibility for those claims.

Canonical bindings are a node's inline `### Bindings` property containing bullets such as ``- binds: `src/tasks/create.ts#createTask` — as: handler``. Multiple sites are allowed. Advisory `as` roles include handler, model, component, route, topic and test; text after the backticked locator is prose a parser may ignore. An optional `- provenance: inferred` bullet in the Bindings block carries its trust until human-confirmed, independent of the surrounding intent's trust. The accepted deprecated sidecar form is `kind: binding` with `## Bind: <FacetType>:<Name>` entries; conforming tools MUST read it and MUST merge its locators into inline `### Bindings` before any migration that removes the sidecar file.

Locators have an open scheme set, `<scheme>:<opaque-locator>`. Code-family locators include `path#symbol`, a whole path, `path#L40-L72` (last resort), `route:POST /api/tasks`, `topic:tasks.created` and `table:tasks`. Domains may use system, workflow, form, agent, queue, calendar or other schemes. Unknown schemes are valid; an unsupported scheme is unverifiable, never invalid.

The declared graph consists of intent nodes and declared relations; the realized graph consists of sites and recovered relations. Bindings project them into a common space for diffing. Review is bounded: for each declared edge, inspect the bound site and check that claim rather than reconstructing the entire system. Tools MAY supply a precomputed realized-graph manifest; its format, enforcement mechanics and report formats are not specified. Structural counterparts are checked by graph-diff; guarantee semantics require inspecting realization. Guarantees whose outcomes cannot be verified use procedure verification.

| Finding | Condition | Severity / owner |
|---|---|---|
| `UNBOUND_NODE` | Declared node has no binding. | Informational at Level 1/2; MISSING at Level 3. |
| `DANGLING_BINDING` | Site no longer exists. | INCORRECT; Realizer. |
| `MISSING_EDGE` | Declared edge has no realized counterpart at its bound site. | MISSING; Realizer. |
| `EDGE_MISMATCH` | Edge exists on both sides with different endpoints. | INCORRECT; Realizer. |
| `UNDECLARED_EDGE` | Realized behavior has no declared counterpart. | UNDOCUMENTED; Architect. |
| `AMBIGUOUS_BINDING` | Conflicting sites for one node, or two nodes share one site. | Ambiguous; user input. |

Every finding carries confidence: `high` when the bound realization clearly matches or clearly does not; `needs-human-check` when dynamic or ambiguous realization prevents a conclusion. A clean report means every declared edge was reviewed as realized and no undeclared behavior was found at inspected bound sites, at stated confidence; it is not global proof. Proxy confidence concerns procedure conformance, never outcome truth. The impact set is every node reachable from a changed node by following inbound edges.

### Verification modes

For cheaply and completely checkable outcomes, state Ensures and verify the result; do not also prescribe a procedure. For an unverifiable guarantee, state a Flow invoked by the Contract and verify its normative Steps. These modes compose per guarantee: output-check what is observable and cover only the remainder by procedure. Procedure conformance MUST NOT be reported as outcome verification; proxy-verified guarantees never earn high outcome confidence. When uncertain, check output and prescribe procedure only where output cannot answer.

## 10. Diagnostics

Evaluate conformance over the complete resolved project graph, never a file alone. Each facet's own hard errors and informational conditions are listed in its block (§6); the ones below cross facets. A conforming tool reports both. Tools MAY further partition informational conditions into readiness tiers (such as structural `gap`, owner `question`, and advisory `note`) to gate build or process execution, provided every hard error and informational condition is preserved.

### Hard errors

- Missing/malformed frontmatter or required `aim`/`kind`; path/header mismatch; declared parent without an intent file; missing H1; missing/empty Requirements; invalid facet heading type/name; duplicate effective facet definitions; child collision with an authoritative parent facet; generic filenames; auto-discovered child omitted from an explicit Children list.
- Unresolved Requires alias; dangling edge or unresolved `ref()` Record; `ref()` field absent from a resolved Record; `satisfies` index out of range, label absent or duplicated; address type differing from the resolved node; illegal verb/endpoints triple.
- `cross-owner(...)` outside a backticked Authz role entry or Persona View-access edge; unresolved or non-Record grant target; grant target absent from the operation's declared reads/mutations or the accessed View's declared reads.

### Informational conditions

- Missing Tests; intent without facets; shadowed lower-precedence source; unresolved Import alias; inferred/unconfirmed provenance; confirmation coverage; unrecognized frontmatter keys (permitted and ignored).
- Inferred provenance combined with approved status or approved_by: acceptance changes provenance and records approval together.
- Breadth outside 3–9 or single-child chains; wrapper child with exactly one facet, no own requirements and no children; nature contradicting content.
- Orphan: a facet nothing reaches as its block defines (Contract, View, Event, Trigger). A Flow or Contract entered by `triggers` or `subscribes` is not an orphan; Style, State and Capability are never orphans.
- Intent-level subscription retained at Level 3; Requirements item with no inbound satisfies (tools MAY promote this to a Level-3 finding); positional satisfies reference; authored inverse differing from derivation.
- Probable duplicate: same type/name in intents not linked by import/reference/`plays`. Confirm distinction or canonicalize; name equality alone proves nothing.
- Monolith: excessive embedded facets. Extract genuinely shared facets to sibling files/core; promote distinct behavioral clusters, or process phases. Detection is heuristic/tunable and should distinguish these remedies; facet count matters principally without children.
- Over-hoisted facet: all consumers lie in one descendant subtree. Move it to its consumer, unless retaining a canonical entity awaiting further consumers; count reference subtrees where edges exist. Preserve local roles separately from canonical entities.
- Noun-cluster: inside a mixed intent, a Record plus several like-named operations, often a View, form an unpromoted capability. Promote the existing cluster together. Detection is heuristic/tunable; a reasonable default is a Record named in at least three sibling operations with at least two unrelated content facets remaining. MUST NOT flag an intent containing only that focused cluster.
- Unsupplied material: missing View copy or entries for a read-but-never-mutated Record. This is a handoff finding, never a model defect, hard error or level change; supply material beside the model.
- Stale satisfier: a requirement changed but an item carrying satisfies did not. Apply the commitment-change rule below; never remove the edge as repair.

## 11. Decomposition and verification rules

Design nodes and relations before serializing files. Parents are lean indexes of cross-cutting requirements, Children and dependencies. Shared facets belong at their consumers' lowest common ancestor; only entities move upward, never the local roles reading them. Embed a handful there; sibling facet files earn themselves when the set grows. Cross-top-level entities have one importable canonical home, conventionally `<app>.core`. Before defining an entity, search the project graph and reference an existing definition rather than regenerate it.

A child owns one observable capability, its requirements/tests and specific facets. A child with only one facet and no own commitments adds no meaning; keep the facet on its parent/entity until it earns a level through purpose, requirements, entry points or multiple facets. Split distinct behaviors, preserving the shape rules. Promote noun-clusters together when the next change touches them. Promote substantive Persona/Record entities with their own operations into entity-intents; their operations arrive as facets, not one-operation child wrappers.

Organizational process boundaries follow end-to-end commitments across people, software and systems. A project's root Summary states purpose; Requirements state existential commitments and the root canonically owns organization-wide shared entities. Children fulfill ancestor commitments through satisfies; organizational requirements use labels. Software, processes and obligations may be siblings. Derive structure from commitments, bottom-up or top-down; do not mirror reporting lines. Represent actors as Personas, permission as Authz and performance by declared performer relations.

## 12. Evolution

Authoring operations are EXTEND an existing intent and ADD an intent. Tools reshape structure using promote (capability to child), split (distinct behaviors to siblings under an index), move/re-home, merge or rename. These are transforms, not language syntax or additional author primitives.

A transform changes addresses, never commitments. It MUST preserve behavior and relations, and:

1. Repoint all inbound references across the whole graph; introduce no dangling reference or illegal triple.
2. Requalify elided outbound addresses on cross-intent moves wherever new scope would change their targets.
3. Update every affected Children index.
4. Restore agreement of directory, filename, aim and parent.
5. Carry inline bindings with nodes; relocate/update legacy sidecars. Preserve realization locators because the realization has not moved.
6. Have Architect confirmation before merging purported duplicates; remove the duplicate, choose one canonical node and repoint both sets of references.

Transforms yield graph-diffs of nodes, addresses, edges and bindings, with computable impact sets. A change record MAY preserve this delta under `/aim/work/` for realization handoff. It is non-authoritative, point-in-time, archived after application; on disagreement `.aim` wins and review falls back to full graph-diff. Its format is not specified. A valid transform introduces no attributable hard error or orphan, shadow, duplicate or monolith smell.

EXTEND that rewrites a requirement changes a commitment. Revisit every item containing a satisfies edge to it: revise the item or explicitly confirm and report that it still holds. Stale satisfier compares both sides of a change: requirement text changed at the same label, or same position if unlabeled, while the satisfying list item/step/paragraph did not. It also flags harmless rewording for confirmation. Removing satisfies is never repair. New requirements have no existing satisfiers to revisit; removed requirements produce dangling references; reordered labeled items do not change identity.

## 13. Re-encoding existing realization

Reverse encoding infers intent from artifacts or testimony, acting as Architect and Realizer and emitting bindings in the same pass. Cite artifact sources. Record who supplied testimony and when; testimony defaults to needs-human-check until its source or principal confirms. Retain asserted but unevidenced rules with confirming questions. Capture exceptions in On Error or separate operations and ask about them explicitly.

Re-encoded files MUST carry `provenance: inferred`; remove it or set confirmed on human acceptance. Absence means confirmed. Overall file provenance and per-node binding provenance compose independently. Inferred intent is provisionally authoritative for resolution and diagnostics but MUST be visually/reportably distinguished wherever presented. Confirmation coverage is informational.

Record `high` or `needs-human-check` confidence in a non-authoritative encoding report under `/aim/work/`, never in `.aim`; the model carries provenance. Emit a binding for every inferred node with an identifiable realization site. Personas as roles and manual steps known only from testimony are exempt; otherwise reverse encoding provides Level-3 binding coverage immediately. Bound each examination by intent; an entire tree MAY be drafted together but humans confirm each intent separately. Resolve-or-reference existing entities before defining new ones; duplicates use the ordinary diagnostic and Architect-confirmed merge.
