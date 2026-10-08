from agents import function_tool

from app.enterprise.account_client import fetch_account

@function_tool
def get_account(account_id: str) -> dict:
    """Retrieve the current account record from NorthStar."""
    return fetch_account(account_id)


