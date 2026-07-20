---
aim_version: 5.2
aim_root: ./aim/
spec: https://intentmodel.dev/spec.md
---

# Agents

This project uses the **Agentic Intent Model (AIM) v5.1** for behavioral specification.

The `./aim/` tree is the behavioral authority for a small support-ticket app (see [README.md](./README.md) for the guided tour). `.aim` files are a projection of a node-and-edge graph: headings are addressable nodes, `[verb](aim:<address>)` tokens are typed edges, and the graph is derived — never authored as a separate artifact. The intent tree reads parent/children; each child intent lives in its own directory with its intent file, and mapping/binding facets sit alongside the intent they realize.

Roles: the **Architect** authors intent, the **Developer** realizes it in code, the **Reviewer** diffs reality against the declared graph. Realization detail (symbols, routes, tables) belongs in `### Bindings` properties (or deprecated `kind: binding` sidecars) only — behavioral files never carry code paths.
