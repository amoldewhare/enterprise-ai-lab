# Article 4 — Enterprise API Connectivity

## Experiment

Connect the Transfer Review Assistant to a fictional
NorthStar Account System through a local HTTP API.

## Architecture

LLM → Agent Runtime → get_account tool → HTTPX
→ FastAPI → Account System of Record

## Observed Results

### Scenario A: Eligible Account

- Account: NS-48291
- Account status: ACTIVE
- Transfer eligible: True
- Policy: TP-101
- Missing requirements: []
- Recommendation: READY
- Human approval remains required.

### Scenario B: Ineligible Account

- Account: NS-48292
- Account status: ACTIVE
- Transfer eligible: False
- Policy: TP-101
- Missing requirements: []
- Recommendation: BLOCKED
- Agent recommended human review.

## Key Observation

Complete transfer documentation does not establish
account eligibility.

The agent retrieved account state through an HTTP-backed
tool and used it alongside transfer policy information.

## Limitations

- NorthStar is a fictional local API.
- Results reflect observed individual runs, not statistical reliability.
- Account eligibility is interpreted by the LLM.
- Deterministic enforcement of eligibility is not yet implemented.
- No financial transaction was executed.
