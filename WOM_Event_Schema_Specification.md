# WOM Event Schema Specification

Project: Weekly Operation Model (WOM)

Specification Version: 1.0  
Status: Draft  
Date: March 2026

---

# 1. Purpose

The WOM Event Schema defines the canonical structure for all economic events processed by the WOM Planning Kernel.

This schema serves as the **protocol layer of WOM**.

It enables:

- deterministic economic simulation
- distributed planning systems
- multi-agent planning
- database persistence
- event replay and auditing

The WOM Event Schema is conceptually similar to the role of **Internet Protocol (IP)** in computer networks.

Just as IP standardizes packet communication between machines, WOM Event Schema standardizes economic events between planning nodes.

---

# 2. Design Principles

The schema follows several design principles.

### Event Sourcing

Events are the **source of truth**.

State is derived from events.

---

### Determinism

All events must contain enough information to guarantee deterministic replay.

---

### Minimality

The schema contains only the fields required for economic flow simulation.

---

### Extensibility

Optional metadata fields allow domain-specific extensions.

---

# 3. Core Event Types

The WOM runtime operates on the following event classes.

Core Entities:

Lot  
FlowEvent  
DemandEvent  
SaleEvent  
TrustEvent  

These entities represent the minimal economic model.

---

# 4. Lot Header

A Lot represents a production or procurement batch.

Lots act as the **economic container** that generates FlowEvents.

### Lot Schema

```json
{
  "lot_id": "string",
  "product_id": "string",
  "origin_node": "string",
  "destination_node": "string | null",
  "quantity_cpu": "float",
  "created_time_bucket": "YYYYWW",
  "attributes": "optional dictionary"
}

Field Description

| Field               | Description                       |
| ------------------- | --------------------------------- |
| lot_id              | globally unique lot identifier    |
| product_id          | product identifier                |
| origin_node         | production or source node         |
| destination_node    | destination node                  |
| quantity_cpu        | quantity in common planning units |
| created_time_bucket | week identifier                   |
| attributes          | optional extension metadata       |
---


5. FlowEvent Schema

FlowEvent represents an economic movement in the supply chain.

Event Types

production
shipment
arrival
sale
inventory_adjustment

FlowEvent Schema
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
  "metadata": "optional dictionary"
}

Field Description

| Field             | Description                  |
| ----------------- | ---------------------------- |
| flow_id           | globally unique event id     |
| lot_id            | parent lot identifier        |
| event_type        | type of flow event           |
| product_id        | product identifier           |
| from_node         | source node                  |
| to_node           | destination node             |
| time_bucket       | execution week               |
| quantity_cpu      | event quantity               |
| creation_sequence | deterministic ordering index |
| metadata          | optional extension data      |
---

6. DemandEvent Schema

DemandEvent represents market demand signals.

Demand events trigger sale processing.

DemandEvent Schema
{
  "demand_id": "string",
  "market_id": "string",
  "product_id": "string",
  "time_bucket": "YYYYWW",
  "quantity_cpu": "float",
  "price": "optional float",
  "channel_id": "optional string",
  "metadata": "optional dictionary"
}

Field Description

| Field        | Description              |
| ------------ | ------------------------ |
| demand_id    | unique demand identifier |
| market_id    | market node              |
| product_id   | product                  |
| time_bucket  | demand week              |
| quantity_cpu | demanded quantity        |
| price        | optional market price    |
| channel_id   | sales channel            |
| metadata     | optional additional data |
---

7. SaleEvent Schema

SaleEvent represents the fulfillment of demand.

This event links supply flows with demand consumption.

SaleEvent Schema
{
  "sale_id": "string",
  "market_id": "string",
  "product_id": "string",
  "time_bucket": "YYYYWW",
  "quantity_cpu": "float",
  "source_node": "string",
  "demand_id": "string",
  "metadata": "optional dictionary"
}

Field Description

| Field        | Description              |
| ------------ | ------------------------ |
| sale_id      | unique sale event id     |
| market_id    | market                   |
| product_id   | product                  |
| time_bucket  | sale week                |
| quantity_cpu | sold quantity            |
| source_node  | node fulfilling the sale |
| demand_id    | associated demand        |
| metadata     | optional metadata        |
---

8. TrustEvent Schema

TrustEvents represent anomalies detected during planning simulation.

These events signal that corrective operators may be required.

TrustEvent Schema
{
  "trust_event_id": "string",
  "event_type": "string",
  "severity": "float",
  "node_id": "string | null",
  "product_id": "string | null",
  "time_bucket": "YYYYWW",
  "message": "string",
  "evidence": "optional dictionary"
}

Example Event Types

E_STOCKOUT_RISK
E_CAPACITY_OVERLOAD
E_NEGATIVE_INVENTORY
E_INVALID_SHIPMENT
E_INVALID_SALE

9. Event Ordering Rules

WOM execution must follow deterministic ordering.

Sorting key:

(time_bucket,
 event_priority,
 creation_sequence,
 flow_id)

This guarantees:

reproducible planning

explainable results

deterministic simulation

10. Event Persistence

All events may be stored in an event store.

Possible storage implementations:

SQL database
event log
distributed event stream

The kernel reconstructs state by replaying events.

11. Distributed WOM Systems

The event schema enables distributed planning architectures.

Example:

Regional Planner Node
    ↓
Global Coordination Node
    ↓
Market Nodes

Events become the shared communication format.

12. Multi-Agent Planning

In multi-agent WOM systems:

each agent generates operators

operators generate events

events synchronize the global state

The Event Schema acts as the coordination protocol.

13. Summary

The WOM Event Schema defines the minimal economic protocol used by the WOM system.

It standardizes the representation of:

lots
flows
demand
sales
trust events

This schema enables:

deterministic planning
distributed economic simulation
multi-agent planning systems
economic operating systems

The WOM Event Schema therefore acts as the protocol layer of the WOM Economic OS.