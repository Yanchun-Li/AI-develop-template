# DESIGN.md

Design should optimize for agent legibility before cleverness.

## Principles

- Prefer explicit naming over compression.
- Prefer stable local abstractions over opaque third-party magic.
- Prefer repository-local knowledge over off-repo tribal knowledge.
- Prefer boring, composable technology when it improves reasoning and maintenance.

## Design Review Questions

- Can a new agent discover this design from the repository alone?
- Is the boundary expressed in code and docs, not only in prompts?
- Can the behavior be validated mechanically?
