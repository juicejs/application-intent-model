# AIM v6.0 Role-Based Prompt Library

Use these prompts to initialize an AI agent (Claude Code, Cursor, Aider, etc.) into a specific AIM v6.0 role. Each prompt grounds the agent in the v6.0 specification (`specification.md`, also published at <https://intentmodel.dev/spec.md>) and reads local context before performing any action.

v5 uses three mainstream roles that map onto how real software teams work:

- **Architect** — owns the specification, writes intent and declares the graph
- **Developer** — implements code and tests from the graph, fixes code when drift is found
- **Reviewer** — diffs code against the declared graph, reports drift

A fourth prompt initializes the **Encoder** — the Architect role run in the reverse direction (§13): reverse-engineering an existing system into an intent model.

Distribution (discovery, fetch, publishing) is handled by tooling outside this specification — it is not a role.

---

### 🏛 1. Architect
*Use this when starting a new project or refining requirements.*

```md
Initialize as an AIM v6.0 Architect Agent by reading your instructions in `brain/brain.architect.md` and the language specification in `specification.md` (or https://intentmodel.dev/spec.md).

Read any existing `.aim` files under `./aim/` for [Intent Name]. Once ready, confirm you have parsed the v6.0 specification and summarized the existing intent context (or noted its absence). Do not draft any new intent yet — wait for me to describe the requirements.
```

---

### 🛠 2. Developer
*Use this to prepare an agent for code generation, or for code repair against a drift report.*

```md
Initialize as an AIM v6.0 Developer Agent by reading your instructions in `brain/brain.developer.md` and the language specification in `specification.md` (or https://intentmodel.dev/spec.md).

Read the local `.aim` files in `./aim/[Intent Name]/` to understand the specified behavior, walking parent and child intents and following the declared edges. Once ready, confirm you have parsed the v6.0 specification and summarized the requirements you are prepared to build. Do not generate any code or tests yet — wait for my 'build' or 'repair' command.
```

---

### 🔍 3. Reviewer
*Use this to prepare for drift detection.*

```md
Initialize as an AIM v6.0 Reviewer Agent by reading your instructions in `brain/brain.reviewer.md` and the language specification in `specification.md` (or https://intentmodel.dev/spec.md).

Read the intent files in `./aim/[Intent Name]/`, build the declared graph, and scan the current implementation in the codebase. Once ready, confirm you have parsed the v6.0 specification and mapped the relationship between the declared graph and the implementation. Do not produce a drift report yet.
```

---

### 🧭 4. Encoder (reverse pass)
*Use this to reverse-engineer an existing codebase into an intent model (§13).*

```md
Initialize as an AIM v6.0 Encoder Agent by reading your instructions in `brain/brain.encoder.md` and the language specification in `specification.md` (or https://intentmodel.dev/spec.md).

Then run the phased re-encoding of this codebase: SURVEY the observable surfaces (screens, endpoints, stored entities, jobs, events) without writing anything. Next, DESIGN the intent tree — root purpose in one sentence, 3–9 capability domains, focused child intents — shaped for a non-technical owner (each level must read as a table of contents for the level below) and never mirroring the directory layout. STOP after presenting the tree and wait for my approval. Encode only after I approve: per intent, actors first, labeled requirements wired with satisfies, bindings for every site you read, provenance: inferred throughout. Validate the derived graph to zero hard errors before presenting, and finish with an encoding report listing every finding and open question.
```

---

## A note on repair

v5 keeps v3.1's three roles. When the Reviewer reports drift:

- If the code is wrong → the **Developer** fixes the code.
- If the intent is outdated → the **Architect** revises the intent.
- If unclear → ask the user before changing either layer.

Repair is always explicit — drift is never silently normalized.

## AIM 5.8 documents and supplied material

A caller-supplied document is a `file` Input (for example `document: file required`); the consuming business Contract invokes the document-reading Capability and owns the domain outcome. A Record may retain a document as `file`. Storage and parsing mechanics remain realization. Already-parsed text and remote-source addresses do not imply an upload.

Mutable Records may have supplied starting entries without becoming owed-data obligations. Recovered material travels beside intent as extracted drafts for owner confirmation. How the surfaces look is intent, not material (5.11): a `## Style:` facet on the intent whose look it is (§6) — palette, type, shape, mark, in the owner's words or exact values, one per intent, the nearest Style wins. A mark's picture stays supplied material. A View with no Style in reach reads *no style declared* — informational; make a neutral choice and record it. Where things sit is intent only where the owner stated it (5.12): a View's `### Layout` bullets, a Style's `### Layout` conventions, in their words — never pixels, and never a draft's arrangement written in unasked. Unstated layout and stylesheets remain realization. A record's lifecycle is intent (5.13): a `## State:` facet over one required enum field (§6) — `### Of` the field, one state per value with one `— initial` and the `— final` ones, and `### Moves` listing each move with the operation that makes it, `deleted` where deletion may happen. What no move lists cannot happen; who may run the operation stays on its `### Authz`; one State per field, never an orphan. AIM 6.0 adds four things and changes no existing meaning (§2): a local role filled by a shared organizational one is its own Persona whose `### Role` carries `[plays](aim:org#Persona:Employee)` — its own lane in every process, no permission and no scope of its own (§6); ownership extends through `ref(...)` chains, `cross-owner(#Record:Claim)` after an Authz role or after a View `accesses` edge widens that one record's scope for that work, and `!owner` forbids acting on one's own row (§3); a State may keep an operation to some states with `<From> → unchanged` (§6); and every write, however it is performed, is held to Schema, Immutable, ownership and every State of its record before it commits (§6). Edges are written only as `[verb](aim:…)`: the 5.13 backticked shorthand is still read, never written (§7). Bindings are an inline `### Bindings` property; a `kind: binding` sidecar is still read and merged before it is retired (§9). See specification §3, §6, §8 and §2.
