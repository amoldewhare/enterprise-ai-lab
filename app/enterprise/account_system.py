ACCOUNTS = {
    "NS-48291":{
        "account_id": "NS-48291",
        "customer_name": "John Smith",
        "account_type": "Individual Brokerage",
        "account_status": "ACTIVE",
        "transfer_eligible": True,
    },
     "NS-48292":{
        "account_id": "NS-48292",
        "customer_name": "Jane Smith",
        "account_type": "Individual Brokerage",
        "account_status": "ACTIVE",
        "transfer_eligible": False,
    },
}


def get_account_record(account_id: str) -> dict:
    return ACCOUNTS.get(account_id, {})
