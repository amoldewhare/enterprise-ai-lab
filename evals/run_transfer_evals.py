from evals.datasets.transfer_cases import transfer_eval_cases
from evals.datasets.transfer_evaluator import evaluate_transfer_result

from app.workflow.review import build_transfer_review_prompt
from models.openai.provider import OpenAIProvider

def run_evals():

    provider = OpenAIProvider()

    for case in transfer_eval_cases:
        print(f"\nRunning eval: {case['case_id']}")

        prompt = build_transfer_review_prompt(case["input"])

        actual = provider.generate(prompt)

        print(f"Actual: {actual}")

        passed = evaluate_transfer_result(
            case["expected"],
            actual,
        )


        result = "PASS" if passed else "FAIL"

        print(f"Eval Result: {result}")


if __name__ == "__main__":
    run_evals()

