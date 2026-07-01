# Claude Code Review Setup

Use this recipe to make Claude useful and consistent during code review.

## Goals

- Make review expectations explicit.
- Reduce generic feedback.
- Bias Claude toward practical, repository-specific comments.
- Keep review output easy for humans to triage.

## Recommended Files

- `CLAUDE.md` — repository behavior, commands, and review preferences.
- `.github/pull_request_template.md` — context authors should provide.
- `prompts/code-review-yagni.md` — reusable review prompt.

## Review Prompt Pattern

Ask Claude to:

1. inspect the diff before suggesting changes
2. separate blocking issues from polish
3. cite exact files and lines
4. avoid speculative rewrites
5. suggest the smallest safe fix

## Suggested Review Command

```text
Review this PR using the repository instructions in CLAUDE.md.
Prioritize correctness, security, maintainability, and YAGNI.
Return only actionable findings, grouped by severity.
If no blocking issues exist, say so clearly.
```

## Anti-Patterns

- Asking for a broad “make this better” review.
- Accepting architecture rewrites without a concrete bug or requirement.
- Letting Claude comment on style already enforced by formatter/linter.
- Mixing product feedback and code review in one pass.
