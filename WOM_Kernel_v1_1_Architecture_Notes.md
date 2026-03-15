# WOM Kernel v1.1 Architecture Notes

Project: Weekly Operation Model (WOM)  
Component: WOM Planning Kernel  
Version: v1.1 Architecture Draft  
Date: March 2026

---

# 1. Purpose

WOM Kernel v1 introduced a minimal deterministic planning runtime based on event-sourced simulation.

Kernel v1.1 strengthens the kernel by completing the minimal **economic event model**.

The primary architectural change is the introduction of an **explicit Sale Event**, which completes the minimal economic flow chain.

---

# 2. Minimal Economic Event Chain

Kernel v1

Production
Shipment
Arrival
(implicit sale)

Kernel v1.1

Production
Shipment
Arrival
Sale

Optional:

UnmetDemand / Backlog

---

# 3. Event Model

## 3.1 Core Event Types

The WOM kernel operates on **FlowEvent** records.

Each event represents a deterministic economic action.

Event types:

production
shipment
arrival
sale
inventory_adjustment

---

## 3.2 Event Semantics

### Production Event

Creates inventory at a node.

effect:
inventory[node] += quantity

capacity usage is recorded.

---

### Shipment Event

Moves inventory from one node to another.

effect:

inventory[from_node] -= quantity

inventory[to_node] unchanged until arrival event.

---

### Arrival Event

Completes the shipment.

effect:

inventory[to_node] += quantity

---

### Sale Event (new in v1.1)

Represents a market transaction.

effect:

inventory[node] -= quantity

This event links supply flow with demand fulfillment.

---

# 4. Demand Processing Model

Kernel v1 demand handling:

DemandEvent
→ direct inventory reduction

Kernel v1.1 demand handling:

DemandEvent
↓
SaleEvent
↓
inventory update

Optional:

DemandEvent
↓
SaleEvent
↓
UnmetDemandEvent

---

# 5. State Derivation

StateView remains a **derived structure**.

StateView is never mutated directly.

State fields:

inventory_by_node_product_time
demand_by_market_product_time
supply_by_node_product_time
backlog_by_market_product_time
capacity_usage_by_resource_time

StateView is reconstructed by replaying FlowEvents.

---

# 6. Deterministic Event Ordering

Event execution order:

(time_bucket,
 event_priority,
 creation_sequence,
 flow_id)

This guarantees:

reproducibility
explainability
deterministic planning behavior

---

# 7. Runtime Integrity Checks

Kernel v1.1 introduces new trust event types.

New trust events:

E_NEGATIVE_INVENTORY

inventory < 0

E_INVALID_SHIPMENT

shipment exceeds available inventory

E_INVALID_SALE

sale exceeds available inventory

These events represent **execution integrity violations**.

---

# 8. Trust Event Layer

Trust events are produced by monitoring derived state.

Trust events do not mutate state.

They only trigger operator generation.

Examples:

E_STOCKOUT_RISK
E_CAPACITY_OVERLOAD
E_NEGATIVE_INVENTORY

---

# 9. Planning Control Loop

Kernel execution loop:

simulate
↓
derive state
↓
detect trust events
↓
generate operators
↓
apply operator
↓
re-simulate

This forms a **self-correcting planning system**.

---

# 10. Architectural Role of Kernel

The kernel defines the **economic execution semantics**.

The kernel does NOT define planning intelligence.

Planning intelligence is implemented in the Planning Engine layer.

Architecture:

Planning Engine
↑
WOM Kernel

---

# 11. Summary

Kernel v1.1 completes the minimal economic event model by introducing:

explicit sale events
runtime integrity validation
improved event traceability

The kernel remains:

minimal
deterministic
event-sourced
explainable

This provides a stable foundation for the Planning Engine layer.