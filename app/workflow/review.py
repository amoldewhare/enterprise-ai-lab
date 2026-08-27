def build_transfer_review_prompt(transfer_case: dict) -> str:
    return f"""
You are assisting a wealth-management operations specialist.

Review the following asset-transfer case.

Transfer case:
{transfer_case}

Your job is to identify missing information and recommend next steps.

Do not authorize or execute financial transactions.
All consequential financial actions require human approval.
"""
