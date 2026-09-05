import pytest

from app.main import run_transfer_workflow
from app.workflow.review_result import TransferReviewResult
from app.workflow.approval import ApprovalDecision
from pydantic import ValidationError

class FakeProvider:

    def generate(self, prompt):
        return TransferReviewResult(
            status="BLOCKED",
            policy_id="TP-101",
            missing_requirements=["Customer signature"],
            recommended_action="Obtain signature",
            reason="Customer signature is missing",
        )

class FakeReadyProvider:
    def generate(self, prompt):
        return TransferReviewResult(
            status="READY",
            policy_id="TP-101",
            missing_requirements=[],
            recommended_action="Route for human approval",
            reason="All transfer requirements are present",
        )


def test_blocked_case_never_reaches_processing():
    provider = FakeProvider()

    approval_called = False
    processing_called = False

    def fake_approval():
        nonlocal approval_called
        approval_called = True

    def fake_processing(transfer_case):
        nonlocal processing_called
        processing_called = True

    run_transfer_workflow(
        provider,
        fake_approval,
        fake_processing,
    )

    assert approval_called is False
    assert processing_called is False

def test_ready_approved_case_reaches_processing():
    provider = FakeReadyProvider()

    processing_called = False

    def fake_approval():
        return ApprovalDecision(
            approved=True,
            reviewer="Test Reviewer",
            comments="Approved",
        )

    def fake_processing(transfer_case):
        nonlocal processing_called
        processing_called = True

    run_transfer_workflow(
        provider,
        fake_approval,
        fake_processing,
    )

    assert processing_called is True

def test_ready_rejected_case_does_not_reach_processing():
    provider = FakeReadyProvider()

    processing_called = False

    def fake_approval():
        return ApprovalDecision(
            approved=False,
            reviewer="Test Reviewer",
            comments="Rejected",
        )

    def fake_processing(transfer_case):
        nonlocal processing_called
        processing_called = True

    run_transfer_workflow(
        provider,
        fake_approval,
        fake_processing,
    )

    assert processing_called is False

def test_invalid_status_is_rejected():
    with pytest.raises(ValidationError):
        TransferReviewResult(
            status="PENDING",
            policy_id="TP-101",
            missing_requirements=[],
            recommended_action="Wait",
            reason="Testing invalid status",
        )