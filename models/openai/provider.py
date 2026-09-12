from agents import Agent, Runner

from app.workflow.review_result import TransferReviewResult
from app.tools.transfer_policy import get_transfer_policy
from models.base import ModelProvider


class OpenAIProvider(ModelProvider):

    def __init__(self, agent_tools=None):

        if agent_tools is None:
            agent_tools = [get_transfer_policy]

        self.agent = Agent(
            name = "Transfer Review Assistant",
            instructions=(

                "You assist wealth-management operations specialists "
                "with reviewing asset-transfer cases. "
                "Use available tools when needed to determine whether "
                "a transfer case is complete or what action is permitted. "
                "Do not authorize or execute financial transactions. "
                "Consequential financial actions require human approval."
                ),

            tools=agent_tools,
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
