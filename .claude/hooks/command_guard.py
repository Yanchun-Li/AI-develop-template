#!/usr/bin/env python3
from __future__ import annotations

import re
import shlex
import sys

from hook_utils import block
from hook_utils import read_hook_input
from hook_utils import tool_input

PINNED_SPEC_RE = re.compile(r"^[A-Za-z0-9_.-]+(\[[^\]]+\])?==[^\s]+$")
PNPM_PINNED_RE = re.compile(r"^(@[A-Za-z0-9_.-]+/)?[A-Za-z0-9_.-]+@[0-9][^\s]*$")
UV_OPTIONS_WITH_VALUES = {"--group", "--optional", "--python", "--script", "--index", "--default-index"}
PNPM_OPTIONS_WITH_VALUES = {"--filter", "--workspace-root", "--dir", "-C", "--config"}


def split_commands(command: str) -> list[list[str]]:
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return []

    commands: list[list[str]] = []
    current: list[str] = []
    separators = {"&&", "||", ";", "|"}
    for token in tokens:
        if token in separators:
            if current:
                commands.append(current)
                current = []
        else:
            current.append(token)
    if current:
        commands.append(current)
    return commands


def package_args(args: list[str], options_with_values: set[str]) -> list[str]:
    packages: list[str] = []
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if not arg:
            continue
        if arg in options_with_values:
            skip_next = True
            continue
        if arg.startswith("-"):
            continue
        packages.append(arg)
    return packages


def has_pinned_python_package(args: list[str]) -> bool:
    packages = package_args(args, UV_OPTIONS_WITH_VALUES)
    return bool(packages) and all(PINNED_SPEC_RE.match(package) for package in packages)


def has_pinned_node_package(args: list[str]) -> bool:
    packages = package_args(args, PNPM_OPTIONS_WITH_VALUES)
    return bool(packages) and all(PNPM_PINNED_RE.match(package) for package in packages)


def violation(tokens: list[str]) -> str | None:
    if not tokens:
        return None

    executable = tokens[0]
    args = tokens[1:]
    reason = None

    if executable in {"pip", "pip3"} and args[:1] == ["install"]:
        reason = "Use uv with pinned versions instead of pip install, for example: uv add package==x.y.z"
    elif executable in {"python", "python3"} and len(args) >= 3 and args[:3] == ["-m", "pip", "install"]:
        reason = "Use uv with pinned versions instead of python -m pip install, for example: uv add package==x.y.z"
    elif executable == "uv" and args[:1] == ["add"] and not has_pinned_python_package(args[1:]):
        reason = "uv add must pin package versions, for example: uv add fastapi==0.115.6"
    elif executable == "npm" and args and args[0] in {"install", "i"}:
        reason = (
            "This template uses uv by default. Add Node tooling only after documenting "
            "the package manager and pinning dependency versions."
        )
    elif executable == "npx":
        reason = (
            "npx downloads and executes external code. Add the tool as a pinned "
            "dev dependency and run it through a project script."
        )
    elif executable == "pnpm" and args[:1] == ["add"] and not has_pinned_node_package(args[1:]):
        reason = "pnpm add must use explicit versions, for example: pnpm add prettier@3.6.2"

    return reason


def main() -> int:
    data = read_hook_input()
    command = tool_input(data).get("command")
    if not isinstance(command, str) or not command.strip():
        return 0

    for tokens in split_commands(command):
        reason = violation(tokens)
        if reason:
            return block(f"Blocked install command: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
