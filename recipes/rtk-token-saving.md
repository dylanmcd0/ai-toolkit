# RTK Token-Saving Setup

This recipe captures the intended pattern for token/context saving across AI coding tools.

## Goal

Reduce repeated context by storing reusable repository guidance, prompts, and setup notes in predictable files.

## Suggested Structure

```text
recipes/
  rtk-token-saving.md
prompts/
  code-review-yagni.md
scripts/
  install-rtk-for-claude.sh
  save-codex-token-context.sh
context-snapshots/
  local files ignored by git
```

## What To Save

- stable repo architecture summaries
- repeated setup commands
- code review rubrics
- model/tool-specific preferences
- common troubleshooting notes

## What Not To Save

- secrets or API keys
- full dependency trees
- generated logs unless actively debugging
- stale decisions that no longer match the repo

## Workflow

1. Write durable instructions in Markdown.
2. Keep local/generated context under `context-snapshots/`.
3. Reference reusable prompts instead of pasting them repeatedly.
4. Periodically delete or refresh stale snapshots.
