# CI.md

This note records how to validate work in the target repository.
The overlay does not install or replace CI by default.

## Basic Policy

- Treat the target repo's existing CI as authoritative.
- Prefer local commands that match CI.
- Do not add template workflows unless explicitly asked.
- If CI is failing, inspect the concrete failing job and logs before proposing fixes.

## Discovery Checklist

When taking over a task, check these places for validation commands:

1. README or contributor docs.
2. Makefile, package scripts, task runner config, or language-specific tooling.
3. `.github/workflows/` or the repo's CI provider config.
4. Nearby tests for the files being changed.

## Validation Notes

Record task-specific validation in the active task note:

```text
Command:
Result:
Reason this is sufficient:
Remaining gap:
```

If no automated validation exists, record the manual inspection performed and the risk that remains.
