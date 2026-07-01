#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
RUN_DOCTORS=1

usage() {
  cat <<'USAGE'
Usage: scripts/update-ai-clis.sh [--dry-run] [--no-doctor]

Updates local AI CLI tools when installed:
  - Claude Code: prefers native `claude update`; falls back to Homebrew/WinGet hints.
  - Codex CLI: uses Homebrew when installed as `codex` cask; otherwise tries `codex update`.
  - RTK: uses Homebrew when installed as `rtk`; otherwise prints manual guidance.

Options:
  --dry-run     Print what would run without updating.
  --no-doctor   Skip post-update doctor/verification commands.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      ;;
    --no-doctor)
      RUN_DOCTORS=0
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

run() {
  echo "+ $*"
  if [[ "$DRY_RUN" -eq 0 ]]; then
    "$@"
  fi
}

have() {
  command -v "$1" >/dev/null 2>&1
}

brew_has_cask() {
  have brew && brew list --cask "$1" >/dev/null 2>&1
}

brew_has_formula() {
  have brew && brew list --formula "$1" >/dev/null 2>&1
}

print_version() {
  local name="$1"
  shift
  if have "$1"; then
    echo "${name}: $($@ 2>/dev/null || true)"
  else
    echo "${name}: not installed"
  fi
}

echo "== Current versions =="
print_version "Claude Code" claude claude --version
print_version "Codex" codex codex --version
print_version "RTK" rtk rtk --version
echo

if have claude; then
  echo "== Updating Claude Code =="
  if brew_has_cask claude-code; then
    run brew upgrade --cask claude-code
  elif brew_has_cask claude-code@latest; then
    run brew upgrade --cask claude-code@latest
  elif have winget; then
    echo "If Claude Code was installed with WinGet, run: winget upgrade Anthropic.ClaudeCode"
    echo "Otherwise, native Claude Code usually auto-updates; forcing native update now."
    run claude update
  else
    run claude update
  fi
else
  echo "== Claude Code =="
  echo "claude not found; install with: curl -fsSL https://claude.ai/install.sh | bash"
fi
echo

if have codex; then
  echo "== Updating Codex =="
  if brew_has_cask codex; then
    run brew upgrade --cask codex
  elif have npm && npm list -g @openai/codex --depth=0 >/dev/null 2>&1; then
    run npm update -g @openai/codex
  else
    run codex update
  fi
else
  echo "== Codex =="
  echo "codex not found; install with: brew install --cask codex"
fi
echo

if have rtk; then
  echo "== Updating RTK =="
  if brew_has_formula rtk; then
    run brew upgrade rtk
  else
    echo "rtk is installed, but not via Homebrew formula 'rtk'."
    echo "Update based on install method, e.g. cargo install --git https://github.com/rtk-ai/rtk"
  fi
else
  echo "== RTK =="
  echo "rtk not found; install with: brew install rtk"
fi
echo

if [[ "$RUN_DOCTORS" -eq 1 ]]; then
  echo "== Post-update checks =="
  have claude && run claude doctor || true
  have codex && run codex doctor || true
  have rtk && run rtk gain || true
fi

echo
echo "Done. Restart any open Claude Code/Codex sessions to pick up updated binaries."
