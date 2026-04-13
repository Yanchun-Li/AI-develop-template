#!/usr/bin/env python3
"""Repository architecture linter for the harness engineering template."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = ROOT / "src"
DOMAINS_ROOT = SRC_ROOT / "domains"
PROVIDERS_ROOT = SRC_ROOT / "providers"
LAYER_ORDER = ["types", "config", "repo", "service", "runtime", "ui"]
LAYER_INDEX = {name: idx for idx, name in enumerate(LAYER_ORDER)}

# Configure raw vendor libraries that must only be imported via providers.
PROVIDER_ONLY_LIBRARIES = {
    "openai",
    "anthropic",
    "requests",
    "httpx",
    "sqlalchemy",
    "psycopg",
    "redis",
    "boto3",
    "structlog",
    "loguru",
    "prometheus_client",
    "opentelemetry",
}

INTERNAL_PREFIXES = {"src", ""}
PYTHON_SUFFIX = ".py"


def main() -> int:
    errors: list[str] = []

    if not SRC_ROOT.exists():
        print("lint_repo_rules: no src/ directory found, nothing to lint")
        return 0

    python_files = sorted(SRC_ROOT.rglob(f"*{PYTHON_SUFFIX}"))
    external_import_usage: dict[str, list[Path]] = {}

    for file_path in python_files:
        imports = parse_imports(file_path, errors)
        location = classify_file(file_path)

        for imported_module in imports:
            top_level = imported_module.split(".")[0]

            if location is not None and is_internal_domain_import(imported_module):
                maybe_add_layer_error(file_path, location, imported_module, errors)

            if top_level and top_level not in INTERNAL_PREFIXES and file_path.is_relative_to(SRC_ROOT):
                external_import_usage.setdefault(top_level, []).append(file_path)
                if top_level in PROVIDER_ONLY_LIBRARIES and not file_path.is_relative_to(PROVIDERS_ROOT):
                    errors.append(
                        f"{rel(file_path)} imports provider-only library '{top_level}' outside src/providers/"
                    )

    for library, paths in sorted(external_import_usage.items()):
        unique_paths = sorted({rel(path) for path in paths})
        non_provider_paths = [
            path for path in paths if not path.is_relative_to(PROVIDERS_ROOT)
        ]
        if len(non_provider_paths) > 1:
            errors.append(
                "external library "
                f"'{library}' is imported directly in multiple non-provider files: "
                + ", ".join(sorted({rel(path) for path in non_provider_paths}))
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("lint_repo_rules: OK")
    return 0


def parse_imports(file_path: Path, errors: list[str]) -> list[str]:
    try:
        tree = ast.parse(file_path.read_text(), filename=str(file_path))
    except SyntaxError as exc:
        errors.append(f"{rel(file_path)} has invalid Python syntax: {exc.msg}")
        return []

    imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = resolve_import_from(file_path, node)
            if module:
                imports.append(module)

    return imports


def resolve_import_from(file_path: Path, node: ast.ImportFrom) -> str | None:
    module = node.module or ""
    if node.level == 0:
        return module

    current_parts = module_path_parts(file_path)
    if not current_parts:
        return module

    if node.level > len(current_parts):
        return module

    prefix = current_parts[:-node.level]
    if module:
        return ".".join(prefix + module.split("."))
    return ".".join(prefix)


def module_path_parts(file_path: Path) -> list[str]:
    relative = file_path.relative_to(ROOT)
    without_suffix = relative.with_suffix("")
    return list(without_suffix.parts)


def classify_file(file_path: Path) -> tuple[str, str] | None:
    if not file_path.is_relative_to(DOMAINS_ROOT):
        return None

    relative = file_path.relative_to(DOMAINS_ROOT)
    parts = relative.parts
    if len(parts) < 3:
        return None

    domain = parts[0]
    layer = parts[1]
    if layer not in LAYER_INDEX:
        return None
    return domain, layer


def is_internal_domain_import(module_name: str) -> bool:
    return module_name.startswith("src.domains.")


def maybe_add_layer_error(
    file_path: Path,
    location: tuple[str, str],
    imported_module: str,
    errors: list[str],
) -> None:
    match = re.match(r"src\.domains\.([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)", imported_module)
    if not match:
        return

    imported_domain, imported_layer = match.groups()
    current_domain, current_layer = location

    if imported_domain != current_domain:
        return
    if imported_layer not in LAYER_INDEX:
        return
    if LAYER_INDEX[imported_layer] > LAYER_INDEX[current_layer]:
        errors.append(
            f"{rel(file_path)} in layer '{current_layer}' imports later layer "
            f"'{imported_layer}' via '{imported_module}'"
        )


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


if __name__ == "__main__":
    sys.exit(main())
