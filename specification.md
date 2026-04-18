# Application Intent Model (AIM) v2.1

Application Intent Model (AIM) is an intent-first specification language for humans and AI agents. It captures product behavior in a form that is readable enough for product and design discussion and structured enough for implementation, verification, repair, and deterministic synthesis.

AIM supports progressive precision:

- start with a single intent envelope
- add precision facets only where stronger guarantees are needed

This keeps simple components easy to author while allowing high-fidelity implementation and synthesis for complex systems.

---

## 1. Core Model

A component is identified by a namespace such as `company.subsystem` (for example `game.snake`, `juice.tasks`).

Each component has:

- one required intent envelope
- zero or more optional precision facets: `schema`, `flow`, `contract`, `persona`, `view`, `event`
- zero or more optional mapping files using facet `mapping`

The intent envelope is the canonical entrypoint for a component. All other detail is attached to that entrypoint directly or indirectly.

### 1.1 AIM As A Coordination Layer

AIM is the authoritative shared artifact between humans and coding agents.

It describes intended system behavior, structure, and constraints in a form that multiple agents can read and act on consistently. AIM is not an agent protocol, agent topology, or swarm configuration language. The number of agents involved in a workflow is outside the language and may vary by project, task, or implementation strategy.

The intent envelope is the primary behavioral reference for a component. Precision facets add detail and stronger guarantees, but they do not replace the authority of the intent envelope.

### 1.2 How Agents Should Treat Intent

One or more agents may participate in any of the following responsibilities:

- interpret requirements by creating or refining intent
- implement code and tests by reading intent and available facets
- validate code, tests, and outputs against intent
- repair mismatches by updating code or, when necessary, revising intent explicitly

Agents should coordinate primarily through AIM artifacts rather than relying on unstated assumptions, private memory, or ad hoc chat context.

Normative guidance:

- implementation should not invent material behavior absent from intent
- when detail is missing, agents should preserve the documented intent and minimize assumptions
- when assumptions are necessary, they should be surfaced for review or converted into explicit intent updates
- when implementation and intent disagree, the mismatch must be resolved explicitly rather than silently normalized
- if the implementation is wrong, fix the code
- if the intent is outdated, revise the intent before continuing implementation
- if requirements changed, update intent before further coding or repair

### 1.3 Agent Operating Roles

The following roles are defined as operational guidance for systems and teams using AIM. They are not AIM language constructs and do not appear in `.intent` source files.

A workflow may use one agent, many agents, or any combination of these roles. One agent may perform multiple roles, and multiple agents may share one role.

#### Intent Author

Purpose:

- interpret requirements and translate them into AIM artifacts

Reads:

- product requirements
- existing AIM files
- relevant code and tests when refining an existing system

Writes:

- intent envelope
- precision facets when needed
- explicit clarifications of assumptions or ambiguities

Primary goal:

- make intended behavior explicit, reviewable, and implementation-ready

Must do:

- express requirements in intent rather than leaving them implicit
- add facets only when they increase useful precision
- surface ambiguity when requirements are incomplete or conflicting

Must not do:

- treat implementation accidents as authoritative requirements
- add unnecessary implementation detail when it is not part of intended behavior

Handoff output:

- updated AIM artifacts
- short explanation of clarified assumptions and open questions

#### Implementer

Purpose:

- build code and tests from resolved intent and facets

Reads:

- intent envelope
- resolved precision facets
- mappings and dependency surfaces when relevant

Writes:

- code
- tests
- implementation notes that trace work back to intent when needed

Primary goal:

- implement the specified behavior faithfully

Must do:

- treat the resolved intent and facets as the authoritative implementation reference
- preserve documented behavior when detail is incomplete
- surface specification inconsistencies before inventing behavior

Must not do:

- invent material behavior not grounded in intent
- silently redefine the specification through implementation choices

Handoff output:

- code and tests aligned to intent
- short traceability note when useful

#### Verifier

Purpose:

- compare implementation and outputs against resolved intent and facets

Reads:

- AIM artifacts
- code
- tests
- observable outputs and behavior

Writes:

- findings
- drift reports
- recommendations for repair or intent revision

Primary goal:

- detect mismatches between intended and implemented behavior

Must do:

- distinguish missing behavior, incorrect behavior, and undocumented extra behavior
- ground findings in intent and available evidence
- identify whether the likely fix belongs in code or in intent

Must not do:

- evaluate primarily on personal preference
- collapse materially different problems into vague feedback

Handoff output:

- concrete mismatch report with rationale and suggested direction

#### Repairer

Purpose:

- restore alignment when intent and implementation diverge

Reads:

- AIM artifacts
- verifier findings
- code and tests

Writes:

- code fixes
- targeted test fixes
- intent revision proposals when the specification is outdated

Primary goal:

- restore alignment with minimal unnecessary change

Must do:

- fix code when implementation drift is the problem
- request or apply intent revision when the specification is outdated
- preserve traceability between the repair and the intent it satisfies

Must not do:

- silently normalize drift by changing behavior without resolving the underlying mismatch
- expand scope beyond what is needed to restore alignment

Handoff output:

- repaired implementation or explicit intent revision recommendation
- short explanation of what drift was corrected

### 1.4 Example Agent Prompts

The following prompts are non-normative examples. They illustrate how an AIM-based system may instruct agents to operate consistently around the specification. The exact prompt wording is implementation-defined.

#### Example Prompt: Intent Author

```text
You are working from product requirements and existing AIM files.
Your job is to produce or refine the AIM specification so the intended behavior is clear, testable, and implementation-ready.

Rules:
- Treat AIM as the authoritative specification artifact.
- Make requirements explicit in the intent envelope and facets rather than leaving them implicit.
- Add precision facets only when they increase useful precision.
- Do not add implementation details unless they are part of intended behavior.
- If requirements are unclear or conflicting, surface the ambiguity explicitly.

Output:
- updated AIM artifacts
- a short summary of clarified assumptions
- any unresolved ambiguity
```

#### Example Prompt: Implementer

```text
You are implementing from AIM.
Your job is to read the resolved intent and available facets and produce code and tests that follow them closely.

Rules:
- Treat the resolved intent and facets as the authoritative implementation reference.
- Do not invent material behavior not grounded in intent.
- If detail is missing, minimize assumptions and preserve documented behavior.
- If the specification appears inconsistent, surface the inconsistency before continuing.

Output:
- code changes
- tests
- a short note mapping the implementation back to intent
```

#### Example Prompt: Verifier

```text
You are verifying implementation against AIM.
Your job is to compare the current code, tests, and observable behavior with the resolved intent and facets.

Rules:
- Report mismatches against intent, not personal preference.
- Distinguish missing behavior, incorrect behavior, and undocumented extra behavior.
- Treat drift as any material mismatch between intended and implemented behavior.
- Be explicit about what evidence supports each finding.

Output:
- list of mismatches
- rationale for each finding
- recommendation for code repair or intent revision
```

#### Example Prompt: Repairer

```text
You are repairing drift between implementation and AIM.
Your job is to restore alignment by changing code when implementation is wrong, or by recommending intent revision when the specification is outdated.

Rules:
- Prefer the smallest change that restores alignment.
- Do not silently redefine intent through implementation.
- If requirements changed, update intent before continuing repair.
- Preserve traceability between the fix and the intent it satisfies.

Output:
- repair changes
- explanation of what drift was corrected
- note on whether the intent remains valid or needs revision
```

---

## 2. Header And Identity

Every `.intent` source file must begin with exactly one declaration line:

```ail
AIM: <component>#<facet>@<x.y>
```

Example:

```ail
AIM: juice.games.snake#schema@2.1
```

### 2.1 Header Grammar

```regex
^AIM:\s+([a-z0-9]+(?:\.[a-z0-9]+)*)#(intent|schema|flow|contract|persona|view|event|mapping)@([0-9]+\.[0-9]+)$
```

Rules:

- `<component>` must be lowercase namespace segments separated by dots
- `<facet>` must be one of `intent|schema|flow|contract|persona|view|event|mapping`
- `<version>` uses the exact short form `x.y`

### 2.2 Exact Version Rule

Version matching is exact within a component.

- the intent envelope version is authoritative
- every included or co-located file for the same component must use the same exact `x.y` version
- AIM v2.1 does not define compatibility bands, major-only matching, or "version families"

---

## 3. Project Layout

### 3.1 Canonical Write Layout

Canonical authoring and materialization layout is nested.

Component sources:

- intent envelope: `/aim/<namespace segments>/<component>.intent`
- facet files: `/aim/<namespace segments>/<component>.<facet>.intent`

Mapping sources:

- mapping file: `/aim/mappings/<namespace segments>/<component>.mapping.intent`

Examples:

- `/aim/game/snake/game.snake.intent`
- `/aim/game/snake/game.snake.schema.intent`
- `/aim/game/snake/game.snake.contract.intent`
- `/aim/mappings/game/snake/game.snake.mapping.intent`

Generic filenames are never valid. These are invalid:

- `intent.intent`
- `schema.intent`
- `mapping.intent`

### 3.2 Compatibility Read Layout

Implementations may read flat legacy sources for compatibility:

- `/aim/<component>.intent`
- `/aim/<component>.<facet>.intent`
- `/aim/mappings/<component>.mapping.intent`

Compatibility rules:

- flat layout is read-compatible only
- tools should materialize and rewrite to canonical nested layout
- a project must not contain both flat and nested sources for the same component and facet

### 3.3 Single-Component Vs Multi-Component Projects

- single-component projects may be read from flat legacy layout
- multi-component projects must use nested layout
- the root `/aim` folder should contain component subfolders and, optionally, legacy single-component flat files only during migration

### 3.4 Path Derivation

Path-derived identity is used for validation.

For canonical nested layout:

- component is derived from the nested directory segments and filename
- facet is derived from the filename suffix

For flat compatibility layout:

- component is derived from the filename
- facet is derived from the filename suffix

The header remains the ultimate source of truth, but any path/header mismatch is a hard error.

---

## 4. File Structure

### 4.1 Shared Structural Rules

All AIM files share these rules:

- header line must be first
- constructs are brace-delimited
- lists use hyphen-led entries
- natural-language prose should be quoted
- no commas are required between entries

Minimal shared notation:

```ebnf
file          := header newline body
header        := "AIM: " component "#" facet "@" version
body          := construct*
construct     := block | assignment | list_block
block         := KEYWORD identifier? "{" body "}"
assignment    := KEYWORD ":" value
list_block    := KEYWORD "{" list_item+ "}"
list_item     := "-" value
identifier    := /[A-Za-z][A-Za-z0-9_]*/
value         := quoted_string | bare_token_sequence
```

This notation is intentionally minimal. Each facet section below narrows what top-level constructs are valid.

### 4.2 Allowed Top-Level Constructs By File Type

`facet=intent` files may contain:

- exactly one `INTENT`
- zero or one `INCLUDES`
- zero or one `DEPENDENCIES`
- zero or more `REQUIREMENT`
- zero or more top-level facet blocks of types `SCHEMA|FLOW|CONTRACT|PERSONA|VIEW|EVENT`

Standalone facet files may contain:

- one or more blocks of their declared facet type
- zero or one `DEPENDENCIES`
- zero or more `REQUIREMENT`

`facet=mapping` files may contain:

- one or more `MAP` blocks

Cross-facet mixing is invalid in standalone facet files. For example, a `#schema` file must not contain `FLOW` or `CONTRACT` blocks.

### 4.3 Intent Body Grammar

Inside `INTENT <Name> { ... }`, the following are valid:

- exactly one `SUMMARY`
- exactly one `REQUIREMENTS`
- zero or one `TESTS`
- zero or more embedded facet blocks of types `SCHEMA|FLOW|CONTRACT|PERSONA|VIEW|EVENT`

Embedded facet blocks are valid only inside `INTENT`.

### 4.4 Attribute And List Syntax

Attribute lines use this shape:

```text
<name>: <type> <modifier>*
```

Examples:

```ail
title: string required
humidityPct: integer optional min(0) max(100)
ownerId: string required ref(User.id)
```

List items use this shape:

```ail
- "Natural language statement"
- CALL ResolveUser
- VIEW TodoDashboard
```

---

## 5. Intent Envelope

The intent file is the canonical component entrypoint.

Hard minimum for validity:

- valid `AIM: ...` header with `facet=intent`
- exactly one `INTENT <Name> { ... }`
- one `SUMMARY` inside the `INTENT` body
- one `REQUIREMENTS` block inside the `INTENT` body with at least one item

Recommended:

- `TESTS`

### 5.1 Minimal Template

```ail
AIM: demo.todo#intent@2.1

INTENT TodoComponent {
  SUMMARY: "A simple personal todo tracker."
  REQUIREMENTS {
    - "User can add, complete, and delete todos."
  }
}
```

### 5.2 Extended Template

```ail
AIM: game.snake#intent@2.1

INCLUDES {
  contract: "game.snake.contract.intent"
  view: "game.snake.view.intent"
}

INTENT SnakeGame {
  SUMMARY: "A single-player snake game with persistent top scores."
  REQUIREMENTS {
    - "Movement is tick-based."
    - "Wall and self collision end the run."
  }
  TESTS {
    - "A collision ends the current run."
    - "Top scores persist across sessions."
  }

  FLOW AdvanceTick {
    SUMMARY: "Advances the game loop by one tick."
    TRIGGER {
      - "Invoked by the active game timer."
    }
    STEPS {
      - "Update head position from current direction."
      - "Detect wall collision."
      - "Detect self collision."
      - "Grow snake if food was consumed."
    }
  }
}
```

---

## 6. External Facets With `INCLUDES`

Intent files may link external detail files using `INCLUDES`.

Canonical form:

```ail
INCLUDES {
  schema: "game.snake.schema.intent"
  flow: "game.snake.flow.intent"
  contract: "game.snake.contract.intent"
  persona: "game.snake.persona.intent"
  view: "game.snake.view.intent"
  event: "game.snake.event.intent"
}
```

### 6.1 `INCLUDES` Validation

For each entry:

- key must be one of `schema|flow|contract|persona|view|event`
- value must be a relative `.intent` path
- resolution is relative to the including file's directory
- normalized resolution must remain inside `/aim`
- target file must exist
- target header must match:
  - the same component namespace
  - the same facet as the include key
  - the same exact version

### 6.2 Resolution Algorithm

For each facet, resolve effective content in this order:

1. external facet file referenced by `INCLUDES`
2. top-level facet blocks in the intent file
3. embedded facet blocks inside `INTENT`
4. facet absent

If a higher-precedence source exists, lower-precedence sources for that facet are ignored for synthesis and produce informational diagnostics.

### 6.3 Duplicate Rules

These are hard errors:

- duplicate effective source identities across flat and nested layout
- duplicate construct names within the effective source for the same facet
- multiple authoritative definitions for the same construct after precedence is applied

Multiple constructs of the same facet type are valid when their names are distinct. For example, one `SCHEMA` source may contain both `SCHEMA User` and `SCHEMA Session`.

### 6.4 No Implicit Discovery

Core AIM semantics do not auto-discover sibling facets beyond explicit `INCLUDES` and the intent envelope itself.

Implementations may provide opt-in convenience discovery, but that behavior is outside the core language.

---

## 7. Precision Facets

Detail facets are optional precision overlays. They make implementation, verification, and synthesis more deterministic but are not required for component validity.

### 7.1 Schema Facet

Purpose: data at rest and structural types.

Syntax:

```ail
SCHEMA <Name> { ... }
```

Common blocks:

- `SUMMARY`
- `ATTRIBUTES`
- `RELATIONSHIPS`
- `CONSTRAINTS`
- `IMMUTABLE`

`SUMMARY` is required.

### 7.2 Contract Facet

Purpose: externally observable execution guardrails and guarantees.

Contracts specify:

- accepted input
- authorization requirements
- preconditions
- postconditions and durable mutations
- returned results
- guaranteed emissions

Syntax:

```ail
CONTRACT <Name> { ... }
```

Common blocks:

- `SUMMARY`
- `INPUT`
- `AUTHZ`
- `EXPECTS`
- `ENSURES`
- `RETURNS`

`SUMMARY` is required.

### 7.3 Flow Facet

Purpose: internal orchestration for satisfying a contract or internal behavior.

Flows specify:

- internal control sequence
- branching and retries
- external provider calls
- error handling

Flows do not define the external guarantees of an operation. That belongs to `CONTRACT`.

Syntax:

```ail
FLOW <Name> { ... }
```

Common blocks:

- `SUMMARY`
- `TRIGGER`
- `STEPS`
- `ON_ERROR`

Common step keywords:

- `CALL`
- `EVALUATE`
- `BRANCH`
- `ITERATE`
- `AWAIT`
- `TRANSITION`

`SUMMARY` is required.

### 7.4 Persona Facet

Purpose: actor identity, role semantics, and view access.

Syntax:

```ail
PERSONA <Name> { ... }
```

Common blocks:

- `SUMMARY`
- `ROLE`
- `ACCESS`

`ROLE` and `ACCESS` are required. `SUMMARY` is optional.

### 7.5 View Facet

Purpose: shared interface surfaces and user-visible actions.

Syntax:

```ail
VIEW <Name> { ... }
```

Common blocks:

- `SUMMARY`
- `DISPLAY`
- `ACTIONS`

`SUMMARY` is required.

### 7.6 Event Facet

Purpose: asynchronous payloads, emissions, and routing.

Syntax:

```ail
EVENT <Name> { ... }
```

Common blocks:

- `SUMMARY`
- `PAYLOAD`
- `EMITTED_BY`
- `ROUTING`

`SUMMARY` is required.

### 7.7 Summary Rule

`SCHEMA`, `FLOW`, `CONTRACT`, `VIEW`, and `EVENT` must include `SUMMARY`.

`PERSONA` may omit `SUMMARY` when it acts only as a role/access declaration.

---

## 8. Dependencies, Requirements, And Mapping

### 8.1 Dependencies

`DEPENDENCIES` may appear in intent files and standalone facet files.

```ail
DEPENDENCIES {
  IMPORT {
    company.storage.Contract AS Storage
  }
  REQUIRES {
    Identity AS AssigneeUsers
  }
}
```

- `IMPORT` references concrete provider surfaces
- `REQUIRES` declares required capabilities by alias

If dependency declarations are distributed across files:

- resolve by union
- conflicting declarations emit informational diagnostics
- facet-local declarations take precedence for synthesis decisions in that facet

### 8.2 Requirement Surfaces

Required capabilities may be documented with `REQUIREMENT` blocks.

```ail
REQUIREMENT AssigneeUsers {
  SUMMARY: "Capability required to resolve user identities."
  OPERATIONS {
    - "ResolveUser(id) -> UserRecord"
  }
}
```

`REQUIREMENT` blocks describe what a required alias is expected to provide. They do not bind it to an implementation.

### 8.3 Mapping Files

Mappings live under `/aim/mappings` and use `facet=mapping`.

Example path:

- `/aim/mappings/company/billing/invoice/company.billing.invoice.mapping.intent`

Header:

```ail
AIM: company.billing.invoice#mapping@2.1
```

Example:

```ail
MAP AssigneeUsers {
  TARGET: "company.identity"
  OPERATION_MAP {
    - "AssigneeUsers.ResolveUser -> Identity.ResolveUser"
  }
}
```

or

```ail
MAP AssigneeUsers {
  TARGET: "ExistingCode.IdentityGateway"
  OPERATION_MAP {
    - "AssigneeUsers.ResolveUser -> ExistingCode.IdentityGateway.resolveUser"
  }
}
```

Unresolved required aliases remain hard errors.

---

## 9. Traceability

When the relevant detail facets exist, the intended chain is:

```text
Persona -> View -> Contract -> Flow / Schema / Event
```

Interpretation:

- `PERSONA.ACCESS` should reference `VIEW`
- `VIEW.ACTIONS` should reference `CONTRACT`
- `CONTRACT` may reference or imply `FLOW`
- `CONTRACT` and `FLOW` may read or mutate `SCHEMA`
- `CONTRACT.ENSURES` may guarantee `EVENT` emission

For intent-only components:

- strict chain enforcement is skipped
- validation and synthesis emit a reduced-fidelity informational note

---

## 10. Synthesis Tiers

- Tier 1: intent-only
- Tier 2: intent plus some facets
- Tier 3: intent plus full traceable facets

Tier affects:

- expected implementation and verification precision
- expected synthesis precision
- generated structural depth
- strictness of traceability checks

---

## 11. Registry And Materialization

### 11.1 Registry Package Catalog

Remote package discovery is defined by `registry/index.json`.

Each package object must include:

- `name`
- `version`
- `entry`

Package validity rules:

- `entry` must exist and end with `.intent`
- `entry` header must match `AIM: <name>#intent@<version>`
- a package directory must contain exactly one `#intent` source across recursive scan
- stale per-package manifests such as `package.json` and `manifest.intent` are invalid

### 11.2 Local Materialization Rule

Even when sources are fetched remotely, implementation, verification, repair, and synthesis must run against local project files under `/aim`.

Required behavior:

1. fetch the selected package entry and related facet sources
2. materialize them into local `/aim` using canonical nested layout
3. materialize mapping sources into local `/aim/mappings` using canonical nested layout
4. synthesize from local sources so users can edit and rebuild without refetching

---

## 12. Diagnostics

### 12.1 Hard Errors

1. Header and identity violations
- missing header
- header not matching grammar
- filename/path/header mismatch
- path-derived component not matching header component
- path-derived facet not matching header facet
- duplicate source identity across flat and nested layouts
- invalid nested source path shape
- generic filenames such as `schema.intent`, `event.intent`, or `mapping.intent`

2. Layout violations
- mixed flat and nested authoritative sources for the same component/facet
- multi-component project authored in flat layout

3. Intent minima missing
- missing `INTENT`
- multiple `INTENT` declarations in one intent file
- missing intent name
- missing `SUMMARY` in intent body
- missing `REQUIREMENTS` in intent body

4. `INCLUDES` violations
- invalid include key
- non-relative include path
- include path escaping `/aim`
- missing included file
- included file component/facet/version mismatch

5. Grammar violations
- invalid embedded facet key in `INTENT`
- invalid top-level construct for the file's declared facet
- malformed braces
- malformed attribute syntax

6. Effective source conflicts
- duplicate construct names within an effective facet source
- multiple authoritative definitions for the same construct after precedence

7. Unresolved required references
- unresolved `REQUIRES` alias in `CALL Alias.Operation`
- unresolved `REQUIRES` alias in `ref(Alias.Type)`
- missing provider or mapping for a required alias

8. Legacy metadata tokens in source files
- `:::AIL_METADATA`
- `FEATURE:`
- `FACET:`
- `VERSION:`

### 12.2 Informational Diagnostics

- missing optional `TESTS`
- no detail facets provided
- top-level facet overridden by external facet
- embedded facet overridden by top-level or external facet
- unresolved `IMPORT` alias
- narrative/detail conflict where detail authority wins

---

## 13. Execution And Synthesis Model

1. Discover the intent envelope for each component.
2. Validate the header and path identity.
3. Parse the intent envelope.
4. Resolve `INCLUDES`.
5. For each facet, choose effective content by precedence:
   - external include
   - top-level facet block in intent file
   - embedded facet block in `INTENT`
   - absent
6. Parse dependencies and requirement surfaces.
7. Load mappings from `/aim/mappings` when present.
8. Resolve required aliases.
9. Determine implementation and synthesis tier.
10. Use the resolved intent and facet set as the authoritative reference for implementation, verification, and repair.
11. Compare code, tests, and produced artifacts against the resolved intent and facets.
12. Repair mismatches by changing code when implementation drift is detected, or by revising intent when the specification is outdated.
13. Synthesize artifacts with tier-appropriate precision when synthesis is part of the workflow.
14. Apply traceability checks when the relevant facets exist.

---

## 14. Conformance Scenarios

Valid:

1. `AIM: juice.games.snake#schema@2.1`
2. `/aim/company/billing/invoice/company.billing.invoice.intent` with `AIM: company.billing.invoice#intent@2.1`
3. `/aim/company/billing/invoice/company.billing.invoice.schema.intent` with `AIM: company.billing.invoice#schema@2.1`
4. `/aim/mappings/company/billing/invoice/company.billing.invoice.mapping.intent` with `AIM: company.billing.invoice#mapping@2.1`
5. Intent-only component parses successfully.
6. Intent file with embedded `SCHEMA` only parses successfully.
7. Intent file with top-level facet blocks plus `INCLUDES` parses successfully.
8. External facet overrides top-level and embedded facet content for the same facet.
9. Top-level facet overrides embedded facet content when no external facet exists.
10. Remote package fetch materializes into nested local `/aim` and rebuilds locally.

Invalid:

1. `AIM: Snake-App#schema@2.1`
2. `AIM: juice.games.snake#data@2.1`
3. `AIM: juice.games.snake#schema@2.1.0`
4. `/aim/company/billing/invoice/schema.intent`
5. `/aim/company/billing/invoice/event.intent`
6. `/aim/mappings/company/billing/invoice/mapping.intent`
7. Flat and nested sources both present for `company.billing.invoice#schema`
8. Included file version differs from envelope version
9. Invalid embedded facet key such as `DATA`
10. Duplicate `SCHEMA User` definitions in the effective schema source
11. Unresolved `REQUIRES` alias

---

## 15. Practical Guidance

Default authoring rule:

- start with a single `<component>.intent` file
- keep facets embedded in that intent file by default
- split facets into separate files only when size, churn, reuse, or complexity makes the single-file form harder to understand or maintain

Typical reasons to split:

- the intent file becomes long enough that scanning it is materially slower
- one facet needs independent ownership or frequent editing
- a facet is reused or reviewed independently
- contract or schema stability matters enough to justify isolated files
- the component has enough precision detail that one-file authoring reduces clarity

This means AIM should be authored single-file first, then expanded into multi-file form only when that improves readability, maintainability, implementation discipline, or synthesis precision.

Use intent-only when:

- the component is simple
- requirements are still evolving
- speed matters more than strict precision

Add detail facets when:

- schema compatibility must be explicit
- externally visible operation guarantees must be stable
- internal orchestration must be deterministic
- persona and view traceability matters
- event emission or routing must be explicit

The intended AIM workflow is:

1. start from requirements and write or refine one intent envelope
2. add only the facets that increase useful precision
3. implement code and tests by reading the resolved intent and available facets
4. validate implementation and outputs against intent
5. repair drift by changing code or revising intent explicitly
6. keep authoring in canonical nested layout
7. rely on explicit `INCLUDES` rather than implicit discovery

Closed-loop summary:

- requirements -> intent
- intent -> implementation
- implementation -> validation against intent
- validation failures -> code repair or intent revision
