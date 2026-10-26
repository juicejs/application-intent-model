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

## 6. Precision facets

The facets are Record, Contract, Flow, Persona, View, Event, Trigger, Style and State. Capability is the external surface defined under Dependencies. Properties belong to their node; a schema is a property, not a node.

### Record

A Record is passive data that operations store, read or process. It declares its fields in `### Schema` using the schema grammar. `### Constraints` declares data constraints as bullets; `### Immutable` lists fields that must not change after row creation. Other nodes use the same schema grammar in their data properties: Contract `### Input`, Event `### Payload`, or an entity-intent's top-level `## Schema`.

A Record may become an intent when its data and lifecycle warrant a file. Its schema becomes top-level `## Schema`, it carries `nature: record`, and its operations co-locate as facets. The intent is the entity; it MUST NOT contain a redundant same-named Record facet.

### Contract

A Contract specifies externally observable guarantees and obligations:

- `### Summary`: the operation's purpose.
- `### Input`: caller-supplied fields, in a `schema` fence.
- `### Authz`: who may perform it, as bullets.
- `### Expects`: preconditions, as bullets.
- `### Ensures`: postconditions and resulting graph actions, as bullets.
- `### Returns`: externally returned results, as bullets.

An operation acquiring external information MUST declare the Capability it consults with `invokes`; a source named only in prose is insufficient. For caller-supplied documents, the Input declares a `file`; the reading Capability parses it, and the Contract owns the resulting records. Acquisition may be a collect operation that invokes the Capability and mutates a Record; downstream operations read that Record.

#### Decisions

A decision is the Contract or Flow that reaches a judgment, with its authority and criteria. It is not a separate node. The deciding node declares `### Decides`:

```markdown
### Decides

- **Approved** — every claim is supported — [emits](aim:#Event:Approved)
- **Returned** — any claim lacks support — [invokes](aim:#Contract:Correct)
```

Each bullet is one outcome. Its bold label follows the facet-name grammar and is addressable as `#Contract:<Name> → Decides[<Label>]` for a deciding Contract. Text after the dash states normative judgment criteria. The realization MUST decide on those criteria. Edge tokens belong to their outcome bullet; `emits`, `invokes`, `mutates` and `reads` may describe its effects and data access.

The block MUST contain at least two outcomes and asserts that they are mutually exclusive and exhaustive. It derives one exclusivity group for the deciding node, containing ordered labels, criteria and their edges. These are alternatives; operations sharing a step without such a decision relationship are joint work.

#### Every write is held to the model

However a realization performs a Contract — coded, interpreted or by a runtime engine — every Record mutation it makes MUST satisfy `### Schema`, `### Immutable`, `owner`/`!owner` and every `## State` governing the Record, before the mutation commits. When a realization may perform a Contract without interpretation is realization, not language.

### Flow

A Flow declares operational sequencing, branching, retries and error handling. It declares sequencing in an ordered `### Steps` list and may declare error handling under `### On Error`. Its callers are derived from their `invokes` edges; a Flow MUST NOT author an inverse `### Trigger` block.

#### Steps

1. One numbered list item is one step. List position determines sequence; authored numbers are display only. Indented continuation lines belong to the preceding step.
2. Inline edge tokens are that step's operations. Every such edge retains the step index in the derived graph.
3. Multiple `invokes` in one item are one step, never an internal sequence. They are exclusive alternatives only when they are outcomes of a deciding Contract; otherwise they are unordered joint work.
4. Joint operations MAY run concurrently, in either order or interleaved. The following step is a join and MUST NOT begin until all joint operations complete. Multi-step parallel branches are separate Flows or process-intents jointly invoked by one step.
5. An item without edges is a human step and appears in process projections. An item whose only operations are `reads`, `mutates` or `emits` is work performed by the Flow itself.
6. A step's words describe work but never declare a performer. Performer resolution uses Persona `invokes` edges and Flow inheritance, independently of language or names in prose.

Joint work does not express a race or cancellation. Where first-completes-wins is a real commitment, state it in step prose and verify its procedure; race and cancellation constructs are not admitted language features.

#### Decision continuation

A step invoking a deciding Contract carries the fork. If one outcome continues the procedure, its continuation is the next step and MUST NOT also be declared on that outcome. Every other outcome declares its own consequence in its Decides bullet. A corrective outcome may invoke corrective work that invokes the deciding Contract again; such Contract cycles are legal while Steps remain the linear procedure.

If no single outcome proceeds, the deciding step is last and every outcome declares its continuation. Express a correction loop's bound as a deadline Trigger anchored on the phase's start and disarmed by the confirming Event. A count bound such as a maximum number of failed reviews is not expressible.

#### Event continuation

Sequence always proceeds to its next step by position, regardless of emissions or subscribers. Only `invokes` and `emits` continue work along an edge; `reads`, `mutates` and `satisfies` do not.

An emitted Event continues a branch through its subscribers. A subscriber without Steps is the next work on that branch. A subscriber with its own Steps starts a separate run; it does not continue the emitting run. An Event without subscribers ends only that event branch. Thus an outcome whose sole consequence emits an unobserved Event ends its leg; the emitting Flow's remaining steps still proceed. A Trigger anchored on an Event arms a timer and does not continue the branch.

#### Process-intents and phases

A process with its own operations, records and requirements may become an intent carrying `nature: flow`. Its sequence is top-level `## Steps`, with the same grammar and edges declared from the intent node. Its operations and records co-locate as facets; no same-named Flow restates the process.

Where an organization has several such processes, each may own a flow-natured child intent. A project consisting of one process uses the root as that process; it MUST NOT introduce a lone flow-natured child merely to wrap it.

A large single process decomposes into phases: consecutive steps producing one artifact. A phase with its own Record and operations becomes a flow-natured child. The root keeps shared Personas, the entry Trigger, cross-cutting Requirements, the Children index, and an orchestrating Steps list or Flow invoking the phases in order. Each phase keeps its Steps, Contracts, Events and Record. The parent sequence names phases; a phase sequence names its steps. Each step is declared at its owning level, not repeated at both. References cross phase boundaries normally.

Long-running orchestration uses existing constructs: a Flow invokes work, mutates a progress Record, and emits or subscribes to compensation Events. Durable timer and signal mechanics belong to realization.

### Persona, permission and performance

A Persona declares an actor's identity or a role played in one intent. `### Role` describes the actor; `### Access` declares the Views or intents it accesses and operations it invokes.

An entity shared across processes has a canonical home; a process-specific role remains with the intent reading that role. Moving shared entities upward MUST NOT merge distinct roles and erase a handoff. Use `[plays](aim:...)` where a local process role is filled by a canonical organizational Persona, or use an Imports alias when the canonical entity is referenced directly without splitting into multiple roles; do not create a second canonical entity for the same organizational group.

#### Role-in-context (`plays`)

When an intent distinguishes local roles that are filled by the same shared organizational Persona (for example, both `Submitter` and `Approver` are employees, or a `Reviewer` is a member of `HR`), each local role is declared as its own `Persona` and links to the underlying organizational Persona in `### Role` with `[plays](aim:<address>)`:

```markdown
## Persona: Submitter

### Role
- Submits expense claims for reimbursement — [plays](aim:org#Persona:Employee)

### Access
- [invokes](aim:#Contract:SubmitClaim)

## Persona: Approver

### Role
- Reviews and approves submitted expense claims — [plays](aim:org#Persona:Employee)

### Access
- [invokes](aim:#Contract:ApproveClaim)
```

`Submitter` and `Approver` remain distinct performers in process projections and handoffs, while inheriting candidate identity records from the played organizational Persona. `plays` grants no permission or cross-owner scope; each local role's Authz and View-access declarations apply separately.

#### Performer resolution

Resolve the performer of work in this order:

1. A Persona directly invoking the operation is its performer. Several Personas invoking the same operation are alternative performers; any one may act. To require a particular actor in a particular step, that step invokes an operation only that actor invokes. Joint performance requires a step per actor, not several invokers of one operation.
2. A step containing only `reads`, `mutates` or `emits` is performed by the Flow itself and inherits no Persona.
3. A human step or invoked operation without its own performer inherits the nearest enclosing Flow's or promoted process's performer. That Flow's performer is direct or inherited in turn; the first declaration stops inheritance.

These facts MUST remain distinct:

- `Authz` declares permission, never performance. It names roles by backticked addresses, for example `#Persona:Approver` or `org#Persona:Employee`, resolved like link addresses. An entry may carry `cross-owner(<Record-address>)` and `!owner` under the scope rules in §3. Several named roles are alternatives. A role mentioned only in Authz prose names nobody. Where Authz names roles, the performer MUST be among them; with no named role, whoever performs the operation is permitted.
- A Persona accessing a View that exposes an operation can reach it; that does not commit the Persona to performing it.
- A Trigger starts work and never performs it.
- Role prose and step prose do not assign work.

Work owes a performer when it is a Flow or process step, is invoked by a step, or is started by a Trigger or subscription. Such work is incomplete without a performer under these rules. An operation merely offered through a View owes no performer; whoever reaches it may act within its Authz.

A Persona that acquires its own data and operations may become a `nature: persona` intent. Its acting face becomes top-level `## Role` and `## Access`, its data top-level `## Schema`, and its operations co-located facets. The intent is the actor and MUST NOT contain a same-named Persona. An entity-specific operation belongs under the entity, not scattered on its parent.

### View

A View declares a shared interface surface. `### Display` states what it shows and which Records it reads. `### Actions` names user-visible commitments and exposes or invokes their operations. Display declares that copy exists, not the words of that copy: the words are supplied material. Action labels remain intent because they name commitments.

When a View reads directly or indirectly owned rows, ownership scope applies by default regardless of the caller's Persona or `plays` links. Only `cross-owner(<Record-address>)` on that Persona's access edge to that View widens its reads for the named Record. Authz on an exposed operation does not widen the View's reads, and View access does not widen any operation's scope.

Optional `### Layout` states only arrangements the owner has specified: one bullet per commitment, in the owner's words, describing relative position, order, grouping or prominence. A bullet identifies its subject through the View's Display terms, Action labels or read Records. It declares no edges; parser validation MUST NOT compare its prose with other blocks. Review judges it. Pixels, grid systems and stylesheet mechanics are realization.

Unstated arrangement remains realization freedom. A tool-generated arrangement MUST NOT become Layout unasked; a tool SHOULD distinguish owner commitments from its choices. Owner feedback on a draft may become an ordinary Layout change.

#### Surface ownership

A page or UI piece with its own accountable outcome is a child intent once that purpose is understood, before it owns data or operations. Its Summary and testable Requirements express that purpose; its constituent sections are View facets. The page-intent MUST NOT add a same-named View restating itself. A Persona may access the intent, covering every View inside it.

A static or host-fed piece within a screen, with no behavior of its own, is a Display bullet, not a node. A piece acquiring its own data, operations or surface owns corresponding facets: a child intent when they form a coherent capability, or a View with sibling facets on the intent served. A promoted piece used only inline usually SHOULD NOT declare its own View; its host owns the surface. A reusable surface must be reachable by a Persona or belong to its host.

Behavior and reachability use existing `reads`, `exposes`, `invokes` or `navigates` edges. Inline visual composition itself has no edge and is realization, except owner-stated arrangement committed in Layout.

### Event

An Event declares an asynchronous announcement and its data. `### Payload` uses a schema fence. `### Routing` may state routing properties as bullets, such as `Channel: tasks.created` and `Durable: true`. Emitters are derived from emitting nodes' `emits` edges; an Event MUST NOT author `### Emitted By`.

### Trigger

A Trigger declares a non-actor entry point and uses `### Fires` with `triggers` edges to the Flow, Contract or promoted process-intent it starts. Its `### Kind` names `schedule`, `deadline`, `webhook` or `external`. Event-anchored timing uses `deadline`; calendar recurrence uses `schedule`. Webhook and external origins describe their source in prose rather than a Schedule. External announcements enter through a Trigger that `triggers` an ingest Flow which emits the internal Event, so that Event has an emitter.

Schedules, polling loops, external systems, SLAs, escalation windows, expiries and recurring obligations use this construct. `### Schedule` admits:

- Machine-precise `cron: <expression>`.
- Event-anchored `<n> <unit> after [Event:<Name>]`, with `minutes`, `hours`, `days`, `business-days` or `weeks`.
- Calendar-recurring `monthly on the <n>th`, `weekly on <weekday>` or `yearly on <date>`.

The latter forms may include informal disarming prose, such as `— unless [Event:Confirmed]` or `— unless [Event:ReportReceived] for the period`. This clause is not executable or conformance-checkable. Where disarming verification matters, its condition SHOULD be an Event emitted by the fulfilling operation, and the clause SHOULD name it; the graph can then check the Event and its emitter, not evaluate the words. The calendar used for business-days is realization; duration and anchor are intent. Escalation ladders chain deadline Triggers; expiry triggers revocation.

### Style

A Style declares owner-stated visual identity at identity grain, not stylesheet mechanics. It is authored in its intent file, never a separate sidecar kind. Each intent declares at most one Style. It applies to every View in that intent and its descendants; a nearer Style wins. No edge selects it. Style declares no edges, receives none, is not an orphan and is outside behavioral traceability.

Besides Summary, optional sub-blocks are `### Palette`, `### Type`, `### Shape`, `### Mark` and `### Layout`. Each uses bullets of `<token>: <value>`. A token is one lowercase word; the token vocabulary is open and tooling MUST accept any token. Values are owner words, exact values or both. A realization MUST use exact values verbatim and elaborate descriptive words consistently, recording its choice. A Summary-only Style is valid; a parser does not judge the grain of its values.

Style Layout declares conventions for every screen wearing it. A View's Layout wins over a Style convention for that screen. Unstated arrangement and implementation remain realization.

A Mark's description is intent. Its image file is supplied material under `content/assets/`, never inside an AIM file; a supplied file is used verbatim. A View without a reachable Style is complete: realization chooses and records a clean neutral style, and tooling reports only an informational absence.

A recovered identity is proposed with provenance and requires the owner's signature before entering the model. Owner-entered legacy `content/style/` tokens MAY be moved into a Style without inventing values: preserve words and exact values, record the migration in file history, and keep the tokens readable as backup.

### State

A State exhaustively specifies permitted changes and state-gated mutations of one Record enum field. It has only Summary and these sub-blocks:

- `### Of`: exactly one bullet containing a backticked `Record:<Name>.<field>` or `<ns>#Record:<Name>.<field>`. It resolves upward; the target MUST be a required enum field.
- `### States`: one bullet per enum value, corresponding one to one. Names compare case-insensitively, with spaces treated as underscores; `In review` denotes `in_review`. An explicit different value follows in parentheses: `Waiting (on_hold)`. Exactly one state is marked `— initial`; any number may be marked `— final`.
- `### Moves`: one bullet per move or in-state guard, `<From> → <To> — <operations>`. `->` is accepted for `→`. Operations are one or more comma-separated bracketed Contract or Flow references, local or qualified: `[Contract:Approve]`, `[Flow:Close]`, `[org.close#Contract:Approve]`. Each named operation MUST mutate the governed Record. Reserved target `deleted` declares deletion; reserved target `unchanged` declares an **in-state guard** (`<From> → unchanged — [Contract:EditDraft]`), permitting the named operations to mutate other fields of the Record only while the governed field is in `<From>` without changing the state value. An explicit self-move `<From> → <From>` remains a hard error.

Moves are structured references, not edge tokens. A State declares no edge tokens; states are names within its node, not separately addressable nodes.

The following rules apply to every operation writing the Record:

- A changed state value MUST match a declared before/after `<From> → <To>` move and the writing operation MUST be named on that move. Realization MUST reject any other change before committing it.
- Creation starts in the initial state, by any creating operation; creation is not a move.
- If deletion moves (`<From> → deleted`) exist, deletion is permitted only from their named states and by their named operations. A declared deletion may leave a final state. With no deletion moves, State imposes no deletion rule.
- No other move leaves a final state. Other fields and related records are not frozen unless gated by an in-state guard (`<From> → unchanged`).
- Writing the same state value is not a transition; if the operation is named on one or more `<From> → unchanged` guards, the row MUST be in one of those `<From>` states, otherwise the operation's own rules govern it.
- A legal move grants no permission and changes no operation Input, Authz, Expects or Ensures.

Failure to enforce this check is realization drift; such a realization MUST NOT be described as enforcing the State.

A State lives with its Record or in a descendant intent. Exactly one State may govern a field across the whole model. Separate fields have independent States, not combined states. References are rewritten when their Record or operations move.

The derived graph contains a `state` node, a `governs` structural edge to the Record, and `moved-by` structural edges to named operations. These are derived structure, not authored verbs. Moves retain resolved operations and the roles admitted by those operations' Authz. A State is not an orphan and is outside the traceability chain. Its impact includes its Record, named operations and every other operation mutating that Record.

An enum without State declares only its values. A machine MUST NOT be inferred from an enum or guard prose. A recovered machine is proposed with provenance and requires the owner's signature before entering the model.

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

`## Dependencies` contains `### Imports` for concrete provider surfaces and `### Requires` for capability aliases. Requires entries use `- <capability-kind> as <Alias>`, for example `- Identity as AssigneeUsers`. Imports declare file-local aliases, such as ``- `org.Employee` as Traveler``; aliases have no separate identity. Use-site edges name the canonical node. Tools MAY display an alias beside the canonical name, consulting the importing file. Where a process has multiple distinct roles played by the same shared organizational Persona, model each local role as a `Persona` with `[plays](aim:...)` (§6) rather than collapsing them through `Imports`.

A required external service or information source may have a `## Capability: <Alias>` surface with Summary and Operations. These declare the required kind; provider, transport, query mechanics and credentials are realization. A consuming operation invokes the Capability. Acquire document-shaped information in a collect Contract that invokes the Capability and mutates a Record; downstream operations read that Record. Unresolved capabilities, Records read but never mutated in-model, and schedules to arm derive what a performed intent needs supplied.

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

Evaluate conformance over the complete resolved project graph, never a file alone. Tools MAY further partition informational conditions into readiness tiers (such as structural `gap`, owner `question`, and advisory `note`) to gate build or process execution, provided every hard error and informational condition below is preserved.

### Hard errors

- Missing/malformed frontmatter or required `aim`/`kind`; path/header mismatch; declared parent without an intent file; missing H1; missing/empty Requirements; invalid facet heading type/name; duplicate effective facet definitions; child collision with an authoritative parent facet; generic filenames; auto-discovered child omitted from an explicit Children list.
- Unresolved Requires alias; dangling edge or unresolved `ref()` Record; `ref()` field absent from a resolved Record; multiple `owner` fields on one Record; `satisfies` index out of range, label absent or duplicated; address type differing from the resolved node; illegal verb/endpoints triple.
- `cross-owner(...)` outside a backticked Authz role entry or Persona View-access edge; unresolved or non-Record grant target; grant target absent from the operation's declared reads/mutations or the accessed View's declared reads.
- More than one Style on an intent.
- State Of absent or not a required Record enum field; State values and enum values differing or repeated; zero or multiple initial states; unknown move endpoint (`deleted` and `unchanged` allowed only as target); move out of final state except to `deleted`; explicit self-move (`<From> → <From>`); missing/unresolved move operation, operation not Contract/Flow or not mutating the Record; duplicate same move/operation; multiple States governing one field anywhere; State sub-block other than Summary, Of, States or Moves.

### Informational conditions

- Missing Tests; intent without facets; shadowed lower-precedence source; unresolved Import alias; inferred/unconfirmed provenance; confirmation coverage; unrecognized frontmatter keys (permitted and ignored).
- Inferred provenance combined with approved status or approved_by: acceptance changes provenance and records approval together.
- Breadth outside 3–9 or single-child chains; wrapper child with exactly one facet, no own requirements and no children; nature contradicting content.
- Orphan: Contract with no exposes/invokes/triggers entry; Event with no emitter; View with no Persona access to it, its intent or an ancestor; Trigger with no outbound triggers. A Flow/Contract entered by triggers or subscribes is not orphaned. Style and State are never orphaned.
- Intent-level subscription retained at Level 3; Requirements item with no inbound satisfies (tools MAY promote this to a Level-3 finding); positional satisfies reference; authored inverse differing from derivation.
- Probable duplicate: same type/name in intents not linked by import/reference/`plays`. Confirm distinction or canonicalize; name equality alone proves nothing.
- Monolith: excessive embedded facets. Extract genuinely shared facets to sibling files/core; promote distinct behavioral clusters, or process phases. Detection is heuristic/tunable and should distinguish these remedies; facet count matters principally without children.
- Over-hoisted facet: all consumers lie in one descendant subtree. Move it to its consumer, unless retaining a canonical entity awaiting further consumers; count reference subtrees where edges exist. Preserve local roles separately from canonical entities.
- Noun-cluster: inside a mixed intent, a Record plus several like-named operations, often a View, form an unpromoted capability. Promote the existing cluster together. Detection is heuristic/tunable; a reasonable default is a Record named in at least three sibling operations with at least two unrelated content facets remaining. MUST NOT flag an intent containing only that focused cluster.
- Unanchored deadline: after/unless Events do not resolve. Declare the Event and its actual emitter.
- Decision outcome Event with no subscriber or Trigger anchor/disarmer; fewer than two outcomes; outcome lacking criteria; two or more emitted Events with divergent consumers but no Decides (ask whether it is a decision; concurrent announcements need no change).
- Redundant continuation: an outcome repeats the next step's operation. Keep continuation on the next step only. Ambiguous continuation: a deciding step precedes further Steps but zero or several outcomes are proceeding (lack their own continuation). Specify non-proceeding continuations or end the sequence at the decision.
- Flow step reachability and termination: a process sequence with no entry point, a step unreachable from any entry point, a non-terminal step that cannot reach any terminal outcome, or a cycle (such as a correction loop) with no decision outcome or deadline Trigger that exits the loop.
- Ungrounded decision: no reads, capability invokes or Input; declare the basis or confirm self-contained criteria. Unused Capability: no inbound invokes and no Requires alias.
- State unreachable from any move except initial; nonfinal state with no outgoing move; mutator of a governed Record named in no move or in-state guard; State with no moves. A mutator outside moves may legitimately leave status unchanged when not constrained by an in-state guard.
- View without an in-scope Style: Realizer chooses and records a clean neutral look; accept it or declare Style.
- Unsupplied material: missing View copy or entries for a read-but-never-mutated Record. This is a handoff finding, never a model defect, hard error or level change; supply material beside the model.
- Owed work without a declared performer: no performer, permission only (`Authz` without Persona `invokes`), or Trigger only. Tools SHOULD distinguish these and ask once per Flow where inherited performance answers several steps. The owner supplies the commitment; the Architect never invents it. Performer outside Authz: align the declarations, or separate work when all roles must act. Multiple Authz roles are alternatives. Persona with no performance, reachability, `plays` link or Authz role: give it its part or remove it; step prose does not declare performance.
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
