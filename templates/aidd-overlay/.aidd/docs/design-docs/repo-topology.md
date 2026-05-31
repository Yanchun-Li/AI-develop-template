# Local Overlay Topology

This document describes how the AIDD overlay sits beside an existing repository.

```text
target-repo/
├── AGENTS.md                  # local bridge for Codex
├── CLAUDE.md                  # local bridge for Claude Code
├── .aidd/
│   ├── RULES.md               # local overlay rules
│   └── docs/
│       ├── tasks/
│       │   ├── active/
│       │   └── completed/
│       ├── exec-plans/
│       │   ├── active/
│       │   └── completed/
│       ├── product-specs/
│       ├── adr/
│       ├── design-docs/
│       ├── STATUS.md
│       └── WORKFLOW.md
└── <existing repo files>
```

## Boundary

- Existing repo files remain the implementation source of truth.
- `.aidd/` records local planning, task state, and decision context.
- The overlay does not define or enforce a repository architecture.
- The overlay does not install CI, hooks, skills, or agents by default.

## Agent Reading Order

1. Root `AGENTS.md` or `CLAUDE.md`.
2. `.aidd/RULES.md`.
3. `.aidd/docs/WORKFLOW.md`.
4. `.aidd/docs/STATUS.md`.
5. Active task or plan notes.
6. Existing repo README, tests, CI, and nearby docs.
