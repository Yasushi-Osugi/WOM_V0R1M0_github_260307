# WOM FlowEvent Schema v1.1

Project: Weekly Operation Model (WOM)  
Specification Version: 1.1  
Status: Draft  
Date: March 2026

---

# 1. Purpose

The WOM FlowEvent Schema defines the canonical runtime event structure used by the WOM Planning Kernel.

A FlowEvent represents a concrete economic action that affects the simulated supply chain.

FlowEvents are the primary execution records of WOM.

They serve as:

- the source of truth for simulation
- the basis for deterministic replay
- the bridge between lots and derived state
- the audit trail of economic activity

If the Lot Header is the protocol identity of an economic token, the FlowEvent is the protocol record of what happened to that token.

---

# 2. Role in WOM Architecture

The WOM architecture can be understood as:

```text
Lot Header
    ↓
FlowEvent
    ↓
State Derivation
    ↓
Trust Detection
    ↓
Operator Intervention

A lot does not directly change state.

State changes only through FlowEvents.

Therefore:

FlowEvents = source of truth
StateView = derived view

3. Design Principles

The FlowEvent Schema follows these principles.

3.1 Event Sourcing

All state transitions must be explainable from FlowEvents.

3.2 Determinism

FlowEvents must contain enough ordering information to guarantee deterministic execution.

3.3 Minimal Runtime Semantics

The schema captures the minimal information required for economic flow simulation.

3.4 Extensibility

Optional metadata fields allow future expansion without breaking the canonical schema.

4. Canonical FlowEvent Schema
{
  "flow_id": "string",
  "lot_id": "string",
  "event_type": "string",
  "product_id": "string",
  "from_node": "string | null",
  "to_node": "string | null",
  "time_bucket": "YYYYWW",
  "quantity_cpu": "float",
  "creation_sequence": "integer",
  "event_priority": "optional integer",
  "causal_event_id": "optional string",
  "operator_id": "optional string",
  "source_type": "optional string",
  "status": "optional string",
  "metadata": "optional dictionary"
}
5. Core Fields
5.1 flow_id

Globally unique identifier for the FlowEvent.

Purpose:

event uniqueness

deterministic tie-breaking

audit traceability

event referencing

Example:

f-lot-20260313-P1-0001-arr
5.2 lot_id

Identifier of the parent lot.

Purpose:

lot genealogy

event grouping

traceability across production, shipment, arrival, and sale

A FlowEvent must always belong to exactly one lot.

5.3 event_type

Type of economic event.

Canonical event types in v1.1:

production

shipment

arrival

sale

inventory_adjustment

Optional future event types:

reservation

release

inspection

quarantine

disposal

return

Kernel v1.1 must remain compatible with the canonical core types.

5.4 product_id

Identifier of the product associated with the event.

Purpose:

inventory matching

demand fulfillment consistency

event validation

5.5 from_node

Source node of the event.

Examples:

factory_A

dc_EU

market_TYO

Interpretation depends on event_type.

Examples:

production: source context or production node

shipment: shipping origin

arrival: upstream source

sale: inventory source node

5.6 to_node

Destination node of the event.

Interpretation depends on event_type.

Examples:

production: usually same as producing node

shipment: shipment destination

arrival: receiving node

sale: optional consuming market node or same as market node

5.7 time_bucket

Execution time of the event.

Format:

YYYYWW

Purpose:

simulation ordering

temporal replay

planning cycle consistency

5.8 quantity_cpu

Quantity processed by the event in Common Planning Units.

Purpose:

unified quantity semantics

inventory movement

PSI consistency

5.9 creation_sequence

Deterministic sequence number assigned at event creation.

Purpose:

deterministic replay

tie-breaking among events with same time_bucket and priority

reproducible simulation results

This is a required runtime control field.

6. Extended Runtime Fields
6.1 event_priority

Optional explicit event priority.

Typical canonical priority mapping:

production = 10

shipment = 20

arrival = 30

sale = 40

inventory_adjustment = 50

If omitted, priority may be inferred from event_type by kernel logic.

Purpose:

explicit ordering control

cross-system interoperability

event-log portability

6.2 causal_event_id

Optional reference to the event that directly caused this FlowEvent.

Examples:

arrival caused by shipment

sale caused by demand-linked release

inventory adjustment caused by reconciliation event

Purpose:

causal traceability

event chain reconstruction

debugging support

Example:

shipment_event → arrival_event

arrival_event.causal_event_id = shipment_event.flow_id

6.3 operator_id

Optional identifier of the operator that created or modified this event.

Examples:

op-prod-te-stockout-market_TYO-202611

op-reroute-001

Purpose:

explain which intervention created the event

support planning traceability

support learning and policy evaluation

This field is especially important for self-correcting planning loops.

6.4 source_type

Optional origin category of the event.

Examples:

initial_lot

resolver_generated

manual_override

imported_plan

plugin_generated

Purpose:

provenance tracking

debugging

governance and audit control

6.5 status

Optional operational or lifecycle state of the event.

Examples:

planned

committed

executed

cancelled

invalidated

Important:

In a pure simulation kernel, status should usually remain informational unless governed by explicit event logic.

Purpose:

operational interoperability

external system integration

human-readable monitoring

6.6 metadata

Optional extensible dictionary.

Examples:

lane_id

transport_mode

tariff_zone

carbon_factor

urgency_reason

customer allocation context

Purpose:

domain-specific extension

future compatibility

plugin support

7. Canonical Event Semantics
7.1 Production Event

Meaning:

Inventory is created at a node.

Typical semantics:

inventory[node, product] += quantity
capacity_usage[node, time_bucket] += quantity

Typical field pattern:

{
  "event_type": "production",
  "from_node": "factory_A",
  "to_node": "factory_A"
}
7.2 Shipment Event

Meaning:

Inventory leaves the source node.

Typical semantics:

inventory[from_node, product] -= quantity

Destination inventory is not increased until arrival.

Typical field pattern:

{
  "event_type": "shipment",
  "from_node": "factory_A",
  "to_node": "dc_JP"
}
7.3 Arrival Event

Meaning:

Inventory becomes available at the receiving node.

Typical semantics:

inventory[to_node, product] += quantity
supply[to_node, product, time_bucket] += quantity

Typical field pattern:

{
  "event_type": "arrival",
  "from_node": "factory_A",
  "to_node": "dc_JP",
  "causal_event_id": "shipment_flow_id"
}
7.4 Sale Event

Meaning:

Inventory is consumed to fulfill demand.

Typical semantics:

inventory[source_node, product] -= quantity
fulfilled_demand += quantity

SaleEvent is the explicit demand-fulfillment event introduced in the v1.1 semantic model.

Typical field pattern:

{
  "event_type": "sale",
  "from_node": "market_TYO",
  "to_node": "market_TYO"
}

or alternatively:

{
  "event_type": "sale",
  "from_node": "dc_JP",
  "to_node": "market_TYO"
}

The choice depends on whether the market node itself holds inventory in the model.

7.5 Inventory Adjustment Event

Meaning:

Manual or system-driven inventory correction.

Typical semantics:

inventory[node, product] += or -= quantity

This event should be used carefully, because it bypasses the standard physical flow chain.

Typical use cases:

reconciliation

opening balance correction

shrinkage adjustment

write-off

emergency override

8. Deterministic Ordering Rules

FlowEvents must be processed in deterministic order.

Canonical sorting key:

(time_bucket,
 event_priority,
 creation_sequence,
 flow_id)

If event_priority is not explicitly stored in the event record, the kernel may derive it from event_type.

This ordering guarantees:

reproducible simulation

explainable execution

stable replay across systems

9. Minimal Required Schema

The minimal required schema compatible with Kernel v1 is:

{
  "flow_id": "string",
  "lot_id": "string",
  "event_type": "string",
  "product_id": "string",
  "from_node": "string | null",
  "to_node": "string | null",
  "time_bucket": "YYYYWW",
  "quantity_cpu": "float",
  "creation_sequence": "integer"
}

This should remain the compatibility baseline.

10. Recommended Standard Schema for v1.1

The recommended schema for interoperable WOM systems is:

{
  "flow_id": "string",
  "lot_id": "string",
  "event_type": "string",
  "product_id": "string",
  "from_node": "string | null",
  "to_node": "string | null",
  "time_bucket": "YYYYWW",
  "quantity_cpu": "float",
  "creation_sequence": "integer",
  "event_priority": "optional integer",
  "causal_event_id": "optional string",
  "operator_id": "optional string",
  "source_type": "optional string",
  "metadata": "optional dictionary"
}
11. Relationship to Lot Header

The Lot Header defines the identity and execution context of the lot.

The FlowEvent records what actually happens to that lot.

Relationship:

Lot Header
    ↓
FlowEvent sequence
    ↓
State derivation

One lot typically generates multiple FlowEvents.

Example:

Lot
↓
Production
↓
Shipment
↓
Arrival
↓
Sale
12. Relationship to Demand and Trust Events

FlowEvents are execution events.

DemandEvents are demand-side signals.

TrustEvents are anomaly signals.

The three layers are distinct:

DemandEvent = what is requested
FlowEvent   = what happens
TrustEvent  = what is wrong

This separation is essential for explainability and modularity.

13. Role in DB Persistence

FlowEvents are suitable for storage in:

SQL event tables

event stores

append-only logs

distributed message streams

Suggested SQL-style primary key:

flow_id

Suggested useful indexes:

lot_id

product_id

time_bucket

event_type

operator_id

Because state can be replayed from FlowEvents, they form the core persistent runtime record.

14. Role in Distributed WOM

In distributed WOM systems, FlowEvents are the common exchange format between planning nodes.

Examples:

regional planner publishes shipment and arrival events

factory planner publishes production events

market planner publishes sale events

Because all nodes interpret the same canonical schema, state can be reconstructed consistently.

FlowEvents therefore function as the shared runtime protocol of distributed WOM.

15. Role in Multi-Agent WOM

In multi-agent WOM systems:

agents generate candidate operators

operators create or modify FlowEvents

FlowEvents synchronize shared economic reality

This makes FlowEvent Schema the practical coordination contract between agents.

Without a stable FlowEvent protocol, agent interoperability becomes fragile.

16. Example Event Sequence
16.1 Production
{
  "flow_id": "f-lot-20260313-P1-0001-prod",
  "lot_id": "lot-20260313-P1-0001",
  "event_type": "production",
  "product_id": "P1",
  "from_node": "factory_A",
  "to_node": "factory_A",
  "time_bucket": "202611",
  "quantity_cpu": 100.0,
  "creation_sequence": 1,
  "source_type": "initial_lot"
}
16.2 Shipment
{
  "flow_id": "f-lot-20260313-P1-0001-ship",
  "lot_id": "lot-20260313-P1-0001",
  "event_type": "shipment",
  "product_id": "P1",
  "from_node": "factory_A",
  "to_node": "dc_JP",
  "time_bucket": "202611",
  "quantity_cpu": 100.0,
  "creation_sequence": 2,
  "source_type": "initial_lot"
}
16.3 Arrival
{
  "flow_id": "f-lot-20260313-P1-0001-arr",
  "lot_id": "lot-20260313-P1-0001",
  "event_type": "arrival",
  "product_id": "P1",
  "from_node": "factory_A",
  "to_node": "dc_JP",
  "time_bucket": "202612",
  "quantity_cpu": 100.0,
  "creation_sequence": 3,
  "causal_event_id": "f-lot-20260313-P1-0001-ship",
  "source_type": "initial_lot"
}
16.4 Sale
{
  "flow_id": "f-lot-20260313-P1-0001-sale",
  "lot_id": "lot-20260313-P1-0001",
  "event_type": "sale",
  "product_id": "P1",
  "from_node": "dc_JP",
  "to_node": "market_TYO",
  "time_bucket": "202613",
  "quantity_cpu": 80.0,
  "creation_sequence": 4,
  "source_type": "demand_fulfillment",
  "metadata": {
    "demand_id": "d-202613-market_TYO-P1-001"
  }
}
17. Summary

The WOM FlowEvent Schema v1.1 defines the canonical runtime event structure of the WOM system.

It standardizes how economic actions are represented across:

kernel execution

event replay

planning engine logic

persistence layers

distributed WOM nodes

multi-agent systems

Together with the Lot Header, the FlowEvent Schema forms the core protocol layer of the WOM Economic OS.

It should therefore be treated as a stable and carefully governed specification.