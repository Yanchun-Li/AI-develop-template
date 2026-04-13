# ARCHITECTURE.md

This repository uses an agent-readable layered architecture.

## Layer Order

Business-domain code may only depend forward through this fixed order:

1. `types`
2. `config`
3. `repo`
4. `service`
5. `runtime`
6. `ui`

Interpretation:

- A file in `types` may import only `types`.
- A file in `config` may import `types` or `config`.
- A file in `repo` may import `types`, `config`, or `repo`.
- A file in `service` may import `types`, `config`, `repo`, or `service`.
- A file in `runtime` may import `types`, `config`, `repo`, `service`, or `runtime`.
- A file in `ui` may import any domain layer above.

Reverse imports are forbidden. Example:

- `repo` must not import `service`
- `types` must not import `ui`
- `service` must not import `runtime`

## Expected Directory Shape

```text
src/
  domains/
    billing/
      types/
      config/
      repo/
      service/
      runtime/
      ui/
    auth/
      types/
      config/
      repo/
      service/
      runtime/
      ui/
  providers/
    logging/
    database/
    cache/
    llm/
```

## Providers Boundary

Cross-cutting concerns enter the system through `src/providers/` only.

Examples of cross-cutting concerns:

- database clients
- HTTP clients
- logging
- metrics
- tracing
- cache clients
- queue clients
- LLM SDKs
- feature flag SDKs

Rules:

- Third-party libraries for cross-cutting concerns should be imported in provider modules, not scattered across domain files.
- Domain code should import provider-owned interfaces or adapters, not raw vendor SDKs.
- If the same external library appears in multiple non-provider files, treat that as an architecture violation unless there is a documented exception.

## Mechanical Enforcement

The repository linter enforces:

- domain layer import direction
- provider-only imports for configured external libraries
- duplicate direct external imports outside providers

Run:

```bash
python3 scripts/lint_repo_rules.py
```
