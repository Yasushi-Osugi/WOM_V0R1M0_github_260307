# WOM Planning Pipeline Specification

This document defines the planning pipeline used by WOM
(Weekly Operation Model).

The pipeline is responsible for computing PSI planning results
across a supply chain network.

This specification is used by:

- AI Engine Developer
- AI Plugin Developer
- AI Tester
- Codex implementation agents

The pipeline must satisfy the following properties:

- deterministic
- explainable
- reproducible
- extensible via plugins

---

# 1 Pipeline Overview

The planning pipeline transforms a scenario and network model
into a PSI planning result.

Pipeline structure:

Scenario
↓
Network Model
↓
Planning Pipeline
↓
Result Generation


The planning pipeline consists of four stages.

Stage 1: Demand Propagation  
Stage 2: Supply Allocation  
Stage 3: Capacity Adjustment  
Stage 4: Inventory Balancing

---

# 2 Data Model

The pipeline operates on a **time-series network state**.

Each node maintains a weekly PSI structure.

Node state:

P[t] : Production or Purchase  
S[t] : Shipment or Sales  
I[t] : Inventory  

For each week t.

Inventory balance equation:

I[t] = I[t-1] + P[t] - S[t]

Nodes are connected through supply edges.

Edge attributes:

lead_time  
transport_capacity  
cost  

---

# 3 Stage 1 — Demand Propagation

Purpose:

Propagate downstream demand to upstream nodes.

Example:

Market demand
→ Distribution Center
→ Factory

Algorithm:

1. Read demand at market nodes
2. Convert demand to shipment requirement
3. Propagate demand upstream considering lead time
4. Create required supply signals

Pseudo logic:

for each market node:
    demand = demand[t]

for each upstream edge:
    upstream_demand[t - lead_time] += demand[t]

Output:

Required supply demand at upstream nodes.

---

# 4 Stage 2 — Supply Allocation

Purpose:

Allocate available supply to satisfy propagated demand.

Constraints:

production capacity  
inventory availability  
transport limits  

Algorithm:

1. Check available supply sources
2. Allocate supply based on priority rule
3. Update shipment plans

Possible allocation policies:

- priority based
- proportional
- cost minimization

Pseudo logic:

for node in supply_nodes:
    available_supply = inventory + production

for demand_request:
    allocate supply until demand satisfied or capacity reached

Output:

Shipment plan S[t]

---

# 5 Stage 3 — Capacity Adjustment

Purpose:

Ensure that production and transport capacity constraints
are respected.

Types of capacity constraints:

production capacity  
transport capacity  
inventory limits  

Algorithm:

1. Detect capacity violations
2. Adjust production or shipment
3. Shift production if necessary

Pseudo logic:

if production > capacity:
    reduce production
    push unmet demand downstream

if transport > capacity:
    delay shipment

Output:

Feasible supply plan.

---

# 6 Stage 4 — Inventory Balancing

Purpose:

Compute final inventory levels.

Equation:

I[t] = I[t-1] + P[t] - S[t]

Algorithm:

1. Apply PSI balance equation
2. Detect negative inventory
3. Adjust shipments if necessary

Pseudo logic:

for each node:
    inventory[t] = inventory[t-1] + P[t] - S[t]

if inventory < 0:
    trigger shortage logic

Output:

Final PSI time series.

---

# 7 Plugin Hooks

Plugins allow extensions without modifying the core pipeline.

Plugins may run at the following stages:

before_stage_1  
after_stage_1  

before_stage_2  
after_stage_2  

before_stage_3  
after_stage_3  

before_stage_4  
after_stage_4  

Plugin interface:

def apply_plugin(state, context):
    return modified_state

Plugins may implement:

inventory buffering  
priority rules  
promotion demand adjustment  
dynamic capacity policies

---

# 8 Result Generation

The final output includes:

PSI time series  
inventory levels  
shipment flows  
capacity utilization  

Results must be exportable to:

CSV  
Excel  
visualization tools

---

# 9 Determinism Requirements

The pipeline must be deterministic.

Given:

scenario input  
network model  
plugin configuration  

The output must always be identical.

This enables:

reproducible simulations  
AI diagnostics  
scenario comparisons

---

# 10 Test Requirements

All pipeline changes must pass the following scenarios.

phone_supply_chain  
pharma_cold_chain  

Additional stress tests:

capacity_stress  
demand_spike  

Tests must verify:

execution success  
PSI balance validity  
reproducibility

---

# 11 Future Extensions

Future pipeline capabilities may include:

multi-source allocation  
price-based planning  
service-level optimization  
AI-assisted planning operators  

The pipeline architecture must remain stable while enabling
incremental expansion.
