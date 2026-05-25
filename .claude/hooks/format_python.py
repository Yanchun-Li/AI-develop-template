#!/usr/bin/env python3
from __future__ import annotations

import sys

from hook_utils import ROOT
from hook_utils import edited_paths
from hook_utils import read_hook_input
from hook_utils import run_command


def main() -> int:
    data = read_hook_input()
    for path in edited_paths(data):
        if path.suffix == ".py" and (ROOT / path).exists():
            return run_command(["uv", "run", "ruff", "format", str(path)])
    return 0


if __name__ == "__main__":
    sys.exit(main())
