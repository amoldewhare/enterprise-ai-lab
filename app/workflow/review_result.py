from typing import Literal
from pydantic import BaseModel


class TransferReviewResult(BaseModel):
    status: Literal["BLOCKED", "READY"]
    policy_id: str
    missing_requirements: list[str]
    recommended_action: str
    reason: str
