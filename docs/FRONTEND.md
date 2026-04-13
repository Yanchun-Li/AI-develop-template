# FRONTEND.md

Frontend code should be testable, observable, and agent-drivable.

## Rules

- Keep UI state transitions explicit.
- Prefer components that can be exercised with browser automation.
- Expose stable selectors for end-to-end automation where appropriate.
- Document critical user journeys that must remain healthy.

## Validation

- UI changes should define expected states before and after interactions.
- When possible, pair UI changes with screenshot, DOM, or browser checks.
