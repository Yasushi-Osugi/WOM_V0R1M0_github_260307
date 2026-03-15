# WOM Lot Header Specification

Project: Weekly Operation Model (WOM)  
Specification Version: 1.0  
Status: Draft  
Date: March 2026

---

# 1. Purpose

The WOM Lot Header defines the canonical header structure attached to a lot object in the WOM system.

A lot is not merely a quantity container.

A lot is the minimal economic object that moves through the WOM network.

The Lot Header therefore acts as the routing, identity, and execution context descriptor for economic flow.

Conceptually, the WOM Lot Header is closer to an **MPLS label header** than to an IP address.

It describes how a lot should be handled inside the planning network.

---

# 2. Design Concept

In conventional planning systems:

quantity is the planning primitive

In WOM:

lot is the planning primitive

A lot carries:

- identity
- product meaning
- routing context
- time context
- execution attributes
- optional policy information

The Lot Header is the minimal protocol structure that allows the kernel and planning engine to interpret a lot consistently.

---

# 3. Design Principles

The Lot Header follows these principles.

## 3.1 Minimality

Only fields required for lot identity and execution semantics belong in the header.

---

## 3.2 Determinism

A lot must contain enough information to be replayed deterministically through the WOM runtime.

---

## 3.3 Extensibility

The header must support optional attributes for industry-specific or scenario-specific use.

---

## 3.4 Network Interpretability

The header must be interpretable by all planning nodes in a distributed WOM network.

---

# 4. Conceptual Role of a Lot

A lot is the smallest meaningful execution object in WOM.

A lot is not just inventory.

A lot is:

- a production batch
- a shipment unit
- a fulfillment unit
- a planning token
- an economic carrier

The Lot Header provides the metadata needed to process that token.

---

# 5. Canonical Lot Header Schema

```json
{
  "lot_id": "string",
  "lot_type": "string",
  "product_id": "string",
  "origin_node": "string",
  "destination_node": "string | null",
  "final_market_node": "string | null",
  "quantity_cpu": "float",
  "uom": "optional string",
  "created_time_bucket": "YYYYWW",
  "requested_arrival_time_bucket": "optional YYYYWW",
  "priority_class": "optional string",
  "service_class": "optional string",
  "routing_group": "optional string",
  "cost_class": "optional string",
  "ownership_node": "optional string",
  "status": "optional string",
  "attributes": "optional dictionary"
}
6. Field Definitions
6.1 lot_id

Globally unique identifier for the lot.

Purpose:

unique lot tracking

event linkage

genealogy management

deterministic reference

Example:

lot-20260313-P1-factoryA-0001
6.2 lot_type

Type classification of the lot.

Possible examples:

production_lot

transfer_lot

purchase_lot

safety_stock_lot

demand_anchored_lot

Purpose:

execution interpretation

policy selection

resolver behavior differentiation

6.3 product_id

Identifier of the product represented by the lot.

Purpose:

inventory matching

flow compatibility

demand fulfillment consistency

6.4 origin_node

The node at which the lot is created or sourced.

Examples:

factory

supplier

procurement origin

initial inventory node

Purpose:

production reference

source traceability

upstream planning

6.5 destination_node

Immediate intended destination of the lot.

This is not always the final market destination.

Purpose:

routing target

shipment planning

multi-leg flow support

6.6 final_market_node

Optional final consumption or market node.

This field is important when intermediate nodes exist.

Example:

factory_A -> dc_EU -> market_DE

destination_node = dc_EU
final_market_node = market_DE

Purpose:

demand anchoring

end-to-end routing visibility

multi-stage planning support

6.7 quantity_cpu

Lot quantity expressed in CPU:

Common Planning Unit

Purpose:

unified planning quantity across WOM

event execution quantity

PSI consistency

6.8 uom

Optional unit of measure.

Examples:

case

pallet

ton

set

piece

This field is descriptive and does not replace CPU.

Purpose:

human interpretation

ERP interface compatibility

6.9 created_time_bucket

The time bucket in which the lot is created.

Format:

YYYYWW

Purpose:

event scheduling

deterministic replay

lot sequencing

6.10 requested_arrival_time_bucket

Optional requested arrival bucket.

Purpose:

service target definition

lateness evaluation

operator prioritization

This is particularly useful for demand-anchored lots.

6.11 priority_class

Optional execution priority.

Possible examples:

emergency

normal

low

strategic

Purpose:

operator ranking

capacity allocation precedence

conflict resolution

6.12 service_class

Optional service-level category.

Possible examples:

premium

standard

economy

critical_supply

Purpose:

fulfillment policy

reallocation strategy

planning differentiation

6.13 routing_group

Optional routing or lane classification.

Examples:

APAC_standard

EU_express

cold_chain

bonded_route

Purpose:

path selection

plugin interpretation

transport constraints

6.14 cost_class

Optional costing category.

Examples:

standard_cost

expedited_cost

bonded_cost

tariff_sensitive

Purpose:

later economic evaluation

profit simulation

planning tradeoff analysis

6.15 ownership_node

Optional ownership or financial responsibility holder.

Examples:

company_A

legal_entity_JP

distributor_X

Purpose:

transfer pricing

legal inventory ownership

financial modeling

6.16 status

Optional runtime state of the lot.

Possible examples:

planned

in_transit

arrived

sold

cancelled

quarantined

Important:

Status must be treated as a derived or externally managed field unless explicitly governed by event logic.

Purpose:

operational visibility

UI display

debugging support

6.17 attributes

Optional extensible dictionary.

Examples:

temperature control requirement

customer allocation key

batch property

region tag

carbon class

regulatory marker

Purpose:

extensibility without changing the canonical schema

7. Minimal Required Header

The absolute minimal required lot header is:

{
  "lot_id": "string",
  "product_id": "string",
  "origin_node": "string",
  "destination_node": "string | null",
  "quantity_cpu": "float",
  "created_time_bucket": "YYYYWW"
}

This maintains compatibility with the minimal WOM Kernel.

8. Recommended Standard Header

For kernel-to-engine interoperability, the recommended standard is:

{
  "lot_id": "string",
  "lot_type": "string",
  "product_id": "string",
  "origin_node": "string",
  "destination_node": "string | null",
  "final_market_node": "string | null",
  "quantity_cpu": "float",
  "created_time_bucket": "YYYYWW",
  "requested_arrival_time_bucket": "optional YYYYWW",
  "priority_class": "optional string",
  "service_class": "optional string",
  "attributes": "optional dictionary"
}
9. Why Lot Header Is Closer to MPLS Than IP

An IP address identifies a destination endpoint.

An MPLS label carries forwarding meaning inside a network.

The WOM Lot Header behaves more like MPLS because it carries:

execution context

routing hints

service class

priority information

planning interpretation

A lot is therefore not just addressed.

It is classified for treatment inside the WOM planning network.

This is why:

Lot ID ≠ IP address
Lot Header ≈ MPLS-like execution label

10. Relationship to Flow Events

A lot does not directly mutate system state.

A lot generates flow events.

Example:

Lot
↓
Production Event
↓
Shipment Event
↓
Arrival Event
↓
Sale Event

The Lot Header provides the contextual information that allows those events to be generated consistently.

11. Role in Distributed WOM

In distributed WOM systems, lots may move across multiple planning nodes.

The Lot Header acts as the shared protocol structure understood by all participating nodes.

This enables:

inter-node planning consistency

distributed replay

lot traceability

shared operator logic

12. Role in Multi-Agent WOM

In multi-agent WOM systems, agents may:

generate lots

modify routing

prioritize lots

allocate capacity by lot class

The Lot Header acts as the common semantic contract between agents.

Without a stable Lot Header, multi-agent interoperability becomes ambiguous.

13. Example Standard Lot Header
{
  "lot_id": "lot-20260313-P1-0001",
  "lot_type": "demand_anchored_lot",
  "product_id": "P1",
  "origin_node": "factory_A",
  "destination_node": "dc_JP",
  "final_market_node": "market_TYO",
  "quantity_cpu": 100.0,
  "uom": "case",
  "created_time_bucket": "202611",
  "requested_arrival_time_bucket": "202613",
  "priority_class": "normal",
  "service_class": "standard",
  "routing_group": "JP_standard",
  "cost_class": "standard_cost",
  "ownership_node": "legal_entity_JP",
  "status": "planned",
  "attributes": {
    "customer_segment": "retail",
    "temperature_control": false
  }
}
14. Summary

The WOM Lot Header defines the protocol-level identity and execution context of a lot.

It standardizes how a lot is interpreted across:

kernel execution

planning engine logic

databases

distributed WOM nodes

multi-agent planning systems

The Lot Header is therefore a foundational protocol component of the WOM Economic OS.

It should be treated as a stable specification and evolved carefully.