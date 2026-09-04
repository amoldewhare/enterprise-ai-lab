from agents import function_tool

TRANSFER_POLICY = {
    "policy_id": "TP-101",
    "title": "Full Account Transfer Requirements",
    "requirements": [
        "The transfer form must contain the source account number.",
        "The transfer form must be signed by the customer.",
        "A current brokerage statement must be provided.",
    ],
    "authorization_rule": (
        "A transfer may not proceed when a required customer "
        "authorization or signature is missing."
    ),
}

@function_tool
def get_transfer_policy() -> dict:
    return TRANSFER_POLICY

