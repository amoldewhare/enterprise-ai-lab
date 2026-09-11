# Enterprise AI Deployment Lab

A hands-on, model-agnostic lab for exploring how LLM-based systems move from promising prototypes toward controlled enterprise deployments.

The project uses a fictional wealth-management asset-transfer workflow to examine what must surround an LLM in an enterprise system: authoritative context, tools, workflow controls, human authorization, testing, enterprise integration, evaluation, observability, and model-selection tradeoffs.

> This is an evolving lab. Capabilities described as implemented below exist in the current system. Future architectural layers are explicitly identified in the roadmap.

---

## Why This Project Exists

A good LLM response is not enough for many enterprise workflows.

Enterprise AI systems also need to answer questions such as:

- What information is authoritative?
- What may the model reason about?
- Which tools may it call?
- Where should deterministic business logic take over?
- Which actions require human authorization?
- How do we test failure conditions?
- How do we know what actually happened during execution?
- How should model quality, latency, cost, control, and deployment tradeoffs be evaluated?

This lab explores those questions through working code, tests, and observable experiments rather than architecture diagrams alone.

---

## Fictional Enterprise Scenario

The lab uses a fictional company, **NorthStar Wealth Management**, and fictional customer information.

The initial use case is:

**Wealth-management asset-transfer review**

The AI-assisted workflow reviews transfer information, obtains applicable policy information, identifies missing requirements, and prepares a recommendation.

Consequential financial actions are not delegated directly to the LLM.

The core design principle is:

> **AI prepares and recommends. Deterministic application controls and authorized humans govern consequential actions.**

---

## Current Implementation

The current implementation includes:

- A Python-based asset-transfer review workflow
- A model-provider abstraction
- An OpenAI Agents SDK provider
- A policy lookup exposed as an agent-accessible function tool
- Fictional transfer policy `TP-101`
- Structured review results
- Deterministic `READY` / `BLOCKED` workflow control
- A human approval gate
- A controlled post-approval processing step
- Automated tests for critical workflow-control paths

The current implementation uses OpenAI as the model provider. Additional providers are planned as the lab evolves.

---

## What Has Been Tested

The current automated tests verify important workflow-control behavior, including:

- A `BLOCKED` transfer does not proceed to approval or processing
- A `READY` transfer receiving human approval can reach the controlled processing step
- A `READY` transfer rejected by the human reviewer does not proceed to processing
- An invalid workflow status is rejected

These tests focus on deterministic application behavior around the model rather than attempting to prove that probabilistic model output is always correct.

---

## Current Architecture

```text
Transfer Case
     |
     v
Review Prompt
     |
     v
Model Provider
     |
     v
OpenAI Agent
     |
     +----> Transfer Policy Tool
     |           |
     |         TP-101
     |           |
     +<----------+
     |
     v
Structured Review Result
     |
     +---- BLOCKED ----------------> Stop
     |
     +---- READY ----> Human Approval
                           |
                     +-----+-----+
                     |           |
                  Reject       Approve
                     |           |
                    Stop         v
                            Controlled
                            Processing
```

The architecture intentionally separates several responsibilities.

The **LLM** provides probabilistic reasoning.

The **policy tool** provides information that the application defines as authoritative for the workflow.

The **application** applies deterministic workflow controls.

The **human approval step** controls whether an eligible case may proceed.

The **processing component** represents the controlled action that occurs only after the required conditions have been satisfied.

These are separate architectural responsibilities rather than capabilities delegated entirely to the model.

---

## Observable Agent Behavior

The current implementation also allows inspection of the OpenAI Agents SDK execution lifecycle.

During a policy-grounded transfer review, the observed sequence includes:

```text
ToolCallItem
     |
     v
get_transfer_policy()
     |
     v
ToolCallOutputItem
     |
     v
TP-101 returned to the model
     |
     v
MessageOutputItem
```

This provides evidence that the policy tool was actually requested and executed rather than assuming tool use from the final natural-language response.

It does **not** imply that tool use eliminates hallucination or guarantees correct interpretation of the policy.

---

## Model Strategy

The application workflow is intentionally separated from the model-provider implementation.

```text
Application Workflow
        |
        v
   ModelProvider
        |
        +---- OpenAI       [CURRENT]
        |
        +---- Anthropic    [PLANNED]
        |
        +---- Local Qwen   [PLANNED]
```

The eventual goal is not simply to determine which model produces the most impressive answer.

The lab will examine how model choice interacts with the surrounding enterprise architecture, including:

- task quality
- policy adherence
- tool behavior
- structured output reliability
- latency
- cost
- deployment control
- operational complexity

Model comparisons will be made only after common evaluation criteria and test cases are implemented.

---

## Project Structure

The current repository is organized around separation of application workflow, tools, model providers, and tests.

```text
enterprise-ai-lab/
├── app/
│   ├── main.py
│   ├── tools/
│   │   └── transfer_policy.py
│   └── workflow/
│       ├── approval.py
│       ├── processing.py
│       ├── review.py
│       ├── review_result.py
│       └── transfer_case.py
│
├── models/
│   ├── base.py
│   ├── openai/
│   │   └── provider.py
│   ├── anthropic/
│   └── qwen/
│
├── tests/
│   └── test_workflow.py
│
├── .env.example
├── .gitignore
└── README.md
```

The repository structure will evolve as additional architectural layers are implemented.

---

## Running the Current Lab

The project should be run from the repository root so that Python package imports resolve correctly.

```bash
python -m app.main
```

The workflow currently:

```text
Loads fictional transfer case
        ↓
Builds review request
        ↓
Runs AI-assisted review
        ↓
Retrieves TP-101 when requested
        ↓
Produces structured review result
        ↓
Applies deterministic status control
        ↓
BLOCKED → Stop

or

READY → Human Approval
             ↓
        Approve / Reject
             ↓
     Controlled Processing
```

No real financial transaction is executed.

---

## Running the Tests

The deterministic workflow-control tests can be run with:

```bash
pytest
```

The test suite will expand as new architectural capabilities are introduced.

---

## Roadmap

The lab will progressively explore additional enterprise AI architectural layers.

### Current

- OpenAI model integration
- Agent/tool execution
- Policy grounding
- Structured review results
- Deterministic workflow controls
- Human approval
- Controlled processing boundary
- Workflow-control tests

### Planned

- Enterprise retrieval / RAG
- Context provenance and freshness
- Additional enterprise tools and APIs
- MCP-based integration patterns
- Identity and authorization boundaries
- Broader evaluation datasets
- LLM behavior evaluations
- Failure taxonomy and regression testing
- Tracing and observability
- Security and governance artifacts
- Production deployment architecture
- Anthropic Claude integration
- Local Qwen integration
- Cross-model evaluation
- Latency and cost analysis
- Deployment economics

Capabilities will be documented as implemented and tested rather than presented as completed in advance.

---

## Building an Enterprise AI Agent: Lessons from the Lab

This repository is the evolving technical evidence behind an 8-part series exploring enterprise AI deployment.

1. **A Good LLM Answer Isn't Good Enough for the Enterprise**  
   Plausibility vs. authoritative grounding.

2. **What Actually Happens When an AI Agent Calls a Tool?**  
   Model reasoning, tool selection, execution, and the agent runtime.

3. **Context Is an Architecture Problem, Not Just a Prompt Problem**  
   Retrieval, provenance, freshness, and access boundaries.

4. **How Does an AI Agent Actually Connect to the Enterprise?**  
   APIs, tools, MCP, identity, permissions, and systems of record.

5. **When Should an AI Agent Be Allowed to Act?**  
   Deterministic controls, authorization, and human judgment.

6. **How Do You Know an AI Agent Actually Works?**  
   Evaluations, failure analysis, regression testing, and measurable performance.

7. **From Prototype to Production: What Changes?**  
   Reliability, security, observability, auditability, latency, and scale.

8. **OpenAI vs. Claude vs. Local Qwen: What Actually Matters in Enterprise Model Selection?**  
   Quality, tool behavior, latency, cost, control, and operational fit.

The repository may move ahead of the article series as the underlying system evolves.

---

## Evidence-First Approach

This project follows a simple operating principle:

> **BUILD → TEST → OBSERVE → DOCUMENT**

Architecture and capabilities are described as implemented only when there is corresponding code or observable evidence.

Planned functionality is identified as planned.

The objective is not to demonstrate a particular AI framework. It is to understand the architectural boundaries required to move an LLM-based system toward a controlled enterprise deployment.

---

## Disclaimer

**NorthStar Wealth Management is fictional.**

The company, customer information, transfer cases, policy `TP-101`, operational assumptions, and any business metrics used in this project are fictional and exist only for architectural experimentation.

No real client or customer data is used.

This repository is an educational and architectural lab. It does not provide financial, investment, legal, or compliance advice.
