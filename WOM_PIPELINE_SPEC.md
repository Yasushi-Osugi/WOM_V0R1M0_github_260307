# WOM Planning Pipeline Specification (v2)

This document defines the core planning pipeline of WOM
(Weekly Operation Model).

This specification follows the **V0R8 canonical design**
defined in:

251024WSO仕様書

In WOM, PSI is not represented as scalar quantities.
Instead, the planning engine operates on **lot_ID lists**.

All quantities are derived as:

quantity = len(list)

The planning engine core process is therefore:

PSI list handling.

---

# 1 Canonical Data Model

Each node maintains weekly PSI buckets.

For each week w:

psi[w] = [S_ids, CO_ids, I_ids, P_ids]

Where:

S_ids : shipped lot_ID list  
CO_ids : carry-over list  
I_ids : inventory lot_ID list  
P_ids : production / purchase lot_ID list

All elements are:

list[str]

Example:

I_ids[w] = ["LOT_A1", "LOT_A2", "LOT_A3"]

Quantity:

len(I_ids[w]) = 3

---

# 2 Planning Pipeline Overview

The WOM planning pipeline executes the following stages.

Stage 0 Network Initialization  
Stage 1 Demand Propagation  
Stage 2 Supply Allocation  
Stage 3 Capacity Adjustment  
Stage 4 PSI List Balancing  

Pipeline flow:

Scenario
↓
Network Construction
↓
Planning Pipeline
↓
Result Generation

---

# 3 Stage 0 — Network Initialization

Purpose:

Construct the supply chain network and initialize PSI structures.

For each node:

initialize weekly PSI buckets.

Example:

psi[w] = [[], [], [], []]

Meaning:

S_ids = []
CO_ids = []
I_ids = []
P_ids = []

Initial inventory is represented as lot_ID entries in I_ids[week0].

Example:

I_ids[0] = ["INIT_A1","INIT_A2","INIT_A3"]

---

# 4 Stage 1 — Demand Propagation

Purpose:

Propagate downstream demand upstream through the network.

Demand is expressed as required shipment lots.

Example:

market demand = 50 units

Converted to lot demand:

n_lots = demand / LOT_SIZE

Algorithm:

for each demand node:

generate required lot_IDs

Example:

DEM_MKT_W10_001
DEM_MKT_W10_002
...

Demand propagation:

Market → Distribution Center → Factory

Lead time is applied.

If lead_time = 2:

demand at week w

creates supply request at

week w-2.

Output:

required shipment lots at upstream nodes.

---

# 5 Stage 2 — Supply Allocation

Purpose:

Allocate supply lots to satisfy propagated demand.

Sources of supply:

inventory lots  
production lots  

Supply pool:

available_lots = I_ids + P_ids

Allocation rule:

match available lots to demand lots.

Pseudo process:

for demand_lot in demand_list:

if inventory lot available:
    allocate inventory lot

else if production capacity available:
    create production lot

else:
    shortage

Shipment lot_IDs are appended to S_ids.

Example:

S_ids[w].append(lot_id)

---

# 6 Stage 3 — Capacity Adjustment

Purpose:

Ensure production and transport capacity constraints are respected.

Capacity constraints include:

production capacity  
transport capacity  
inventory capacity  

Algorithm:

detect violations.

Example:

if len(P_ids[w]) > production_capacity:

excess lots must be shifted or removed.

Possible adjustments:

production delay  
shipment delay  
backlog creation  

Capacity adjustment modifies the lot lists.

Example:

move lot_ID from P_ids[w] to P_ids[w+1]

---

# 7 Stage 4 — PSI List Balancing

This stage performs the core WOM process.

PSI list handling.

Scalar PSI equations are **not directly executed**.
Instead, inventory balance emerges from list operations.

---

## 7.1 Inventory Roll Forward

Inventory list rolls to next week.

Algorithm:

I_ids[w] = copy(I_ids[w-1])

---

## 7.2 Production Merge

Production lots are added to inventory.

Algorithm:

I_ids[w].extend(P_ids[w])

---

## 7.3 Shipment Consumption

Shipment lots are removed from inventory.

Algorithm:

for lot in shipment_request:

remove lot from I_ids[w]

add lot to S_ids[w]

---

## 7.4 Shortage Handling

If inventory is insufficient.

Synthetic lot_IDs may be generated.

Example:

SYN_NODE_W10_001

These represent shortage coverage.

---

# 8 Derived PSI Quantities

Scalar PSI quantities are derived.

Example:

Inventory quantity:

I_qty[w] = len(I_ids[w])

Production quantity:

P_qty[w] = len(P_ids[w])

Shipment quantity:

S_qty[w] = len(S_ids[w])

Derived invariant:

len(I_ids[w]) =
len(I_ids[w-1])
+ len(P_ids[w])
- len(real_shipped_lots)

---

# 9 Plugin Hooks

Plugins may modify PSI lists.

Plugin execution points:

before_stage_1  
after_stage_1  

before_stage_2  
after_stage_2  

before_stage_3  
after_stage_3  

before_stage_4  
after_stage_4  

Plugin interface:

def apply_plugin(node_state, context):
    return modified_state

Plugins may implement:

inventory buffers  
priority rules  
promotion adjustments  
allocation policies  

---

# 10 Result Generation

Final outputs include:

PSI lot lists  
PSI scalar quantities  
shipment flows  
inventory levels  

Exports:

CSV  
Excel  
visualization tools  

---

# 11 Determinism Requirement

The WOM planning pipeline must be deterministic.

Given:

scenario  
network configuration  
plugin set  

The pipeline must produce identical results.

This enables:

scenario comparison  
AI diagnosis  
AI planning assistance  

---

# 12 Testing Requirements

Pipeline changes must pass regression scenarios.

Example scenarios:

phone_supply_chain  
pharma_cold_chain  

Stress tests:

capacity stress  
demand spike  

Validation criteria:

PSI list consistency  
no orphan lot_IDs  
inventory balance integrity  

---

# 13 Long-Term Evolution

Future pipeline extensions may include:

multi-source allocation  
price-based planning  
profit evaluation  
AI-assisted planning  

The canonical PSI representation (lot_ID lists)
must remain stable.
