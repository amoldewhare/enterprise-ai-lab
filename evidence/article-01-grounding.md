# Article 01 Evidence — Grounding Comparison

This experiment compares the behavior of the same AI-assisted transfer-review system with and without access to an authoritative transfer policy.

The experiment uses the same fictional transfer case, prompt builder, model provider, structured output schema, and application code in both runs.

The experimental variable is access to the transfer-policy tool:

- **BEFORE:** No policy tool is available to the agent.
- **AFTER:** The agent has access to `get_transfer_policy()`, which returns fictional policy `TP-101`.

The purpose of this experiment is not to benchmark model quality. It is to observe how access to authoritative enterprise context changes the basis of the model's recommendation.

## Experimental Controls

The following remained the same across both runs:

- Fictional transfer case
- Review prompt
- OpenAI model provider
- Agent instructions
- Structured `TransferReviewResult` output
- Model execution path

Only one capability changed:

| Run | Policy Tool Access |
| --- | --- |
| BEFORE | None |
| AFTER | `get_transfer_policy()` returning `TP-101` |

This isolates policy access as the architectural variable being examined.

## BEFORE — No Policy Tool

The baseline provider was created with no agent tools:

```python
baseline_provider = OpenAIProvider(
    agent_tools=[]
)
```

### Observed Agent Execution

```text
MessageOutputItem
```

No tool call occurred.

### Observed Result

```text
status='BLOCKED'
policy_id='asset-transfer-review'
missing_requirements=[
    'Receiving custodian/account details are not provided',
    'Transfer form completeness beyond account number and signature is unverified',
    'Required transfer method/registration and any medallion or custodian-specific requirements are not confirmed'
]
recommended_action='Obtain and verify the receiving account details and complete transfer-form requirements; route the case for human operations approval before submission or processing.'
reason='The case includes identity, statement, account number, and signature documentation, but lacks sufficient receiving-account and completeness information to determine transfer readiness.'
```

### Observation

The model identified additional requirements that were not specified in the transfer case or supplied through an authoritative policy source, including receiving-account details and possible medallion or custodian-specific requirements.

The model also produced `policy_id='asset-transfer-review'`, even though no policy source was available to the agent in this run.

These recommendations may be plausible in a real asset-transfer process, but this experiment did not provide evidence establishing them as requirements.

## AFTER — TP-101 Policy Tool Available

The grounded provider was created with access to the transfer-policy tool:

```python
grounded_provider = OpenAIProvider(
    agent_tools=[get_transfer_policy]
)
```

### Observed Agent Execution

```text
ToolCallItem
ToolCallOutputItem
MessageOutputItem
```

The agent requested the policy tool, the tool returned the policy information, and the model then produced its final structured response.

### Observed Result

```text
status='READY'
policy_id='TP-101'
missing_requirements=[]
recommended_action='Case appears complete for document requirements. Obtain required human approval before proceeding; do not execute automatically.'
reason='The transfer form includes the source account number and customer signature, and a current brokerage statement is listed among the documents received.'
```

### Observation

With access to `get_transfer_policy()`, the agent retrieved `TP-101` and based its recommendation on the requirements supplied by that policy.

The resulting recommendation referenced the source account number, customer signature, and brokerage statement—the requirements defined by `TP-101`—rather than introducing the additional requirements observed in the baseline run.

## What This Experiment Demonstrates

In this observed run, access to an authoritative policy source materially changed the model's recommendation.

Without policy access, the model produced plausible additional requirements without a supplied authoritative basis.

With policy access, the agent retrieved `TP-101` and produced a recommendation grounded in the requirements returned by that tool.

The experiment illustrates an important distinction for enterprise AI systems:

> Plausibility is not the same as authority.

## What This Experiment Does Not Demonstrate

This experiment does **not** establish that:

- Tool access eliminates hallucinations.
- A tool-backed response is automatically correct.
- `TP-101` represents a complete real-world asset-transfer policy.
- Grounding alone makes an AI system production-ready.
- The observed behavior will occur identically on every model run.
- One experiment is sufficient to measure model reliability.

This is a single controlled observation using a fictional workflow and fictional policy. Broader reliability claims require repeatable evaluation across multiple cases and runs.

## Reproducing the Experiment

The comparison can be run from the repository root with:

```bash
python -m experiments.grounding_comparison
```

The experiment creates two `OpenAIProvider` instances:

```text
Baseline  → agent_tools=[]
Grounded  → agent_tools=[get_transfer_policy]
```

Both providers receive the same fictional transfer case and review prompt. The experiment then prints the agent execution lifecycle and structured result for each run.

Because model generation is probabilistic, future runs may not produce identical wording or recommendations. The evidence above records the behavior observed during this run.
