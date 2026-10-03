# Article 03 — Context Retrieval Evidence

## Experiment 1 — Opaque Policy ID Lookup

The transfer case identified the business context as:

- Transfer type: Full Account Transfer

The available tool required the LLM to provide a policy ID:

get_transfer_policy(policy_id)

The LLM requested:

get_transfer_policy("asset_transfer_review")

No matching policy existed, so the tool returned an empty result.

The final recommendation was BLOCKED and included requirements that were not present in the enterprise policy repository.

### Observation

Giving the LLM access to an enterprise knowledge tool did not guarantee that it could retrieve the correct context when the tool required an opaque identifier that the LLM had not been given.


## Experiment 2 — Searchable Policy Context

The policy tool was changed from an opaque ID lookup to:

search_transfer_policies(query)

The transfer case and agent instructions were not changed.

The LLM generated a search query using information from the transfer case.

The simple deterministic search returned three candidate policies:

- TP-101 — Full Account Transfer Requirements
- TP-102 — Partial Account Transfer Requirements
- TP-103 — Retirement Account Transfer Requirements

The LLM selected TP-101 as the applicable policy and evaluated the transfer case against its requirements.

Observed result:

- Status: READY
- Policy: TP-101
- Missing requirements: None

The application then required explicit human approval before the controlled transfer-processing function executed.

### Observation

The LLM did not need to know the opaque enterprise policy identifier in advance.

When given discoverable enterprise context, it could use the business information in the transfer case to identify the applicable policy.

The retrieval implementation used in this experiment is intentionally simple and returned multiple candidate policies. This experiment does not establish that this retrieval approach would scale to a large enterprise policy repository.