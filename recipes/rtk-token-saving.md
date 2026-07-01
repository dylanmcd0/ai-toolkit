# RTK Token-Saving Setup

RTK means [`rtk-ai/rtk`](https://github.com/rtk-ai/rtk): Rust Token Killer, a CLI proxy that compresses common development command output before it reaches an AI coding tool.

Use this recipe for Claude Code, Codex, and other agent tools where repeated shell output burns context.

## What RTK Does

RTK wraps or rewrites common commands so the agent sees compact, task-relevant output instead of raw logs. It is most useful for commands like:

- `git status`, `git diff`, `git log`
- `ls`, `find`, `grep`, `rg`, `cat`
- `pytest`, `cargo test`, `npm test`, `vitest`, `jest`
- linters, builds, Docker, GitHub CLI, and cloud CLI output

The upstream project describes RTK as a single Rust binary that filters and compresses command outputs with low overhead.

## Install

### Homebrew

```bash
brew install rtk
```

### Upstream Install Script

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

The upstream script installs to `~/.local/bin`, so make sure that directory is on your `PATH`.

### Cargo

```bash
cargo install --git https://github.com/rtk-ai/rtk
```

Avoid `cargo install rtk`; upstream warns that another crate named `rtk` exists on crates.io.

## Verify

```bash
rtk --version
rtk gain
```

## Initialize For Agents

### Claude Code / GitHub Copilot-style Hooks

```bash
rtk init -g
```

### Codex

```bash
rtk init -g --codex
```

### Other Supported Agents

```bash
rtk init -g --gemini
rtk init -g --agent cursor
rtk init -g --agent windsurf
```

Restart the AI tool after initialization.

## Usage Pattern

After hook setup, supported shell commands may be rewritten automatically. You can also call RTK directly:

```bash
rtk git status
rtk git diff
rtk read README.md
rtk grep "pattern" .
rtk pytest
rtk err npm test
rtk gain --graph
```

## Important Caveat

RTK hooks operate on shell/Bash commands. Built-in agent tools that read or search files directly may not pass through RTK. When you specifically want compact RTK output, use shell commands or call RTK directly.

## Toolkit Convention

- Keep RTK setup docs in this recipe.
- Keep install helpers in `scripts/`.
- Do not store RTK output snapshots in git unless they are intentionally curated examples.
- Use `context-snapshots/` for local context captures; it is ignored by git.
