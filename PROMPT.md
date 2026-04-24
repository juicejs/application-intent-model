# AIM v2.2 Role-Based Prompt Library

Use these prompts to initialize an AI agent (Claude Code, Cursor, Aider) directly into a specific AIM v2.2 Operating Role.

---

### 📦 1. Registry Agent
*Use this to fetch and materialize packages from the registry.*

```md
Initialize as an AIM v2.2 Agent (https://intentmodel.dev/brain.md) in the Registry role. 

Command: fetch [Package Name]

Execute the protocol:
1. Resolve the package from the registry.
2. Fetch the entry intent and all included facets.
3. Materialize into local ./aim/ using the V2.2 Nested Layout.
```

---

### ✍️ 2. Intent Author
*Use this when you are starting a new project or refining requirements.*

```md
Initialize as an AIM v2.2 Agent (https://intentmodel.dev/brain.md) in the Intent Author role. 

I want to describe the intended behavior for [Component Name]. 
Help me draft the .intent envelope and necessary facets (Schema, Contract, Flow). 
Ask me about the core requirements first.
```

---

### 🛠️ 3. Implementer
*Use this to turn intent into code (The "Build" command).*

```md
Initialize as an AIM v2.2 Agent (https://intentmodel.dev/brain.md) in the Implementer role. 

Command: build [Package Name] in [Tech Stack].

Execute the protocol:
1. Read the local intent files in ./aim/[Package Name].
2. Synthesize the production-ready code and tests.
```

---

### 🔍 4. Verifier
*Use this to check if your code has drifted from your intent.*

```md
Initialize as an AIM v2.2 Agent (https://intentmodel.dev/brain.md) in the Verifier role. 

I want to verify my local implementation against the intent files in ./aim/[Package Name]. 
Compare the logic, schemas, and contracts. Output a DRIFT REPORT highlighting any mismatches.
```

---

### 🩹 5. Repairer
*Use this to fix drift between intent and code.*

```md
Initialize as an AIM v2.2 Agent (https://intentmodel.dev/brain.md) in the Repairer role. 

My intent and implementation are out of sync for [Package Name]. 
Read the drift report and restore alignment. Prefer fixing the code unless I specify the intent is outdated.
```
