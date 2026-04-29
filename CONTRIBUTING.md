# Contributing

## Component Registry Publishing

Community component packages are published via pull requests to `registry/packages`.

1. Create a package directory: `registry/packages/<component>/`.
2. Add exactly one `#intent` facet file: `<component>.intent`.
3. Add optional facet files referenced by `INCLUDES`.
4. Add your package to the `packages` array in `registry/index.json`.
5. Open a pull request.

CI validates package integrity and AIM header conventions using `scripts/validate_registry.py`.

## Spec Changes

Protocol changes should update:

- `specification.md` (canonical language spec)
- `README.md` (landing summary, if needed)

If a spec change affects registry rules, update `scripts/validate_registry.py`.
