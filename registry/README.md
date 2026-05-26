# AIM Component Registry

This directory is the publish surface for community AIM component packages.

## Package Layout

Each package lives in:

- `registry/packages/<component>/`

Each package must contain:

1. Exactly one root intent file: `<component>.aim` with valid v3.1 frontmatter
2. Optional additional facet files (e.g., `<component>.schema.aim`, `<component>.contract.aim`) referenced by the entry file
3. Optional sub-component directories with their own intent files

## `registry/index.json` Schema

Required fields:

- `version`: index schema version (currently `"2"`)
- `packages`: array of package objects

Each package object requires:

- `name`: component namespace (lowercase, dot-separated segments; single-segment allowed)
- `aim_version`: AIM language version this package conforms to (`"3.0"` for current, `"2.2"` for legacy)
- `version`: package release version (semver, e.g. `"1.0.0"`)
- `entry`: path to root intent file relative to project root (e.g., `registry/packages/name/name.aim`)

Legacy v2.2 packages may declare `legacy: true` and continue to use `.intent` extensions until migrated.

## Pull Request Publishing Flow

1. Fork and create a branch.
2. Add or update package files in `registry/packages/<component>/`.
3. Update `registry/index.json` by adding your package to the `packages` array.
4. Open a PR.
5. CI runs `scripts/validate_registry.py`.
6. Maintainers review and merge.

Merged PRs are the publishing mechanism.

## Consumption Model

Consumers fetch the package `entry` from this registry, resolve related sources (sibling facet files, sub-components), and install files into local project `/aim/` (and `/aim/mappings/` when applicable) before code generation.

## Validation Rules

CI enforces:

- Index schema validity and non-empty package list
- Package/index consistency (one index record per package directory)
- `entry` exists and points to `.aim` for v3.0 packages (`.intent` allowed for legacy v2.2)
- Entry frontmatter matches `aim`, `facet: intent`, and `version`
- Exactly one root `facet: intent` file per package
- Optional sibling and sub-component files exist and have matching component, facet, and version
- Stale manifest files (`package.json`, `manifest.intent`) are rejected
- Legacy metadata tokens are rejected

## Notes

- Keep package changes focused per PR.
- Include release notes in the PR description for version bumps.
