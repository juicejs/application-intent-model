# Contributing

## Component Registry Publishing

Community component packages are published via pull requests to `registry/packages`.

1. Create a package directory: `registry/packages/<component>/`.
2. Add exactly one root intent file: `<component>.aim` with valid v3.1 frontmatter (`aim:` + `facet: intent`). Per-file `version:` and `spec:` are not used.
3. Add optional facet files (`<component>.<facet>.aim`) and sub-component intent files as needed.
4. Add your package to the `packages` array in `registry/index.json`, with `aim_version: "3.1"`.
5. Open a pull request.

CI validates package integrity and AIM header conventions using `scripts/validate_registry.py`.

## Spec Changes

Protocol changes should update:

- `specification.md` (the canonical v3.1 language spec)
- `README.md` (landing summary, if needed)

If a spec change affects registry rules, update `scripts/validate_registry.py`.
