# Acceptance scenarios for the 6.4 countdown

Eleven runs of `nasa.esdmd.artemis3.countdown.aim` in this folder, one per edge the fills of `proposals/6.4-flow-constructs.md` define. Each names what happens, which rule decides, and what a realization MUST show afterwards. A realization of 6.4 passes when every scenario ends as written; a case that ends differently is drift, whatever the realization's own reasons.

Every scenario starts the same way: the launch director invokes the countdown; step 1 emits `CountdownStarted` and creates the Countdown row with `stations: [booster, core, upper_stage, orion, range, weather]`, `status: running`; `WindowCloses` is armed for three hours from that Event; `Ends on` lists `LaunchScrubbed`. "The case's order" is the one order of the case's Events the realization keeps (Part 0). Minutes count from step 1.

## 1. Early readiness — Part 0

**What happens.** At step 4, while the weather is being polled, SpaceX invokes `ReportLanderReadiness`; `LanderReady` is emitted for this countdown. The count passes steps 4 and 5 and reaches step 6.

**Rule.** A wait hears every Event of its case since the case began; a wait reached after its Event arrived finds it and continues at once.

**Afterwards.** Step 6 completes without pausing; the case is at step 7. The case's order shows `LanderReady` before step 6 was reached. No second `LanderReady` is waited for.

## 2. A scrub during the wait — Part 2, `Ends on`

**What happens.** The case is waiting at step 6; no readiness has come. The launch director invokes `Scrub` (it is in their Access); `Scrub` moves the countdown to `scrubbed` and emits `LaunchScrubbed` for this countdown.

**Rule.** `LaunchScrubbed` is under `Ends on`: when it is placed in the case's order the case ends at that point, at once.

**Afterwards.** The case has ended at step 6. `Countdown.status` is `scrubbed`, moved by `Scrub` (Holding → Scrubbed). A `LanderReady` that arrives later belongs to no running case and is heard by nothing. `WindowCloses` is still armed; when it expires there is no case to interrupt; its triggered `Scrub` finds the countdown already scrubbed and makes no move (writing the same state value is no move, §6.10).

## 3. Readiness, then a scrub before the wait is reached — Part 0 with Part 2

**What happens.** At step 4 `LanderReady` is emitted. At step 5, while the range is being polled, the launch director invokes `Scrub`; `LaunchScrubbed` is emitted. Step 6 has not been reached.

**Rule.** An `Ends on` Event ends the case at its place in the case's order, wherever the case is. The early readiness is in the order too, but a wait hears only a case that still runs.

**Afterwards.** The case ended at step 5, the moment `LaunchScrubbed` was placed in its order; `ClearRange`, if it was running, does not advance the case. Step 6 is never reached; the early `LanderReady` is taken by nothing. `Countdown.status` is `scrubbed`. This is the scenario the race could not survive: with the scrub as a side of the race, the earlier readiness would have won at step 6 and the count would have gone on into a scrubbed countdown.

## 4. Expiry while the stations are being polled — Part 2 with Parts 0 and 3

**What happens.** The case is at step 7; four of six item runs have completed, two polls are running. The three hours expire.

**Rule.** The case is interrupted at once: no step starts, no wait completes, no Event advances it; item runs end with their step. Then the triggered `Scrub` runs. When it completes, the case ends.

**Afterwards.** The two running polls' item runs have ended; whether their `StationAnswer` rows exist is the realization's own business and changes nothing. `Scrub` moved the countdown to `scrubbed` and emitted `LaunchScrubbed` — which is under `Ends on` and finds the case already interrupted; it ends nothing twice. Step 8 never ran. The case's order shows the expiry before any later Event. Had a step of this countdown invoked a process instead of a Operation, its child cases would have ended with the case the same way, their own cleanup not run (Part 0); no step here does, so the rule is stated, not exercised.

## 5. Expiry at the same instant as readiness — Part 0 with Part 2

**What happens.** The case is waiting at step 6. `LanderReady` and the expiry of `WindowCloses` fall on the same instant.

**Rule.** Two things that arrive together are placed in the case's order; the order decides, never the clock.

**Afterwards.** Either the order places `LanderReady` first: the wait completes, the case reaches step 7, and the expiry interrupts it there — the case ends scrubbed at step 7. Or the order places the expiry first: the case is interrupted at step 6, `LanderReady` is taken by nothing, the case ends scrubbed at step 6. Both are correct; a realization MUST show which, and MUST NOT let `LanderReady` advance a case the expiry has already interrupted.

## 6. A scrub that does not complete — Part 2

**What happens.** The three hours expire at step 7. The triggered `Scrub` fails: the realization's call to safe the vehicle errors and the Operation does not reach its Ensures.

**Rule.** The case stays interrupted; a realization MUST show it as interrupted with the triggered work incomplete; recovery is explicit — run the triggered work again, or end the case by hand — and nothing happens on its own. A case ended by hand with its cleanup incomplete carries the run-time finding *cleanup incomplete*.

**Afterwards.** `Countdown.status` is still `holding`; no move was made. The case is shown to the owner as interrupted at step 7 with `Scrub` incomplete. No Event advances it: a `StationAnswer` arriving now is recorded by nothing. When the operator runs `Scrub` again and it completes, the countdown is `scrubbed` and the case ends. Had the operator ended the case by hand instead, the countdown would stay `holding`, the case would end, and the finding *cleanup incomplete* would be kept with it and shown wherever the case is — no graph diagnostic sees this: Holding has declared exits, and nothing in the files is wrong.

## 7. The stations list changes after the poll started — Part 3

**What happens.** Step 7 starts over the six stations. While the first polls run, `Countdown.stations` is changed to seven stations.

**Rule.** The items are the collection's content when the step starts; items added afterwards do not join.

**Afterwards.** Six item runs, six `StationAnswer` rows; the seventh station is never polled by this step. Step 8's `PollGoNoGo` reads six answers against a Countdown that now lists seven stations; its Expects — "every station of the countdown has an answer" — does not hold, so the realization refuses it and the case stops at step 8 as incomplete, visibly, which is what a changed list during a poll deserves.

## 8. One station's poll fails — Part 3

**What happens.** Step 7 starts over six stations. Five polls complete; the poll of `orion` does not: its Operation does not reach its Ensures.

**Rule.** Completion means every item completed; a failed item leaves the step incomplete and the case goes to `## On Error` for that step.

**Afterwards.** Step 8 has not started. The case is at step 7, incomplete, with five answers on record. On Error says the station is polled again by voice: the operator invokes `PollStation` for `orion` again; when it completes, the step completes and step 8 starts. Had every poll completed with one `no_go`, the step would have completed and step 8's `PollGoNoGo` would have decided **NoGo** — the gate is the step after the collection, never the items.

## 9. The resume moment is written only after the hold is released — Part 4

**What happens.** Every station answered go at minute 40; `PollGoNoGo` decided **Go** and released the hold; the case reaches step 9 at minute 40 and `Countdown.resumeAt` has no value. At minute 60 the launch director invokes `SetResumeTime` with minute 70. At minute 65 they invoke it again with minute 120.

**Rule.** An absent value waits for one; the write schedules it; the instant is resolved then and kept; a later change does not move an existing wait.

**Afterwards.** The case waited at step 9 from minute 40 to minute 60 with no due instant. At minute 60 the instant was resolved to minute 70 and kept. The write at minute 65 arrived while the case was still waiting; it changed the row and moved nothing. The count resumed at minute 70 and step 10 ran; the row shows minute 120; the realization's record of the case shows minute 70 as the instant it waited for. RESUME holds: the count left the hold no earlier than the planned moment, and only after every station answered go.

## 10. A violated criterion the forecast clears — Part 5

**What happens.** At step 4 the launch director invokes `PollWeather` with `wind: 35`, `lightningWithinTenMiles: false`, `ceiling: 2000`, `clearingForecastInWindow: true`. In a second run the same values come with `clearingForecastInWindow: false`.

**Rule.** When Criteria is present it is the whole decision; rules are tried in order; the first that holds decides; `otherwise` catches the rest.

**Afterwards.** First run: `Red when wind > 30, clearingForecastInWindow = false` does not hold (the forecast clears), nor do the other two; `otherwise Green` decides; the case continues to step 5, and the outcome's words — "or will be inside the window" — are exactly what the rules tested. Second run: the first rule holds; **Red** decides; its consequence invokes `Scrub`, the countdown is `scrubbed`, `LaunchScrubbed` is emitted and, under `Ends on`, ends the case at step 4. In neither run did the realization weigh anything the rules did not name.

## 11. A readiness after the scrub, and a scrub after the readiness — Part 2

**What happens.** First run: the case ended at step 5 as in scenario 3; a minute later SpaceX reports readiness again. Second run: readiness came at step 4 and was found at step 6 as in scenario 1; at step 8, with four stations polled go, the launch director scrubs.

**Rule.** An ended case hears nothing; an `Ends on` Event ends a running case wherever it is.

**Afterwards.** First run: the second `LanderReady` belongs to a countdown whose case has ended; nothing takes it; nothing starts. Second run: the case ends at step 8 the moment `LaunchScrubbed` is placed in its order; the item runs of step 7 had completed, the go poll never runs, the countdown is `scrubbed`. The readiness that won nothing and the readiness that was found both leave the case exactly where the scrub put it.

## What these scenarios do not cover

Step interruption (not in 6.4), a Criteria input from a Record read or a Capability result (not in 6.4), a race between operations, a genuine race between Events (none in the countdown — see Part 1), and a child case ending with its parent (no step of the countdown invokes a process; the rule is stated in scenario 4). A realization that behaves correctly on all eleven and differently on those is within the text.

## Two lines the 6.3 tree would gain

`nasa#Persona:LaunchDirector`'s Access, in `aim/nasa/nasa.aim`, would carry two more performer lines for this form of the countdown: `SetResumeTime` and `PollStation`. They are left out of the 6.3 tree so that it stays 6.3.
