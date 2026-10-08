from fastapi import FastAPI, HTTPException

from app.enterprise.account_system import get_account_record


app = FastAPI(title="NorthStar Account System")


@app.get("/accounts/{account_id}")
def read_account(account_id: str) -> dict:
    account = get_account_record(account_id)

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    return account
