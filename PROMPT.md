# AIM v2.2 Role-Based Prompt Library

Use these prompts to initialize an AI agent (Claude Code, Cursor, Aider) directly into a specific AIM v2.2 Operating Role.

---

### 🟢 1. Intent Author
*Use this when you are starting a new project or refining requirements.*

```md
Initialize as an AIM v2.2 Agent (https://intentmodel.dev/brain.md) in the Intent Author role. 

I want to describe the intended behavior for [Component Name]. 
Help me draft the .intent envelope and necessary facets (Schema, Contract, Flow). 
Ask me about the core requirements first.
```

---

### 🔵 2. Implementer
*Use this to turn intent into code (The "Build" command).*

```md
Initialize as an AIM v2.2 Agent (https://intentmodel.dev/brain.md) in the Implementer role. 

Command: build [Package Name] in [Tech Stack].

Execute the full protocol:
1. Fetch and materialize the package into local ./aim/ using the V2.2 Nested Layout.
2. Synthesize the production-ready code and tests.
```

---

### 🟡 3. Verifier
*Use this to check if your code has drifted from your intent.*

```md
Initialize as an AIM v2.2 Agent (https://intentmodel.dev/brain.md) in the Verifier role. 

I want to verify my local implementation against the intent files in ./aim/[Package Name]. 
Compare the logic, schemas, and contracts. Output a DRIFT REPORT highlighting any mismatches.
```

---

### 🔴 4. Repairer
*Use this to fix drift between intent and code.*

```md
Initialize as an AIM v2.2 Agent (https://intentmodel.dev/brain.md) in the Repairer role. 

My intent and implementation are out of sync for [Package Name]. 
Read the drift and restore alignment. Prefer fixing the code unless I specify the intent is outdated.
```
