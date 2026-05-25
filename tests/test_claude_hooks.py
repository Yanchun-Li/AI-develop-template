from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS = ROOT / ".claude" / "hooks"


def run_hook(script: str, payload: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(HOOKS / script)],
        input=json.dumps(payload),
        text=True,
        cwd=ROOT,
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT)},
        capture_output=True,
        check=False,
    )


def test_file_guard_blocks_src_when_architecture_is_tbd() -> None:
    result = run_hook("file_guard.py", {"tool_input": {"file_path": str(ROOT / "src/example.py")}})

    assert result.returncode == 2
    assert "kind is 'tbd'" in result.stderr


def test_file_guard_blocks_existing_immutable_docs() -> None:
    result = run_hook(
        "file_guard.py",
        {"tool_input": {"file_path": str(ROOT / "docs/architectures/index.md")}},
    )

    assert result.returncode == 2
    assert "immutable existing doc" in result.stderr


def test_file_guard_allows_new_adr_files() -> None:
    result = run_hook("file_guard.py", {"tool_input": {"file_path": str(ROOT / "docs/adr/0001-new.md")}})

    assert result.returncode == 0


def test_command_guard_blocks_uncontrolled_install_commands() -> None:
    blocked_commands = [
        "pip install requests",
        "python3 -m pip install requests",
        "uv add fastapi",
        "echo ok; uv add requests",
        "cd app&&uv add requests",
        "npm install",
        "npx prettier --write .",
        "pnpm add prettier",
    ]

    for command in blocked_commands:
        result = run_hook("command_guard.py", {"tool_input": {"command": command}})
        assert result.returncode == 2, command
        assert "Blocked install command" in result.stderr


def test_command_guard_allows_pinned_uv_and_pnpm_adds() -> None:
    allowed_commands = [
        "uv add fastapi==0.115.6",
        "uv add --dev pytest==9.0.3",
        "pnpm add prettier@3.6.2",
        "make lint",
    ]

    for command in allowed_commands:
        result = run_hook("command_guard.py", {"tool_input": {"command": command}})
        assert result.returncode == 0, command
