# Enterprise AI Deployment Lab

A hands-on, model-agnostic lab for exploring how LLM-based systems move from promising prototypes toward controlled enterprise deployments.

The project uses a fictional wealth-management asset-transfer workflow to examine the architectural layers that need to surround an LLM before it can participate responsibly in an enterprise process.

The lab is intentionally evolving. Some capabilities are implemented and tested today; others are represented in the repository structure as planned architectural layers.

The guiding principle is:

> **AI prepares and recommends. Deterministic application controls and authorized humans govern consequential actions.**

---

## Why This Project Exists

Enterprise AI systems require more than a capable language model.

A model may produce a plausible answer while still lacking authoritative enterprise context, appropriate permissions, deterministic controls, evaluation, observability, or the ability to explain the basis of its recommendation.

This lab explores those boundaries by progressively building an enterprise AI workflow and examining questions such as:

- What happens when an LLM does not have authoritative enterprise context?
- How does grounding change the basis of a recommendation?
- What actually happens when an agent calls a tool?
- How should enterprise knowledge and policies be retrieved?
- How should agents interact with enterprise APIs and systems of record?
- Which decisions belong to the model, deterministic application logic, or humans?
- How should AI behavior be evaluated?
- What changes when moving from prototype to production?
- How do model choices affect quality, latency, cost, control, and deployment architecture?

The objective is not to demonstrate that an LLM can generate an answer.

The objective is to understand the architecture required to make AI behavior more grounded, controlled, observable, testable, and useful inside enterprise workflows.

---

## Fictional Enterprise Scenario

The lab uses a fictional company:

**NorthStar Wealth Management**

The example workflow is a customer asset transfer between brokerage institutions.

A representative fictional transfer case contains information such as:

- client name
- account type
- transfer type
- current custodian
- transfer documents
- account number
- customer signature
- brokerage statement

The AI assistant reviews the case, determines whether required information is present, consults available policy information, and prepares a recommendation.

The AI does **not** independently authorize or execute the financial transaction.

Consequential actions remain subject to deterministic application controls and human authorization.

All companies, customers, policies, cases, metrics, and business scenarios in this repository are fictional unless explicitly stated otherwise.

---

## Current Implementation

The current implementation includes:

- a fictional wealth-management transfer case
- prompt construction for transfer review
- an OpenAI Agents SDK-based provider
- structured model output using Pydantic
- a fictional transfer-policy tool
- observable agent/tool execution
- deterministic application-level workflow controls
- explicit human approval
- controlled post-approval processing
- automated workflow tests
- a reproducible grounding comparison experiment
- documented evidence from an observed grounding experiment

The current workflow can distinguish between:

```text
READY
```

and:

```text
BLOCKED
```

A `BLOCKED` case cannot reach approval or processing.

A `READY` case must still receive explicit human approval before the controlled processing function can execute.

---

## Current Architecture

The implemented workflow currently resembles:

```text
                     TRANSFER CASE
                          |
                          v
                   REVIEW PROMPT
                          |
                          v
                  OPENAI PROVIDER
                          |
                          v
                     AI AGENT
                          |
                    +-----+-----+
                    |           |
                    v           |
              POLICY TOOL       |
                 TP-101         |
                    |           |
                    +-----+-----+
                          |
                          v
              STRUCTURED REVIEW RESULT
                          |
                 +--------+--------+
                 |                 |
              BLOCKED             READY
                 |                 |
                 v                 v
            STOP WORKFLOW    HUMAN APPROVAL
                                   |
                           +-------+-------+
                           |               |
                         REJECT          APPROVE
                           |               |
                           v               v
                          STOP      CONTROLLED ACTION
```

This architecture intentionally separates several responsibilities:

**Model reasoning**  
The model interprets the case and generates a recommendation.

**Authoritative information**  
Tools provide information that should not simply be invented by the model.

**Deterministic application logic**  
Python controls whether a workflow is allowed to advance.

**Human authorization**  
An authorized reviewer decides whether a consequential action may proceed.

**Controlled execution**  
Processing occurs only after the application control and human approval requirements have been satisfied.

---

## Grounding Experiment

One of the first experiments in the lab examines the difference between a model producing a plausible recommendation and an agent having access to an authoritative policy source.

The same transfer case, prompt, provider implementation, agent instructions, and structured output are used in two runs.

Only policy-tool access changes:

```text
BEFORE
Transfer Case
     |
     v
    LLM
     |
     v
Plausible Recommendation
```

versus:

```text
AFTER
Transfer Case
     |
     v
   Agent
     |
     +------> Policy Tool TP-101
     |              |
     <--------------+
     |
     v
    LLM
     |
     v
Grounded Recommendation
```

In the observed baseline run, the model had no policy tool and produced additional requirements that were not established by an authoritative source supplied in the experiment.

In the observed grounded run, the agent called the policy tool and based its recommendation on the requirements returned by fictional policy `TP-101`.

This does **not** demonstrate that tool access eliminates hallucinations or guarantees correctness.

It demonstrates a narrower but important point:

> **Plausibility is not the same as authority.**

The reproducible experiment is located at:

```text
experiments/grounding_comparison.py
```

The observed Article 1 evidence is documented at:

```text
evidence/article-01-grounding.md
```

---

## Observable Agent Behavior

The lab exposes the execution lifecycle produced by the agent runtime.

When no tool was available in the grounding baseline, the observed execution was:

```text
MessageOutputItem
```

When the policy tool was available and selected by the agent, the observed execution was:

```text
ToolCallItem
ToolCallOutputItem
MessageOutputItem
```

Conceptually:

```text
Model Call
    |
    v
Tool Request
    |
    v
SDK Executes Python Tool
    |
    v
Tool Result
    |
    v
Model Continues
    |
    v
Final Structured Response
```

This distinction matters because the LLM itself is not directly executing enterprise code.

The agent runtime mediates the interaction between model reasoning and executable tools.

---

## Deterministic Workflow Controls

The model's recommendation does not determine whether a financial action executes.

Application code enforces the workflow boundary.

Conceptually:

```python
if response.status == "BLOCKED":
    stop_workflow()

if response.status == "READY":
    request_human_approval()
```

Only an approved `READY` case can reach the processing function.

This separation is intentional.

The model can recommend.

The application controls workflow state.

The human authorizes consequential action.

---

## What Has Been Tested

The current automated test suite contains four deterministic workflow tests.

### 1. BLOCKED cases stop

A `BLOCKED` model result must never reach:

- human approval
- transfer processing

### 2. READY + approved reaches processing

A `READY` result followed by explicit human approval can reach the controlled processing function.

### 3. READY + rejected stops

A `READY` model recommendation does not override a human rejection.

### 4. Invalid workflow states are rejected

The structured output schema accepts only:

```text
READY
BLOCKED
```

An unsupported state such as:

```text
PENDING
```

is rejected by Pydantic validation.

Run the tests with:

```bash
python -m pytest
```

---

## Project Structure

```text
enterprise-ai-lab/
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── guardrails/
│   ├── rag/
│   ├── tools/
│   │   └── transfer_policy.py
│   └── workflow/
│       ├── approval.py
│       ├── processing.py
│       ├── review.py
│       ├── review_result.py
│       └── transfer_case.py
│
├── architecture/
├── business-case/
│
├── data/
│   └── sample/
│
├── evals/
│   ├── datasets/
│   ├── evaluators/
│   └── results/
│
├── evidence/
│   └── article-01-grounding.md
│
├── experiments/
│   └── grounding_comparison.py
│
├── governance/
│
├── models/
│   ├── base.py
│   ├── anthropic/
│   │   ├── __init__.py
│   │   └── provider.py
│   ├── openai/
│   │   ├── __init__.py
│   │   └── provider.py
│   └── qwen/
│       ├── __init__.py
│       └── provider.py
│
├── tests/
│   └── test_workflow.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

Some directories represent architectural capabilities that are planned but not yet implemented.

Their presence in the repository should not be interpreted as evidence that those capabilities are complete.

---

## Model Strategy

The project is intentionally model-agnostic at the application architecture level.

The `ModelProvider` abstraction separates the workflow from a specific model provider:

```text
Enterprise Workflow
        |
        v
  ModelProvider
        |
   +----+----+----------+
   |         |          |
 OpenAI   Anthropic    Qwen
```

### Current

The OpenAI provider is currently used for the implemented agent workflow.

### Planned

Anthropic and local Qwen providers are represented in the repository structure for future comparison and experimentation.

Their presence does not imply equivalent functionality has already been implemented or tested.

The longer-term objective is to run comparable enterprise workflows and evaluations across multiple model/provider configurations.

---

## Setup

This project requires **Python 3.12 or later**.

Clone the repository and move into the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Configure required environment variables using `.env.example` as a reference.

Do not commit API keys or other secrets to the repository.

---

## Running the Current Lab

From the repository root:

```bash
python -m app.main
```

The workflow will:

1. load the fictional transfer case
2. construct the review prompt
3. run the AI agent
4. allow the agent to retrieve the transfer policy when needed
5. return a structured review result
6. apply deterministic workflow controls
7. request human approval when the case is `READY`
8. execute the controlled processing function only after approval

---

## Running the Grounding Experiment

From the repository root:

```bash
python -m experiments.grounding_comparison
```

The experiment creates two providers:

```text
Baseline  → agent_tools=[]
Grounded  → agent_tools=[get_transfer_policy]
```

Both receive the same fictional transfer case and review prompt.

The experiment prints both the agent execution lifecycle and the resulting structured recommendation.

Because model generation is probabilistic, repeated runs may not produce identical wording or recommendations.

The evidence file records one observed run; it should not be interpreted as a statistical benchmark.

---

## Running the Tests

Run:

```bash
python -m pytest
```

The project also uses GitHub Actions to run the automated tests on repository pushes and pull requests.

The CI workflow is defined in:

```text
.github/workflows/tests.yml
```

This provides an independent environment for validating the deterministic workflow tests.

---

## Implemented vs. Planned

A central goal of this repository is to distinguish what has actually been built from what is still being explored.

### Implemented / Tested

- fictional asset-transfer workflow
- structured AI review result
- OpenAI Agents SDK integration
- policy function tool
- observable tool-call lifecycle
- deterministic BLOCKED/READY workflow controls
- explicit human approval
- controlled processing action
- automated workflow tests
- GitHub Actions test execution
- grounding comparison experiment
- Article 1 grounding evidence

### Planned / Evolving

- enterprise RAG and retrieval architecture
- richer guardrails
- identity and authorization boundaries
- enterprise API integration patterns
- MCP experiments
- evaluation datasets and evaluators
- trace-based evaluation
- failure taxonomy
- regression evaluation
- production observability
- latency and cost measurement
- reliability testing
- Anthropic provider experiments
- local Qwen provider experiments
- cross-model evaluation

These planned capabilities will be documented as they are actually implemented and tested.

---

## Roadmap

The lab will evolve through several architectural layers:

```text
BUSINESS PROBLEM
       |
       v
LLM BEHAVIOR
       |
       v
GROUNDING
       |
       v
CONTEXT / RETRIEVAL
       |
       v
TOOLS / ENTERPRISE INTEGRATION
       |
       v
CONTROL / AUTHORIZATION
       |
       v
EVALUATION
       |
       v
PRODUCTION ARCHITECTURE
       |
       v
MODEL / ECONOMICS DECISION
```

The goal is not to add architectural complexity for its own sake.

Each layer should address an observed enterprise requirement, failure mode, control boundary, or measurable operational concern.

---

## Building an Enterprise AI Agent: Lessons from the Lab

The repository supports an eight-part series documenting what is built, tested, and observed as the architecture evolves.

### Part 1 — A Good LLM Answer Isn't Good Enough for the Enterprise

Grounding, authority, and the difference between plausible recommendations and recommendations supported by authoritative enterprise information.

### Part 2 — What Actually Happens When an AI Agent Calls a Tool?

Agent runtime behavior, tool selection, tool execution, and the model/tool interaction loop.

### Part 3 — Context Is an Architecture Problem, Not Just a Prompt Problem

Retrieval, RAG, policies, provenance, freshness, and access boundaries.

### Part 4 — How Does an AI Agent Actually Connect to the Enterprise?

APIs, tools, MCP, enterprise systems, authentication, identity, data boundaries, and systems of record.

### Part 5 — When Should an AI Agent Be Allowed to Act?

Human approval, deterministic controls, authorization, read/write boundaries, and security.

### Part 6 — How Do You Know an AI Agent Actually Works?

Evaluations, test cases, traces, failure taxonomy, regression testing, model quality, and operational metrics.

### Part 7 — From Prototype to Production: What Changes?

Deployment architecture, observability, resilience, latency, security, auditability, scaling, and operational change.

### Part 8 — OpenAI vs. Claude vs. Local Qwen: What Actually Matters in Enterprise Model Selection?

Comparing models using the same workflow, policies, and evaluation framework across quality, tool behavior, latency, cost, control, and deployment options.

---

## Evidence-First Approach

The development approach for this lab is:

> **BUILD → TEST → OBSERVE → DOCUMENT**

Claims in the accompanying articles should correspond to something that has actually been:

- implemented
- executed
- tested
- observed
- measured

Planned capabilities are identified as planned rather than presented as completed work.

The repository may evolve ahead of the article series. Git history and evidence artifacts provide the technical record behind specific observations discussed in the articles.

The Article 1 grounding experiment can be reproduced with:

```text
experiments/grounding_comparison.py
```

and its observed evidence is recorded in:

```text
evidence/article-01-grounding.md
```

---

## Enterprise Architecture Principle

The central architectural idea explored by this project is that:

> **The LLM is a component of the system, not the system itself.**

A production enterprise AI architecture may ultimately need to coordinate:

```text
Enterprise Application
        |
        v
API / Orchestration Layer
        |
        v
Agent Runtime
        |
        v
Model
        |
        +--------------------+
        |                    |
        v                    v
Context / Retrieval       Tool Gateway
                              |
                              v
                       Enterprise APIs
                              |
                              v
                       Systems of Record
```

with cross-cutting concerns including:

```text
Identity
Authentication
Authorization
Security
Data Boundaries
Policy
Human Approval
Evaluation
Tracing
Observability
Audit
Cost
Latency
Reliability
```

This repository will progressively explore those concerns rather than assuming the model alone solves them.

---

## Disclaimer

This repository is an educational and architectural lab.

NorthStar Wealth Management, its customers, transfer cases, policies, operational metrics, and business scenarios are fictional.

Nothing in this repository should be interpreted as financial, investment, compliance, or legal advice.

The workflow is intentionally designed so that AI recommendations do not independently authorize consequential financial actions.# Enterprise AI Deployment Lab

A hands-on, model-agnostic lab for exploring how LLM-based systems move from promising prototypes toward controlled enterprise deployments.

The project uses a fictional wealth-management asset-transfer workflow to examine the architectural layers that need to surround an LLM before it can participate responsibly in an enterprise process.

The lab is intentionally evolving. Some capabilities are implemented and tested today; others are represented in the repository structure as planned architectural layers.

The guiding principle is:

> **AI prepares and recommends. Deterministic application controls and authorized humans govern consequential actions.**

---

## Why This Project Exists

Enterprise AI systems require more than a capable language model.

A model may produce a plausible answer while still lacking authoritative enterprise context, appropriate permissions, deterministic controls, evaluation, observability, or the ability to explain the basis of its recommendation.

This lab explores those boundaries by progressively building an enterprise AI workflow and examining questions such as:

- What happens when an LLM does not have authoritative enterprise context?
- How does grounding change the basis of a recommendation?
- What actually happens when an agent calls a tool?
- How should enterprise knowledge and policies be retrieved?
- How should agents interact with enterprise APIs and systems of record?
- Which decisions belong to the model, deterministic application logic, or humans?
- How should AI behavior be evaluated?
- What changes when moving from prototype to production?
- How do model choices affect quality, latency, cost, control, and deployment architecture?

The objective is not to demonstrate that an LLM can generate an answer.

The objective is to understand the architecture required to make AI behavior more grounded, controlled, observable, testable, and useful inside enterprise workflows.

---

## Fictional Enterprise Scenario

The lab uses a fictional company:

**NorthStar Wealth Management**

The example workflow is a customer asset transfer between brokerage institutions.

A representative fictional transfer case contains information such as:

- client name
- account type
- transfer type
- current custodian
- transfer documents
- account number
- customer signature
- brokerage statement

The AI assistant reviews the case, determines whether required information is present, consults available policy information, and prepares a recommendation.

The AI does **not** independently authorize or execute the financial transaction.

Consequential actions remain subject to deterministic application controls and human authorization.

All companies, customers, policies, cases, metrics, and business scenarios in this repository are fictional unless explicitly stated otherwise.

---

## Current Implementation

The current implementation includes:

- a fictional wealth-management transfer case
- prompt construction for transfer review
- an OpenAI Agents SDK-based provider
- structured model output using Pydantic
- a fictional transfer-policy tool
- observable agent/tool execution
- deterministic application-level workflow controls
- explicit human approval
- controlled post-approval processing
- automated workflow tests
- a reproducible grounding comparison experiment
- documented evidence from an observed grounding experiment

The current workflow can distinguish between:

```text
READY
```

and:

```text
BLOCKED
```

A `BLOCKED` case cannot reach approval or processing.

A `READY` case must still receive explicit human approval before the controlled processing function can execute.

---

## Current Architecture

The implemented workflow currently resembles:

```text
                     TRANSFER CASE
                          |
                          v
                   REVIEW PROMPT
                          |
                          v
                  OPENAI PROVIDER
                          |
                          v
                     AI AGENT
                          |
                    +-----+-----+
                    |           |
                    v           |
              POLICY TOOL       |
                 TP-101         |
                    |           |
                    +-----+-----+
                          |
                          v
              STRUCTURED REVIEW RESULT
                          |
                 +--------+--------+
                 |                 |
              BLOCKED             READY
                 |                 |
                 v                 v
            STOP WORKFLOW    HUMAN APPROVAL
                                   |
                           +-------+-------+
                           |               |
                         REJECT          APPROVE
                           |               |
                           v               v
                          STOP      CONTROLLED ACTION
```

This architecture intentionally separates several responsibilities:

**Model reasoning**  
The model interprets the case and generates a recommendation.

**Authoritative information**  
Tools provide information that should not simply be invented by the model.

**Deterministic application logic**  
Python controls whether a workflow is allowed to advance.

**Human authorization**  
An authorized reviewer decides whether a consequential action may proceed.

**Controlled execution**  
Processing occurs only after the application control and human approval requirements have been satisfied.

---

## Grounding Experiment

One of the first experiments in the lab examines the difference between a model producing a plausible recommendation and an agent having access to an authoritative policy source.

The same transfer case, prompt, provider implementation, agent instructions, and structured output are used in two runs.

Only policy-tool access changes:

```text
BEFORE
Transfer Case
     |
     v
    LLM
     |
     v
Plausible Recommendation
```

versus:

```text
AFTER
Transfer Case
     |
     v
   Agent
     |
     +------> Policy Tool TP-101
     |              |
     <--------------+
     |
     v
    LLM
     |
     v
Grounded Recommendation
```

In the observed baseline run, the model had no policy tool and produced additional requirements that were not established by an authoritative source supplied in the experiment.

In the observed grounded run, the agent called the policy tool and based its recommendation on the requirements returned by fictional policy `TP-101`.

This does **not** demonstrate that tool access eliminates hallucinations or guarantees correctness.

It demonstrates a narrower but important point:

> **Plausibility is not the same as authority.**

The reproducible experiment is located at:

```text
experiments/grounding_comparison.py
```

The observed Article 1 evidence is documented at:

```text
evidence/article-01-grounding.md
```

---

## Observable Agent Behavior

The lab exposes the execution lifecycle produced by the agent runtime.

When no tool was available in the grounding baseline, the observed execution was:

```text
MessageOutputItem
```

When the policy tool was available and selected by the agent, the observed execution was:

```text
ToolCallItem
ToolCallOutputItem
MessageOutputItem
```

Conceptually:

```text
Model Call
    |
    v
Tool Request
    |
    v
SDK Executes Python Tool
    |
    v
Tool Result
    |
    v
Model Continues
    |
    v
Final Structured Response
```

This distinction matters because the LLM itself is not directly executing enterprise code.

The agent runtime mediates the interaction between model reasoning and executable tools.

---

## Deterministic Workflow Controls

The model's recommendation does not determine whether a financial action executes.

Application code enforces the workflow boundary.

Conceptually:

```python
if response.status == "BLOCKED":
    stop_workflow()

if response.status == "READY":
    request_human_approval()
```

Only an approved `READY` case can reach the processing function.

This separation is intentional.

The model can recommend.

The application controls workflow state.

The human authorizes consequential action.

---

## What Has Been Tested

The current automated test suite contains four deterministic workflow tests.

### 1. BLOCKED cases stop

A `BLOCKED` model result must never reach:

- human approval
- transfer processing

### 2. READY + approved reaches processing

A `READY` result followed by explicit human approval can reach the controlled processing function.

### 3. READY + rejected stops

A `READY` model recommendation does not override a human rejection.

### 4. Invalid workflow states are rejected

The structured output schema accepts only:

```text
READY
BLOCKED
```

An unsupported state such as:

```text
PENDING
```

is rejected by Pydantic validation.

Run the tests with:

```bash
python -m pytest
```

---

## Project Structure

```text
enterprise-ai-lab/
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── guardrails/
│   ├── rag/
│   ├── tools/
│   │   └── transfer_policy.py
│   └── workflow/
│       ├── approval.py
│       ├── processing.py
│       ├── review.py
│       ├── review_result.py
│       └── transfer_case.py
│
├── architecture/
├── business-case/
│
├── data/
│   └── sample/
│
├── evals/
│   ├── datasets/
│   ├── evaluators/
│   └── results/
│
├── evidence/
│   └── article-01-grounding.md
│
├── experiments/
│   └── grounding_comparison.py
│
├── governance/
│
├── models/
│   ├── base.py
│   ├── anthropic/
│   │   ├── __init__.py
│   │   └── provider.py
│   ├── openai/
│   │   ├── __init__.py
│   │   └── provider.py
│   └── qwen/
│       ├── __init__.py
│       └── provider.py
│
├── tests/
│   └── test_workflow.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

Some directories represent architectural capabilities that are planned but not yet implemented.

Their presence in the repository should not be interpreted as evidence that those capabilities are complete.

---

## Model Strategy

The project is intentionally model-agnostic at the application architecture level.

The `ModelProvider` abstraction separates the workflow from a specific model provider:

```text
Enterprise Workflow
        |
        v
  ModelProvider
        |
   +----+----+----------+
   |         |          |
 OpenAI   Anthropic    Qwen
```

### Current

The OpenAI provider is currently used for the implemented agent workflow.

### Planned

Anthropic and local Qwen providers are represented in the repository structure for future comparison and experimentation.

Their presence does not imply equivalent functionality has already been implemented or tested.

The longer-term objective is to run comparable enterprise workflows and evaluations across multiple model/provider configurations.

---

## Setup

This project requires **Python 3.12 or later**.

Clone the repository and move into the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Configure required environment variables using `.env.example` as a reference.

Do not commit API keys or other secrets to the repository.

---

## Running the Current Lab

From the repository root:

```bash
python -m app.main
```

The workflow will:

1. load the fictional transfer case
2. construct the review prompt
3. run the AI agent
4. allow the agent to retrieve the transfer policy when needed
5. return a structured review result
6. apply deterministic workflow controls
7. request human approval when the case is `READY`
8. execute the controlled processing function only after approval

---

## Running the Grounding Experiment

From the repository root:

```bash
python -m experiments.grounding_comparison
```

The experiment creates two providers:

```text
Baseline  → agent_tools=[]
Grounded  → agent_tools=[get_transfer_policy]
```

Both receive the same fictional transfer case and review prompt.

The experiment prints both the agent execution lifecycle and the resulting structured recommendation.

Because model generation is probabilistic, repeated runs may not produce identical wording or recommendations.

The evidence file records one observed run; it should not be interpreted as a statistical benchmark.

---

## Running the Tests

Run:

```bash
python -m pytest
```

The project also uses GitHub Actions to run the automated tests on repository pushes and pull requests.

The CI workflow is defined in:

```text
.github/workflows/tests.yml
```

This provides an independent environment for validating the deterministic workflow tests.

---

## Implemented vs. Planned

A central goal of this repository is to distinguish what has actually been built from what is still being explored.

### Implemented / Tested

- fictional asset-transfer workflow
- structured AI review result
- OpenAI Agents SDK integration
- policy function tool
- observable tool-call lifecycle
- deterministic BLOCKED/READY workflow controls
- explicit human approval
- controlled processing action
- automated workflow tests
- GitHub Actions test execution
- grounding comparison experiment
- Article 1 grounding evidence

### Planned / Evolving

- enterprise RAG and retrieval architecture
- richer guardrails
- identity and authorization boundaries
- enterprise API integration patterns
- MCP experiments
- evaluation datasets and evaluators
- trace-based evaluation
- failure taxonomy
- regression evaluation
- production observability
- latency and cost measurement
- reliability testing
- Anthropic provider experiments
- local Qwen provider experiments
- cross-model evaluation

These planned capabilities will be documented as they are actually implemented and tested.

---

## Roadmap

The lab will evolve through several architectural layers:

```text
BUSINESS PROBLEM
       |
       v
LLM BEHAVIOR
       |
       v
GROUNDING
       |
       v
CONTEXT / RETRIEVAL
       |
       v
TOOLS / ENTERPRISE INTEGRATION
       |
       v
CONTROL / AUTHORIZATION
       |
       v
EVALUATION
       |
       v
PRODUCTION ARCHITECTURE
       |
       v
MODEL / ECONOMICS DECISION
```

The goal is not to add architectural complexity for its own sake.

Each layer should address an observed enterprise requirement, failure mode, control boundary, or measurable operational concern.

---

## Building an Enterprise AI Agent: Lessons from the Lab

The repository supports an eight-part series documenting what is built, tested, and observed as the architecture evolves.

### Part 1 — A Good LLM Answer Isn't Good Enough for the Enterprise

Grounding, authority, and the difference between plausible recommendations and recommendations supported by authoritative enterprise information.

### Part 2 — What Actually Happens When an AI Agent Calls a Tool?

Agent runtime behavior, tool selection, tool execution, and the model/tool interaction loop.

### Part 3 — Context Is an Architecture Problem, Not Just a Prompt Problem

Retrieval, RAG, policies, provenance, freshness, and access boundaries.

### Part 4 — How Does an AI Agent Actually Connect to the Enterprise?

APIs, tools, MCP, enterprise systems, authentication, identity, data boundaries, and systems of record.

### Part 5 — When Should an AI Agent Be Allowed to Act?

Human approval, deterministic controls, authorization, read/write boundaries, and security.

### Part 6 — How Do You Know an AI Agent Actually Works?

Evaluations, test cases, traces, failure taxonomy, regression testing, model quality, and operational metrics.

### Part 7 — From Prototype to Production: What Changes?

Deployment architecture, observability, resilience, latency, security, auditability, scaling, and operational change.

### Part 8 — OpenAI vs. Claude vs. Local Qwen: What Actually Matters in Enterprise Model Selection?

Comparing models using the same workflow, policies, and evaluation framework across quality, tool behavior, latency, cost, control, and deployment options.

---

## Evidence-First Approach

The development approach for this lab is:

> **BUILD → TEST → OBSERVE → DOCUMENT**

Claims in the accompanying articles should correspond to something that has actually been:

- implemented
- executed
- tested
- observed
- measured

Planned capabilities are identified as planned rather than presented as completed work.

The repository may evolve ahead of the article series. Git history and evidence artifacts provide the technical record behind specific observations discussed in the articles.

The Article 1 grounding experiment can be reproduced with:

```text
experiments/grounding_comparison.py
```

and its observed evidence is recorded in:

```text
evidence/article-01-grounding.md
```

---

## Enterprise Architecture Principle

The central architectural idea explored by this project is that:

> **The LLM is a component of the system, not the system itself.**

A production enterprise AI architecture may ultimately need to coordinate:

```text
Enterprise Application
        |
        v
API / Orchestration Layer
        |
        v
Agent Runtime
        |
        v
Model
        |
        +--------------------+
        |                    |
        v                    v
Context / Retrieval       Tool Gateway
                              |
                              v
                       Enterprise APIs
                              |
                              v
                       Systems of Record
```

with cross-cutting concerns including:

```text
Identity
Authentication
Authorization
Security
Data Boundaries
Policy
Human Approval
Evaluation
Tracing
Observability
Audit
Cost
Latency
Reliability
```

This repository will progressively explore those concerns rather than assuming the model alone solves them.

---

## Disclaimer

This repository is an educational and architectural lab.

NorthStar Wealth Management, its customers, transfer cases, policies, operational metrics, and business scenarios are fictional.

Nothing in this repository should be interpreted as financial, investment, compliance, or legal advice.

The workflow is intentionally designed so that AI recommendations do not independently authorize consequential financial actions.# Enterprise AI Deployment Lab

A hands-on, model-agnostic lab for exploring how LLM-based systems move from promising prototypes toward controlled enterprise deployments.

The project uses a fictional wealth-management asset-transfer workflow to examine the architectural layers that need to surround an LLM before it can participate responsibly in an enterprise process.

The lab is intentionally evolving. Some capabilities are implemented and tested today; others are represented in the repository structure as planned architectural layers.

The guiding principle is:

> **AI prepares and recommends. Deterministic application controls and authorized humans govern consequential actions.**

---

## Why This Project Exists

Enterprise AI systems require more than a capable language model.

A model may produce a plausible answer while still lacking authoritative enterprise context, appropriate permissions, deterministic controls, evaluation, observability, or the ability to explain the basis of its recommendation.

This lab explores those boundaries by progressively building an enterprise AI workflow and examining questions such as:

- What happens when an LLM does not have authoritative enterprise context?
- How does grounding change the basis of a recommendation?
- What actually happens when an agent calls a tool?
- How should enterprise knowledge and policies be retrieved?
- How should agents interact with enterprise APIs and systems of record?
- Which decisions belong to the model, deterministic application logic, or humans?
- How should AI behavior be evaluated?
- What changes when moving from prototype to production?
- How do model choices affect quality, latency, cost, control, and deployment architecture?

The objective is not to demonstrate that an LLM can generate an answer.

The objective is to understand the architecture required to make AI behavior more grounded, controlled, observable, testable, and useful inside enterprise workflows.

---

## Fictional Enterprise Scenario

The lab uses a fictional company:

**NorthStar Wealth Management**

The example workflow is a customer asset transfer between brokerage institutions.

A representative fictional transfer case contains information such as:

- client name
- account type
- transfer type
- current custodian
- transfer documents
- account number
- customer signature
- brokerage statement

The AI assistant reviews the case, determines whether required information is present, consults available policy information, and prepares a recommendation.

The AI does **not** independently authorize or execute the financial transaction.

Consequential actions remain subject to deterministic application controls and human authorization.

All companies, customers, policies, cases, metrics, and business scenarios in this repository are fictional unless explicitly stated otherwise.

---

## Current Implementation

The current implementation includes:

- a fictional wealth-management transfer case
- prompt construction for transfer review
- an OpenAI Agents SDK-based provider
- structured model output using Pydantic
- a fictional transfer-policy tool
- observable agent/tool execution
- deterministic application-level workflow controls
- explicit human approval
- controlled post-approval processing
- automated workflow tests
- a reproducible grounding comparison experiment
- documented evidence from an observed grounding experiment

The current workflow can distinguish between:

```text
READY
```

and:

```text
BLOCKED
```

A `BLOCKED` case cannot reach approval or processing.

A `READY` case must still receive explicit human approval before the controlled processing function can execute.

---

## Current Architecture

The implemented workflow currently resembles:

```text
                     TRANSFER CASE
                          |
                          v
                   REVIEW PROMPT
                          |
                          v
                  OPENAI PROVIDER
                          |
                          v
                     AI AGENT
                          |
                    +-----+-----+
                    |           |
                    v           |
              POLICY TOOL       |
                 TP-101         |
                    |           |
                    +-----+-----+
                          |
                          v
              STRUCTURED REVIEW RESULT
                          |
                 +--------+--------+
                 |                 |
              BLOCKED             READY
                 |                 |
                 v                 v
            STOP WORKFLOW    HUMAN APPROVAL
                                   |
                           +-------+-------+
                           |               |
                         REJECT          APPROVE
                           |               |
                           v               v
                          STOP      CONTROLLED ACTION
```

This architecture intentionally separates several responsibilities:

**Model reasoning**  
The model interprets the case and generates a recommendation.

**Authoritative information**  
Tools provide information that should not simply be invented by the model.

**Deterministic application logic**  
Python controls whether a workflow is allowed to advance.

**Human authorization**  
An authorized reviewer decides whether a consequential action may proceed.

**Controlled execution**  
Processing occurs only after the application control and human approval requirements have been satisfied.

---

## Grounding Experiment

One of the first experiments in the lab examines the difference between a model producing a plausible recommendation and an agent having access to an authoritative policy source.

The same transfer case, prompt, provider implementation, agent instructions, and structured output are used in two runs.

Only policy-tool access changes:

```text
BEFORE
Transfer Case
     |
     v
    LLM
     |
     v
Plausible Recommendation
```

versus:

```text
AFTER
Transfer Case
     |
     v
   Agent
     |
     +------> Policy Tool TP-101
     |              |
     <--------------+
     |
     v
    LLM
     |
     v
Grounded Recommendation
```

In the observed baseline run, the model had no policy tool and produced additional requirements that were not established by an authoritative source supplied in the experiment.

In the observed grounded run, the agent called the policy tool and based its recommendation on the requirements returned by fictional policy `TP-101`.

This does **not** demonstrate that tool access eliminates hallucinations or guarantees correctness.

It demonstrates a narrower but important point:

> **Plausibility is not the same as authority.**

The reproducible experiment is located at:

```text
experiments/grounding_comparison.py
```

The observed Article 1 evidence is documented at:

```text
evidence/article-01-grounding.md
```

---

## Observable Agent Behavior

The lab exposes the execution lifecycle produced by the agent runtime.

When no tool was available in the grounding baseline, the observed execution was:

```text
MessageOutputItem
```

When the policy tool was available and selected by the agent, the observed execution was:

```text
ToolCallItem
ToolCallOutputItem
MessageOutputItem
```

Conceptually:

```text
Model Call
    |
    v
Tool Request
    |
    v
SDK Executes Python Tool
    |
    v
Tool Result
    |
    v
Model Continues
    |
    v
Final Structured Response
```

This distinction matters because the LLM itself is not directly executing enterprise code.

The agent runtime mediates the interaction between model reasoning and executable tools.

---

## Deterministic Workflow Controls

The model's recommendation does not determine whether a financial action executes.

Application code enforces the workflow boundary.

Conceptually:

```python
if response.status == "BLOCKED":
    stop_workflow()

if response.status == "READY":
    request_human_approval()
```

Only an approved `READY` case can reach the processing function.

This separation is intentional.

The model can recommend.

The application controls workflow state.

The human authorizes consequential action.

---

## What Has Been Tested

The current automated test suite contains four deterministic workflow tests.

### 1. BLOCKED cases stop

A `BLOCKED` model result must never reach:

- human approval
- transfer processing

### 2. READY + approved reaches processing

A `READY` result followed by explicit human approval can reach the controlled processing function.

### 3. READY + rejected stops

A `READY` model recommendation does not override a human rejection.

### 4. Invalid workflow states are rejected

The structured output schema accepts only:

```text
READY
BLOCKED
```

An unsupported state such as:

```text
PENDING
```

is rejected by Pydantic validation.

Run the tests with:

```bash
python -m pytest
```

---

## Project Structure

```text
enterprise-ai-lab/
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── guardrails/
│   ├── rag/
│   ├── tools/
│   │   └── transfer_policy.py
│   └── workflow/
│       ├── approval.py
│       ├── processing.py
│       ├── review.py
│       ├── review_result.py
│       └── transfer_case.py
│
├── architecture/
├── business-case/
│
├── data/
│   └── sample/
│
├── evals/
│   ├── datasets/
│   ├── evaluators/
│   └── results/
│
├── evidence/
│   └── article-01-grounding.md
│
├── experiments/
│   └── grounding_comparison.py
│
├── governance/
│
├── models/
│   ├── base.py
│   ├── anthropic/
│   │   ├── __init__.py
│   │   └── provider.py
│   ├── openai/
│   │   ├── __init__.py
│   │   └── provider.py
│   └── qwen/
│       ├── __init__.py
│       └── provider.py
│
├── tests/
│   └── test_workflow.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

Some directories represent architectural capabilities that are planned but not yet implemented.

Their presence in the repository should not be interpreted as evidence that those capabilities are complete.

---

## Model Strategy

The project is intentionally model-agnostic at the application architecture level.

The `ModelProvider` abstraction separates the workflow from a specific model provider:

```text
Enterprise Workflow
        |
        v
  ModelProvider
        |
   +----+----+----------+
   |         |          |
 OpenAI   Anthropic    Qwen
```

### Current

The OpenAI provider is currently used for the implemented agent workflow.

### Planned

Anthropic and local Qwen providers are represented in the repository structure for future comparison and experimentation.

Their presence does not imply equivalent functionality has already been implemented or tested.

The longer-term objective is to run comparable enterprise workflows and evaluations across multiple model/provider configurations.

---

## Setup

This project requires **Python 3.12 or later**.

Clone the repository and move into the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Configure required environment variables using `.env.example` as a reference.

Do not commit API keys or other secrets to the repository.

---

## Running the Current Lab

From the repository root:

```bash
python -m app.main
```

The workflow will:

1. load the fictional transfer case
2. construct the review prompt
3. run the AI agent
4. allow the agent to retrieve the transfer policy when needed
5. return a structured review result
6. apply deterministic workflow controls
7. request human approval when the case is `READY`
8. execute the controlled processing function only after approval

---

## Running the Grounding Experiment

From the repository root:

```bash
python -m experiments.grounding_comparison
```

The experiment creates two providers:

```text
Baseline  → agent_tools=[]
Grounded  → agent_tools=[get_transfer_policy]
```

Both receive the same fictional transfer case and review prompt.

The experiment prints both the agent execution lifecycle and the resulting structured recommendation.

Because model generation is probabilistic, repeated runs may not produce identical wording or recommendations.

The evidence file records one observed run; it should not be interpreted as a statistical benchmark.

---

## Running the Tests

Run:

```bash
python -m pytest
```

The project also uses GitHub Actions to run the automated tests on repository pushes and pull requests.

The CI workflow is defined in:

```text
.github/workflows/tests.yml
```

This provides an independent environment for validating the deterministic workflow tests.

---

## Implemented vs. Planned

A central goal of this repository is to distinguish what has actually been built from what is still being explored.

### Implemented / Tested

- fictional asset-transfer workflow
- structured AI review result
- OpenAI Agents SDK integration
- policy function tool
- observable tool-call lifecycle
- deterministic BLOCKED/READY workflow controls
- explicit human approval
- controlled processing action
- automated workflow tests
- GitHub Actions test execution
- grounding comparison experiment
- Article 1 grounding evidence

### Planned / Evolving

- enterprise RAG and retrieval architecture
- richer guardrails
- identity and authorization boundaries
- enterprise API integration patterns
- MCP experiments
- evaluation datasets and evaluators
- trace-based evaluation
- failure taxonomy
- regression evaluation
- production observability
- latency and cost measurement
- reliability testing
- Anthropic provider experiments
- local Qwen provider experiments
- cross-model evaluation

These planned capabilities will be documented as they are actually implemented and tested.

---

## Roadmap

The lab will evolve through several architectural layers:

```text
BUSINESS PROBLEM
       |
       v
LLM BEHAVIOR
       |
       v
GROUNDING
       |
       v
CONTEXT / RETRIEVAL
       |
       v
TOOLS / ENTERPRISE INTEGRATION
       |
       v
CONTROL / AUTHORIZATION
       |
       v
EVALUATION
       |
       v
PRODUCTION ARCHITECTURE
       |
       v
MODEL / ECONOMICS DECISION
```

The goal is not to add architectural complexity for its own sake.

Each layer should address an observed enterprise requirement, failure mode, control boundary, or measurable operational concern.

---

## Building an Enterprise AI Agent: Lessons from the Lab

The repository supports an eight-part series documenting what is built, tested, and observed as the architecture evolves.

### Part 1 — A Good LLM Answer Isn't Good Enough for the Enterprise

Grounding, authority, and the difference between plausible recommendations and recommendations supported by authoritative enterprise information.

### Part 2 — What Actually Happens When an AI Agent Calls a Tool?

Agent runtime behavior, tool selection, tool execution, and the model/tool interaction loop.

### Part 3 — Context Is an Architecture Problem, Not Just a Prompt Problem

Retrieval, RAG, policies, provenance, freshness, and access boundaries.

### Part 4 — How Does an AI Agent Actually Connect to the Enterprise?

APIs, tools, MCP, enterprise systems, authentication, identity, data boundaries, and systems of record.

### Part 5 — When Should an AI Agent Be Allowed to Act?

Human approval, deterministic controls, authorization, read/write boundaries, and security.

### Part 6 — How Do You Know an AI Agent Actually Works?

Evaluations, test cases, traces, failure taxonomy, regression testing, model quality, and operational metrics.

### Part 7 — From Prototype to Production: What Changes?

Deployment architecture, observability, resilience, latency, security, auditability, scaling, and operational change.

### Part 8 — OpenAI vs. Claude vs. Local Qwen: What Actually Matters in Enterprise Model Selection?

Comparing models using the same workflow, policies, and evaluation framework across quality, tool behavior, latency, cost, control, and deployment options.

---

## Evidence-First Approach

The development approach for this lab is:

> **BUILD → TEST → OBSERVE → DOCUMENT**

Claims in the accompanying articles should correspond to something that has actually been:

- implemented
- executed
- tested
- observed
- measured

Planned capabilities are identified as planned rather than presented as completed work.

The repository may evolve ahead of the article series. Git history and evidence artifacts provide the technical record behind specific observations discussed in the articles.

The Article 1 grounding experiment can be reproduced with:

```text
experiments/grounding_comparison.py
```

and its observed evidence is recorded in:

```text
evidence/article-01-grounding.md
```

---

## Enterprise Architecture Principle

The central architectural idea explored by this project is that:

> **The LLM is a component of the system, not the system itself.**

A production enterprise AI architecture may ultimately need to coordinate:

```text
Enterprise Application
        |
        v
API / Orchestration Layer
        |
        v
Agent Runtime
        |
        v
Model
        |
        +--------------------+
        |                    |
        v                    v
Context / Retrieval       Tool Gateway
                              |
                              v
                       Enterprise APIs
                              |
                              v
                       Systems of Record
```

with cross-cutting concerns including:

```text
Identity
Authentication
Authorization
Security
Data Boundaries
Policy
Human Approval
Evaluation
Tracing
Observability
Audit
Cost
Latency
Reliability
```

This repository will progressively explore those concerns rather than assuming the model alone solves them.

---

## Disclaimer

This repository is an educational and architectural lab.

NorthStar Wealth Management, its customers, transfer cases, policies, operational metrics, and business scenarios are fictional.

Nothing in this repository should be interpreted as financial, investment, compliance, or legal advice.

The workflow is intentionally designed so that AI recommendations do not independently authorize consequential financial actions.
