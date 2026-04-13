# SECURITY.md

Security requirements must be explicit and local to the repository.

## Baseline

- Secrets must not be committed.
- External access should pass through reviewed provider modules.
- Authentication and authorization rules must be documented near the owning domain.
- Dangerous operations should require explicit interfaces and auditability where possible.

## Review Questions

- Which data is sensitive?
- Which boundary enforces access control?
- Which provider talks to the outside world?
- What evidence shows the control is working?
