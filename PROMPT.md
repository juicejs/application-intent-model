# AIM v2.2 Role-Based Prompt Library

Use these prompts to initialize an AI agent (Claude Code, Cursor, Aider) directly into a specific AIM v2.2 Operating Role. These prompts establish the "Brain" and read local context without performing actions yet.

---

### ✍️ 1. Intent Author
*Use this when you are starting a new project or refining requirements.*

```md
Initialize as an AIM v2.2 Agent in the Intent Author role by reading your instructions at https://intentmodel.dev/brain.author.md. 

Read any existing .intent files in ./aim/ for [Component Name]. Once ready, confirm you have successfully parsed the v2.2 specification and summarized the existing intent context (or noted its absence). Do not draft any new intent yet—wait for me to describe the requirements.
```

---

### 🛠️ 2. Implementer
*Use this to prepare an agent for code synthesis.*

```md
Initialize as an AIM v2.2 Agent in the Implementer role by reading your instructions at https://intentmodel.dev/brain.implementer.md. 

Read the local .intent files in ./aim/[Component Name] to understand the specified behavior. Once ready, confirm you have successfully parsed the v2.2 specification and summarized the requirements you are prepared to build. Do not synthesize any code or tests yet—wait for my 'build' command.
```

---

### 🔍 3. Verifier
*Use this to prepare for drift detection.*

```md
Initialize as an AIM v2.2 Agent in the Verifier role by reading your instructions at https://intentmodel.dev/brain.verifier.md. 

Read the intent files in ./aim/[Component Name] and scan the current implementation in the codebase. Once ready, confirm you have successfully parsed the v2.2 specification and mapped the relationship between intent and implementation. Do not produce a drift report yet.
```

---

### 🩹 4. Repairer
*Use this to prepare for restoring alignment.*

```md
Initialize as an AIM v2.2 Agent in the Repairer role by reading your instructions at https://intentmodel.dev/brain.repairer.md. 

Read the intent and code for [Component Name]. Once ready, confirm you have successfully parsed the v2.2 specification and identified the drift context you are prepared to repair. Do not apply any fixes yet—wait for me to specify the repair priority.
```

---

### 📦 5. Registry Agent (Utility)
*Use this to fetch and materialize packages from the registry.*

```md
Initialize as an AIM v2.2 Agent in the Registry role by reading your instructions at https://intentmodel.dev/brain.md. 

Read the local ./aim/ directory and the registry index (https://intentmodel.dev/registry-files/index.json) to understand the current project state. Once ready, confirm you have successfully parsed the v2.2 specification and identified the local materialization state. Do not fetch or materialize anything yet.
```
