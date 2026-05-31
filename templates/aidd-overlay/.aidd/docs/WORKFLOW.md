# WORKFLOW.md

This document defines the local AIDD overlay workflow for taking tasks in an existing repository.

## Basic Policy

- Humans decide direction; AI agents execute within the agreed scope.
- Existing repo code and tracked docs remain authoritative.
- `.aidd/` stores local task planning, decisions, and verification notes.
- Conversation agreements should be written back to `.aidd/docs/` when they affect future work.

## Before Starting a Task

1. Read root `AGENTS.md`.
2. Read `.aidd/RULES.md`.
3. Read `.aidd/docs/STATUS.md`.
4. Read active task notes under `.aidd/docs/tasks/active/`.
5. Read the target repo's README, tests, CI, and nearby docs relevant to the request.
6. Confirm objective, scope, constraints, and validation path before non-trivial edits.

## Task Lifecycle

1. Create `.aidd/docs/tasks/active/YYYY-MM-DD-short-topic.md`.
2. Record objective, scope, constraints, current understanding, plan, and validation.
3. Implement and update the task note if the plan changes.
4. Record result, validation commands or manual checks, and remaining risks.
5. Move the file to `.aidd/docs/tasks/completed/`.

## Larger Change Lifecycle

Use `.aidd/docs/exec-plans/active/` when a change affects multiple components, API contracts, data models, deployment, runtime behavior, or shared rules.

1. Create `.aidd/docs/exec-plans/active/YYYY-MM-DD-short-topic-plan.md`.
2. Get user agreement or review before implementation.
3. Update the plan when scope or assumptions change.
4. Record validation and remaining risks.
5. Move the plan to `.aidd/docs/exec-plans/completed/`.

## Recommended Repository Artifacts

- `.aidd/docs/tasks/active/`: current task notes.
- `.aidd/docs/tasks/completed/`: completed task notes.
- `.aidd/docs/product-specs/`: feature intent.
- `.aidd/docs/exec-plans/active/`: larger implementation plans.
- `.aidd/docs/exec-plans/completed/`: completed implementation plans.
- `.aidd/docs/exec-plans/tech-debt-tracker.md`: known debt.
- `.aidd/docs/STATUS.md`: current state for agents.
- `.aidd/docs/CI.md`: validation and CI notes.

## After Changes

- Confirm changed files are within the requested scope.
- Confirm docs are updated when behavior, contracts, or decisions changed.
- Run the most relevant validation commands available in the target repo.
- If verification is incomplete, record why and what risk remains.
