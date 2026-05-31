.PHONY: help init setup hooks lock-check lint fmt test clean skills-sync skills-check

UV_SYNC_FLAGS := --all-extras --all-groups

help: ## Show this help
	@grep -E '^[a-zA-Z_/-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

init: setup hooks ## Install Python deps and configure git hooks

setup: ## Install Python dependencies with uv
	@command -v uv >/dev/null 2>&1 || { \
		echo "uv is required. Install it first: https://docs.astral.sh/uv/getting-started/installation/"; \
		exit 1; \
	}
	uv sync $(UV_SYNC_FLAGS)

hooks: ## Configure repository git hooks
	bash scripts/install_git_hooks.sh

lock-check: ## Check uv.lock is in sync with pyproject.toml
	uv lock --check

lint: ## Run repository and Python linters
	uv run python scripts/lint_repo_rules.py
	uv run ruff format --check src scripts tests .claude/hooks
	uv run ruff check src scripts tests .claude/hooks

fmt: ## Format and autofix Python files
	uv run ruff format src scripts tests .claude/hooks
	uv run ruff check --fix src scripts tests .claude/hooks

test: ## Run pytest
	uv run pytest

skills-sync: ## Sync skill dirs .claude/skills/*/ -> .codex/skills/ (canonical source is .claude/skills; per-tool README.md kept)
	@mkdir -p .codex/skills
	@for d in .claude/skills/*/; do \
		name=$$(basename "$$d"); \
		rm -rf ".codex/skills/$$name"; \
		cp -R "$$d" ".codex/skills/$$name"; \
		echo "synced $$name"; \
	done
	@echo "Synced .claude/skills/*/ -> .codex/skills/. Restart Codex to pick up changes."

skills-check: ## Verify .codex/skills skill dirs match .claude/skills (drift guard; README.md excluded)
	@diff -r -x README.md .claude/skills .codex/skills >/dev/null 2>&1 && echo "OK: .codex/skills is in sync with .claude/skills" || { \
		echo "DRIFT: .codex/skills differs from .claude/skills. Run 'make skills-sync'."; \
		diff -rq -x README.md .claude/skills .codex/skills || true; \
		exit 1; \
	}

clean: ## Remove local Python caches
	rm -rf .ruff_cache .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
