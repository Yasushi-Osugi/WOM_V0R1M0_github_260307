# WOM Planning Theory

This document explains the core planning theory of WOM
(Weekly Operation Model).

While traditional supply chain planning systems operate
on quantity-based planning models, WOM is designed as a
**lot-based planning system anchored in final demand.**

The WOM planning theory integrates:

- demand-driven planning
- lot-level traceability
- hybrid push–pull supply chain control

---

# 1 Fundamental Idea

The central idea of WOM is:

Demand creates lots.  
Supply fulfills lots.

In WOM, planning does not start from factories.

Planning starts from **final consumption demand**.

Each demand unit is represented as a **LOT_ID**.

---

# 2 Demand Anchor Model

All planning begins from the **demand anchor**.

The demand anchor is the leaf node of the outbound
supply chain network.

Example:


Market Node (Leaf)
↓
Retail / Distribution
↓
Decoupling Stock Point
↓
Distribution Yard (DAD)
↓
Manufacturing (MOM)
↓
Material Supply Network


At the leaf node, demand is converted into **lot_ID lists**.

Each lot represents:

- product
- market location
- consumption week
- lot sequence

---

# 3 Planning Timeline

The WOM planning process operates in the following stages.


Demand Generation
↓
LOT_ID Creation
↓
Backward Lead-Time Shift
↓
Forward Supply Simulation
↓
Shipment Allocation


---

# 4 Backward Planning

After demand lots are generated,
they are shifted backward in time
according to supply chain lead times.

Example:


Market Consumption Week = 2026-W05
Total Lead Time = 2 weeks


Backward shift:


Demand week → production shipment position

2026-W05 → 2026-W03


Important rule:

**LOT_ID identity never changes.**

Only its position in the planning timeline moves.

---

# 5 Forward Planning

After backward positioning,
WOM executes a forward simulation of the supply chain.

This simulation uses a **hybrid push–pull control model**.

---

# 6 Inbound Supply Chain (PUSH)

Inbound supply chain connects

material suppliers → manufacturing.

Structure:


Material Nodes
↓
Component Suppliers
↓
Manufacturing Plant (MOM)


Characteristics:

- supply-side synchronization
- production flow optimization

Supply is pushed forward toward the manufacturing plant.

---

# 7 Outbound Supply Chain PUSH

Outbound supply chain begins at the
distribution yard.


Manufacturing (MOM)
↓
Distribution Yard (DAD)
↓
Decoupling Stock Point


Products are pushed from production
to the decoupling stock point.

Purpose:

- stabilize production
- absorb demand volatility

Inventory accumulates at the decoupling point.

---

# 8 Decoupling Stock Point

The decoupling stock point is the
boundary between:


production-driven supply
and
demand-driven shipment


This location stores finished goods
to buffer demand fluctuations.

---

# 9 Outbound Supply Chain PULL

From the decoupling point to the market,
shipments are demand-driven.


Decoupling Stock
↓
Regional Distribution
↓
Market Node (Leaf)


Shipment decisions prioritize:

- urgency
- customer priority
- profit contribution

---

# 10 Hybrid Push–Pull Control

The full WOM planning model is therefore:


Inbound Supply Chain
PUSH
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


This hybrid structure allows:

- stable production
- flexible demand fulfillment

---

# 11 Lot-Based Planning

Unlike traditional planning systems
that operate on scalar quantities,
WOM operates on **lot objects**.

Planning state is represented as:


P_ids = production lot list
I_ids = inventory lot list
S_ids = shipment lot list


Quantities are derived from list length.


quantity = len(lot_id_list)


This enables:

- full lot traceability
- explainable planning behavior
- deterministic simulations

---

# 12 Explainable Supply Chain Simulation

Because every lot is tracked individually,
WOM can reconstruct the entire
supply chain flow.

Example:


LOT_ID

TOKYO_DC-DRUG_A-2026050002


Traceable history:


production node
shipment node
inventory node
market node


This enables transparent planning diagnostics.

---

# 13 Why This Model Matters

Traditional APS systems suffer from:

- opaque optimization logic
- weak traceability
- unstable plan adjustments

WOM addresses these issues by:

- representing planning units as lot objects
- anchoring supply planning to final demand
- combining push production with pull distribution

---

# 14 WOM Planning Philosophy

The philosophy of WOM can be summarized as:


Demand defines the lot.

Lots define the plan.

Supply fulfills the lots.


This principle allows WOM to serve as the
planning core of a future **economic operating system**.