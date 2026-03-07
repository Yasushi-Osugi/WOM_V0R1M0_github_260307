# WOM System Overview

This document provides a high-level overview of WOM
(Weekly Operation Model).

WOM is designed as a **lot-based global supply chain planning system**
capable of simulating production, logistics, and demand fulfillment
using deterministic lot-level planning.

The system integrates:

- demand-driven planning
- hybrid push–pull supply chain control
- lot-level traceability
- explainable planning simulation

---

# 1 Core Concept

WOM planning is built on a simple principle:

Demand defines the lot.  
Lots define the plan.  
Supply fulfills the lots.

Instead of planning using scalar quantities,
WOM operates on **LOT_ID objects**.

All quantities are derived from:


quantity = len(lot_ID_list)


---

# 2 WOM Planning Model

The WOM planning model consists of four conceptual layers.


Demand Layer
↓
Planning Engine Layer
↓
Supply Chain Network Layer
↓
Execution / Visualization Layer


---

# 3 Demand Layer

Planning begins from **final market demand**.

Demand is represented as:


LOT_ID lists


Each LOT_ID represents:

- product
- market location
- consumption week
- lot sequence

Example:


TOKYO_DC-DRUG_A-2026050001


Demand is anchored at **leaf nodes of the outbound supply chain**.

---

# 4 Planning Engine Layer

The WOM planning engine simulates supply chain flows
using a deterministic pipeline.

Planning process:


Demand generation
↓
LOT_ID creation
↓
Backward lead-time shift
↓
Forward supply simulation
↓
Shipment allocation


The planning engine operates on **PSI lot lists**.


P_ids = production lot list
I_ids = inventory lot list
S_ids = shipment lot list


---

# 5 Supply Chain Network Layer

WOM models supply chains as **directed tree networks**.

Two interconnected supply chains exist.

## Inbound Supply Chain


Material suppliers
↓
Component suppliers
↓
Manufacturing plant (MOM)


Control logic:


PUSH


Production is synchronized and flows forward.

---

## Outbound Supply Chain


Manufacturing (MOM)
↓
Distribution yard (DAD)
↓
Decoupling stock point
↓
Regional distribution
↓
Market node (leaf)


Control logic:


PUSH → PULL


Products are pushed to the decoupling point,
then pulled by market demand.

---

# 6 Decoupling Stock Point

The decoupling stock point separates:


production-driven supply
and
demand-driven shipment


Functions:

- buffer demand volatility
- stabilize production
- enable prioritized shipment

---

# 7 Hybrid Push–Pull Control

The complete WOM flow is:


Inbound Supply Chain
(PUSH)

↓
Manufacturing (MOM)

↓
Outbound PUSH

↓
Decoupling Stock Point

↓
Outbound PULL

↓
Market Demand


This structure enables both:

- stable production planning
- flexible demand fulfillment

---

# 8 Explainable Planning

Because WOM operates on LOT_ID objects,
every lot can be traced through the network.

Example trace:


LOT_ID

TOKYO_DC-DRUG_A-2026050002

production node
↓
distribution yard
↓
inventory buffer
↓
market shipment


This enables transparent planning diagnostics.

---

# 9 WOM Architecture Components

The WOM system consists of the following modules.


WOM
├ planning engine
├ supply chain network model
├ plugin system
├ scenario system
└ visualization layer


---

## Planning Engine

Core lot-based PSI simulation.

Defined in:


WOM_PIPELINE_SPEC.md


---

## Network Model

Represents supply chain structure
as node-edge tree networks.

Handles:

- lead times
- capacities
- inventory buffers

---

## Plugin System

Allows custom planning logic to be injected.

Examples:

- promotion planning
- allocation rules
- scenario adjustments

---

## Scenario System

Defines planning scenarios such as:


As-Is
To-Be
What-If
Stress test


Used for supply chain simulation experiments.

---

## Visualization Layer

Current implementations include:

- matplotlib-based visual interface
- Excel integration (planned)
- scenario comparison graphs

---

# 10 WOM as an Economic Planning Platform

While WOM began as a supply chain planning engine,
its architecture enables broader applications.

Potential extensions include:

- enterprise planning systems
- AI-assisted planning environments
- economic system simulation

WOM may serve as a foundation for a future
**economic operating system**.

---

# 11 Relationship Between Core Documents

The WOM repository documentation hierarchy is:


WOM_DESIGN_PRINCIPLES.md
↓
WOM_PLANNING_THEORY.md
↓
WOM_SYSTEM_OVERVIEW.md
↓
ARCHITECTURE.md
↓
WOM_PIPELINE_SPEC.md
↓
LOT_ID_SPEC.md


This structure ensures that:

- philosophy
- theory
- architecture
- algorithms
- data models

are consistently defined.

---

# 12 Summary

WOM introduces a new approach to supply chain planning.

Key characteristics:

- demand-anchored planning
- lot-based simulation
- hybrid push–pull supply chains
- explainable planning logic

This combination enables deterministic,
transparent, and flexible supply chain planning.