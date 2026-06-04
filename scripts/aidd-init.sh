#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: aidd-init.sh [--force] [TARGET_DIR]

Install the local AIDD overlay into an existing repository or directory.
When TARGET_DIR is omitted, the current git root is used if available;
otherwise the current directory is used.

By default, the installer does not overwrite existing .aidd, AGENTS.md,
or CLAUDE.md files. Use --force to refresh .aidd from the template.
AGENTS.md and CLAUDE.md are never overwritten.
USAGE
}

force=0
target_dir=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h | --help)
      usage
      exit 0
      ;;
    --force)
      force=1
      shift
      ;;
    -*)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [[ -n "$target_dir" ]]; then
        echo "error: only one TARGET_DIR may be provided" >&2
        usage >&2
        exit 1
      fi
      target_dir="$1"
      shift
      ;;
  esac
done

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
template_root="$(cd "$script_dir/.." && pwd)"
overlay_root="$template_root/templates/aidd-overlay"

if [[ ! -d "$overlay_root/.aidd" ]]; then
  echo "error: overlay template not found at $overlay_root" >&2
  exit 1
fi

if [[ -z "$target_dir" ]]; then
  target_dir="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
fi

mkdir -p "$target_dir"
target_dir="$(cd "$target_dir" && pwd)"

if [[ -e "$target_dir/.aidd" && "$force" -ne 1 ]]; then
  echo "skip: .aidd already exists (use --force to refresh it)"
else
  rsync -a "$overlay_root/.aidd/" "$target_dir/.aidd/"
  echo "synced: .aidd"
fi

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
