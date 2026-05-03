#!/usr/bin/env python3
"""Repository architecture linter.

Reads `[tool.repo-arch]` from pyproject.toml and enforces:

1. Layer dependency rule: each top-level directory under `src` may only import
   from the layers listed for it under `[tool.repo-arch.layers]`.
2. Provider boundary: libraries in `[tool.repo-arch.provider_only].libraries`
   may only be imported from files under any of `[tool.repo-arch].provider_dirs`.

Stdlib modules and the project's own internal packages are always allowed.

When `[tool.repo-arch].kind == "tbd"` (or no `layers` table is defined), layer
checks are skipped but provider-only checks still run.
"""

from __future__ import annotations

import ast
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_PATH = ROOT / "pyproject.toml"
PYTHON_SUFFIX = ".py"

STDLIB_MODULES = set(sys.stdlib_module_names) | {"__future__"}


class ConfigError(RuntimeError):
    pass


def main() -> int:
    try:
        config = load_config()
    except ConfigError as exc:
        print(f"ERROR: {exc}")
        return 1

    src_root = ROOT / config["src"]
    if not src_root.exists():
        print(f"lint_repo_rules: src root '{config['src']}' does not exist, nothing to lint")
        return 0

    errors: list[str] = []
    python_files = sorted(src_root.rglob(f"*{PYTHON_SUFFIX}"))
    internal_top_levels = collect_internal_top_levels(src_root)

    for file_path in python_files:
        imports = parse_imports(file_path, errors)
        file_layer = top_layer_of(file_path, src_root)

        for imported in imports:
            top_level = imported.split(".", maxsplit=1)[0]

            if is_stdlib(top_level) or top_level in internal_top_levels:
                check_layer_rule(file_path, file_layer, imported, src_root, config, errors)
                continue

            if top_level in config["provider_only"] and not is_in_provider_dir(file_path, src_root, config):
                errors.append(
                    f"{rel(file_path)} imports provider-only library '{top_level}' "
                    f"outside provider directories ({sorted(config['provider_dirs'])})"
                )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"lint_repo_rules: OK (kind={config['kind']}, files={len(python_files)})")
    return 0


def load_config() -> dict:
    if not PYPROJECT_PATH.exists():
        raise ConfigError("pyproject.toml not found at repository root")

    with PYPROJECT_PATH.open("rb") as fh:
        data = tomllib.load(fh)

    repo_arch = data.get("tool", {}).get("repo-arch", {})
    if not repo_arch:
        raise ConfigError("[tool.repo-arch] is missing from pyproject.toml")

    kind = repo_arch.get("kind", "tbd")
    src = repo_arch.get("src", "src")
    provider_dirs = set(repo_arch.get("provider_dirs", ["providers"]))
    layers_raw = repo_arch.get("layers", {}) or {}
    provider_only_raw = repo_arch.get("provider_only", {}) or {}
    provider_only = set(provider_only_raw.get("libraries", []))

    layers: dict[str, set[str]] = {}
    for layer, allowed in layers_raw.items():
        if not isinstance(allowed, list):
            raise ConfigError(f"[tool.repo-arch.layers].{layer} must be a list")
        layers[layer] = set(allowed) | {layer}

    return {
        "kind": kind,
        "src": src,
        "provider_dirs": provider_dirs,
        "layers": layers,
        "provider_only": provider_only,
    }


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

    current_parts = list(file_path.relative_to(ROOT).with_suffix("").parts)
    if not current_parts or node.level > len(current_parts):
        return module

    prefix = current_parts[: -node.level]
    if module:
        return ".".join([*prefix, *module.split(".")])
    return ".".join(prefix)


def top_layer_of(file_path: Path, src_root: Path) -> str | None:
    """Return the top-level layer directory name under `src_root` for `file_path`."""
    try:
        relative = file_path.relative_to(src_root)
    except ValueError:
        return None
    if len(relative.parts) < 2:
        return None
    return relative.parts[0]


def collect_internal_top_levels(src_root: Path) -> set[str]:
    """Top-level dirs under `src_root` are treated as internal packages.

    Note: when `pythonpath = ["src"]` (pytest), imports look like
    `from feature.foo import ...`, so the top-level token is the layer name.
    """
    return {child.name for child in src_root.iterdir() if child.is_dir()}


def is_stdlib(top_level: str) -> bool:
    return top_level in STDLIB_MODULES


def is_in_provider_dir(file_path: Path, src_root: Path, config: dict) -> bool:
    try:
        relative = file_path.relative_to(src_root)
    except ValueError:
        return False
    if not relative.parts:
        return False
    return relative.parts[0] in config["provider_dirs"]


def check_layer_rule(
    file_path: Path,
    file_layer: str | None,
    imported: str,
    src_root: Path,
    config: dict,
    errors: list[str],
) -> None:
    if not config["layers"]:
        return
    if file_layer is None or file_layer not in config["layers"]:
        return

    imported_top = imported.split(".", maxsplit=1)[0]
    if imported_top not in config["layers"]:
        return

    allowed = config["layers"][file_layer]
    if imported_top not in allowed:
        errors.append(
            f"{rel(file_path)} in layer '{file_layer}' imports forbidden layer "
            f"'{imported_top}' via '{imported}' (allowed: {sorted(allowed)})"
        )


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


if __name__ == "__main__":
    sys.exit(main())
