transfer_eval_cases = [
    {
        "case_id": "complete_transfer",
        "input": {
            "client_name": "John Smith",
            "account_type": "Individual Brokerage",
            "transfer_type": "Full Account Transfer",
            "current_custodian": "ABC Brokerage",
            "documents_received": [
                "Transfer form",
                "Brokerage statement",
                "Government ID",
            ],
            "transfer_form": {
                "account_number_present": True,
                "customer_signature_present": True,
            },
        },
        "expected": {
            "status": "READY",
            "policy_id": "TP-101",
            "missing_requirements": [],
        },
    },

    {
        "case_id": "missing_signature",
        "input": {
            "client_name": "John Smith",
            "account_type": "Individual Brokerage",
            "transfer_type": "Full Account Transfer",
            "current_custodian": "ABC Brokerage",
            "documents_received": [
                "Transfer form",
                "Brokerage statement",
                "Government ID",
            ],
            "transfer_form": {
                "account_number_present": True,
                "customer_signature_present": False,
            },
        },
        "expected": {
            "status": "BLOCKED",
            "policy_id": "TP-101",
            "missing_requirements": [
                "customer signature",
            ],
        },
    },
]
