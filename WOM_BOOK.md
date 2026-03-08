# WOM — The Story Behind the Weekly Operation Model

Author: Yasushi Osugi

This document explains the philosophy and motivation behind WOM
(Weekly Operation Model).

Unlike other documents in this repository, this is not a specification
or a technical description.

This is the story of **why WOM exists**.

---

# 1 The Fundamental Question

Modern global supply chains are extremely complex.

A single product may involve:

- raw material suppliers
- component factories
- assembly plants
- logistics networks
- distribution centers
- retail channels
- final consumers

Traditional planning systems try to manage this complexity
using aggregated quantities.

Typical planning objects are:

- monthly demand quantities
- forecast numbers
- aggregated inventory levels

But this raises a fundamental problem.

The system plans using **numbers**,  
while the real world moves **physical objects**.

This mismatch creates planning errors.

---

# 2 The Invisible Unit of Supply Chains

In reality, supply chains do not move abstract quantities.

They move **batches**, **lots**, and **shipments**.

A factory does not produce "100 units".

It produces:


production lots


A logistics system does not transport "200 units".

It transports:


shipments


A warehouse does not store "500 units".

It stores:


inventory lots


But most planning systems ignore this reality.

They treat supply chains as continuous flows of numbers.

This is the conceptual mistake WOM attempts to correct.

---

# 3 The Core Insight

The central idea of WOM is simple:

Supply chain planning should operate on **lots**,  
not abstract quantities.

In WOM, the atomic planning unit is called:


LOT_ID


Each LOT_ID represents a concrete unit of supply chain activity.

Example:


TOKYO_STORE-PRODUCT_A-2025460001


Meaning:

- node: TOKYO_STORE
- product: PRODUCT_A
- time: 2025 week 46
- sequence: lot 0001

A LOT_ID is therefore a **traceable unit of demand fulfillment**.

---

# 4 Demand Creates the World

In WOM, the planning process begins with demand.

Demand does not create numbers.

Demand creates LOT_IDs.


Demand
│
▼
LOT_ID generation


For example:

Weekly demand: 250 units  
Lot size: 100

The system generates:


LOT_0001
LOT_0002
LOT_0003


These lots represent the physical shipments that must eventually reach the market.

From this point forward, the planning system does not manipulate quantities.

It moves LOT_IDs.

---

# 5 Backward Planning

Once demand LOT_IDs are created,
the system determines when production must occur.

This is done using lead times.

Example:


Market demand: 2025 week 46
Lead time: 4 weeks


Production must occur at:


2025 week 42


This process is called:


backward planning


Every LOT_ID is shifted upstream through the supply chain
according to lead times.

---

# 6 The Supply Chain Tree

A supply chain can be represented as a tree.

Inbound side:


material suppliers
│
▼
component factories
│
▼
final assembly plant


Outbound side:


factory
│
distribution center
│
decoupling stock point
│
market nodes


WOM models this structure explicitly.

Each node participates in the planning process.

---

# 7 The Weekly Rhythm

Why does WOM use weekly planning?

Because real operations tend to synchronize around weekly cycles.

Factories plan weekly production.

Logistics networks operate weekly shipment schedules.

Retail demand patterns often stabilize at weekly granularity.

Therefore WOM adopts a natural planning rhythm:


Weekly planning cycles


This balances:

- responsiveness
- computational tractability
- operational realism

---

# 8 Push and Pull

Supply chains exhibit two different behaviors.

Inbound supply chains are usually **push-oriented**.

Materials flow toward factories according to production plans.


supplier → factory


Outbound supply chains must respond to demand variability.

They therefore rely on **decoupling stock points**.


factory → distribution → decoupling stock


From there, shipments are triggered by demand.


decoupling stock → market


WOM integrates these two behaviors.


push + pull


---

# 9 Decoupling Stock Points

Demand fluctuates.

Production prefers stability.

To reconcile these two forces,
supply chains introduce inventory buffers.

These buffers are called:


decoupling stock points


Their purpose is to absorb demand variability.

In WOM, these points play a critical role.

When shipments must be prioritized,
the system allocates inventory according to:

- urgency
- customer priority
- profitability

---

# 10 Planning as Simulation

Traditional planning systems often try to compute optimal solutions.

WOM takes a different approach.

It treats planning as a **deterministic simulation**.

The engine simulates how LOT_IDs move through the supply chain.

The result is a fully traceable planning outcome.

This has important advantages:

- explainable decisions
- reproducible scenarios
- clear operational interpretation

---

# 11 From Quantities to Objects

The conceptual shift from quantities to LOT_IDs changes everything.

Instead of:


inventory = 500 units


WOM stores:


inventory = {LOT_001, LOT_002, LOT_003, ...}


Planning therefore becomes the management of **object sets**.

This makes the system naturally compatible with:

- traceability
- scenario simulation
- financial evaluation

---

# 12 The Economic Layer

Once LOT flows are determined,
WOM attaches economic attributes.

Each LOT may carry:

- production cost
- logistics cost
- selling price
- margin contribution

This allows the system to evaluate:


profit
inventory value
service level
capacity utilization


within the same planning model.

---

# 13 WOM as a Planning Engine

WOM is not a user interface.

WOM is not a database.

WOM is primarily:


a planning engine


Its purpose is to simulate global supply chains
using deterministic lot-based planning.

Other systems may provide:

- visualization
- dashboards
- scenario editors

But the core intelligence resides in the planning engine.

---

# 14 Toward an Economic Operating System

The vision behind WOM extends beyond supply chain planning.

If supply chains across industries synchronize around
transparent planning cycles,
economic activity itself can become more coordinated.

This suggests a broader idea:


an economic operating system


In such a system:

- supply
- demand
- production
- logistics
- consumption

could be synchronized through shared planning frameworks.

WOM is a small step toward exploring this possibility.

---

# 15 Final Thought

Supply chains are the circulatory system of the global economy.

If we understand how goods move,
we better understand how economies function.

WOM proposes a simple but powerful idea:

Plan supply chains using **traceable lot objects**,
and simulate how they move through time.

From this foundation,
more transparent and adaptive economic systems may emerge.