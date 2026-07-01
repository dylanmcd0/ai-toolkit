# Code Review Prompt: YAGNI + Maintainability

Use this when reviewing pull requests where the main risk is overengineering, unclear abstractions, or hidden maintenance cost.

## Prompt

Review this change with a strong bias toward simplicity and future maintenance.

Focus on:

1. **YAGNI** — call out abstractions, options, configuration, or layers that are not justified by current requirements.
2. **Correctness** — identify behavior that may fail in realistic edge cases.
3. **Readability** — flag code that requires too much context to understand.
4. **Operational risk** — note migrations, secrets, permissions, deploy assumptions, or missing rollback paths.
5. **Tests** — identify the smallest useful tests that would increase confidence.

For each issue, include:

- severity: `blocking`, `important`, or `minor`
- the concrete location
- why it matters
- a simpler alternative when possible

Do not reward cleverness unless it directly reduces user or maintainer burden.
