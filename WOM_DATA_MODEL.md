# WOM DATA MODEL

This document defines the conceptual data model of WOM
(Weekly Operation Model).

It explains the core objects used by the planning engine
and how they relate to each other.

The WOM data model is built around one central concept:

LOT_ID

Unlike traditional APS systems that operate on scalar quantities,
WOM operates on **explicit lot objects**.

---

# 1 Core Design Principle

Traditional planning systems:

Demand → Quantity

WOM:

Demand → LOT_ID objects

Every demand signal generates a set of LOT_IDs,
which become the atomic planning units throughout the entire supply chain.

---

# 2 WOM Core Data Structure

The WOM planning model can be understood as the interaction of
five core data structures.


Scenario
│
▼
Network
│
▼
LOT_ID
│
▼
PSI Lists
│
▼
Evaluation


Each structure represents a different layer of planning.

---

# 3 Scenario

A Scenario defines the planning problem.

Typical elements:


Scenario
├ planning horizon
├ demand input
├ product definitions
├ node configuration
├ lot size configuration
├ lead times
└ capacity constraints


Scenarios are loaded by:


pysi/scenario/


---

# 4 Network Model

The Network model represents the physical supply chain.


Network
├ Node
│ ├ factory (MOM)
│ ├ distribution center (DAD)
│ ├ decoupling stock point
│ └ market leaf node
│
└ Edge
├ logistics link
├ lead time
└ capacity


Nodes form a **tree structure** representing supply chain topology.

Inbound supply chain:


Material → Factory


Outbound supply chain:


Factory → Distribution → Market


Defined in:


pysi/network/


---

# 5 LOT_ID (Core Object)

The most important object in WOM is:


LOT_ID


A LOT_ID represents a specific unit of demand fulfillment.

Format:


NODE-PRODUCT-YYYYWWNNNN


Example:


TOKYO_STORE-A-PRODUCT_X-2025460003


Meaning:


node : TOKYO_STORE-A
product : PRODUCT_X
time bucket : 2025 week 46
sequence : lot 0003


A LOT_ID represents:


one physical production / shipment lot


---

# 6 LOT_ID Generation

LOT_IDs are generated from demand signals.

Process:


Monthly Demand
│
▼
Daily Expansion
│
▼
Weekly Aggregation
│
▼
Lot Size Conversion
│
▼
LOT_ID List


Example:


weekly demand = 250 units
lot size = 100

S_lot = 3

LOT_ID list:

TOKYO-A-2025460001
TOKYO-A-2025460002
TOKYO-A-2025460003


These LOT_IDs become the **planning objects** of the engine.

---

# 7 PSI Data Structure

WOM planning is executed using PSI lists.


PSI
├ P[t] = Production LOT_ID list
├ S[t] = Shipment LOT_ID list
└ I[t] = Inventory LOT_ID list


Important:


PSI lists contain LOT_ID objects
not scalar quantities


Example:


S[2025-W46]

[
LOT_2025460001,
LOT_2025460002
]


Inventory is also represented as LOT_ID sets.

---

# 8 Planning Transformation

Planning transforms LOT_ID positions over time.

Initial state:


LOT_ID located at market node


Backward planning:


shift by lead time


Example:


market demand
2025-W46

factory production
2025-W42


Forward planning then determines the final execution schedule.

---

# 9 Supply Chain Control Logic

WOM uses hybrid push–pull planning.

Inbound supply chain:


PUSH


Material flows forward toward factories.


supplier → factory


Outbound supply chain:


PUSH + PULL

factory → distribution → decoupling stock


Then:


decoupling stock → market


using demand-driven pull.

---

# 10 Inventory Representation

Inventory is the set of LOT_IDs currently stored at a node.


Inventory(node, t)
= set of LOT_ID


Inventory balancing equation:


I[t] = I[t-1] + P[t] - S[t]


But instead of scalar arithmetic,
WOM performs set operations on LOT_ID lists.

---

# 11 Evaluation Layer

After planning, WOM evaluates results.

Evaluation dimensions:


cost
revenue
margin
service level
inventory level
capacity utilization


Evaluation attaches financial metrics to LOT flows.

Implemented in:


pysi/evaluate/


---

# 12 WOM Data Model Summary

The WOM system can be summarized as:


Scenario
│
▼
Network
│
▼
LOT_ID generation
│
▼
PSI planning
│
▼
Push–Pull execution
│
▼
Evaluation


---

# 13 Mental Model

A simple way to understand WOM:


Demand creates LOT_IDs
LOT_IDs move through the network
PSI tracks their movement
planning decides their timing
evaluation measures their value


---

# 14 Relationship to Other Documents

This document connects the core WOM design documents.


WOM_SYSTEM_OVERVIEW.md
│
▼
WOM_PLANNING_THEORY.md
│
▼
WOM_PIPELINE_SPEC.md
│
▼
LOT_ID_SPEC.md
│
▼
WOM_DATA_MODEL.md


---

# 15 Final Insight

The most important idea of WOM is:


Supply chain planning should operate
on traceable lot objects
rather than anonymous quantities.


This allows:


traceability
explainable planning
scenario simulation
economic evaluation


within a single unified planning engine.