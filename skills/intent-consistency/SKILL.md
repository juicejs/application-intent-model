# Skill: Intent-Code Consistency (AIM v3.0)

Use this skill to manage the relationship between product requirements and actual code implementation. This skill is specifically designed to eliminate "logic drift" and "AI hallucinations" by using the Application Intent Model (AIM).

## When to Activate
- When the user reports that AI-generated code is "hallucinating" features or ignoring constraints.
- When there is a mismatch (drift) between what the system is supposed to do and what the code actually does.
- When the user wants to perform a "deterministic build" or "review" their system against a specification.
- When coordinating complex logic between multiple agents or across large codebases.

## Capabilities
- **Authoring:** Guides the user through defining system behavior in `.aim` files.
- **Review:** Systematically compares existing code against the `.aim` specification to generate a "Drift Report."
- **Repair:** Performs surgical fixes to code or intent to restore alignment.
- **Code generation:** Generates production-ready code that is 100% traceable to specific requirements.

## Core Mandates
- Every action must be grounded in an `.aim` artifact.
- Use the `@aim-architect`, `@aim-developer`, and `@aim-reviewer` personas for specialized tasks. Repair is folded into the Developer (code fixes) or the Architect (intent revision).
- Never settle for "loose" Markdown notes when precision is required.
