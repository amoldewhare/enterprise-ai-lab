from app.workflow.review import build_transfer_review_prompt
from app.workflow.transfer_case import transfer_case
from models.openai.provider import OpenAIProvider
from app.workflow.approval import request_human_approval
from app.workflow.processing import submit_transfer_for_processing

def main():
    provider = OpenAIProvider()

    prompt = build_transfer_review_prompt(transfer_case)

    response = provider.generate(prompt)

    print("\n===== MODEL RECOMMENDATION =====")
    print(response)
    
    # Hard Application Control
    # A BLOCKED case can never reach human execution approval.

    if response.status == 'BLOCKED':
        print("\n===== WORKFLOW BLOCKED =====")
        print(f"Policy: {response.policy_id}")
        print(f"Reason: {response.reason}")
        print(f"Missing requirements: {response.missing_requirements}")
        print(f"Required action: {response.recommended_action}")
        return

    # ONLY READY cases reach this point
    decision = request_human_approval()

    if not decision.approved:
        print(f"\nWorkflow stopped. Rejected by {decision.reviewer}")

        if decision.comments:
            print(f"\nCOMMENTS: {decision.comments}")

        return
    

    # Human explicitly approved processing.
    print(f"\nAPPROVED BY {decision.reviewer}")

    if decision.comments:
        print(f"\nCOMMENTS: {decision.comments}")

    submit_transfer_for_processing(transfer_case)


if __name__ == "__main__":
    main()

