# WOM Architecture Diagram

This document explains the full structure of WOM
(Weekly Operation Model) in a single conceptual diagram.

The purpose of this document is to provide a visual and structural
overview of the WOM system for:

- repository readers
- AI development agents
- system designers
- future research publications

---

# 1 Full Conceptual Diagram

```text
┌──────────────────────────────────────────────────────────────┐
│                      FINAL MARKET DEMAND                    │
│        (leaf node / final consumption / sales channel)      │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ Demand is converted into
                              │ LOT_ID lists
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                         LOT_ID LAYER                         │
│   NODE + PRODUCT + YYYYWW + SEQUENCE                        │
│   Example: TOKYO_DC-DRUG_A-2026050001                       │
│   Meaning: demand-anchored final consumption lot            │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ backward lead-time shift
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    BACKWARD PLANNING LAYER                   │
│   LOT_IDs are shifted upstream in time                      │
│   to the latest feasible shipment / production position     │
│   Identity is preserved                                     │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ initialize feasible positions
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    WOM PLANNING ENGINE                       │
│                  (lot-based PSI simulation)                  │
│                                                              │
│   Stage 1  Demand Propagation                               │
│   Stage 2  Supply Allocation                                │
│   Stage 3  Capacity Adjustment                              │
│   Stage 4  PSI List Balancing                               │
│                                                              │
│   State representation:                                     │
│   P_ids / I_ids / S_ids / CO_ids                            │
│                                                              │
│   quantity = len(lot_id_list)                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ forward supply simulation
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                 SUPPLY CHAIN NETWORK MODEL                   │
│                                                              │
│   Inbound Supply Chain: PUSH                                │
│   Material / Parts leaf nodes                               │
│        ↓                                                     │
│   Suppliers / Components                                    │
│        ↓                                                     │
│   MOM (Mother Of Manufacturing)                             │
│                                                              │
│   Outbound Supply Chain: PUSH → PULL                        │
│   MOM                                                        │
│    ↓                                                         │
│   DAD (Distribution And Delivery)                           │
│    ↓  PUSH                                                   │
│   Decoupling Stock Point                                    │
│    ↓  PULL                                                   │
│   Regional / Market Distribution                            │
│    ↓                                                         │
│   Leaf Market Node                                          │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ prioritized shipment
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                  DECISION / CONTROL LOGIC                    │
│                                                              │
│   Outbound shipment priority:                               │
│   - urgency                                                  │
│   - priority customer                                        │
│   - profit contribution                                      │
│                                                              │
│   Decoupling point absorbs demand gap between:              │
│   - volatile market demand                                  │
│   - leveled production                                       │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ results
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    RESULT / OUTPUT LAYER                     │
│                                                              │
│   PSI time series                                            │
│   shipment flow                                              │
│   inventory levels                                           │
│   capacity utilization                                       │
│   service / shortage diagnostics                             │
│   scenario comparison                                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ visualization / interaction
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                 EXECUTION / INTERACTION LAYER                │
│                                                              │
│   Developer mode:                                            │
│   - matplotlib visualization                                 │
│   - debug tools                                              │
│                                                              │
│   Business mode:                                             │
│   - Excel templates                                          │
│   - Excel dashboards                                         │
│   - scenario comparison sheets                               │
│                                                              │
│   Preferred business interaction:                            │
│   Excel → WOM Engine → Excel                                 │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ explainable analysis
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    AI / RESEARCH LAB LAYER                   │
│                                                              │
│   AI Team                                                    │
│   - Architect                                                │
│   - Engine Developer                                         │
│   - Plugin Developer                                         │
│   - Scenario Designer                                        │
│   - Excel UX Designer                                        │
│   - Tester                                                   │
│                                                              │
│   AI Meeting Protocol                                        │
│   AI Self-Evolution                                          │
│   Dev Roadmap                                                │
└──────────────────────────────────────────────────────────────┘
2 Interpretation

The WOM architecture can be understood as the integration of:

demand-anchored lot identity

backward positioning logic

forward hybrid push–pull simulation

explainable output generation

AI-assisted system evolution

WOM is therefore not just a planning engine.

It is a structured planning platform composed of:

theory

algorithm

data model

execution model

AI development model

3 Layer Summary
Demand Layer

The starting point of WOM.

Final market demand is represented as LOT_ID lists.

LOT_ID Layer

The canonical planning unit.

Each LOT_ID encodes:

leaf market node

product

consumption week

lot sequence

Backward Planning Layer

Moves demand lots backward through time
according to lead time.

This defines the latest feasible fulfillment position.

Planning Engine Layer

Performs deterministic PSI list handling.

Core planning state is represented by lot lists:

P_ids

I_ids

S_ids

CO_ids

Supply Chain Network Layer

Represents the physical and logical structure of supply chains.

Includes both:

inbound PUSH structure

outbound PUSH → PULL structure

Decision Layer

Defines shipment priorities and decoupling logic.

This is where demand volatility and production leveling
are reconciled.

Result Layer

Produces explainable planning results.

This enables diagnostics, simulation comparison,
and AI-assisted planning support.

Interaction Layer

Provides developer and business interfaces.

Current direction:

lightweight developer visualization

Excel-centered business interaction

AI / Research Lab Layer

Defines how WOM itself is developed and improved.

This includes:

AI team roles

AI meeting governance

AI self-evolution loop

4 Simplified Figure

A shorter conceptual view is:

Demand Anchor
      ↓
   LOT_ID
      ↓
Backward LT Shift
      ↓
Planning Engine
      ↓
Hybrid Push–Pull Network
      ↓
Result / Diagnostics
      ↓
Excel / AI Interaction
5 Why This Diagram Matters

This diagram shows that WOM is not merely:

a spreadsheet tool

a simulation script

a visualization GUI

WOM is a lot-based planning operating model.

Its defining features are:

demand-anchored lot identity

hybrid push–pull network simulation

deterministic explainable planning

AI-assisted development structure

6 Relationship to Core Documents

This diagram should be read together with:

WOM_DESIGN_PRINCIPLES.md

WOM_PLANNING_THEORY.md

WOM_SYSTEM_OVERVIEW.md

ARCHITECTURE.md

WOM_PIPELINE_SPEC.md

LOT_ID_SPEC.md

The diagram provides the visual overview,
while the other documents provide deeper detail.