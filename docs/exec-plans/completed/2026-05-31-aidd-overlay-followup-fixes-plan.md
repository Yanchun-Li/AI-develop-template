---
plan_id: 2026-05-31-aidd-overlay-followup-fixes
status: completed
review_status: approved
created: 2026-05-31
last_verified: 2026-05-31
owner: codex
related_specs:
  - N/A: follow-up fixes for local overlay installer
affected_modules:
  - scripts/aidd-init.sh
  - tests/test_template.py
  - README.md
  - AGENTS.md
superseded_by:
---

# AIDD Overlay Follow-up Fixes Plan

## Goal

Fix the three reviewed AIDD overlay issues: protect existing `.aidd` files on re-run, remove stale absolute README command paths, and correct the stale AGENTS plan reference.

## Non-Goals

- Do not change the overlay directory layout.
- Do not add skills, agents, hooks, or CI workflow installation.

## 影響範囲

### files_to_modify

- `scripts/aidd-init.sh` — add safe default behavior and an explicit overwrite flag.
- `tests/test_template.py` — pin installer re-run behavior.
- `README.md` — replace machine-specific command examples.
- `AGENTS.md` — update stale exec-plan path reference.

### files_to_create

- N/A: no new runtime artifact is needed.

### files_to_delete

- N/A: no file is removed.

## 実装ステップ

### Step 1: Harden installer re-run behavior

- 内容: Add `--force` and skip `.aidd` sync when `.aidd` exists without force.
- 完了条件: Existing `.aidd/RULES.md` survives a normal re-run.
- 検証方法: pytest.

### Step 2: Fix documentation references

- 内容: Replace hard-coded Downloads path in README and correct AGENTS active/completed plan path.
- 完了条件: Docs no longer reference the stale path.
- 検証方法: `rg` targeted checks.

### Step 3: Run validation

- 内容: Run focused and repo-level validation.
- 完了条件: tests and lint pass.
- 検証方法: `uv run pytest tests/test_template.py`, `make lint`, `make test`, `git diff --check`.

## 接口定義

```bash
scripts/aidd-init.sh [--force] [TARGET_DIR]
```

```text
Default:
  create .aidd only if absent
  create AGENTS.md only if absent
  create CLAUDE.md only if absent

--force:
  refresh .aidd from templates/aidd-overlay/.aidd
  still do not overwrite AGENTS.md or CLAUDE.md
```

## 検討した代替案

### 案 A: Always overwrite but document the behavior

- 概要: Keep the installer unchanged and tell users not to re-run it after editing `.aidd`.
- 却下理由: The current test reproduction showed a normal re-run erases local edits; relying on memory conflicts with the overlay's purpose as local working context.

### 案 B: Add backup files before overwriting

- 概要: Preserve `.aidd` as `.aidd.bak.<timestamp>` on every run.
- 却下理由: This creates extra local directories in target repos and still changes active files without explicit user intent.

## Open Questions

- N/A: the requested fixes are concrete.

## Review Notes

- Reviewer: user
- Result: approved
- Notes: User asked to modify the three review findings.

## Completion

- Completed: 2026-05-31
- Validation:
  - `uv run pytest tests/test_template.py` — passed, 5 tests.
  - `make lint` — passed.
  - `make test` — passed, 10 tests.
  - `git diff --check` — passed.
  - Targeted `rg` check for stale README/AGENTS/script strings — no matches.
- Related PR / commit: N/A, local changes only.
- Remaining follow-up: Optional: decide whether to expose a shorter user-level `aidd-init` command or shell alias.
