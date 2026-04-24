# Skill: Intent-Code Consistency (AIM)

Use this skill to manage the relationship between product requirements and actual code implementation. This skill is specifically designed to eliminate "logic drift" and "AI hallucinations" by using the Application Intent Model (AIM).

## When to Activate
- When the user reports that AI-generated code is "hallucinating" features or ignoring constraints.
- When there is a mismatch (drift) between what the system is supposed to do and what the code actually does.
- When the user wants to perform a "deterministic build" or "verify" their system against a specification.
- When coordinating complex logic between multiple agents or across large codebases.

## Capabilities
- **Authoring:** Guides the user through defining system behavior in `.intent` files.
- **Verification:** Systematically compares existing code against the `.intent` specification to generate a "Drift Report."
- **Repair:** Performs surgical fixes to code or intent to restore alignment.
- **Synthesis:** Generates production-ready code blocks that are 100% traceable to specific requirements.

## Core Mandates
- Every action must be grounded in an `.intent` artifact.
- Use the `@aim-author`, `@aim-implementer`, `@aim-verifier`, and `@aim-repairer` personas for specialized tasks.
- Never settle for "loose" Markdown notes when precision is required.
