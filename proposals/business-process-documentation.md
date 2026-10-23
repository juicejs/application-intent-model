# Proposal for business process documentation in AIM

Status: **Draft for discussion** · Date: 2026-10-22 · Baseline: the working AIM 5.13 specification, including the admitted State facet · Version: unassigned

## Recommendation

Adopt AIM's existing process vocabulary now, and agree a focused set of standard clarifications before tools give its declarations different meanings. Business process documentation is a complete outcome: people can understand, agree, maintain and review their work without planning to automate it.

The first increment adds no facet, verb, schema grammar or model type. It clarifies documentation outcomes, human work, model precision, discovery and evidence. Amy can improve its authoring and projections using existing constructs in parallel. Two deeper questions remain separate language-design work: incomplete state machines and a portable observational model that does not assert policy. Neither should acquire accidental semantics through an Amy-specific tag.

This proposal builds on [State in 5.13](./5.13-state-facet.md). It preserves that facet's complete-list semantics and does not revive the earlier nested Lifecycle proposal. The standard's existing working changes are the baseline, not changes made by this proposal.

## What the standard already supports

The [specification](../specification.md) already supplies most of the language needed:

| Business concern | Existing AIM representation |
|---|---|
| Purpose and policy | Summary, Requirements and `satisfies` links; §6, §8, §18 |
| Activities and order | Flow steps and promoted processes; §7.3 |
| Human work | Manual steps; performing Personas and their `invokes` links; §7.3–§7.4 |
| Permission | An operation's Authz; separate from its performer; §7.4 |
| Alternatives and exceptions | Decides, outcome continuations and On Error; §7.2–§7.3 |
| Business information | Records, schemas, inputs and outputs; §7.1–§7.2 |
| Lifecycle | State over a Record's enum field; §7.9 |
| Announcements and deadlines | Events and Triggers; §7.6–§7.7 |
| External resources | Capabilities and bindings to forms, systems and workflows; §9–§10 |
| Ownership and confirmation | Existing frontmatter and encoding provenance; §3.2, §17 |
| Progressive precision | Levels 1–3, with bindings optional at Levels 1–2; §10.3, §11.2 |

The [refund example](../examples/performers/aim/refunds/refunds.aim) already demonstrates a business process with human performers and no application View. It also establishes an important constraint for every new example: since 5.10, a step's wording does not declare its performer. The Persona's edges do; unassigned work can inherit a Flow's declared performer.

## Problems to resolve

The user need is to document work across people and systems, often through interviews, before all exceptions are known. Useful questions include who approves, what a handoff delivers, what a status means and what happens when the normal path fails. Answers need not include API routes, database identifiers or automation providers.

Four points in the present standard need attention:

1. **Documentation is supported, but some guidance assumes eventual automation.** Section 18 calls an unbound manual step “precisely, the digitalization backlog.” Section 17.5 explicitly permits legitimately unbound manual steps. A manual process may remain the desired result indefinitely.
2. **Precision can be mistaken for readiness.** Section 11.2 describes levels largely through implementation and code generation. More bindings do not establish that the business process is complete, executable or enforced.
3. **Closed declarations are easy to create too early.** A State is a complete move list. An omitted move is forbidden, even in a file marked `status: draft` or `provenance: inferred`. Decides likewise asserts exhaustive outcomes. Neither construct means “the possibilities discussed so far.”
4. **Observed practice and intended policy can disagree.** An interview may reveal that payment sometimes precedes approval. Confirming that the interview was recorded accurately is not an instruction to permit that behavior. The normative graph and its provisional authority make that distinction consequential.

There is also a specific consistency correction: §18 still describes a step's opening Persona as a performer declaration. That sentence predates the edges-only rule in §7.3–§7.4 and should be updated with this work.

## Proposed standard wording

The following passages are proposed additions or replacements, not current normative text. Section numbering follows the working 5.13 specification.

### Documentation as an outcome

Add to §18 after the opening explanation of an organization as realized intent:

> **Documentation is a complete outcome.** A model may exist to explain, agree, maintain or review how people work. Its usefulness and completeness are assessed against that stated purpose and scope. No intention to generate software or execute the process is implied. A manual process may remain manual indefinitely. Authoring tools MUST NOT demand application screens, runtime connections, deployment or automation configuration solely to complete a documentation task.
>
> Facets are introduced when the known commitments warrant them. An author MUST NOT invent information fields, performers, decisions, lifecycle moves or implementation details to satisfy a tool's execution requirements. Questions about the work remain questions until their owner answers them.

Replace the last sentence of §18's “Siblings may be different kinds of thing” paragraph:

> A process step with no system edge or binding may be intentionally manual. It becomes a candidate for digitization when the owner seeks that outcome; its absence of automation is not itself a gap in the process model.

### Business meaning of existing facets

Add to §7.1:

> A Record can describe information retained in a business case, a paper form or an existing document. Declaring it does not prescribe a database table, generated identifier or storage service. Its schema states the information and constraints the process actually needs. A separate Record is not required for every noun mentioned in a process.

Add to §7.2:

> A Contract can describe a human activity, such as approving a request or checking a receipt. Its inputs, permission, preconditions and guarantees remain business commitments. The declaration does not imply an API endpoint. A simple manual action may remain a Flow step; a distinct operation becomes useful when it needs its own performer, decision, guards, information relations or State move reference.

Replace the stale performer example in §18:

> “The Accountant may post” is permission, expressed in the operation's Authz. “The CFO approves the budget” is performance, declared by the CFO Persona invoking the approval operation, or through the Flow performer inheritance rules in §7.4. The step's prose explains that assignment to people; it does not declare it.

### Precision and review claims

Add to §11.2:

> Specification level describes structural precision and traceability. It does not measure business completeness, ratification, execution readiness or enforcement. A Level 1 or Level 2 model may fully meet an agreed documentation purpose. A Level 3 model may still contain unanswered business questions or have no automated execution environment.

Add guidance to §12:

> Tools SHOULD distinguish malformed declarations, unanswered business questions, review evidence and requirements of a requested realization. Missing automation infrastructure is not a defect in a documentation outcome. A structural check reports only the scope it checked; it MUST NOT present an untraced path as verified or infer that all cases terminate from the absence of findings.
>
> This distinction does not waive any declared constraint, reference error, performer conflict or contradiction. Existing binding requirements and the legitimate exemptions in §17.5 retain their meaning.

These are reporting distinctions, not new levels, persisted lifecycle states or alternate interpretations of the model. Tool-specific codes and user interface wording remain outside the language.

### State in a human process

Add to §7.9:

> A State may describe the lifecycle of a business case handled by people. A move's Contract or Flow can be human-performed; its `mutates` relation states that it changes the governed business information, without prescribing a storage implementation. The same move restrictions apply to human and automated realizations.
>
> A diagram shows the declared policy. It does not establish that real work followed that policy or that software enforces it. Review of human work uses available evidence and the confidence rules of §12.3 and §17.4. An automated realization that commits changes to the governed field must enforce the declared restrictions at its write boundary, as specified above. Tools MUST distinguish a declared policy, evidence of conformance and automatic enforcement.

The initial state, finality, enum correspondence, move operations and deletion rules remain exactly as admitted in 5.13. Creation requires no move; declaring no deletion moves makes no claim about deletion. A documentation task therefore does not require inventing a creation or deletion operation.

### Discovery without accidental prohibitions

Add to the authoring guidance in §1.2 and cross-reference it from §7.9:

> An Architect MUST NOT serialize an incomplete list of discovered possibilities as an exhaustive declaration. In particular, `status: draft` and `provenance: inferred` do not relax the semantics of State or Decides. If the owner has not established an exhaustive lifecycle, retain the known information and positive commitments using existing Records, requirements and operation prose, and retain unresolved questions in the authoring environment or a linked work artifact. Do not emit a partial State as though it were complete.

For example, when the owner has established the complete set of statuses as Submitted, Under review, Approved and Rejected, an enum may inventory those values while the handling of withdrawal remains unknown. Without a State facet, this enum asserts no move policy. A tool can show its values and the related documented operations; it must not draw guessed moves or label missing arrows “forbidden.” If the status inventory itself is incomplete, retain the discovered possibilities in prose or discovery material rather than declaring an exhaustive enum. Once the owner agrees the full lifecycle, the State facet makes those restrictions explicit.

This approach preserves useful discovery under existing syntax. It does **not** provide a machine-readable partial transition graph. If users need that graph to travel between tools, a separate extension is required; see the admission conditions below.

### Evidence and policy acceptance

Add to §17.1–§17.3:

> An encoding workflow MUST distinguish confirmation that an observation or testimony was recorded accurately from acceptance of a commitment as the model's intended policy. A faithful report of a policy violation is not approval of that behavior. Contrary observations and their sources belong in the encoding or drift report; accepted commitments remain in the normative model. Ratifying an inferred intent accepts its commitments, not merely the accuracy of a transcript.
>
> Recovered `.aim` declarations remain provisionally authoritative under §17.3. A workflow that needs observations to carry no normative authority must keep those observations in its evidence material until it proposes an intent. Neither `status: draft` nor a project-specific metadata key turns an inferred AIM graph into a descriptive-only graph.

Use the existing `owner`, `provenance`, `status` and `approved_by` fields for their defined purposes. Do not introduce a second approval system, place interview annotations inside Requirements, or identify the file maintainer as the process performer. The hosting environment retains source dates, testimony and review history; no particular storage product is required.

## Effect on charts and tree shaping

These are adoption recommendations grounded in §2, §7 and §18. They do not mandate Amy's tab names or layout in the standard.

| Projection | What it should help a person understand | Meaning it must preserve |
|---|---|---|
| Process | Activities, sequence, alternatives, handoffs and outputs | Lanes use declared performers; permission is shown separately. Human steps remain visible. |
| States | Where a case can start, move and end | Draw the actual State values and moves. Show an incomplete discovery inventory as an inventory, not a complete machine. |
| Information | Forms, documents and other records needed or produced | Business information does not imply a software database. |
| Purpose and impact | Which rules justify work and what a change affects | Links remain tied to canonical model nodes and the selected model version. |

For a request awaiting approval, the process chart may show a clerk registering it and a manager reviewing it. The State chart shows Submitted → Under review → Approved or Rejected. The two are connected through the operations named by the State moves. Who may perform a move comes from Authz; who performs the work comes from §7.4. They are not interchangeable.

The tree follows business purpose and meaningful capabilities or phases. A small process can stay at the root. Larger ones can expose request intake, review and fulfillment when each has earned its own commitments and operations. Shared roles and information have one canonical home. Do not introduce one child intent per activity, state or department merely to build navigation.

Under 5.13, the State facet has an address; its individual states are named entries within it. A UI may display those entries as expandable rows, but must not present them as newly addressable AIM nodes. Reshaping preserves the facet's Of reference, move-operation references and commitments under §16.

## Core priorities for documentation and later automation

For documentation, prioritize purpose, responsibilities, handoffs, decisions, states, information, deadlines, exceptions and unresolved questions. Most already have a representation. Ownership and confirmation reuse existing metadata; evidence remains separate from the behavioral model.

When automation is requested, establish the additional commitments needed for the selected scope: which case an event concerns, which attempt a response belongs to, what waiting means, when a deadline ends work, how duplicate requests affect business outcomes, and what happens after partial or uncertain completion. State restrictions, permissions and related-record conditions must survive that transition.

Some of these can matter in a manual process too. “Pay once per approved claim” is already a business commitment; a transaction key or retry mechanism is a realization choice. Their relevance follows the owner's work, not a binary manual/automated classification. This proposal adds no automation constructs and does not pre-approve a future extension.

## Compatibility and delivery

**Standard clarification first where meaning is at stake; adoption now where meaning is settled.** No existing AIM model is rewritten, no model gains a State by inference, and no tag changes declaration semantics. The immediate package adds no grammar. Its authoring and reporting requirements do affect tools that currently treat documentation as preparation for execution.

If accepted, delivery is:

1. Apply the proposed clarifications to `specification.md`, resolve the release version, and correct §18's stale performer wording. The draft assigns no version number.
2. Align `agents/aim-architect.md`, `agents/aim-encoder.md`, `agents/aim-reviewer.md` and their `brain/` counterparts; review `PROMPT.md`, `AGENTS.md`, `README.md` and `skills/amy/SKILL.md` for the same assumptions. Keep implementation mechanics in Realizer guidance.
3. Add a focused process-documentation example using only admitted syntax: human actions, explicit performers, a business Record, a complete State and a refusal outcome. Accompany it with a separate report showing an earlier discovery snapshot, when a lifecycle question was still unresolved, and how the owner's answer informed the completed model. Record any observed deviation separately from that accepted policy. The report must not become a competing behavioral authority.
4. Adopt in Amy: business-language elicitation, visible manual steps, linked process/State/information views, questions for the process owner, and separate statements about model quality and execution. Verify import, export, editing and reshaping preserve the declarations. Runtime implementation changes belong in Amy's repository.

The [contribution process](../CONTRIBUTING.md) calls for an issue and acceptance before specification edits. This file supplies the local proposal requested for that discussion; it does not amend the specification or publish an issue.

### Acceptance scenarios

These are proposed acceptance criteria, not tests reported as passing.

| Scenario | Required outcome |
|---|---|
| A manager describes a process performed entirely by people | A useful model with no fabricated app, database, deployment or provider requirements |
| A human step inherits its Flow's performer | It stays visible and uses the declared performer rules |
| A step names a manager only in prose and has no declared or inherited performer | No inferred assignment; the missing declaration remains a question |
| An operation allows two roles but only one performs it | Process lanes and permissions remain distinct |
| A complete State describes a paper request's lifecycle | The same declared moves and restrictions appear as in a software model |
| Withdrawal has not been discussed | No fabricated move, finality or prohibition; no partial exhaustive State is published |
| An existing State omits withdrawal, with `status: draft` | The existing complete-list semantics remain in force; draft status does not permit withdrawal |
| An interview reports approval is sometimes bypassed | Preserve the observation and source without rewriting the approval requirement |
| A source confirms the transcript, without ratifying policy | No automatic promotion to confirmed behavioral intent |
| A process has no bindings | Validity follows its actual level; automation setup is not demanded |
| A checker cannot trace a branch | The unreviewed scope remains visible; no claim that every path is verified |
| An approval operation is moved to another intent | State and process references follow it; charts retain the same meaning |
| One phase is later automated | Human responsibilities elsewhere and all accepted commitments remain intact |

## Further language work requiring a separate decision

**Partial state machines.** Admit only after specifying how partial and complete declarations differ, what an omitted transition means, whether endpoints and initial/final markers may be unknown, how operation references are handled, and how a discovery model becomes an enforceable policy. Define validation, graph queries, chart labeling, edit/round-trip preservation, compatibility with older readers, and prevention of automatic execution from an incomplete policy. A generic `draft` flag cannot supply these semantics. The immediate proposal deliberately keeps §7.9 unchanged on this point.

**Observation-only models.** A portable graph of what people report or evidence shows, which has no policy authority, would extend the authority model in §1.3, §2 and §17. Confirmation of an observation, policy ratification, contradictions, model comparison, export and downstream realization would all need defined semantics. An unknown frontmatter key that older tools ignore is insufficient. Keep this distinct from provenance: an inferred policy and an observed fact answer different questions.

Use real documentation sessions to determine whether the existing evidence workflow and progressive precision suffice before introducing either construct. Evaluate any extension against §8.6's useful precision, demonstrable need and fully specified meaning requirements. No new `Process`, `Task`, `Handoff`, `Document` or `Approval` facet is justified merely by those business words; existing facets already express them.

## Decisions requested

1. Treat business-process documentation as a successful, potentially permanent outcome and accept the clarification package in principle.
2. Preserve the admitted 5.13 State semantics while adopting the discovery discipline above.
3. Prioritize Amy's adoption and a focused conformance example; use those results to decide whether partial machines or observation-only graphs need a subsequent standards proposal.
