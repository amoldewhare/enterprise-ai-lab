from app.workflow.review_result import TransferReviewResult

def requirement_matches(expected_requirement: str, actual_requirements: list[str],) -> bool:
    
    expected_normalized = expected_requirement.lower().strip()

    for actual_requirement in actual_requirements:
        actual_normalized = actual_requirement.lower().strip()

        if expected_normalized in actual_normalized:
            return True

    return False

def all_requirements_match(expected_requirements: list[str], actual_requirements: list[str],) -> bool:

    if len(expected_requirements) != len(actual_requirements):
        return False

    for expected_requirement in expected_requirements:
        if not requirement_matches(expected_requirement, actual_requirements,):
            return False
    
    return True

def evaluate_transfer_result( expected: dict, actual: TransferReviewResult,) -> bool:

    status_matches = actual.status == expected["status"]

    policy_matches = actual.policy_id == expected["policy_id"]

    requirements_match = all_requirements_match(
            expected["missing_requirements"],
            actual.missing_requirements,
            )

    print(f"Status check: {'PASS' if status_matches else 'FAIL'}")
    print(f"Policy check: {'PASS' if policy_matches else 'FAIL'}")
    print(f"Requirements check: {'PASS' if requirements_match else 'FAIL'}")    
    
    return (
            status_matches
            and policy_matches
            and requirements_match
            )
