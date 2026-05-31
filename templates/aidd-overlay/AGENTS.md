# AGENTS.md

This repository uses a local AIDD overlay for AI-assisted work on an existing codebase.

## Read First

1. `.aidd/RULES.md`
2. `.aidd/docs/WORKFLOW.md`
3. `.aidd/docs/STATUS.md`
4. `.aidd/docs/tasks/active/`
5. Existing repo README, CI config, tests, and nearby docs

## Source of Truth

- Existing repo code, README, CI, tests, and tracked docs remain the source of truth.
- `.aidd/` is a local planning and workflow overlay.
- Do not reshape this repo to match the AIDD template unless explicitly asked.
- If `.aidd/` conflicts with tracked repo docs or code, report the conflict before acting.

## Task Workflow

For non-trivial work:

1. Create or update a task note under `.aidd/docs/tasks/active/`.
2. Clarify objective, scope, constraints, and validation.
3. Implement only after the plan is clear.
4. Record result, validation, and remaining risks.
5. Move completed task notes to `.aidd/docs/tasks/completed/`.

For larger changes that affect contracts, data models, deployment, or multiple components, also use `.aidd/docs/exec-plans/active/`.

## Documentation Roles

- `.aidd/docs/tasks/`: task intake, current plans, and completed task records.
- `.aidd/docs/product-specs/`: what to build and why.
- `.aidd/docs/exec-plans/`: how to implement larger changes.
- `.aidd/docs/adr/`: durable architecture or technology decisions.
- `.aidd/docs/STATUS.md`: lightweight current-state note for agents.
- `.aidd/docs/WORKFLOW.md`: operating workflow for AI-assisted work.

## Editing Rules

- Keep edits narrowly scoped to the user request.
- Preserve unrelated user changes.
- Prefer existing repo patterns over template defaults.
- Do not add template CI, hooks, skills, agents, or architecture directories unless explicitly asked.
- Verify meaningful changes with the most relevant local command available.
