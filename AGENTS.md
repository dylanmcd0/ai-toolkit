# Agent Guide

## Purpose

AI Toolkit is a small personal toolkit for AI coding workflows. It collects MCP
registry helpers, setup recipes, prompts, and operational notes. Keep it
docs-first and modular; do not turn it into a broad framework unless a workflow
has proven useful as a small script or recipe.

## Repository Map

- `tools/`: focused Python utilities, including MCP config helpers.
- `scripts/`: local setup and context-capture scripts.
- `recipes/`: practical Markdown playbooks.
- `prompts/`: reusable prompts and review rubrics.
- `config/`: example configuration files.
- `docs/`: background notes and longer references.
- `tests/`: tests for utilities when added.

## Commands

Use the smallest command that verifies the change:

```bash
python3 tools/mcp/mcp_config.py --help
python3 tools/mcp/mcp_config.py list
python3 -m pytest
```

If using the package entry point locally:

```bash
pip install -e .
mcp-tool --help
```

## Working Rules

1. Prefer small, explicit scripts and Markdown recipes over broad abstractions.
2. Keep examples copy-pastable and easy to adapt.
3. Do not introduce dependencies unless they remove meaningful complexity.
4. Keep the MCP registry format simple and client-agnostic.
5. Never commit secrets, tokens, machine-local paths, or personal config.

## Review Expectations

Prioritize correctness, maintainability, and practical usability. Flag YAGNI
abstractions and framework-heavy changes. Suggest the smallest useful
improvement. Ignore formatting-only issues unless no formatter/linter exists and
the formatting blocks readability.

## Git and Pull Requests

For substantive changes, create a focused branch and open a pull request. Use
an imperative Conventional Commit subject with one leading emoji:

```text
✨ feat: add MCP registry helper
🐛 fix: preserve client config fields
📝 docs: clarify Claude setup recipe
🧪 test: cover MCP config parsing
♻️ refactor: simplify install script
🔧 chore: update workflow tooling
```

Before requesting review:

1. Inspect the diff for secrets, machine-local paths, generated files, and
   unrelated changes.
2. Run the relevant script or test command, or state why it could not run.
3. Explain practical behavior changes and limits.
4. Use `.github/pull_request_template.md`; leave unchecked items visible with a
   short reason when validation is unavailable.

Use the GitHub CLI for pull requests when authentication is valid:

```bash
gh auth status
gh pr create --fill
```

If `gh auth status` fails, push the branch and report the compare URL instead
of implying that a PR was opened.

## Keeping This Useful

Keep this file short and verified. Put detailed procedures in `recipes/` or
`docs/`.
