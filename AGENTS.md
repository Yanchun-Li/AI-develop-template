# AGENTS.md

This repository is designed for agent-first development.

## Purpose

- `AGENTS.md` is the table of contents, not the full manual.
- Deeper repository knowledge lives in versioned documents under `docs/`.
- When a rule and code conflict, update the docs or the code so they match. Do not leave drift unresolved.

## Operating Rules

- Prefer changing repository-local files over relying on chat history or external documents.
- Before large changes, write or update an execution plan in `docs/exec-plans/active/`.
- Complete work with code changes, doc changes, and validation where possible.
- Keep business logic inside domain layers defined in `ARCHITECTURE.md`.
- Cross-cutting infrastructure must enter domains through `src/providers/` only.
- Do not import third-party libraries directly across many domain files when a provider or local abstraction is required.

## Read This First

1. `ARCHITECTURE.md`
2. `docs/design-docs/index.md`
3. `docs/PLANS.md`
4. `docs/QUALITY_SCORE.md`
5. `docs/RELIABILITY.md`
6. `docs/SECURITY.md`

## Repository Map

- `docs/design-docs/`: design principles, core beliefs, and architecture notes.
- `docs/exec-plans/active/`: in-flight execution plans.
- `docs/exec-plans/completed/`: archived execution plans.
- `docs/references/`: LLM-oriented reference material for tools and external systems.
- `scripts/lint_repo_rules.py`: mechanical enforcement for repository architecture rules.

## Definition of Done

- Code follows the layer dependency rule:
  `types -> config -> repo -> service -> runtime -> ui`
- Cross-cutting concerns are accessed only through Providers.
- Docs are updated for any material architectural or workflow change.
- The repository linter passes.
