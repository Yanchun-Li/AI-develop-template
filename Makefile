.PHONY: help init setup hooks lock-check lint fmt test clean

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
	uv run ruff check src scripts tests

fmt: ## Format and autofix Python files
	uv run ruff format src scripts tests
	uv run ruff check --fix src scripts tests

test: ## Run pytest
	uv run pytest

clean: ## Remove local Python caches
	rm -rf .ruff_cache .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
