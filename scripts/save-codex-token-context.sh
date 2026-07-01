#!/usr/bin/env bash
set -euo pipefail

output_dir="${1:-context-snapshots}"
mkdir -p "$output_dir"

snapshot="$output_dir/codex-context-$(date +%Y%m%d-%H%M%S).md"

{
  echo "# Codex Context Snapshot"
  echo
  echo "Generated: $(date)"
  echo
  echo "## Repository"
  git rev-parse --show-toplevel 2>/dev/null || pwd
  echo
  echo "## Current Branch"
  git branch --show-current 2>/dev/null || true
  echo
  echo "## Status"
  git status --short 2>/dev/null || true
  echo
  echo "## Files"
  find . -maxdepth 3 -type f \
    -not -path './.git/*' \
    -not -path './context-snapshots/*' \
    -not -path './tokens/*' \
    | sort
} > "$snapshot"

echo "Saved Codex context snapshot to $snapshot"
