qwh# Application Intent Model (AIM) v2.2

AIM is an intent-driven specification language and coordination layer for humans and AI agents. It eliminates "logic drift" and "hallucinations" by capturing product behavior in structured `.intent` files that agents can build from, verify against, and repair over time.

---

## 🚀 Native Gemini CLI Extension

AIM is now a first-class extension for [Gemini CLI](https://geminicli.com). Stop copying prompts and start using specialized terminal personas.

### Installation
```bash
gemini extensions install application-intent-model
```

### Specialized Personas
Invoke experts directly from your terminal:
- **✍️ @aim-author**: "I want to build a 2FA login flow."
- **📦 @aim-registry**: "fetch weather" (materializes into local `/aim`)
- **🛠️ @aim-implementer**: "build weather in React"
- **🔍 @aim-verifier**: "verify auth package" (generates a Drift Report)
- **🩹 @aim-repairer**: "fix drift in auth"

---

## Why AIM?

- **Eliminate Hallucinations**: Ground your AI agents in explicit contracts, not just loose chat context.
- **Deterministic Synthesis**: Build production-ready code that is 100% traceable to requirements.
- **Automated Verification**: Automatically detect when your code drifts away from your intent.
- **Progressive Precision**: Start with a simple intent envelope and add facets (Schema, Contract, Flow) only as needed.

---

## Core Concepts

Each component has one canonical entrypoint:
- `aim/<component>/<component>.intent`

As logic grows, add precision facets:
- `schema`: Data structures and structural types.
- `contract`: Externally observable guarantees (Input/Output).
- `flow`: Operational sequencing and internal logic.
- `persona`: Actor roles and view access.
- `view`: UI surfaces and user actions.
- `event`: Async payloads and routing.

---

## The Workflow

1. **Author**: Define behavior in `.intent` files (Requirements -> Intent).
2. **Implement**: Generate code and tests from local intent (Intent -> Code).
3. **Verify**: Compare implementation against intent (Code -> Drift Report).
4. **Repair**: Restore alignment when drift is detected (Drift -> Alignment).

---

## Quick Example

AIM uses a block-based syntax (not YAML/JSON) for maximum readability and precision.

```ail
AIM: auth.reset#intent@2.2

INTENT PasswordReset {
  SUMMARY: "Email-based password reset flow."
  REQUIREMENTS {
    - "User can request a reset link by email."
    - "Reset link expires after one hour."
  }

  CONTRACT Request {
    INPUT { email: string required }
    ENSURES { - "Secure token generated" - "Email sent" }
  }
}
```

---

## Technical Reference

- **[specification.md](./specification.md)**: The authoritative v2.2 language spec.
- **[PROMPT.md](./PROMPT.md)**: Role-based prompts for non-CLI assistants (Claude, Cursor, etc.).
- **[Registry](./registry/)**: Browse reusable intent packages.

---

## Repository Layout

- `agents/`: Gemini CLI persona definitions.
- `skills/`: Autonomous skills for Gemini (Intent-Code Consistency).
- `registry/`: The component package catalog.
- `site/`: The [intentmodel.dev](https://intentmodel.dev) website source.

---

Current Spec: **AIM v2.2**  
Built by **[Juice d.o.o.](https://juice.com.hr)**

