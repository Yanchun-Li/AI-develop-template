#!/usr/bin/env python3
from __future__ import annotations

import sys

from hook_utils import edited_paths
from hook_utils import read_hook_input
from hook_utils import run_command


def main() -> int:
    data = read_hook_input()
    if any(str(path) == "pyproject.toml" for path in edited_paths(data)):
        return run_command(["uv", "lock", "--check"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
