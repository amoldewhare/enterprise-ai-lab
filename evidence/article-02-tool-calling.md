# Article 2 Evidence — Tool-Calling Lifecycle

## Experiment

The experiment is implemented in:

`experiments/tool_call_lifecycle.py`

It uses the existing fictional asset-transfer case, transfer-review prompt, and `OpenAIProvider`.

The provider registers the existing `get_transfer_policy` function tool with the Transfer Review Assistant.

The experiment calls:

```python
result = provider.generate(prompt)
```

The experiment does not call `get_transfer_policy()` directly.

## Observed Agent Execution

Running:

```bash
python -m experiments.tool_call_lifecycle
```

produced:

```text
===== AGENT EXECUTION =====
ToolCallItem
ToolCallOutputItem
MessageOutputItem

===== FINAL OUTPUT =====
status='READY' policy_id='TP-101' missing_requirements=[] recommended_action='Proceed to human operations review; do not authorize or execute the transfer automatically.' reason='The transfer form includes the source account number and customer signature, and a current brokerage statement was received. All stated requirements are satisfied.'
```

## What Was Observed

The agent execution contained three observable runtime items:

1. `ToolCallItem`
2. `ToolCallOutputItem`
3. `MessageOutputItem`

The final structured result referenced fictional policy `TP-101` and returned the case as `READY`.

This records one observed execution of the experiment. It should not be interpreted as proof that every execution will produce an identical sequence or identical final wording.