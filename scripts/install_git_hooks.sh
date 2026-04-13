#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

git config core.hooksPath .githooks
echo "Configured git hooks path: .githooks"
echo "The repository linter will now run automatically on git commit."
