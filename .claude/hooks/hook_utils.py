from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()


def read_hook_input() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"Hook skipped: invalid JSON input: {exc}", file=sys.stderr)
        return {}


def tool_input(data: dict[str, Any]) -> dict[str, Any]:
    value = data.get("tool_input")
    return value if isinstance(value, dict) else {}


def rel_path(path_value: str | None) -> Path | None:
    if not path_value:
        return None
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    try:
        return path.resolve().relative_to(ROOT)
    except ValueError:
        return None


def edited_paths(data: dict[str, Any]) -> list[Path]:
    input_data = tool_input(data)
    candidates: list[str] = []
    for key in ("file_path", "path"):
        value = input_data.get(key)
        if isinstance(value, str):
            candidates.append(value)

    paths: list[Path] = []
    for candidate in candidates:
        path = rel_path(candidate)
        if path is not None and path not in paths:
            paths.append(path)
    return paths


def is_existing_file(path: Path) -> bool:
    return (ROOT / path).exists()


def load_repo_arch_kind() -> str:
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.exists():
        return "tbd"

    in_repo_arch = False
    for raw_line in pyproject.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            in_repo_arch = line == "[tool.repo-arch]"
            continue
        if in_repo_arch and line.startswith("kind") and "=" in line:
            return line.split("=", maxsplit=1)[1].strip().strip('"').strip("'")
    return "tbd"


def run_command(args: list[str]) -> int:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def block(message: str) -> int:
    print(message, file=sys.stderr)
    return 2
