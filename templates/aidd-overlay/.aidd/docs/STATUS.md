# STATUS.md

This lightweight note helps AI agents orient before starting work.

## Current Purpose

- Use a local AIDD overlay to plan, execute, and verify work in an existing repository.
- Keep the target repository's tracked structure unchanged unless explicitly asked.

## Current State

- Root `AGENTS.md` and `CLAUDE.md` point agents to `.aidd/`.
- Local rules live in `.aidd/RULES.md`.
- Task notes live in `.aidd/docs/tasks/`.
- Larger implementation plans live in `.aidd/docs/exec-plans/`.
- No architecture-selection docs are included in this overlay.

## Next Actions for Agents

- Read the active task note before editing.
- If no active task note exists, create one for non-trivial work.
- Use the target repo's existing README, CI, tests, and docs as authoritative project context.
- Record validation and remaining risks before closing a task.
