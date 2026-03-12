# WOM Execution Model

## Overview

This document defines the **runtime execution model** of WOM (Weekly Operation Model).

While the architecture documents describe system structure,
this document explains **how the planning engine executes during runtime**.

The execution model describes:

- the planning cycle
- event processing
- simulation loop
- resolver decision process
- artifact generation

The WOM engine operates as a **deterministic planning loop**.

---

# 1 Core Execution Loop

The WOM engine executes a closed-loop planning cycle.


Scenario Initialization
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
Resolver Search
↓
Operator Application
↓
Re-simulation


This loop continues until a termination condition is reached.

---

# 2 Execution Phases

The planning engine runs in several phases.

## Phase 1: Scenario Initialization

The scenario defines the planning environment.

Inputs include:

- demand parameters
- network structure
- capacity constraints
- pricing assumptions
- planning horizon

The scenario initializes:


network topology
initial inventory
policy parameters


---

## Phase 2: Demand Generation

Module:


demand_model.py


Responsibilities:

- generate demand signals
- simulate price response
- apply promotion or policy effects

Output:


DemandEvent

{
product_id
location
time
quantity
}


Demand events represent market demand entering the system.

---

## Phase 3: Flow Simulation

Module:


flow_engine.py


The Flow Engine processes event streams.

Core event types:


ProductionEvent
ShipmentEvent
ArrivalEvent
SaleEvent


Responsibilities:

- generate lots
- simulate production
- simulate logistics flows
- propagate shipments through the network
- compute derived inventory states

Key rule:


Flow events are the primary system truth.


---

# 4 Event Stream Model

The WOM engine is event-driven.

Example event structure:


FlowEvent

{
event_id
lot_id
event_type
node
time
quantity
source
}


Event streams are stored in:


flow_events.json


State views are derived from these events.

---

# 5 State Derivation

The planning state is derived from flow events.

Examples of derived state:


Inventory
Backlog
Service Level
Capacity Usage
Financial Metrics


Important rule:


State must not be directly modified.


State is always recomputed from event streams.

---

# 6 Trust Event Detection

After state derivation, the system detects anomalies.

Examples:


Stockout risk
Inventory overflow
Capacity overload
Supply delay
Demand surge


Detected events are recorded in:


trust_events.json


Trust events trigger planning responses.

---

# 7 Evaluation Phase

Module:


evaluation.py


The evaluation phase computes plan quality.

Typical metrics:


Profit
Service Level
Inventory Stability
Capacity Balance
Risk Exposure


Example evaluation function:

U(plan)

w1 * service_level

w2 * profit

w3 * inventory_cost

w4 * risk


The evaluation score represents the quality of the current plan.

---

# 8 Resolver Search

Module:


resolver.py


The resolver is the decision engine.

Responsibilities:


interpret trust events
generate candidate operators
simulate candidate scenarios
evaluate results
select best operator


Resolver workflow:


Detect issue
→ Generate operators
→ Apply operator
→ Re-run simulation
→ Evaluate result
→ Select best action


---

# 9 Operator Model

Operators modify system behavior.

Examples:


Increase production
Shift shipment
Reroute logistics
Use buffer inventory
Adjust price


Operators are represented as structured instructions.

Example:


operator_spec.json


Operators must modify **flow events**, not state.

---

# 10 Re-Simulation

After operator application, the system re-runs the flow simulation.


Operator → Flow Update → State Recalculation


This produces a new system state.

---

# 11 Termination Conditions

The planning loop stops when:


No trust events remain
Evaluation score converges
Maximum iterations reached
User-defined stopping condition


---

# 12 Execution Artifacts

The WOM engine generates several structured artifacts.

Examples:


flow_events.json
trust_events.json
operator_spec.json
evaluation_results.json
scenario_manifest.json


These artifacts support:

- explainable planning
- reproducibility
- scenario comparison
- AI-assisted analysis

---

# 13 Determinism and Reproducibility

The WOM execution model must guarantee:


deterministic execution
reproducible results
explicit event traces


Random processes must use controlled seeds.

Scenario manifests must record:


input parameters
engine version
operator sequence


---

# 14 Execution Philosophy

The WOM engine follows these core principles:

Flow-first modeling  
Derived state computation  
Operator-based plan modification  
Closed-loop planning simulation  
Explainable decision processes  

---

# 15 Summary

The WOM execution model can be summarized as:


Demand
↓
Flow Simulation
↓
State Derivation
↓
Evaluation
↓
Resolver Decision
↓
Operator Application
↓
Re-Simulation


This cycle transforms WOM from a static planning tool into a **dynamic economic planning engine**.

---

# End of Document