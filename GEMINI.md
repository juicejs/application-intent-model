# Application Intent Model (AIM) Extension

This extension enables the Application Intent Model (AIM) workflow within Gemini CLI. AIM is an intent-driven specification language that captures product behavior in a form that is readable for humans and structured enough for deterministic synthesis and verification by AI agents.

## Core Concepts

- **Component:** Identified by a namespace (e.g., `auth.login`).
- **Facet:** A specific dimension of the component (e.g., `intent`, `schema`, `contract`, `flow`).
- **.intent Files:** The coordination layer. All AIM artifacts must use the `.intent` extension and start with the `AIM: <component>#<facet>@2.2` header.

## Workflow

1. **Author:** Define behavior in `.intent` files using `@aim-author`.
2. **Implement:** Generate code and tests from intent using `@aim-implementer`.
3. **Verify:** Check for drift between code and intent using `@aim-verifier`.
4. **Repair:** Restore alignment between code and intent using `@aim-repairer`.

## Non-Negotiable Rules

- **Strict File Format:** All artifacts MUST be `.intent` files. NEVER use YAML, JSON, or Markdown for intent definitions.
- **Header Mandatory:** Every `.intent` file must start with `AIM: <component>#<facet>@2.2`.
- **Precedence:** Intent files are the authoritative source. Implementation must not invent behavior not grounded in intent.
