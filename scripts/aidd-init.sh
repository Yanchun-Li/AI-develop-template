#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: aidd-init.sh [TARGET_DIR]

Install the local AIDD overlay into an existing repository or directory.
When TARGET_DIR is omitted, the current git root is used if available;
otherwise the current directory is used.

The installer does not overwrite existing AGENTS.md or CLAUDE.md files.
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
template_root="$(cd "$script_dir/.." && pwd)"
overlay_root="$template_root/templates/aidd-overlay"

if [[ ! -d "$overlay_root/.aidd" ]]; then
  echo "error: overlay template not found at $overlay_root" >&2
  exit 1
fi

if [[ $# -gt 0 ]]; then
  target_dir="$1"
else
  target_dir="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
fi

mkdir -p "$target_dir"
target_dir="$(cd "$target_dir" && pwd)"

rsync -a "$overlay_root/.aidd/" "$target_dir/.aidd/"

if [[ -e "$target_dir/AGENTS.md" ]]; then
  echo "skip: AGENTS.md already exists"
else
  cp "$overlay_root/AGENTS.md" "$target_dir/AGENTS.md"
  echo "created: AGENTS.md"
fi

if [[ -e "$target_dir/CLAUDE.md" ]]; then
  echo "skip: CLAUDE.md already exists"
else
  cp "$overlay_root/CLAUDE.md" "$target_dir/CLAUDE.md"
  echo "created: CLAUDE.md"
fi

if git -C "$target_dir" rev-parse --git-dir >/dev/null 2>&1; then
  git_dir="$(git -C "$target_dir" rev-parse --absolute-git-dir)"
  exclude_path="$git_dir/info/exclude"
  mkdir -p "$(dirname "$exclude_path")"
  touch "$exclude_path"

  if ! grep -qxF ".aidd/" "$exclude_path"; then
    {
      printf "\n# Local AIDD overlay\n"
      printf ".aidd/\n"
      printf "AGENTS.md\n"
      printf "CLAUDE.md\n"
    } >> "$exclude_path"
  fi
fi

echo "AIDD overlay initialized in $target_dir"
