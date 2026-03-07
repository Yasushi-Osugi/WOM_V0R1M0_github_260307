# AI Meeting Protocol for WOM AI Research Lab

This document defines the meeting and decision-making protocol used by the WOM AI Research Lab.

The purpose of this protocol is to maintain architectural consistency and enable structured collaboration between AI roles.

This protocol is used whenever non-trivial design decisions are required.

---

# 1 Purpose

The AI meeting protocol ensures that:

- architecture remains consistent
- design decisions are transparent
- development tasks are coordinated across AI roles
- system evolution remains controlled

The protocol follows a **structured polling model**.

---

# 2 Meeting Triggers

An AI meeting should be initiated when any of the following occurs.

Architecture related:

- planning engine structure change
- network model modification
- plugin interface modification

Algorithm related:

- planning algorithm change
- constraint handling modification
- performance redesign

User interaction related:

- Excel interaction model change
- visualization redesign

System evolution:

- large refactoring
- new subsystem introduction

---

# 3 Meeting Participants

Participants correspond to roles defined in `AI_TEAM.md`.

Core participants:


AI Architect
AI Engine Developer
AI Plugin Developer
AI Scenario Designer
AI Excel UX Designer
AI Tester


Optional participants:


Human project owner
Additional domain experts


---

# 4 Meeting Input

Before the meeting begins, the following information should be prepared.

Problem description:


what problem triggered the meeting


Affected modules:


pysi/core
pysi/plan
pysi/plugins
Excel interface
scenario datasets


Proposed change:


initial candidate solution


Reference materials:


code files
scenarios
performance metrics


---

# 5 Polling Discussion Model

Discussion follows a **fixed polling order**.


1 AI Architect
2 AI Engine Developer
3 AI Plugin Developer
4 AI Scenario Designer
5 AI Excel UX Designer
6 AI Tester


Each participant provides three elements:


problem analysis
proposal
risk


Example response format:


Role: AI Engine Developer

Problem
current planning algorithm cannot handle constraint X

Proposal
introduce capacity-aware allocation step

Risk
may increase computation time


The goal is not debate but **structured perspective aggregation**.

---

# 6 Decision Rule

Final decisions are made by:


AI Architect


The Architect integrates all proposals and produces:


final design decision
implementation direction
affected modules


Example output:


Decision

Introduce plugin-based capacity allocation module.

Affected modules

pysi/plugins/capacity_allocator.py
pysi/plan/planning_pipeline.py


---

# 7 Implementation Assignment

After a decision is made, implementation tasks are assigned.

Typical assignments:

| Task | Responsible Role |
|-----|------------------|
planning algorithm update | AI Engine Developer |
plugin implementation | AI Plugin Developer |
scenario update | AI Scenario Designer |
visualization change | AI Excel UX Designer |
validation | AI Tester |

---

# 8 Verification Process

All implementations must be validated.

Testing includes:

Execution test


python -m tools.run_phone_v0


Scenario validation:

- demand scenarios
- supply disruption scenarios
- capacity constraint scenarios

Regression checks must confirm:

- no execution failures
- output consistency
- scenario reproducibility

---

# 9 Meeting Output

Each meeting must produce a structured output.

Required elements:


Decision
Design rationale
Affected modules
Implementation tasks
Responsible roles
Test scenario


Example format:


Decision

Introduce plugin-based allocation stage.

Reason

Improves flexibility of planning pipeline.

Tasks

Implement capacity_allocator plugin
Update planning pipeline
Add test scenario

Responsible roles

Plugin Developer
Engine Developer
Tester


---

# 10 Meeting Log

Meeting results should be recorded in a structured format.

Suggested location:


docs/ai_meetings/


Example file:


docs/ai_meetings/2026-03-07_capacity_allocation_design.md


Meeting logs should contain:


problem
discussion summary
decision
implementation tasks


---

# 11 Guiding Principles

All discussions must follow these principles.

Keep the system:


simple
modular
explainable
reproducible


Avoid:


uncontrolled complexity
hidden algorithm behavior
architecture drift


---

# 12 Long-Term Vision

The WOM AI Research Lab aims to build a planning platform capable of supporting:

- global supply chain planning
- scenario simulation
- planning dialogue with AI systems

The meeting protocol ensures that system evolution remains coherent as complexity grows.
