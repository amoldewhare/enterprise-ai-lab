# Enterprise AI Deployment Lab

A hands-on, model-agnostic lab for exploring how LLM-based systems move from promising prototypes toward controlled enterprise deployments.

The project uses a fictional wealth-management asset-transfer workflow to examine the architectural layers that need to surround an LLM before it can participate responsibly in an enterprise process.

The lab is intentionally evolving. Capabilities are progressively built, tested, observed, and documented as the architecture develops.

The guiding principle is:

> **AI prepares and recommends. Deterministic application controls and authorized humans govern consequential actions.**

---

## Lab Progress

This repository is being built progressively alongside an eight-part **Enterprise AI Deployment Lab** series.

Each part introduces an architectural question, builds or modifies the working lab to investigate it, and documents what was actually observed.

| Part | Focus | Status |
|---|---|---|
| Part 1 | Authoritative grounding | Published / Implemented |
| Part 2 | Tool-calling lifecycle | Published / Implemented |
| Part 3 | Context discovery and retrieval | Published / Implemented |
| Part 4 | Enterprise connectivity | Next |
| Part 5 | Control and authorization | Planned |
| Part 6 | Evaluation | Planned |
| Part 7 | Production architecture | Planned |
| Part 8 | Model selection | Planned |

A capability is not treated as implemented simply because it appears in the architecture or roadmap.

The accompanying articles follow capabilities that have been built, run, and observed in the public repository.

---

## Why This Project Exists

Enterprise AI systems require more than a capable language model.

A model may produce a plausible answer while still lacking authoritative enterprise context, appropriate permissions, deterministic controls, evaluation, observability, or a reliable basis for its recommendation.

This lab explores those boundaries by progressively building an enterprise AI workflow and asking questions such as:

- What happens when an LLM does not have authoritative enterprise context?
- How does grounding change the basis of a recommendation?
- What actually happens when an LLM requests a tool?
- What executes the tool?
- How does the right enterprise context reach the LLM?
- How should enterprise knowledge be discovered and retrieved?
- How should AI systems interact with enterprise APIs and systems of record?
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

The AI system reviews the case, determines what information it needs, retrieves available enterprise policy context, and prepares a structured recommendation.

The AI does **not** independently authorize or execute the financial transaction.

Consequential actions remain subject to deterministic application controls and explicit human authorization.

All companies, customers, policies, cases, metrics, and business scenarios in this repository are fictional unless explicitly stated otherwise.

---

## Current Implementation

The current lab includes:

- a fictional wealth-management transfer workflow
- prompt construction for transfer review
- an OpenAI Agents SDK-based provider
- structured model output using Pydantic
- a fictional enterprise policy repository
- deterministic Python tools
- observable tool-call execution
- a grounding comparison experiment
- a tool-calling lifecycle experiment
- a simple policy context discovery and retrieval experiment
- deterministic application-level workflow controls
- explicit human approval
- controlled post-approval processing
- automated workflow tests
- evaluation cases and evaluators
- evidence files documenting observed experiments

The current workflow can return:

```text
READY
```

or:

```text
BLOCKED
```

A `BLOCKED` case cannot reach approval or processing.

A `READY` recommendation still requires explicit human approval before the controlled processing function can execute.

> **READY is a recommendation, not authorization.**

---

## Current Architecture

The architecture has evolved through the first three experiments.

The current conceptual flow is:

```text
TRANSFER CASE
     |
     v
    LLM
     |
     |  What information do I need?
     v
TOOL REQUEST
     |
     v
AGENT RUNTIME
     |
     v
CONTEXT DISCOVERY / RETRIEVAL
     |
     v
ENTERPRISE POLICY REPOSITORY
     |
     v
CANDIDATE AUTHORITATIVE CONTEXT
     |
     v
    LLM
     |
     |  What does this mean for this case?
     v
STRUCTURED REVIEW RESULT
     |
 +---+---+
 |       |
 v       v
BLOCKED READY
 |       |
 v       v
STOP   HUMAN APPROVAL
          |
      +---+---+
      |       |
      v       v
    REJECT  APPROVE
      |       |
      v       v
     STOP  CONTROLLED ACTION
```

This architecture intentionally separates several responsibilities.

### Model Reasoning

The LLM interprets the business case, determines when available external context is needed, and produces a structured recommendation.

### Tool Request

The LLM can request an available tool. Requesting a tool is not the same as executing it.

### Agent Runtime

The runtime mediates between the LLM and executable capabilities.

The LLM does not directly execute Python functions.

### Deterministic Tools

Python functions perform defined operations such as retrieving information from the fictional enterprise policy repository.

### Enterprise Context

Enterprise knowledge exists outside the LLM and can be supplied dynamically when relevant to the business case.

### Deterministic Application Logic

Application code controls whether the workflow is allowed to advance.

### Human Authorization

An authorized reviewer determines whether a consequential action may proceed.

### Controlled Execution

Processing occurs only after application controls and human approval requirements have been satisfied.

---

## Part 1 Experiment — Authoritative Grounding

The first experiment examined the difference between a model producing a plausible recommendation and a system giving the model access to an authoritative enterprise policy.

Conceptually:

```text
WITHOUT AUTHORITATIVE POLICY

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
WITH AUTHORITATIVE POLICY

Transfer Case
     |
     v
    LLM
     |
     v
Tool Request
     |
     v
Runtime
     |
     v
Policy Tool
     |
     v
Authoritative Policy
     |
     v
    LLM
     |
     v
Grounded Recommendation
```

In the observed baseline run, the model had no policy tool and produced additional requirements that were not established by an authoritative source supplied in the experiment.

In the observed grounded run, the policy was made available through a tool and the recommendation was based on the requirements returned by fictional policy `TP-101`.

This does **not** demonstrate that tool access eliminates hallucinations or guarantees correctness.

It demonstrates a narrower but important point:

> **Plausibility is not the same as authority.**

The reproducible experiment is located at:

```text
experiments/grounding_comparison.py
```

Observed evidence is documented at:

```text
evidence/article-01-grounding.md
```

---

## Part 2 Experiment — What Happens When the LLM Requests a Tool?

The second experiment examined what happens between the model determining that external information is needed and the final structured response.

The observed runtime lifecycle included:

```text
ToolCallItem
ToolCallOutputItem
MessageOutputItem
```

Conceptually:

```text
LLM
 |
 | Tool Request
 v
AGENT RUNTIME
 |
 v
EXECUTABLE PYTHON TOOL
 |
 v
TOOL RESULT
 |
 v
LLM CONTINUES
 |
 v
STRUCTURED RESPONSE
```

This exposed an important architectural distinction.

> **The LLM requests the capability. The runtime executes the capability.**

The LLM itself is not directly executing enterprise Python code.

The runtime mediates the interaction between probabilistic model reasoning and deterministic executable capabilities.

The experiment is located at:

```text
experiments/tool_call_lifecycle.py
```

Observed evidence is documented at:

```text
evidence/article-02-tool-calling.md
```

The evidence represents an observed execution. It should not be interpreted as proof that every model or runtime execution will behave identically.

---

## Part 3 Experiment — Context Discovery and Retrieval

The third experiment asked a different question:

> **How does the right enterprise context get to the LLM in the first place?**

The policy repository contained multiple fictional policies:

```text
TP-101 — Full Account Transfer Requirements
TP-102 — Partial Account Transfer Requirements
TP-103 — Retirement Account Transfer Requirements
```

### Experiment 1 — Opaque Policy Lookup

The available tool required the LLM to provide an internal policy identifier:

```text
get_transfer_policy(policy_id)
```

The transfer case identified the business situation as a:

```text
Full Account Transfer
```

but the LLM had not been given the internal identifier `TP-101`.

In the observed execution, it requested:

```text
get_transfer_policy("asset_transfer_review")
```

No matching policy existed.

The deterministic tool therefore returned:

```text
{}
```

The LLM then continued and produced a `BLOCKED` recommendation containing plausible requirements that were not present in the enterprise policy repository.

The failure exposed an important distinction:

> **Enterprise knowledge existing somewhere in the system does not mean the correct enterprise context reaches the LLM.**

### Experiment 2 — Searchable Policy Context

The retrieval interface was changed to:

```text
search_transfer_policies(query)
```

The transfer case was not changed.

The LLM was not told which policy to select.

Instead, it could express the information it needed using business terms from the transfer case.

The runtime executed the deterministic search against the policy repository.

The simple search returned multiple candidate policies.

The LLM then identified `TP-101 — Full Account Transfer Requirements` as applicable to the case and produced:

```text
status = READY
policy_id = TP-101
missing_requirements = []
```

The experiment demonstrated a narrower architectural lesson:

> **Giving an LLM access to enterprise knowledge is not enough. The architecture has to get the right enterprise context to the model at the right time.**

The retrieval implementation is intentionally simple.

It is **not** intended to represent a production enterprise RAG architecture, sophisticated semantic search system, or authority-resolution mechanism.

Observed evidence is documented at:

```text
evidence/article-03-context-retrieval.md
```

---

## Context as an Architectural Layer

The first three experiments progressively changed the mental model.

Part 1 asked:

```text
Does the recommendation have an authoritative basis?
```

Part 2 asked:

```text
What actually happens when external information is requested?
```

Part 3 asked:

```text
How does the relevant enterprise information get onto that path?
```

The resulting conceptual architecture is:

```text
ENTERPRISE KNOWLEDGE
        |
        v
CONTEXT DISCOVERY / RETRIEVAL
        |
        v
RELEVANT AUTHORITATIVE CONTEXT
        |
        v
       LLM
        |
        v
STRUCTURED RECOMMENDATION
```

The current experiment focuses on discovering relevant context.

More advanced problems—such as conflicting sources, authority resolution, provenance, sophisticated retrieval, and large-scale enterprise knowledge architectures—are outside the scope of the current implementation.

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

Only an approved `READY` case can reach the controlled processing function.

This separation is intentional:

```text
LLM              → recommends
Application      → controls workflow state
Human            → authorizes consequential action
Processing code  → executes approved action
```

A model recommendation is therefore not equivalent to enterprise authorization.

---

## What Has Been Tested

The lab contains deterministic workflow tests covering important application-control boundaries.

These include:

### BLOCKED cases stop

A `BLOCKED` model result must never reach human approval or transfer processing.

### READY + approved reaches processing

A `READY` recommendation followed by explicit human approval can reach the controlled processing function.

### READY + rejected stops

A `READY` recommendation does not override a human rejection.

### Invalid workflow states are rejected

The structured output schema accepts only:

```text
READY
BLOCKED
```

Unsupported workflow states are rejected by schema validation.

The lab also contains evaluation cases used to exercise transfer-review behavior across different missing-requirement scenarios.

These evaluations are groundwork for the deeper evaluation architecture explored later in the series.

Run the automated tests with:

```bash
python -m pytest
```

---

## Model, Runtime, Tool, and Application

The lab uses these terms deliberately.

### LLM

The probabilistic reasoning component.

It interprets information, determines when an available capability may be useful, and generates structured output.

### Agent

The configured AI system construct that combines the LLM with instructions, available tools, structured output expectations, and runtime behavior.

### Agent Runtime

The orchestration layer that manages interaction between the LLM and executable capabilities.

### Tool

A deterministic capability that can be requested by the LLM and executed by the runtime.

### Application

The surrounding deterministic software responsible for workflow state, controls, authorization boundaries, and consequential execution.

Keeping these responsibilities separate is important when reasoning about enterprise AI architecture.

---

## Model Strategy

The project is intentionally model-agnostic at the application architecture level.

The `ModelProvider` abstraction is intended to separate the enterprise workflow from a specific model provider:

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

The OpenAI provider is currently used for the implemented agent workflow and experiments.

### Planned

Anthropic and local Qwen providers are represented for future comparison and experimentation.

Their presence does not imply equivalent functionality has already been implemented or tested.

The longer-term objective is to run comparable enterprise workflows and evaluations across multiple model/provider configurations.

---

## Setup

This project requires **Python 3.12 or later**.

Clone the repository:

```bash
git clone https://github.com/amoldewhare/enterprise-ai-lab.git
cd enterprise-ai-lab
```

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
3. run the configured AI system
4. allow the LLM to request available enterprise context
5. execute the requested tool through the runtime
6. return retrieved context to the LLM
7. produce a structured review result
8. apply deterministic workflow controls
9. request human approval when the case is `READY`
10. execute the controlled processing function only after approval

---

## Running the Experiments

### Part 1 — Grounding

```bash
python -m experiments.grounding_comparison
```

This compares behavior with and without authoritative policy-tool access.

### Part 2 — Tool-Calling Lifecycle

```bash
python -m experiments.tool_call_lifecycle
```

This exposes the observed runtime items associated with tool use.

Part 3 context-discovery behavior is exercised through the current workflow and documented in:

```text
evidence/article-03-context-retrieval.md
```

Because model generation is probabilistic, repeated executions may not produce identical wording, tool requests, or recommendations.

Evidence files record observed executions. They should not be interpreted as statistical benchmarks or guarantees of future behavior.

---

## Running the Tests

Run:

```bash
python -m pytest
```

The project also uses GitHub Actions to run automated tests on repository pushes and pull requests.

The CI workflow is defined in:

```text
.github/workflows/tests.yml
```

This provides an independent environment for validating deterministic workflow tests.

---

## Implemented vs. Planned

A central discipline of this repository is distinguishing what has actually been built from what is still being explored.

### Implemented / Tested / Observed

- fictional asset-transfer workflow
- structured AI review result
- OpenAI Agents SDK integration
- deterministic policy tools
- fictional multi-policy repository
- observable tool-call lifecycle
- simple context discovery and policy retrieval
- deterministic `BLOCKED` / `READY` workflow controls
- explicit human approval
- controlled processing action
- automated workflow tests
- GitHub Actions test execution
- transfer-review evaluation cases
- grounding comparison experiment
- tool-calling lifecycle experiment
- context-retrieval experiment
- evidence for Parts 1–3

### Planned / Evolving

- enterprise API integration patterns
- identity and authentication boundaries
- authorization controls
- richer guardrails
- read/write capability boundaries
- deeper evaluation architecture
- trace-based evaluation
- failure taxonomy
- regression evaluation
- production observability
- resilience and reliability testing
- latency and cost measurement
- Anthropic provider experiments
- local Qwen provider experiments
- cross-model evaluation
- production deployment architecture

Planned capabilities will be documented as implemented only after they have actually been built and exercised.

---

## Roadmap

The lab progresses through eight architectural questions:

```text
PART 1
AUTHORITATIVE GROUNDING
       |
       v
PART 2
TOOL-CALLING LIFECYCLE
       |
       v
PART 3
CONTEXT DISCOVERY / RETRIEVAL
       |
       v
PART 4
ENTERPRISE CONNECTIVITY
       |
       v
PART 5
CONTROL / AUTHORIZATION
       |
       v
PART 6
EVALUATION
       |
       v
PART 7
PRODUCTION ARCHITECTURE
       |
       v
PART 8
MODEL SELECTION
```

The goal is not to add architectural complexity for its own sake.

Each layer should address an observed enterprise requirement, failure mode, control boundary, or measurable operational concern.

---

# Building an Enterprise AI Agent: Lessons from the Lab

The repository supports an eight-part series documenting what is built, tested, and observed as the architecture evolves.

## Part 1 — A Good LLM Answer Isn't Good Enough for the Enterprise

**Core question:** How do you ground an LLM in authoritative enterprise policy rather than accept plausible reasoning?

The experiment compares an ungrounded recommendation with one based on policy information retrieved through a tool.

---

## Part 2 — What Actually Happens When an AI Agent Calls a Tool?

**Core question:** What happens between the model determining that it needs information, requesting a tool, receiving the result, and continuing its reasoning?

The experiment exposes the runtime lifecycle around tool requests and deterministic Python execution.

---

## Part 3 — Context Is an Architecture Problem, Not Just a Prompt Problem

**Core question:** How should enterprise context be supplied and controlled rather than simply placed into prompts?

The experiment explores the difference between having enterprise knowledge available and enabling the system to discover and supply context relevant to the business case.

---

## Part 4 — How Does an AI Agent Actually Connect to the Enterprise?

**Core question:** How do AI systems interact with APIs, enterprise systems, data, and executable capabilities?

This stage will extend the lab beyond the current fictional policy repository toward enterprise connectivity patterns.

---

## Part 5 — When Should an AI Agent Be Allowed to Act?

**Core question:** Where do permissions, deterministic controls, approval boundaries, and human authorization belong?

This stage will examine the boundary between recommending an action and being authorized to execute one.

---

## Part 6 — How Do You Know an AI Agent Actually Works?

**Core question:** How do you evaluate AI behavior systematically rather than judging a handful of convincing responses?

This stage will build on the existing evaluation groundwork and examine repeatable evaluation of AI behavior.

---

## Part 7 — From Prototype to Production: What Changes?

**Core question:** What additional architecture, controls, observability, and operational capabilities are required when moving toward production?

This stage will examine the difference between a working lab and an operational enterprise AI system.

---

## Part 8 — OpenAI vs. Claude vs. Local Qwen: What Actually Matters in Enterprise Model Selection?

**Core question:** How should enterprises think about model choice once the surrounding architecture exists?

The goal is to compare model/provider configurations using a common workflow and evaluation approach rather than comparing models in isolation.

---

## Evidence-First Development

The development discipline for this lab is:

> **BUILD → TEST → COMMIT → PUSH → VERIFY → WRITE → PUBLISH**

The public repository should lead the article series, not follow it.

A technical capability should not appear in an article as implemented before the corresponding code and evidence exist in the public repository.

Claims in the accompanying articles should correspond to something that has actually been:

- implemented
- executed
- tested or experimentally exercised
- observed
- documented

Planned capabilities are identified as planned rather than presented as completed work.

Evidence artifacts provide a technical record behind observations discussed in the series.

Current evidence includes:

```text
evidence/article-01-grounding.md
evidence/article-02-tool-calling.md
evidence/article-03-context-retrieval.md
```

---

## Enterprise Architecture Principle

The central architectural idea explored by this project is:

> **The LLM is a component of the system, not the system itself.**

As the lab evolves, the broader architecture may need to coordinate:

```text
ENTERPRISE APPLICATION
        |
        v
API / ORCHESTRATION LAYER
        |
        v
AGENT RUNTIME
        |
        v
       LLM
        |
   +----+----+
   |         |
   v         v
CONTEXT     TOOL
DISCOVERY   REQUESTS
   |         |
   v         v
ENTERPRISE  CONTROLLED
KNOWLEDGE   CAPABILITIES
             |
             v
        ENTERPRISE APIs
             |
             v
        SYSTEMS OF RECORD
```

with cross-cutting concerns that may include:

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

These are architectural concerns to be progressively explored.

Their presence in this roadmap should not be interpreted as evidence that each capability has already been implemented.

---

## Scope of the Lab

This repository intentionally starts simple.

The objective is to make architectural boundaries visible through small, runnable experiments rather than introduce production-scale infrastructure before the underlying problem has been demonstrated.

For example, the current context experiment uses a small fictional policy repository and deterministic keyword retrieval.

It does not claim to implement production-scale:

- enterprise RAG
- vector search
- hybrid retrieval
- reranking
- authority resolution
- enterprise IAM
- policy engines
- production observability
- large-scale agent orchestration

Those are deeper architectural problems that should be introduced only when the lab reaches the problem they are intended to solve.

---

## Disclaimer

This repository is an educational and architectural lab.

NorthStar Wealth Management, its customers, transfer cases, policies, operational metrics, and business scenarios are fictional.

Nothing in this repository should be interpreted as financial, investment, compliance, or legal advice.

The workflow is intentionally designed so that AI recommendations do not independently authorize consequential financial actions.