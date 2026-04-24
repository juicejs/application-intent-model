# AIM v2.2 Core Mandates

These mandates are foundational. All agents working in this project MUST adhere to these rules without exception.

## 1. File Format & Extension
- **Extension:** Every AIM artifact MUST end in `.intent`.
- **No Substitutes:** Never produce YAML, JSON, XML, or Markdown in place of an `.intent` file.
- **Header:** Every file must start with exactly: `AIM: <component>#<facet>@2.2`
- **Identity:** The component and facet in the header MUST match the filename and directory path.

## 2. Syntax Rules
- **Blocks:** Use UPPERCASE keywords and braces (e.g., `INTENT Name { ... }`).
- **Assignments:** Use `KEY: value`.
- **Lists:** Use hyphen-led entries (`- "item"`).
- **Prose:** Always quote natural language values.
- **No Commas:** Commas are not required between entries.

## 3. Operating Fail-Safes
- **Intent Authority:** The `.intent` files are the "Source of Truth." Implementation must never invent behavior absent from intent.
- **No Generic Names:** Filenames like `schema.intent` are invalid. Use `<component>.<facet>.intent`.
- **Precedence:** Resolve facets in order: `INCLUDES` > Sibling Discovery > Top-level Blocks > Embedded Blocks.
- **Verification:** Always distinguish between missing behavior, incorrect behavior, and undocumented extra behavior.

## 4. Role Dispatch
- **@aim-registry**: Registry -> Local Materialization.
- **@aim-author**: Requirements -> Intent.
- **@aim-implementer**: Intent -> Code/Tests.
- **@aim-verifier**: Code -> Drift Report.
- **@aim-repairer**: Drift -> Alignment.
