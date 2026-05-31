# RULES.md

This file defines the local AIDD overlay rules for an existing repository.
The overlay helps AI agents plan and verify work without changing the repository's tracked structure.

## 1. Source of Truth

- Existing repo code, README, CI, tests, and tracked docs are authoritative.
- `.aidd/` is local planning context and must not override tracked project facts.
- If local overlay notes conflict with the repository, stop and report the conflict.
- Do not preserve important decisions only in chat. Record them in `.aidd/docs/` or, if they should be shared, propose adding them to tracked repo docs.

## 2. Change Scope

- Start from the files and modules named by the user.
- If scope is unclear, inspect the smallest relevant code and docs surface before editing.
- Do not rename, reorganize, or reshape the repository to match this template unless explicitly asked.
- Do not install hooks, CI, skills, agents, or architecture rules unless explicitly asked.

## 3. Task Planning

- Use `.aidd/docs/tasks/active/` for normal task notes.
- Use `.aidd/docs/exec-plans/active/` for larger changes that affect APIs, schemas, deployment, data ownership, or multiple components.
- A task note should include objective, scope, constraints, plan, validation, result, and remaining risks.
- Move completed notes to the matching `completed/` directory after recording validation.

## 4. Documentation Hygiene

- Keep `AGENTS.md` short and use it as an entrypoint.
- Keep local-only working context under `.aidd/`.
- Use `.aidd/docs/product-specs/` for feature intent.
- Use `.aidd/docs/adr/` for durable architecture or technology decisions.
- Mark obsolete notes instead of silently leaving stale guidance.

## 5. Validation

- Prefer the target repo's own validation commands from README, Makefile, package scripts, CI, or nearby docs.
- If no command is available, record the manual inspection performed.
- Report incomplete verification and remaining risks plainly.
