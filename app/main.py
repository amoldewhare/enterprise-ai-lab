from app.workflow.review import build_transfer_review_prompt
from app.workflow.transfer_case import transfer_case
from models.openai.provider import OpenAIProvider
from app.workflow.approval import request_human_approval
from app.workflow.processing import submit_transfer_for_processing



def run_transfer_workflow(provider, approval_function, processing_function):
    
    prompt = build_transfer_review_prompt(transfer_case)

    response = provider.generate(prompt)

    print("\n===== MODEL RECOMMENDATION =====")
    print(response)

    # Hard application control
    if response.status == "BLOCKED":
        print("\n===== WORKFLOW BLOCKED =====")
        print(f"Policy: {response.policy_id}")
        print(f"Reason: {response.reason}")
        print(f"Missing requirements: {response.missing_requirements}")
        print(f"Required action: {response.recommended_action}")
        return

    # Only READY cases reach human approval
    decision = approval_function()

    if not decision.approved:
        print(f"\nWorkflow stopped. Rejected by {decision.reviewer}")

        if decision.comments:
            print(f"\nCOMMENTS: {decision.comments}")

        return

    print(f"\nAPPROVED BY {decision.reviewer}")

    if decision.comments:
        print(f"\nCOMMENTS: {decision.comments}")

    processing_function(transfer_case)



def main():
    provider = OpenAIProvider()


    run_transfer_workflow(provider, request_human_approval, submit_transfer_for_processing,)
 
if __name__ == "__main__":
    main()

