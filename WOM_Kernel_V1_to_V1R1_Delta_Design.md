# WOM Kernel v1 → v1.1 Delta Design

---

# 1. Event Model

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

Optional

UnmetDemand

---

# 2. Demand Handling

Kernel v1

DemandEvent
↓
inventory reduction

Kernel v1.1

DemandEvent
↓
SaleEvent
↓
inventory reduction

Optional

UnmetDemandEvent

---

# 3. Trust Events

Kernel v1

E_STOCKOUT_RISK
E_CAPACITY_OVERLOAD

Kernel v1.1

E_STOCKOUT_RISK
E_CAPACITY_OVERLOAD
E_NEGATIVE_INVENTORY
E_INVALID_SHIPMENT
E_INVALID_SALE

---

# 4. Event Traceability

Kernel v1

flow_events
state history

Kernel v1.1

flow_events
sale_events
trust_events
operator_history

---

# 5. Execution Semantics

Kernel v1

event sourced simulation
deterministic execution

Kernel v1.1

same semantics

+ complete economic event chain

---

# 6. Architectural Impact

Kernel v1

minimal runtime engine

Kernel v1.1

complete minimal economic runtime

Planning Engine can now safely extend planning behavior.

---

# 7. Version Summary

Kernel v1

minimal deterministic planning runtime

Kernel v1.1

complete minimal economic event model
runtime integrity validation
foundation for planning engine