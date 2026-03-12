# WOM Architecture

This document describes the architecture of WOM (Weekly Operation Model).

WOM is designed as a modular planning platform capable of supporting:

- global supply chain planning
- scenario simulation
- AI-assisted planning
- future economic system modeling

The architecture follows the principles defined in:

- WOM_DESIGN_PRINCIPLES.md
- DEV_ROADMAP.md
- AI_TEAM.md
- AI_MEETING_PROTOCOL.md

---

# 1 Architectural Overview

The WOM system consists of five major layers.

Scenario Layer  
Network Model Layer  
Planning Kernel  
Plugin System  
Interaction Layer  

Overall flow:

Scenario  
↓  
Network Construction  
↓  
Planning Kernel  
↓  
Plugin Stages  
↓  
Result Generation  
↓  
Interaction Layer  

This layered architecture ensures:

- modular extensibility
- deterministic planning behavior
- explainable decision logic
- compatibility with AI-assisted planning systems

---

# 2 Architectural Identity

WOM is not merely a weekly PSI calculation system.

WOM is designed as a **planning kernel capable of representing and transforming economic flow networks**.

Its purpose is to:

- represent supply and demand flows
- evaluate constraint violations
- generate corrective planning operators
- simulate alternative scenarios
- support explainable management decisions

The core philosophy of WOM is:

Flow / Event = Source of Truth  
State        = Derived View  

Planning states such as inventory, service level, or capacity utilization are **not primary data**.

Instead, they are derived from flow events.

Example:

Inventory(node,t) =
Σ arrivals(node ≤ t)
− Σ departures(node ≤ t)

This architecture ensures:

- consistent planning logic
- stable simulation behavior
- explainable system states

---

# 3 Scenario Layer

The scenario layer defines the planning context.

Responsibilities:

- demand input
- supply configuration
- network structure
- scenario parameters

Primary locations:

data/  
examples/  
pysi/scenario/

Scenarios must be:

- reproducible
- version-controlled
- deterministic

Scenarios are used for:

- development testing
- regression validation
- AI diagnostics

---

# 4 Network Model Layer

The network layer constructs the supply chain model.

Nodes represent:

- factories
- distribution centers
- markets

Edges represent:

- transport flows
- supply relationships

Primary modules:

pysi/network/

Responsibilities:

- node creation
- edge creation
- capacity definitions
- lead time modeling

The network model forms the structural foundation for planning.

---

# 5 Planning Kernel

The planning kernel performs the PSI planning calculation.

Unlike a simple pipeline, the WOM kernel operates as a **closed-loop planning engine**.

Kernel stages include:

Demand Generation  
Flow Simulation  
State Derivation  
Trust Event Detection  
Evaluation  
Resolver Decision  
Operator Application  

Kernel execution loop:

Network Model  
↓  
Demand Generation  
↓  
Flow Simulation  
↓  
State Derivation  
↓  
Trust Event Detection  
↓  
Evaluation  
↓  
Resolver Decision  
↓  
Operator Application  
↓  
Re-simulation  

Primary modules:

pysi/plan/  
pysi/core/

The kernel must remain:

- deterministic
- explainable
- modular

---

# 6 Decision Loop Architecture

Beyond the basic kernel execution, WOM operates as a **decision loop system**.

The planning cycle follows:

Detect  
↓  
Summarize  
↓  
Decide  
↓  
Apply  
↓  
Recalculate  

Components:

| Stage | Function |
|------|----------|
| Detect | detect constraint violations |
| Summarize | generate trust summaries |
| Decide | select corrective operators |
| Apply | modify flows |
| Recalculate | recompute system state |

Key artifacts generated during execution:

- trust_events.json
- trust_summary.json
- operator_spec.json

This loop forms the basis for **AI-assisted planning**.

---

# 7 Resolver and Search Architecture

The WOM planning kernel includes a **resolver subsystem** responsible for generating and evaluating corrective planning actions.

The resolver converts diagnostic signals into candidate planning operators and determines the most appropriate corrective action.

This subsystem enables WOM to function as an **explainable planning and decision-support engine**.

## 7.1 Resolver Position in the Architecture

Planning State  
↓  
Trust Event Detection  
↓  
Resolver  
↓  
Operator Execution  
↓  
Recalculated Planning State  

Responsibilities of the resolver:

- interpret diagnostic signals
- generate candidate operators
- simulate operator effects
- evaluate outcomes
- select an operator to apply

---

## 7.2 Planning State

The resolver operates on the **derived planning state**.

Planning state includes:

- inventory levels
- capacity utilization
- backlog levels
- service levels
- demand fulfillment status
- financial indicators

Planning state is not stored directly but derived from flow events.

---

## 7.3 Trust Event Detection

Trust events represent anomalies or constraint violations detected during planning.

Examples:

E_INVENTORY_CAP_EXCEEDED  
E_STOCKOUT_RISK  
E_CAPACITY_OVERLOAD  
E_SUPPLY_DELAY  

Trust events are stored in:


trust_events.json


Each trust event contains:

- event_type
- node
- time
- severity
- context_data

---

## 7.4 Candidate Operator Generation

For each trust event, the resolver generates corrective actions called **operators**.

Examples:

- increase production
- delay shipment
- reallocate supply
- activate buffer inventory
- adjust demand priority

Example operator specification:


{
"operator": "increase_production",
"node": "factory_A",
"time": "2026-W12",
"quantity": 200
}


Candidates are stored in:


operator_candidates.json


---

## 7.5 Search Strategy

The resolver may use different search strategies:

- rule-based selection
- greedy improvement
- beam search
- Monte Carlo simulation
- AI-assisted heuristic search

Search strategies are **pluggable**.

This allows experimentation with different planning intelligence approaches.

---

## 7.6 Simulation

Each candidate operator is evaluated via simulation.

Simulation process:

Apply operator  
↓  
Re-run planning kernel  
↓  
Recompute flows  
↓  
Recalculate derived states  

The resulting state is then evaluated.

---

## 7.7 Evaluation Function

Each simulated state is evaluated using an **evaluation function**.

Typical metrics include:

- service level
- inventory stability
- capacity utilization balance
- cost
- revenue impact
- profit impact

Example evaluation result:


{
"operator": "increase_production",
"score": 0.84,
"service_level": 0.97,
"inventory_penalty": 0.12
}


Evaluation functions remain transparent and explainable.

---

## 7.8 Operator Selection

After evaluating candidates, the resolver selects the best operator.

Best operator  
↓  
Applied to planning model  
↓  
Planning kernel recalculated  

The chosen operator is recorded in:


operator_spec.json


This file represents the **planning decision trace**.

---

## 7.9 Explainability and Traceability

Key artifacts:

- trust_events.json
- operator_candidates.json
- operator_spec.json
- trust_summary.json

These artifacts enable:

- reproducibility
- debugging
- AI-assisted planning review
- management explanation

---

# 8 Plugin System

The plugin system enables extensible planning behavior.

Plugins modify planning behavior without changing core engine logic.

Plugin directory:

pysi/plugins/

Example plugins:

- capacity_allocator
- demand_priority
- inventory_buffer_control

Standard plugin interface:


def apply_plugin(state, context):
return modified_state


---

# 9 Interaction Layer

The interaction layer provides user access to the planning system.

Two interaction modes exist.

Developer interaction:

- matplotlib visualization
- debug tools

Business interaction:

- Excel templates
- Excel dashboards
- scenario comparison sheets

Preferred interaction model:

Excel → WOM Engine → Excel

---

# 10 Result Generation

Planning results include:

- PSI time series
- inventory levels
- capacity utilization
- service level metrics

Results are used for:

- scenario evaluation
- visualization
- AI diagnostic analysis

---

# 11 Testing and Validation

Planning results must be validated through reproducible scenarios.

Example executions:

python -m tools.run_phone_v0  
python -m tools.run_pharma_v0  

Validation checks include:

- execution success
- reproducibility
- output stability

Regression scenarios must be maintained.

---

# 12 Integration with AI Development Model

The WOM architecture integrates with the AI development framework.

Development roles:

- AI Architect
- AI Engine Developer
- AI Plugin Developer
- AI Scenario Designer
- AI Excel UX Designer
- AI Tester

Architectural decisions are governed by:

AI_MEETING_PROTOCOL.md

System evolution follows:

DEV_ROADMAP.md

---

# 13 Architectural Principles

The architecture must follow these rules:

Planning kernel clarity is prioritized over feature complexity.

Plugins must extend behavior without modifying core engine logic.

Scenarios must remain reproducible.

User interaction must not introduce architectural coupling.

---

# 14 Long-Term Evolution

The WOM architecture will evolve toward a planning platform capable of supporting:

- global supply chain simulation
- AI planning dialogue
- economic network modeling

The architecture must remain stable while enabling gradual expansion.