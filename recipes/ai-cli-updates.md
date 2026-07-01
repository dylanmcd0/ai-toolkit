# AI CLI Updates

Use this recipe to keep local AI development CLIs current without guessing which ones auto-update.

## Recommended Local Setup

For this machine:

- Claude Code: native installer, usually auto-updates in the background.
- Codex CLI: Homebrew cask, update with Homebrew.
- RTK: Homebrew formula, update with Homebrew.

## One Command

```bash
scripts/update-ai-clis.sh
```

Preview without changing anything:

```bash
scripts/update-ai-clis.sh --dry-run
```

Skip post-update diagnostics:

```bash
scripts/update-ai-clis.sh --no-doctor
```

## Manual Commands

```bash
claude update
brew upgrade --cask codex
brew upgrade rtk
```

Then check:

```bash
claude --version
codex --version
rtk --version
claude doctor
codex doctor
rtk gain
```

## Notes

- Native Claude Code checks for updates on startup and periodically while running.
- Homebrew-installed Claude Code, Codex, and RTK should be updated through Homebrew.
- Restart open CLI/app sessions after updates so they pick up the new binary.
