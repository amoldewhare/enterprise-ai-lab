from evals.datasets.transfer_cases import transfer_eval_cases
from evals.datasets.transfer_evaluator import evaluate_transfer_result

from app.workflow.review import build_transfer_review_prompt
from models.openai.provider import OpenAIProvider

def run_evals():

    provider = OpenAIProvider()

    passed_count = 0
    failed_count = 0

    for case in transfer_eval_cases:
        print(f"\nRunning eval: {case['case_id']}")
        prompt = build_transfer_review_prompt(case["input"])
        actual = provider.generate(prompt)
        print(f"Actual: {actual}")
        passed = evaluate_transfer_result(
            case["expected"],
            actual,
        )
        if passed:
            passed_count += 1
        else:
            failed_count += 1
        result = "PASS" if passed else "FAIL"
        print(f"Eval Result: {result}")


    total = passed_count + failed_count
    pass_rate = (passed_count / total) * 100 if total > 0 else 0

    print("\n===== EVAL SUMMARY =====")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    print(f"Total: {total}")
    print(f"Pass Rate: {pass_rate:.1f}%")



if __name__ == "__main__":
    run_evals()

