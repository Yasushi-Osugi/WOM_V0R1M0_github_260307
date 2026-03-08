# WOM — Weekly Operation Model

A one-page explanation of the WOM planning system.

---

# The Core Idea

Traditional planning systems operate on quantities.


Demand → Numbers


WOM operates on **traceable planning objects**.


Demand → LOT_ID objects


A LOT_ID represents a real physical lot that will be produced,
transported, stored, and delivered.

---

# WOM Planning Flow

       Final Market Demand
                │
                │ Demand creates
                ▼
          LOT_ID Lists
 (NODE + PRODUCT + YYYYWW + SEQ)
                │
                │ Backward planning
                ▼
     Lead-Time Positioned Lots
                │
                │ Forward planning
                ▼
        WOM Planning Engine
                │
    ┌───────────┴───────────┐
    │                       │
    ▼                       ▼

Inbound Supply Chain Outbound Supply Chain
(PUSH) (PUSH + PULL)

supplier → factory factory → distribution
│
▼
Decoupling Stock Point
│
▼
Market


---

# Planning Objects

The fundamental planning object in WOM is:


LOT_ID


Structure:


NODE-PRODUCT-YYYYWWNNNN


Example:


TOKYO_STORE-PRODUCT_A-2025460003


Meaning:

| element | description |
|-------|-------------|
| NODE | location where demand occurs |
| PRODUCT | product identifier |
| YYYYWW | demand week |
| NNNN | lot sequence |

Each LOT_ID represents one physical shipment / production lot.

---

# PSI Representation

Planning uses **PSI lists**.


P[t] = Production LOT_ID list
S[t] = Shipment LOT_ID list
I[t] = Inventory LOT_ID list


Instead of:


inventory = 500 units


WOM stores:


inventory = {LOT_1, LOT_2, LOT_3}


Planning therefore moves **objects**, not numbers.

---

# Hybrid Push–Pull Control

Supply chains behave differently on the inbound and outbound sides.

Inbound supply chain:


supplier → factory


Controlled by:


PUSH planning


Outbound supply chain:


factory → distribution → market


Controlled by:


PUSH + PULL


Inventory buffers (decoupling stock points)
absorb demand fluctuations.

---

# Why Weekly Planning?

WOM uses **weekly planning cycles**.

Because real supply chains naturally synchronize around weekly rhythms:

- factory production planning
- logistics schedules
- retail demand cycles

Weekly time buckets provide a balance between:


operational realism
computational efficiency
planning stability


---

# WOM System Structure


Scenario
│
▼
Network Model
│
▼
LOT_ID Generation
│
▼
Planning Pipeline
│
▼
PSI Simulation
│
▼
Economic Evaluation


---

# Key Advantages

WOM enables:

✔ Traceable supply chain planning  
✔ Explainable planning decisions  
✔ Deterministic scenario simulation  
✔ Integration of logistics and economics  

Traditional planning systems often hide decisions behind aggregated numbers.

WOM exposes the actual movement of goods.

---

# Mental Model

The entire WOM philosophy can be summarized in five sentences.


Demand creates LOT_IDs
LOT_IDs move through the supply chain
PSI tracks their movement
Planning decides their timing
Evaluation measures their value


---

# Relationship to Other Documents


README.md
│
▼
WOM_ONE_PAGE.md
│
▼
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


Start here for a quick understanding,
then move deeper into the system documentation.

---

# Final Insight

The core concept of WOM is simple.

Supply chains should be planned using
**explicit lot objects rather than anonymous quantities**.

This simple shift makes global supply chains:


traceable
explainable
simulatable
economically evaluable


within a single planning engine.