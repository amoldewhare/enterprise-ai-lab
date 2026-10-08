import httpx

ACCOUNT_API_URL = "http://127.0.0.1:8000"

def fetch_account(account_id:str) -> dict:
    
    response = httpx.get(f"{ACCOUNT_API_URL}/accounts/{account_id}",timeout=5.0
                         )
    response.raise_for_status()

    return response.json()
