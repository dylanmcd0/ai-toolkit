#!/usr/bin/env bash
set -euo pipefail

if ! command -v rtk >/dev/null 2>&1; then
  echo "rtk is not installed."
  echo
  echo "Install options:"
  echo "  brew install rtk"
  echo "  curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh"
  echo "  cargo install --git https://github.com/rtk-ai/rtk"
  exit 1
fi

echo "Found $(rtk --version)"
echo "Initializing RTK globally for Codex..."
rtk init -g --codex

echo
echo "Done. Restart Codex, then test with:"
echo "  git status"
echo "  rtk gain"
