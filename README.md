# Enterprise AI Deployment Lab

A model-agnostic enterprise AI prototype demonstrating how a regulated business workflow can move from business problem to AI-assisted execution, evaluation, governance, human approval, and measurable business value.

## Initial Use Case

Wealth-management asset transfer review.

The system will assist operations specialists by:

- reviewing transfer cases
- retrieving applicable policies
- identifying missing information
- flagging potential exceptions
- recommending next actions
- preparing cases for human approval

Consequential financial actions remain under deterministic controls and human authorization.

## Architecture Principle

The business workflow is intentionally separated from the underlying model provider.

The same workflow will progressively be evaluated using:

- OpenAI
- Anthropic Claude
- Qwen 2.5-Coder-32B running locally

## Project Goals

This project will explore:

- LLM tool calling
- Retrieval-Augmented Generation (RAG)
- Agentic workflows
- Model abstraction and routing
- Evaluation frameworks
- AI guardrails
- Human-in-the-loop workflows
- Enterprise AI governance
- AI deployment economics

## Project Structure

```text
app/            Business workflow and application logic
models/         Model-provider adapters
evals/          Evaluation datasets and scoring
architecture/   System architecture
governance/     Security, risk, and governance artifacts
business-case/  ROI and deployment analysis
data/           Sample non-sensitive data
tests/          Automated tests
