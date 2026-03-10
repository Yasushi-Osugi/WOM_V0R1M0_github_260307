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