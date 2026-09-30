from app.workflow.review import build_transfer_review_prompt
from app.workflow.transfer_case import transfer_case
from models.openai.provider import OpenAIProvider

def main():
    prompt = build_transfer_review_prompt(transfer_case)

    provider = OpenAIProvider()

    # Run the transfer case evaluation
    result = provider.generate(prompt)

    print(result)

if __name__ == "__main__":
    main()
