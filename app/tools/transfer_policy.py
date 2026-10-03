from agents import function_tool

TRANSFER_POLICIES = {
    "TP-101": {
        "policy_id": "TP-101",
        "title": "Full Account Transfer Requirements",
        "transfer_type": "full",
        "requirements": [
            "The transfer form must contain the source account number.",
            "The transfer form must be signed by the customer.",
            "A current brokerage statement must be provided.",
        ],
        "authorization_rule": (
            "A transfer may not proceed when a required customer "
            "authorization or signature is missing."
        ),
    },

    "TP-102": {
        "policy_id": "TP-102",
        "title": "Partial Account Transfer Requirements",
        "transfer_type": "partial",
        "requirements": [
            "The transfer form must contain the source account number.",
            "The transfer form must identify the assets to be transferred.",
            "The transfer form must be signed by the customer.",
        ],
        "authorization_rule": (
            "A partial transfer may not proceed when the requested "
            "assets or required customer authorization are missing."
        ),
    },

    "TP-103": {
        "policy_id": "TP-103",
        "title": "Retirement Account Transfer Requirements",
        "transfer_type": "retirement",
        "requirements": [
            "The transfer form must contain the source account number.",
            "The transfer form must identify the retirement account type.",
            "The transfer form must be signed by the customer.",
        ],
        "authorization_rule": (
            "A retirement account transfer may not proceed when "
            "required account information or customer authorization is missing."
        ),
    },
}

@function_tool
def get_transfer_policy(policy_id: str) -> dict:
    return TRANSFER_POLICIES.get(policy_id, {})

@function_tool
def search_transfer_policies(query:str) -> list[dict]:
    query_words = query.lower().split()
    matching_policies = []

    for policy in TRANSFER_POLICIES.values():
        searchable_text = (
                policy["title"]+ " " + policy["transfer_type"] 
            ).lower()

        if any(word in searchable_text for word in query_words):
            matching_policies.append(policy)

    return matching_policies


