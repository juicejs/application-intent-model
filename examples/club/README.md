# Example: a sports club (AIM 6.3 and 6.4)

The smallest organisation everyone knows, written as one tree: a club at the root, two departments, an app the club built, a tournament as a project, and the two things every club does — take people in and collect their fees. It is half the size of `examples/nasa` and reaches every construct of the two proposals without strain: the four facets of 6.3 (`Organisation`, `Project`, `Software`, `Service`), Flow written as Process and Contract as Operation, a requirement's `from` source, and in the processes a genuine race, `Ends on`, deadlines that end the case, a step over a collection with a child case per item, a timed wait and criteria rules. German labels throughout, beside ASCII names.

> A 6.2 reader rejects the new headings and words. Everything else is 6.2 as specified. `AGENTS.md` beside this file says so for agents.

## The story

**TSV Seehausen 1921** has a football department with eleven teams, a gymnastics department, and a member app it built itself. A person applies; the board decides on the statutes; the treasurer sets the fee class by rule; the club sends its offer and waits for the person to accept or decline — a real race; the statutory fourteen days pass; the member is created and gets their card as a PDF. Every fifteenth of January the fee run starts: one collection per member as a run of its own, the direct debit to the bank, a reminder after fourteen days, the board after fourteen more; a member who resigns has the open fee cancelled, which ends the collection wherever it stands. For the **summer tournament 2027**, a project with a committee that exists only for it, every team is put in its age group by rule and registered with the federation through its portal, the club waits for the federation's confirmation, pays, and waits for the draw; the registration window closing ends the run. The football department looks players up in the club's own app, which it reaches as a service.

## What it showcases

| Claim | Where |
|---|---|
| **Organisation at three levels, and outside ones.** The club; its two departments; the federation that confirms registrations (acts), the town that owns the hall (does not) | `tsv.aim`, `tsv.fussball.aim`, `tsv.turnen.aim` |
| **A Persona and a Record that are one thing.** `Persona: Mitglied` acts, `Record: Mitglied` is kept, with a State from applicant to member to resigned, including `→ deleted` moves | `tsv.aim` |
| **A Project that contains work and performs nothing.** The tournament holds its record, its committee, its service and capability, and its one process | `tsv.turnier2027.aim` |
| **Two Projects before they earn a node.** The hall renovation at gymnastics; the committee is an Organisation facet inside the project | `tsv.turnen.aim`, `tsv.turnier2027.aim` |
| **Software described here, with a module.** The member app with its screen, its lookup, its style and the fees module beneath it | `tsv.app.aim`, `tsv.app.beitraege.aim` |
| **The same software as a Service elsewhere.** The football department's `Service: Mitgliederverzeichnis` is the app; the mapping of its lookup capability targets `tsv.app` | `tsv.fussball.aim`, `tsv.fussball.mapping.aim` |
| **A Software facet before it earns a node.** The coaches' team app | `tsv.fussball.aim` |
| **A Process before its steps.** Training, named with a Summary and no steps, still started by a weekly Trigger | `tsv.fussball.aim` |
| **Capability is a function; Service is a system.** SEPA direct debit, membership-card PDF, member lookup and federation registration are what the work must do; the bank, the portal and the app are what answer them | root, fussball, turnier2027 |
| **A Capability answered three ways.** By a mapping to a provider intent (SEPA → `volksbank`), by a mapping to the club's own Software (lookup → `tsv.app`), by a direct binding (the portal; the PDF, bound to the tool's own service) | the two mapping files, the Capabilities' `### Bindings` |
| **A provider intent outside the tree, inferred.** The bank's direct-debit interface, written by discovery, `provenance: inferred`, `nature: service` | `volksbank.aim` |
| **Requirements with their source.** Twenty-two `from` trailers: the statutes, the fee rules, the data protection rules as Knowledge; a company rule one level up; the consumer's right of withdrawal and a board decision as words | every `## Requirements` block |
| **A genuine race.** The applicant accepts or declines the offer; `continues: AngebotAngenommen` | `tsv.aufnahme.aim` step 5 |
| **`Ends on`.** Withdrawal ends an application; cancellation or the report to the board ends a fee collection; the board's withdrawal ends a registration | the three processes' `## Ends on` |
| **Deadlines that end the case.** A stale application after thirty days; a fee unpaid after the reminder; a registration window closing | `AntragVerfallen`, `ZweiteFrist`, `Meldeschluss` |
| **A step over a collection with a child case per item.** One fee collection per member, invoked as a process with its own `## Input`; one age-group decision per team | `tsv.beitrag.aim` step 2, `tsv.turnier2027.anmeldung.aim` step 2 |
| **A timed wait, both forms.** The withdrawal period, `after: 14 days`; the draw, `until` the tournament's `auslosungAm` | `tsv.aufnahme.aim` step 6, `anmeldung` step 5 |
| **Criteria as rules.** The fee class from age and family; the age group from the youngest birth year, five outcomes and `otherwise` | `BeitragsklasseFestlegen`, `AltersklasseBestimmen` |
| **An escalation ladder.** Two chained deadlines, reminder then board | `tsv.beitrag.einzug.aim` |
| **A webhook, a schedule, a yearly run.** The bank's payment notification; training evenings; the fee run on 15 January | the Triggers |
| **Labels.** `Übungsleiterin`, `Beitragsübersicht`, `Bayerischer Fußball-Verband` beside their ASCII names | throughout |

By the numbers: 11 intents, 86 facets, 31 labelled requirements, 22 sources, 129 typed edges; natures organisation ×3, project ×1, software ×2, process ×4, service ×1.

## Layout

```
aim/
  tsv/
    tsv.aim                                  root organisation: Mitglied as Persona and Record, the board, the treasurer, bank, federation, town, statutes, fee rules
    tsv.mapping.aim                          SEPA → volksbank
    fussball/tsv.fussball.aim                department: teams, the coach, Process: Training before its steps, Service: the member app, Software: TeamApp
    fussball/tsv.fussball.mapping.aim        member lookup → tsv.app
    turnen/tsv.turnen.aim                    department: the instructor, Project: Hallensanierung as a facet
    app/tsv.app.aim                          software: Style, View MeineDaten, Operation MitgliedSuchen
    app/beitraege/tsv.app.beitraege.aim      module: the treasurer's fee overview
    turnier2027/tsv.turnier2027.aim          project: Turnier record, the committee, the portal, the registration capability
    turnier2027/anmeldung/…anmeldung.aim     process: age group by rule per team, confirmation, fee, the draw, the window
    aufnahme/tsv.aufnahme.aim                process: application, decision, fee class by rule, offer, race, 14 days, member created
    beitrag/tsv.beitrag.aim                  process: the yearly run, one child collection per member
    beitrag/einzug/tsv.beitrag.einzug.aim    process: one fee — direct debit, payment, reminder, board; Ends on cancellation
  volksbank/volksbank.aim                    the bank's provider model, outside the tree, inferred
```

## What writing it found

1. **A member is both a Persona and a Record, and the model wants them as one node.** They are written as two same-named facets on the root, which §6.0 says promote together. The joining process writes the Record while the Persona acts; nothing in the language links the two until promotion. A real club's model promotes `Mitglied` on day one.
2. **A collection per member needs a child case, not an item run.** The first draft anchored the reminder deadlines on `BeitragGestellt` inside the yearly run; §6.7's "one timer per case" would then have meant one reminder clock for six hundred fees. Invoking `tsv.beitrag.einzug` per member gives each fee its own case and its own clocks — which is 6.4's child-case rule doing exactly what it is for.
3. **A race and a cancellation are different even in a four-step process.** Accept-or-decline is a race; withdrawal is `Ends on`. Writing the withdrawal as a third side of the race would have let an earlier acceptance win over a later withdrawal.
4. **The webhook Trigger has nothing to anchor on and nothing to disarm.** `Zahlungseingang` is `webhook` with prose for its source; the bank's own Event (`volksbank#Event:ZahlungEingegangen`) cannot be named by the club's Trigger because a provider intent is outside the tree. The link between an outside Event and the Trigger that ingests it stays prose.
5. **`for each` over a list of references works; over the rows of a Record it would not have.** The run keeps `mitglieder: list(ref(tsv#Mitglied.id))` on its own record because members do not reference the run. The proposal's Record form needs the rows to reference the case's record; a yearly run over all members is the common case where they do not, and the list field is the honest way.
