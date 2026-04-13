# RELIABILITY.md

Reliability requirements must be concrete enough for an agent to test.

## Guidance

- Turn performance goals into measurable thresholds.
- Define startup, shutdown, and recovery expectations.
- Prefer assertions based on logs, metrics, and traces where possible.

## Example Targets

- service startup completes under a fixed threshold
- key user journeys stay under latency budgets
- no critical background job fails silently
