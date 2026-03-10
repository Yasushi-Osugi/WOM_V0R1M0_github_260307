WOM Architecture (Extended Draft)

This document describes the architecture of WOM (Weekly Operation Model).

WOM is designed as a modular planning platform capable of supporting:

global supply chain planning

scenario simulation

AI-assisted planning

future economic system modeling

WOM is intended not only as a planning tool but as the kernel of a future AI planning and management operating system.

The architecture follows the principles defined in:

WOM_DESIGN_PRINCIPLES.md

DEV_ROADMAP.md

AI_TEAM.md

AI_MEETING_PROTOCOL.md

1 Architectural Overview

The WOM system consists of five major layers.

Scenario Layer
Network Model Layer
Planning Pipeline
Plugin System
Interaction Layer

Overall flow:

Scenario
↓
Network Construction
↓
Planning Pipeline
↓
Plugin Stages
↓
Result Generation
↓
Interaction Layer

This layered architecture ensures:

modular extensibility

deterministic planning behavior

explainable decision logic

compatibility with AI-assisted planning systems

2 Architectural Identity

WOM is not merely a weekly PSI calculation system.

WOM is designed as a planning kernel capable of representing and transforming economic flow networks.

Its purpose is to:

represent supply and demand flows

evaluate constraint violations

generate corrective planning operators

simulate alternative scenarios

support explainable management decisions

The core philosophy of WOM is:

Flow / Event = Source of Truth
State        = Derived View

Planning states such as inventory, service level, or capacity utilization are not treated as primary data.
Instead, they are derived from flow events.

3 Scenario Layer

The scenario layer defines the planning context.

Responsibilities:

demand input

supply configuration

network structure

scenario parameters

Primary locations:

data/
examples/
pysi/scenario/

Scenarios must be:

reproducible

version-controlled

deterministic

Scenarios are used for:

development testing

regression validation

AI diagnostics

4 Network Model Layer

The network layer constructs the supply chain model.

Nodes represent:

factories

distribution centers

markets

Edges represent:

transport flows

supply relationships

Primary modules:

pysi/network/

Responsibilities:

node creation

edge creation

capacity definitions

lead time modeling

The network model forms the structural foundation for planning.

5 Core Data Model

The WOM architecture is based on a flow-centric data model.

Core Entities
Lot
Flow
Event
State View
Lot

Represents the identity of goods moving through the network.

Flow

Represents the movement or transformation of lots.

Example:

production
shipment
arrival
sale
Event

Events describe the time-stamped occurrence of flows.

Example event structure:

time
event_type
node
quantity
State Views

Planning states such as:

inventory

backlog

service level

capacity utilization

are calculated from flow events.

Example:

Inventory(node,t) =
   Σ arrivals(node ≤ t)
 − Σ departures(node ≤ t)

This design ensures:

stable planning logic

efficient LOT handling

consistent Monthly / Weekly aggregation

6 Planning Pipeline

The planning pipeline performs PSI planning calculations.

Pipeline stages:

Demand Propagation
Supply Allocation
Capacity Adjustment
Inventory Balancing

Pipeline flow:

Network Model
↓
Demand Propagation
↓
Supply Allocation
↓
Capacity Adjustment
↓
Inventory Balance
↓
Result Generation

Primary modules:

pysi/plan/
pysi/core/

The pipeline must remain:

deterministic

explainable

modular

7 Decision Loop Architecture

Beyond the basic pipeline, WOM operates as a decision loop system.

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

Stage	Function
Detect	detect constraint violations
Summarize	generate trust summaries
Decide	select corrective operators
Apply	modify flows
Recalculate	recompute system state

Key artifacts:

trust_events.json
trust_summary.json
operator_spec.json

This loop forms the basis for AI-assisted planning.

8 Plugin System

The plugin system enables extensible planning behavior.

Plugins modify planning behavior without changing core engine logic.

Plugin directory:

pysi/plugins/

Example plugins:

capacity_allocator

demand_priority

inventory_buffer_control

Future plugin categories may include:

pricing policy

promotion policy

demand generation models

financial evaluation models

scenario comparison logic

Standard plugin interface:

def apply_plugin(state, context):
    return modified_state
9 Interaction Layer

The interaction layer provides user access to the planning system.

Two interaction modes exist.

Developer interaction

matplotlib visualization

debug tools

Business interaction

Excel templates

Excel dashboards

scenario comparison sheets

Preferred interaction model:

Excel → WOM Engine → Excel

Future extensions may include:

AI planning dialogue

scenario comparison assistants

automated decision recommendations

10 Result Generation

Planning results include:

PSI time series

inventory levels

capacity utilization

service level metrics

financial indicators

Results are used for:

scenario evaluation

visualization

AI diagnostic analysis

11 Testing and Validation

Planning results must be validated through reproducible scenarios.

Example executions:

python -m tools.run_phone_v0
python -m tools.run_pharma_v0

Validation checks include:

execution success

reproducibility

output stability

Regression scenarios must be maintained.

12 Integration with AI Development Model

The WOM architecture integrates with the AI development framework.

Development roles:

AI Architect
AI Engine Developer
AI Plugin Developer
AI Scenario Designer
AI Excel UX Designer
AI Tester

Architectural decisions are governed by:

AI_MEETING_PROTOCOL.md

System evolution follows:

DEV_ROADMAP.md
13 Demand and Financial Extension

While WOM initially focuses on supply chain planning, the architecture supports expansion toward integrated business planning.

Future flow events may include:

demand_event
sale_event
promotion_event
pricing_event
financial_event

This allows WOM to connect:

Supply Flow
↓
Sale Events
↓
Revenue
↓
Profit

Through this mechanism WOM can support:

revenue simulation

profit evaluation

marketing scenario testing

14 Kernel Boundary and Expansion Policy

The WOM kernel is intentionally kept minimal.

The kernel includes:

flow representation

event processing

capacity reasoning

trust event detection

operator execution

explainable simulation loops

The kernel excludes:

UI-specific spreadsheet logic

customer-specific rules

business templates

non-general heuristics

Such logic should be implemented as plugins.

15 Long-Term Evolution

WOM is designed to evolve toward a broader planning platform capable of supporting:

global supply chain simulation

AI planning dialogue

integrated demand and supply modeling

financial scenario evaluation

economic network simulation

The architecture must remain stable while enabling gradual expansion.

WOM is therefore best understood as:

Planning Kernel
for
AI-assisted Economic and Management Systems

16 Resolver and Search Architecture

The WOM planning kernel includes a resolver subsystem responsible for generating and evaluating corrective planning actions.

The resolver transforms diagnostic signals into candidate planning operators and determines the most appropriate corrective action.

This subsystem enables WOM to function as an explainable planning and decision-support engine.

16.1 Role of the Resolver

The resolver sits between diagnostic detection and planning modification.

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

interpret diagnostic signals

generate candidate operators

simulate operator effects

evaluate outcomes

select an operator to apply

The resolver ensures that planning modifications are systematic, explainable, and reproducible.

16.2 Planning State

The resolver operates on the current planning state.

Planning state is derived from the flow/event model and includes:

Inventory levels
Capacity utilization
Backlog levels
Service levels
Demand fulfillment status
Financial indicators

The planning state is not treated as primary data but as a derived view over flow events.

16.3 Trust Event Detection

Trust events represent anomalies or constraint violations detected during planning.

Examples:

E_INVENTORY_CAP_EXCEEDED
E_STOCKOUT_RISK
E_CAPACITY_OVERLOAD
E_SUPPLY_DELAY

Trust events are stored in:

trust_events.json

These events act as triggers for the resolver.

Each trust event contains:

event_type
node
time
severity
context_data
16.4 Candidate Operator Generation

For each trust event, the resolver generates possible corrective actions.

These actions are called operators.

Examples of operators:

Increase production
Delay shipment
Reallocate supply
Activate buffer inventory
Adjust demand priority

Operators are represented as structured instructions.

Example operator specification:

{
  "operator": "increase_production",
  "node": "factory_A",
  "time": "2026-W12",
  "quantity": 200
}

Candidate operators are stored in:

operator_candidates.json
16.5 Search Strategy

The resolver explores candidate operators using a search strategy.

Possible strategies include:

Rule-based selection
Greedy improvement
Beam search
Monte Carlo simulation
AI-assisted heuristic search

The architecture does not enforce a specific strategy.

Instead, the search strategy is pluggable and extensible.

This allows experimentation with different planning intelligence approaches.

16.6 Simulation

Each candidate operator is evaluated through simulation.

Simulation involves:

Apply operator
↓
Re-run planning pipeline
↓
Recompute flows
↓
Recalculate derived states

The resulting state is then evaluated.

Simulation results are stored in the run bundle for reproducibility.

16.7 Evaluation Function

Each simulated candidate state is evaluated using an evaluation function.

Typical evaluation metrics include:

Service level
Inventory stability
Capacity utilization balance
Cost
Revenue impact
Profit impact

Evaluation functions may vary depending on scenario objectives.

Example evaluation output:

{
  "operator": "increase_production",
  "score": 0.84,
  "service_level": 0.97,
  "inventory_penalty": 0.12
}

Evaluation functions are designed to remain transparent and explainable.

16.8 Operator Selection

After evaluating candidate operators, the resolver selects the best operator according to the evaluation function.

Best operator
↓
Applied to planning model
↓
Planning pipeline recalculated

The chosen operator is recorded in:

operator_spec.json

This file represents the planning decision trace.

16.9 Explainability and Traceability

All resolver decisions must remain explainable.

Key artifacts:

trust_events.json
operator_candidates.json
operator_spec.json
trust_summary.json

These files enable:

reproducibility

debugging

AI-assisted planning review

management explanation

The resolver therefore supports transparent decision processes.

16.10 Integration with AI Planning Systems

The resolver architecture allows integration with AI planning systems.

Possible extensions:

LLM-assisted operator generation
Reinforcement learning evaluation
Monte Carlo tree search
Scenario ranking by AI agents

However, the core architecture ensures that:

AI suggestions remain explainable
and reproducible within the planning framework
16.11 Relationship to Management Decision Support

Within the broader WOM architecture, the resolver functions as the decision engine of the planning system.

Detect
↓
Summarize
↓
Resolver Search
↓
Operator Selection
↓
Replan

This loop enables WOM to evolve from a planning tool into a structured management decision-support platform.

The resolver therefore forms a central component of the long-term AI-assisted planning and management operating system vision.