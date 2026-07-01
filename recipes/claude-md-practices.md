# Good CLAUDE.md Practices

`CLAUDE.md` should teach Claude how to work in a specific repository. Keep it short, factual, and operational.

## Include

- project purpose in 2-4 sentences
- key directories and ownership boundaries
- setup commands
- test commands
- lint and format commands
- common failure modes
- style preferences not enforced by tooling
- review expectations

## Avoid

- long product strategy documents
- duplicated README content
- vague preferences like “write clean code”
- stale command lists
- secrets, tokens, or private credentials

## Starter Template

```markdown
# CLAUDE.md

## Project Overview

Briefly describe what this repo does and who it serves.

## Commands

- Install: `...`
- Test: `...`
- Lint: `...`
- Format: `...`

## Architecture Notes

- `src/...` handles ...
- `scripts/...` handles ...

## Coding Preferences

- Prefer small, explicit functions over broad abstractions.
- Do not introduce new dependencies without explaining why.
- Keep changes focused on the requested task.

## Review Expectations

- Prioritize correctness, security, and maintainability.
- Flag YAGNI abstractions.
- Ignore formatting issues handled by tools.
```
