# Agentic Intent Model (AIM) v6.4

This revision says the language once: the specification is rewritten into thirteen sections, a third of its former length, and a model valid under 5.13 is valid 6.0 as it is. It adds four commitments — a local role that `plays` a shared one, ownership through `ref(...)` chains with `cross-owner(...)` and `!owner`, in-state guards (`→ unchanged`), and every write held to Schema, Immutable, ownership and State. See [the 6.0 proposal](./proposals/6.0-language-revision.md) for what changed and where each 5.13 section went.

*Formerly "Application Intent Model" — renamed when the language generalized beyond software.*

AIM is a specification language for humans and AI agents. It captures the **intent** of a system — an application's behavior, a business process, an organization's commitments — in structured `.aim` files that agents read once, realize, review against, and repair over time — replacing the sprawl of PRDs, SOPs, design notes, and plan files that otherwise hold intent hostage in prose. Software was AIM's first domain and remains its most worked example; nothing in the language is specific to it.

**This repository is the specification itself** — the language, its reference examples, and the role prompts. Tooling, the package catalog, and publishing live in separate repositories.

---

## What's new in 6.4

From the NASA example set beside BPMN 2 and DMN: three real processes — lifecycle gates, a launch countdown, anomaly resolution — each had a place where the language ran out. 6.4 fills them the AIM way: no new verb, every fill a property of a construct that exists, and one behaviour where two realizations could otherwise differ. A model valid under 6.3 is valid 6.4. See [the 6.4 proposal](./proposals/6.4-flow-constructs.md).

- **What a case is.** One run of one process. A case keeps its Events in one order; a wait hears every Event of its case since it began, so an Event that came early is taken when the wait is reached. A child case ends with its parent.
- **Races.** A step waiting on several Events takes whichever comes first; `— continues: OfferAccepted` says which go on.
- **What ends a case.** `### Ends on` lists the Events that end the case wherever it is; a deadline with `### Ends` interrupts the case, runs its cleanup and ends it — and a cleanup that does not finish stays visible, never silent.
- **A step over a collection.** `— for each [launch#Record:Countdown.stations] as station` runs the step once per item, together or `in order`; the next step is the join.
- **Timed waits.** `— after: 10 business-days` or `— until [launch#Record:Countdown.resumeAt]` delays a step, in the case's time zone and working days.
- **Criteria as rules.** `### Criteria` beside `### Decides` states the decision as first-hit rules over the operation's inputs, with a required `otherwise`.

## What's new in 6.3

From Amy's Studio, where an owner wrote "we have a shipping department" and got a process, and from writing a whole organisation (NASA) in the language. A model valid under 6.2 is valid 6.3; the renamed spellings are still read and are rewritten when a model is opened. See [the 6.3 proposal](./proposals/6.3-four-facets.md).

- **Four facets, one meaning at any level.** `## Organisation:` (a group that acts as one), `## Project:` (a goal with an end; it never performs), `## Software:` (software described here) and `## Service:` (a system consumed through a connection). A department is an Organisation at the root or three levels down; nesting says where a thing is described, nothing more. Each stays a facet until it earns an intent of its own.
- **Process and Operation.** `Flow` is renamed `Process` and `Contract` is renamed `Operation` — the words owners, BPMN and automations already use. The old spellings stay readable everywhere they are written.
- **A Capability is a function.** Named by what it does (`DDEXGenerator`), never by a vendor; a Service, a Software or a library answers it.
- **A process before its steps.** A Process with only a Summary is a named process, not yet worked out.
- **Where a rule comes from.** A requirement may end with `— from [shop#Knowledge:AGB]` or `— from: customers complained, 2026-10`, so a changed source flags the rules drawn from it.

## What's new in 6.2

From a real owner's first session (a packaging manufacturer modelling its company) and a consistency review of 6.1. A model valid under 6.1 is valid 6.2; old spellings are still read and are rewritten in full when a model is opened. See [the 6.2 proposal](./proposals/6.2-labels-knowledge.md).

- **Owners read their own words.** Names stay ASCII identities; a `### Label`, a field's `label("Länge in mm")` and enum value labels (`InPruefung "In Prüfung"`) carry the spelling people read.
- **Knowledge.** A new facet for what the running work consults to decide — a handbook, a regulation, past correspondence — reached with the new verb `consults`. A Capability is now what the work calls; it may be named by the system the owner chose (`SAP`).
- **One full address per thing.** Every reference names its intent, inside its own intent too. A promoted Record, Persona or process *is* its intent (`company.kunde`, `ref(company.kunde#id)`); promoting or moving rewrites every reference, and no alias keeps an old address alive. An intent is an edge endpoint by what it holds: a Schema makes it data, a Role an actor, Steps a process. Imports are gone.
- **Clearer processes.** A State's `### Only in` says which operations run only in which states (replacing `→ unchanged`). A deciding step says which outcomes continue (`— continues: Machbar, Sonderzuschnitt`). A subscription inside Steps waits for that case's Event. A deadline belongs to its case and restarts when its anchor repeats.
- **Moves never approve.** Moving unconfirmed intent into a confirmed one is a change that says it confirms it.
- **Calendar and clock.** `timezone` and `calendar` on the root say which time zone and which working days every schedule and deadline counts.

## What's new in 6.1

**Parts.** A field can hold one structured value inside its holder — a build's result, a project's GitHub link — as `part(<Record>)`, and several as `list(part(<Record>))`. Before, AIM could only point at a row elsewhere (`ref(...)`), so such fields were written `object` and read as text. A part is checked against its Record's fields, refuses keys the Record does not name, and derives a `holds` edge. Values keyed by run-time text — a sha per file path, a price per currency — are `map(<type>)`; values keyed by rows — a quantity per product — are `map(ref(Product.id), integer)`, with each key a checked reference. Nothing existing changes meaning. See [the 6.1 proposal](./proposals/6.1-parts.md).

## What's new in 6.0 — and why it matters

**The whole language, said once.** An agent reads the specification before it writes or checks a model — in practice, on every turn. 5.13 had grown to 221 KB and 34,000 words: the history of every release, tutorials, before/after demonstrations, and the same rule stated in several places. 6.0 says the same language once, in thirteen sections, about 11,400 words and 74 KB. In Amy, the prompt an agent reads per decision shrank to well under half. Less to read is less to contradict, and every rule now has one home.

**Nothing to migrate.** A model valid under 5.13 is valid 6.0, read as it is (§2). The 5.13 edge shorthand and binding sidecars are still read; they are simply no longer written.

**Four things a model can now say that it could not before.**

1. **A process keeps its own roles, filled by the organization's people.** The Submitter and the Approver of a claim are two roles with two lanes and two sets of permissions — and both are employees. Each local role now names the shared one it is filled by, without merging them and without a second "Employee" (§6):

   ```markdown
   ## Persona: Approver

   ### Role

   - Approves expense claims — [plays](aim:org#Persona:Employee)
   ```

2. **Privacy that reaches what it should, and no further.** `owner` marks whose row it is, and a row that references a private row is private too — the lines of a claim are as private as the claim. Two modifiers state the exceptions exactly: `cross-owner(...)` lets one role act on other people's rows of one record, for one operation or one screen; `!owner` forbids acting on one's own (§3). "Approvers approve other people's claims, never their own" is one line:

   ```markdown
   ### Authz

   - `#Persona:Approver` cross-owner(#Record:Claim) !owner
   ```

3. **A record's lifecycle can protect the rest of the record.** A State already said how the status may move. Now it can also say when the other fields may change (§6):

   ```markdown
   ### Moves

   - Draft → Submitted — [Contract:SubmitClaim]
   - Draft → unchanged — [Contract:EditClaim]
   ```

   `EditClaim` may change the claim only while it is a draft.

4. **Every write is held to the model.** However an operation is performed — code, an automation, an AI interpreter — each change it makes must satisfy the schema, the immutable fields, ownership and every State of its record before it commits (§6). The model is no longer advice the realization may skip; it is the check every write passes.

**Types that mean what they say.** `integer`, `decimal`, `email`, `url` and `phone` join the scalar types, each with the values it admits, and every realization checks them before storing. A field that names another record is a reference — `owner: ref(Member.id)` — and that row must exist (§3).

**Every facet reads as an extension.** Each of the ten facets — Record, Contract, Flow, Persona, View, Event, Trigger, Capability, Style, State — is one self-contained block with the same parts: Purpose, Form, Example, Edges, Rules, Diagnostics and Since (§6). A new facet arrives the same way, with its example and its diagnostics, so the language can grow without anyone rereading the rest.

**Tools can trust each other's output.** A tool that reads a model and writes it back must keep every node, rule, edge, modifier, dependency, binding and authority field, and must not rewrite a file when anything would be lost (§3, *Preservation of meaning*). Models move between editors, agents and repositories without silently losing meaning.

See [the 6.0 proposal](./proposals/6.0-language-revision.md) for the complete list of changes, the editorial decisions, where each 5.13 section went, and the questions still open.

---

## Why AIM

- **Ground agents in explicit, versioned intent** instead of loose chat context that evaporates between sessions.
- **A reviewable contract between intent and reality.** `.aim` files are normally agent-authored from a human's narration, but a small model is something a human can read, correct, and diff — and a Reviewer can check reality against (code, configurations, execution logs) — far more cheaply than inspecting the realization itself.
- **A relation graph, not just a tree.** AIM treats every `.aim` file as a projection of a node-and-edge graph: a View *exposes* a Contract, a Flow *mutates* a Record and *emits* an Event. That graph is derived, traversable, and checkable.
- **Drift as graph-diff.** With optional intent↔realization bindings, review becomes a diff between the declared graph and the realized graph — recovered from code for software, from logs and configurations for processes.

AIM pays off when reading the model is meaningfully easier than inspecting the realization. For trivially small or throwaway work, acting directly is the right call.

---

## The graph foundation (the v4 break)

v4 was the breaking change from v3.1 that founded the language on a graph; v5 generalized it beyond software and finished the naming; 6.0 says it all once (spec §4). The three shifts:

1. **Graph-founded model.** The `.aim` Markdown file is a *projection* of an underlying node-and-edge graph. Every heading is an addressable node.
2. **Typed edge taxonomy.** One CommonMark-native token — `[verb](aim:<address>)` — replaces v3.1's inconsistent prose cross-references. Dangling references, orphan nodes, and impact sets fall out for free, and the traceability chain becomes *computable* rather than aspirational.
3. **Intent↔realization binding layer.** An inline `### Bindings` property on each node (with its own `provenance`; deprecated `kind: binding` sidecars still accepted) maps intent nodes to their realization sites — in code, in systems, in automations — turning drift detection into a graph-diff.

Migrating from v3.1: see Section 13 of the [5.13 specification](https://github.com/juicejs/application-intent-model/blob/5e09691/specification.md) — 6.0 keeps release history in [proposals/](./proposals/) instead of the specification.

---

## File format at a glance

```markdown
---
aim: nemicko.demo.todo
kind: intent
---

# TaskManager

## Summary

A personal task manager.

## Requirements

- Users can create and complete tasks.

## View: TodoDashboard

### Summary

The owner's task-list surface.

### Actions

- Submitting the "New Task" form — [exposes](aim:nemicko.demo.todo#Operation:CreateTodo)
```

The `[exposes](aim:nemicko.demo.todo#Operation:CreateTodo)` token is a typed edge: `View → exposes → Operation:CreateTodo`. Collect every such token across a project and you have the relation graph.

Worked examples ship with the spec:
- [examples/nemicko.demo.todo.aim](./examples/nemicko.demo.todo.aim) — a complete intent in a single file.
- [examples/helpdesk/](./examples/helpdesk/) — a multi-file app (an intent tree, a mapping, and a binding file) whose graph spans files, exercising **every** facet and the closed verb set end to end. Start with its [README](./examples/helpdesk/README.md) for the rendered graph.
- [examples/documents/](./examples/documents/) — document import (5.8); [examples/performers/](./examples/performers/) — who does the work and who may (5.10).
- [examples/nasa/](./examples/nasa/) — an Artemis mission from formulation to flight, against **6.3**: an organisation at depth with a directorate that decides, a mission as a project holding three processes, mission control as software with parts, and the Deep Space Network described at JPL and consumed by mission control as a service. Its [README](./examples/nasa/README.md) lists what writing it found; `6.4/` beside its tree holds the countdown in 6.4 form with eleven acceptance scenarios.
- [examples/club/](./examples/club/) — a sports club, against **6.3 and 6.4**: the smallest organisation everyone knows, half the size of NASA, reaching every construct of the two proposals — a member who is a Persona and a Record, a tournament as a project, the member app as software and as the service a department consumes, and three processes with a race, `Ends on`, deadlines that end the case, a child case per member, timed waits and criteria rules. Start with its [README](./examples/club/README.md).

---

## The roles

1. **Architect** designs the intent graph from a human's narration and serializes it as `.aim` files.
2. **Realizer** makes reality match the model — a development team, an automation, an agent performing a process — and keeps bindings current. (In software this role is the **Developer**, and the shipped prompt templates use that name.)
3. **Reviewer** diffs reality against the declared graph and reports drift — explicitly routed to a realization fix (Realizer) or an intent revision (Architect).

---

## Render `.aim` files as Markdown on GitHub

Drop a `.gitattributes` file at your repo root:

```gitattributes
*.aim linguist-language=Markdown
*.aim linguist-detectable=true
```

GitHub will render `.aim` files as Markdown — frontmatter, headings, lists, and the edge tokens as clickable links.

---

## Repository contents

- **[specification.md](./specification.md)** — the authoritative AIM v6.4 language spec.
- **[AGENTS.md](./AGENTS.md)** — the reference project-bootstrap file (cold-start entry point for any AI coding agent).
- **[PROMPT.md](./PROMPT.md)** — role-based prompts for any AI assistant.
- **[agents/](./agents/)** — Architect, Developer, Reviewer, and Encoder persona files.
- **[brain/](./brain/)** — the shared and per-role operating-brain instructions.
- **[examples/](./examples/)** — conformance examples: a single-file intent, the multi-file [helpdesk](./examples/helpdesk/) app, [documents](./examples/documents/) and [performers](./examples/performers/), and the two organisation-scale examples against 6.3 and 6.4, [nasa](./examples/nasa/) and [club](./examples/club/).
- **[.claude-plugin/](./.claude-plugin/)** + **[skills/amy/](./skills/amy/)** — Claude Code plugin **Amy**: one auto-invoked skill that reads the task and enters the right mode, plus the mode subagents from [agents/](./agents/).
- **[GEMINI.md](./GEMINI.md)** + **[gemini-extension.json](./gemini-extension.json)** — Gemini CLI extension **Amy**: one assistant that reads the request and enters the right mode (Architect / Developer / Reviewer / Encoder).
- **[codex/prompts/amy.md](./codex/prompts/amy.md)** — OpenAI Codex `/amy` prompt; Codex also reads [AGENTS.md](./AGENTS.md) automatically, so an AIM project self-bootstraps with no install.

---

## Meet Amy

**AIM is the language; Amy is the assistant who speaks it.** You don't pick a role from a menu — you talk to Amy and she enters the right mode herself: design the intent, build code from it, review code against it, or reverse-engineer an existing codebase into an intent model.

- **Claude Code** — add this repo as a plugin marketplace, then install Amy:
  ```
  /plugin marketplace add juicejs/application-intent-model
  /plugin install amy@intentmodel
  ```
  Amy auto-invokes whenever you work with `.aim` files or ask to model, build, review, or capture a system.
- **Gemini CLI** — install the extension from this repo:
  ```
  gemini extensions install https://github.com/juicejs/application-intent-model
  ```
- **OpenAI Codex** — drop [codex/prompts/amy.md](./codex/prompts/amy.md) into `~/.codex/prompts/` for a `/amy` command. In any project with an `AGENTS.md` (AIM ships one), Codex picks up the model automatically even without it.

Any other agent: point it at [AGENTS.md](./AGENTS.md) and the spec at <https://intentmodel.dev/spec.md>.

---

Current spec: **AIM v6.4**

Built by **[Juice d.o.o.](https://juice.com.hr)** · MIT License
