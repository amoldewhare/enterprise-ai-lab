from app.tools.transfer_policy import get_transfer_policy
from app.workflow.review import build_transfer_review_prompt
from app.workflow.transfer_case import transfer_case
from models.openai.provider import OpenAIProvider

def run_experiment(label: str, provider: OpenAIProvider):
    print(f"\n===== {label} =====")

    prompt = build_transfer_review_prompt(transfer_case)

    result = provider.generate(prompt)

    print(result)


def main():
    baseline_provider = OpenAIProvider(
        agent_tools=[]
    )

    grounded_provider = OpenAIProvider(
        agent_tools=[get_transfer_policy]
    )

    run_experiment(
        "BEFORE: No Policy Tool",
        baseline_provider,
    )

    run_experiment(
        "AFTER: TP-101 Policy Tool Available",
        grounded_provider,
    )

if __name__ == "__main__":
    main()
