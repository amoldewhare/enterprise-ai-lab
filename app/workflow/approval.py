from dataclasses import dataclass

@dataclass
class ApprovalDecision:
    approved: bool
    reviewer: str
    comments: str = ""

def request_human_approval() -> ApprovalDecision:

    answer = input("Approve this transfer for processing? (yes/no): ").strip().lower()

    approved = answer == "yes"

    reviewer = input("Reviewer name: ").strip()
    comments = input("Comments: ").strip()

    return ApprovalDecision(
            approved=approved,
            reviewer=reviewer,
            comments=comments,
    )
