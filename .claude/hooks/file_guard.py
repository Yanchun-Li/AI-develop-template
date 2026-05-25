#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from hook_utils import block
from hook_utils import edited_paths
from hook_utils import is_existing_file
from hook_utils import load_repo_arch_kind
from hook_utils import read_hook_input


def is_under(path: Path, *parts: str) -> bool:
    return path.parts[: len(parts)] == parts


def is_immutable_existing_doc(path: Path) -> bool:
    if path.name == "README.md":
        return False
    if not is_existing_file(path):
        return False
    if is_under(path, "docs", "architectures"):
        return True
    if is_under(path, "docs", "exec-plans", "completed"):
        return True
    if is_under(path, "docs", "adr") and path.suffix == ".md":
        return True
    return False


def main() -> int:
    data = read_hook_input()
    paths = edited_paths(data)
    if not paths:
        return 0

    kind = load_repo_arch_kind()
    for path in paths:
        if kind == "tbd" and is_under(path, "src"):
            return block(
                "Blocked: pyproject.toml [tool.repo-arch].kind is 'tbd', so src/** must not be edited. "
                "Choose an architecture in docs/architectures/ and update pyproject.toml first."
            )
        if is_immutable_existing_doc(path):
            return block(
                f"Blocked: {path} is an immutable existing doc. "
                "Create a new ADR/plan or superseding document instead of rewriting history."
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
