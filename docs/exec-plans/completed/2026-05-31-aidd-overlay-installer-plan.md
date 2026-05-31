---
plan_id: 2026-05-31-aidd-overlay-installer
status: completed
review_status: approved
created: 2026-05-31
last_verified: 2026-05-31
owner: codex
related_specs:
  - N/A: local overlay installer, not a product feature
affected_modules:
  - README.md
  - templates/aidd-overlay
  - scripts/aidd-init.sh
  - tests/test_template.py
superseded_by:
---

# AIDD Overlay Installer Plan

## Goal

Add a local AIDD overlay distribution and installer command for applying AI-driven development docs to existing repositories without reshaping their code or copying architecture-selection docs.

## Non-Goals

- Do not change the root template layout used for new-project scaffolding.
- Do not install Claude skills, Claude hooks, Codex skills, or Codex agents.
- Do not copy `docs/architectures/` into the overlay distribution.

## 影響範囲

### files_to_modify

- `README.md` — document the overlay installer command and generated target layout.
- `tests/test_template.py` — add regression coverage for overlay structure and installer behavior.

### files_to_create

- `templates/aidd-overlay/AGENTS.md` — local Codex entrypoint for existing repositories.
- `templates/aidd-overlay/CLAUDE.md` — local Claude Code entrypoint that imports AGENTS.md.
- `templates/aidd-overlay/.aidd/RULES.md` — overlay-specific rules without architecture-selection requirements.
- `templates/aidd-overlay/.aidd/docs/**` — overlay docs copied from the template, excluding architectures.
- `scripts/aidd-init.sh` — command that installs the overlay into a target repository.

### files_to_delete

- N/A: no obsolete file is replaced by this change.

## 実装ステップ

### Step 1: Create overlay templates

- 内容: Add `templates/aidd-overlay/` with root entrypoints and `.aidd/` docs.
- 完了条件: Overlay tree exists and does not include `.aidd/docs/architectures/`.
- 検証方法: `find templates/aidd-overlay -maxdepth 4 -type f | sort`

### Step 2: Add installer command

- 内容: Add `scripts/aidd-init.sh` that copies the overlay into the current git repo root or current directory.
- 完了条件: Running the script in a temp git repo creates `AGENTS.md`, `CLAUDE.md`, `.aidd/RULES.md`, `.aidd/docs/`, and updates `.git/info/exclude`.
- 検証方法: pytest installer regression test.

### Step 3: Add regression tests

- 内容: Extend `tests/test_template.py` for overlay structure and init behavior.
- 完了条件: Tests assert required files exist, architecture docs are absent, and existing root entrypoints are not overwritten.
- 検証方法: `uv run pytest tests/test_template.py`

## 接口定義

```bash
scripts/aidd-init.sh [TARGET_DIR]
```

```text
Input:
  TARGET_DIR optional path to an existing repository or directory.

Output:
  TARGET_DIR/AGENTS.md if absent
  TARGET_DIR/CLAUDE.md if absent
  TARGET_DIR/.aidd/RULES.md
  TARGET_DIR/.aidd/docs/**
  TARGET_DIR/.git/info/exclude entry for .aidd/
```

## 検討した代替案

### 案 A: Convert the root template in place

- 概要: Move existing `AGENTS.md`, `RULES.md`, and `docs/` into overlay-oriented paths.
- 却下理由: The current root template is the source for new-project scaffolding; moving it would remove the existing template contract visible in `AGENTS.md` and `RULES.md`.

### 案 B: Generate overlay files with sed from the root template at install time

- 概要: Keep one source tree and rewrite paths during installer execution.
- 却下理由: The root `AGENTS.md` contains architecture-selection requirements and `pyproject.toml [tool.repo-arch]` assumptions; runtime rewriting would be harder to test than a static overlay fixture.

## Open Questions

- N/A: User approved excluding skills, agents, hooks, and architecture docs before implementation.

## Review Notes

- Reviewer: user
- Result: approved
- Notes: User asked to implement the previously discussed overlay distribution and installer.

## Completion

- Completed: 2026-05-31
- Validation:
  - `uv run pytest tests/test_template.py`
  - `make lint`
  - `make test`
- Related PR / commit: N/A: local branch changes only
- Remaining follow-up: Optional: add a user-level shell alias or symlink for `aidd-init` after deciding the preferred command name.
