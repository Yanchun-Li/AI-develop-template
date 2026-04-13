# QUALITY_SCORE.md

Quality should be visible and tracked over time.

## Suggested Scale

- `Q0`: undefined or unverified
- `Q1`: works in happy path only
- `Q2`: basic validation exists
- `Q3`: reliable under normal use
- `Q4`: strong automated validation and observability

## Track By Domain

Record quality for each business domain and each architectural layer.

Example table:

| Area | Score | Notes | Next action |
| --- | --- | --- | --- |
| billing/service | Q1 | basic path only | add failure tests |
| auth/runtime | Q2 | health checks exist | add trace assertions |
