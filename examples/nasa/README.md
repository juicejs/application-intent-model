# Example: NASA — an Artemis mission from formulation to flight (AIM 6.3)

One organisation, real in its shape, written as one connected tree: NASA at the root, a directorate that decides, three centers that build and fly, a mission that is a project, three processes inside it, a piece of software with three parts, and a network described where it is built and used where it is needed. It exercises the four facets that `proposals/6.3-four-facets.md` adds — **Organisation, Project, Software, Service** — beside every facet 6.2 already has, in the situations the proposal's reviews called awkward.

> A 6.2 reader rejects the four new headings as unknown facet types. Everything else is 6.2 as specified. `AGENTS.md` beside this file says so for agents.

## The story

The Exploration Systems Development Mission Directorate runs **Artemis III**, a project with a goal and an end: land two astronauts near the lunar south pole in 2027. The mission passes its **lifecycle gates** — a standing review board conducts each review, the directorate decides the key decision point, rework loops until actions are closed, and a review open ninety business days is escalated. On launch day the **countdown** runs to a built-in hold, polls the weather through a capability the National Weather Service answers, waits for the Space Force's range to clear and for SpaceX to report its lander ready in lunar orbit, polls the team, and lifts off — or scrubs, not least when the window closes. In flight, **mission control software** at Johnson ingests every frame the **Deep Space Network** brings down, flags limit violations, and starts **anomaly resolution**: a flight controller triages on the flight rules, the team proposes, the flight director accepts, rejects or waives, and an accepted resolution goes up as a command through the same network. The network itself is described at JPL, which is NASA's laboratory and Caltech's organisation at once.

## What it showcases

| 6.3 claim | Where |
|---|---|
| **Organisation at every level.** The root, a directorate, three centers; a department not yet earned (`Organisation: FlightOperationsDirectorate` at Johnson) | `nasa.aim`, `nasa.esdmd.aim`, `nasa.jsc.aim`, `nasa.jpl.aim`, `nasa.ksc.aim` |
| **A promoted Organisation that still acts.** The directorate keeps a top-level `## Role` and `## Access` and is named in Authz by its namespace | `nasa.esdmd.aim` → `KeyDecisionPoint` |
| **Outside organisations that perform steps.** SpaceX reports the lander; the Space Force range clears the launch; both are Organisation facets with Access, named in Authz | `nasa.esdmd.artemis3.aim`, `nasa.ksc.aim` → countdown steps 5 and 6 |
| **Nesting is scope, not membership.** Caltech is described under JPL without being part of NASA; the range is described at Kennedy without being NASA's | `nasa.jpl.aim`, `nasa.ksc.aim` |
| **Project contains work, performs nothing.** Artemis III holds the Mission record, its State, three processes and the organisations and services it uses; it has no Role, no Access, no edge | `nasa.esdmd.artemis3.aim` |
| **A Project facet before it earns a node** | `Project: ArtemisIV` in `nasa.esdmd.aim` |
| **Software described here, with parts.** Mission control with telemetry, trajectory and crew systems as Software children; a shared View and Style at the parent; bindings on the parts | `nasa.jsc.mcc.aim` and its three children |
| **The same system as Software and as Service.** The Deep Space Network is a Software at JPL (`nasa.jpl.dsn`, with its own Record, Operations, View, Trigger) and a Service at mission control (`Service: DeepSpaceNetwork`), joined by the mapping of the `SpaceLink` capability to the provider's Operations | `nasa.jpl.dsn.aim`, `nasa.jsc.mcc.aim`, `nasa.jsc.mcc.mapping.aim` |
| **Capability is a function; Service is a system.** `LaunchWeather`, `LanderStatus`, `SpaceLink`, `Ephemeris` are what the work must be able to do; `NOAAWeather`, `StarshipHLS`, `DeepSpaceNetwork`, `JPLHorizons` are what answers them | countdown, artemis3, mcc, trajectory, ksc |
| **A Capability answered three ways.** By a mapping to a provider intent (`SpaceLink` → `nasa.jpl.dsn`), by a direct binding to a connection (`LaunchWeather`, `Ephemeris`, `LanderStatus`) — and one left to the reader: what answers `LanderStatus` if SpaceX changes the link | `nasa.jsc.mcc.mapping.aim`; the `### Bindings` of each Capability |
| **A Process before and after its steps.** Three promoted processes with top-level `## Steps`; deciding steps with `continues:`; a correction loop (`Rework` → `CloseActions` → review again; `Reject` → propose again) bounded by a deadline | lifecycle, countdown, anomaly |
| **Waiting and entry.** The countdown waits on `LanderReady` inside its Steps; anomaly resolution is entered by an intent-level `subscribes` to an Event of another intent | countdown step 6; anomaly Summary |
| **Deadlines per case, business days, a window.** Ninety business days to close a review; twenty-four hours to close an anomaly; three hours from call to stations to the window's close | the three Triggers, `timezone` and `calendar` on the root |
| **States with Only in.** Mission phase, review status, countdown status, anomaly status; operations confined to a state | the four `State` facets |
| **Knowledge consulted, never deciding.** NPR 7120.5 at every gate; the flight rules at triage and proposal | `nasa.aim`, lifecycle, anomaly |
| **Labels.** `NPR 7120.5`, `Space Launch Delta 45`, `Starship HLS`, `Artemis IV` beside their ASCII names | throughout |
| **Shared things at the lowest common ancestor.** The flight director, mission manager and launch director at the root, because Johnson's software and the directorate's processes both need them; the flight controller at Johnson; the network operator at JPL | the Personas |

By the numbers: 14 intents, 90 facets, 41 labelled requirements, 170 typed edges; natures organisation ×5, project ×1, software ×5, process ×3 (Flow renamed Process and Contract renamed Operation, 6.3 Parts 4 and 5).

## Layout

```
aim/nasa/
  nasa.aim                                   root organisation: shared personas, knowledge, the index
  esdmd/nasa.esdmd.aim                       the directorate: a promoted organisation that decides; Project: ArtemisIV as a facet
  esdmd/artemis3/nasa.esdmd.artemis3.aim     the project: Mission + MissionPhase, SpaceX, the review board, Starship HLS, LanderStatus
  esdmd/artemis3/lifecycle/…lifecycle.aim    process: the gates, Review + Action + ReviewStatus, the 90-day deadline
  esdmd/artemis3/countdown/…countdown.aim    process: the count, Countdown + CountdownStatus, LaunchWeather, the window deadline
  esdmd/artemis3/anomaly/…anomaly.aim        process: entered by an Event, Anomaly + Waiver + AnomalyStatus, the 24-hour deadline
  jsc/nasa.jsc.aim                           Johnson: the flight controller; a directorate not yet earned
  jsc/mcc/nasa.jsc.mcc.aim                   software: console View + Style, Service: DeepSpaceNetwork, Capability: SpaceLink
  jsc/mcc/nasa.jsc.mcc.mapping.aim           SpaceLink → nasa.jpl.dsn, operation by operation
  jsc/mcc/telemetry/…telemetry.aim           part: frames, limits, IngestFrames, DetectLimitViolation, SendCommand, PassStart
  jsc/mcc/trajectory/…trajectory.aim         part: Burn, Ephemeris capability, JPL Horizons service, ComputeBurn, ExecuteBurn
  jsc/mcc/crew/…crew.aim                     part: VitalSign, FlagVitalSign, CrewHealth view
  jpl/nasa.jpl.aim                           JPL: Organisation: Caltech, the network operator
  jpl/dsn/nasa.jpl.dsn.aim                   software: the network as described where it is built — passes, downlink, uplink, maintenance
  ksc/nasa.ksc.aim                           Kennedy: Organisation: EasternRange, Service: NOAAWeather
```

## What writing it found

These are places where the files had to choose and the proposal, or the specification, should say what the choice is.

1. **A Service with no provider intent has no formal link to the Capability it answers.** `LaunchWeather` (countdown) and `Service: NOAAWeather` (Kennedy) share a binding locator and nothing else; `Ephemeris` and `JPLHorizons` the same. Where a provider intent exists, the mapping is the link (`SpaceLink` → `nasa.jpl.dsn`), but a mapping's Target is intent-to-intent (§8). The proposal should give a Service facet a way to say which Capabilities it answers — or a mapping a way to target a Service facet — so that "a Service not connected" and "a Capability nothing answers" can be read from the graph.
2. **A Service facet does not name its provider intent either.** `Service: DeepSpaceNetwork` at mission control says `nasa.jpl.dsn` in prose; the mapping targets the intent, the Service facet is beside it. One line on the Service (`### Target`, or a binding `answered-by`) would close both gaps at once.
   *Answered in 6.3 as adopted (2026-11-08):* a Service is connected through its own `### Bindings`, which may name the provider intent — `DeepSpaceNetwork` now binds `aim:nasa.jpl.dsn`. Finding 1 stays open: a mapping's Target is still the provider intent, never the Service facet.
3. **An intent's entry subscription has no named place.** Anomaly resolution is entered by a `subscribes` token written in its Summary paragraph, because a bare top-level section is edge-inert (§4). It works; it is not obvious. The spec could name the place.
4. **A conditional State move cannot be written.** `ConductGateReview` is one Operation for every gate, but only the flight readiness review moves the mission from Development to Launch. The State says `Development → Launch — [ConductGateReview]`; the condition "only for the FRR" lives in the Operation's Ensures prose. Known: the language has no guarded move, by design.
5. **A deadline anchored on the Event that starts the run.** `ResolutionDeadline` is anchored on `AnomalyDetected`, emitted by another intent before the case exists, and disarmed by `AnomalyClosed` of the case. §6.7 reads naturally that the starting Event belongs to the case it starts; the spec could say so in one sentence.
6. **The root was written as a named organisation (`nasa`), not `root`.** The product's rule that every workspace root is addressed `root` is Amy's, for prepared intents and moves between workspaces; a specification example reads better with its name, as the other examples do.
7. **Five things the flow grammar could not say.** The countdown's run is not ended when the window closes; lander-ready versus scrub is a race the steps cannot write; the board's ten days with the package is a wait on time; "close every action" and "poll every station" are steps over a collection written as one Operation; the weather criteria are a table written as a sentence. Each is filled, the AIM way, in `proposals/6.4-flow-constructs.md`, with these processes as its examples. The files here stay 6.3 and do not use the fills; `6.4/` beside `aim/` holds the countdown in 6.4 form and eleven acceptance scenarios for it (`6.4/scenarios.md`).
8. **Eleven rules that come from other rules had no legal way to say so.** The first version put `[satisfies]` on requirement bullets pointing at the ancestor's requirement — an illegal triple, a requirement item is never a source. They now carry the source trailer of 6.3 Part 6, `— from [nasa#Requirements[RANGE]]`, and six more carry a Knowledge or a reason in words (`— from [nasa#Knowledge:NPR7120]`, `— from: the launch commit criteria document`).
