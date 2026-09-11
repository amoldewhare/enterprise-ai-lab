from agents import Agent, Runner

from app.workflow.review_result import TransferReviewResult
from app.tools.transfer_policy import get_transfer_policy
from models.base import ModelProvider


class OpenAIProvider(ModelProvider):

    def __init__(self):
        self.agent = Agent(
            name = "Transfer Review Assistant",
            instructions=(

                "You assist wealth-management operations specialists "
                "with reviewing asset-transfer cases. "
                "Use the transfer policy tool when determining whether "
                "a transfer case is complete or what action is permitted. "
                "Do not authorize or execute financial transaction."
                "Consequential financial actions require human approval."
                ),
            tools = [
                get_transfer_policy
                ],
            
            output_type=TransferReviewResult,

            )

    def generate(self, prompt: str) -> TransferReviewResult:
        result = Runner.run_sync(
                self.agent,
                prompt,
        )

        print("\n===== AGENT EXECUTION =====")

        for item in result.new_items:
            print(type(item).__name__)
        
        print("\n===== FINAL OUTPUT =====")

        return result.final_output
