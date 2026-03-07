# LOT_ID Specification (v2)

This document defines the canonical LOT_ID specification
used in WOM (Weekly Operation Model).

LOT_ID represents the fundamental planning unit of WOM.

Unlike traditional planning systems that operate on scalar quantities,
WOM operates on **lot_ID lists**.

All quantities in PSI are derived as:

quantity = len(lot_ID_list)

Therefore, the structure and semantics of LOT_ID are
critical to the correctness and explainability of the planning engine.

---

# 1 Conceptual Meaning

A LOT_ID represents a **final consumption demand lot**.

Each LOT_ID corresponds to:

- a specific market node (leaf node in outbound supply chain)
- a specific product
- a specific consumption time bucket
- a specific lot sequence within that time bucket

Therefore LOT_ID is **demand-anchored**.

It represents:

"A lot that will be consumed at a specific market location
in a specific week."

This is fundamentally different from manufacturing-based lot identity.

In WOM, production and logistics processes exist to
**fulfill these demand lots**.

---

# 2 Canonical LOT_ID Format

The canonical LOT_ID format is:

NODE_NAME <SEP> PRODUCT_NAME <SEP> YYYYWWNNNN

Example:

TOKYO_DC-COLD_DRUG_A-2026050001

Where:

NODE_NAME = leaf market node  
PRODUCT_NAME = product identifier  
YYYY = ISO year  
WW = ISO week number (2 digits)  
NNNN = lot sequence (4 digits, starting from 0001)

Separator:

SEP = LOT_SEP (typically "-")

---

# 3 Example

Given:

node_name = TOKYO_DC  
product_name = DRUG_A  
iso_year = 2026  
iso_week = 05  
S_lot = 3  

Generated LOT_IDs:

TOKYO_DC-DRUG_A-2026050001  
TOKYO_DC-DRUG_A-2026050002  
TOKYO_DC-DRUG_A-2026050003  

These represent three demand lots
to be consumed at TOKYO_DC in week 2026-W05.

---

# 4 LOT_ID Generation

LOT_IDs are generated during demand planning
when monthly demand is converted into weekly lot demand.

Process:

monthly demand
↓
daily expansion
↓
weekly aggregation
↓
lot_size conversion
↓
lot_ID generation

Pseudo logic:

for i in range(S_lot):
    lot_id = f"{node}{SEP}{product}{SEP}{year}{week:02d}{i+1:04d}"

All generated LOT_IDs are deterministic.

---

# 5 Demand Anchor Principle

LOT_IDs are **anchored at final consumption nodes**.

The node_name in LOT_ID always refers to:

the **leaf node of the outbound supply chain**.

This node represents:

- final market
- retail channel
- end consumption region

This ensures that each lot represents
a specific demand location and time.

---

# 6 Backward Planning Behavior

After demand lots are generated,
demand planning performs **backward planning**.

Backward planning shifts LOT_IDs upstream in time
according to lead time.

Example:

Market consumption week: 2026-W05

Lead time: 2 weeks

Production shipment position:

2026-W03

Important rule:

The LOT_ID identity **does not change**.

Only the time position in the planning simulation shifts.

---

# 7 Forward Planning Behavior

After backward positioning,
the planning engine performs forward simulation.

The forward simulation follows a hybrid push-pull structure.

---

## 7.1 Inbound Supply Chain (PUSH)

Inbound supply chain connects:

material suppliers → manufacturing plant (MOM)

Characteristics:

- supply-side driven
- synchronized production structure

Supply flows:

leaf material nodes
↓
component suppliers
↓
MOM (Mother Of Manufacturing)

Supply moves forward using **PUSH logic**.

---

## 7.2 Outbound Supply Chain PUSH

Outbound supply chain begins at:

DAD (Distribution And Delivery yard)

Products are pushed from:

DAD → decoupling stock point

Purpose:

absorb the demand gap between

- volatile market demand
- leveled production output

Products accumulate as inventory at the decoupling point.

---

## 7.3 Outbound Supply Chain PULL

From the decoupling stock point to market nodes,
shipment follows **PULL logic**.

Flow:

decoupling stock point
↓
regional distribution
↓
leaf market node

Shipment priority rules include:

- urgency
- priority customers
- profit contribution

---

# 8 LOT Identity Preservation

Throughout the planning simulation,
LOT_ID identity must remain unchanged.

The same LOT_ID may move through:

P_ids → I_ids → S_ids

across multiple nodes and weeks.

This enables full lot lineage tracking.

---

# 9 Traceability

Because planning operates on LOT_ID lists,
the system can track lot lineage.

Example:

LOT_ID:

TOKYO_DC-DRUG_A-2026050002

Traceable history:

production node  
shipment node  
inventory node  
final consumption node

This supports explainable supply chain simulation.

---

# 10 Determinism

LOT_ID generation must be deterministic.

Given identical inputs:

scenario  
demand  
lot_size  

the same LOT_IDs must be generated.

This guarantees reproducible simulations.

---

# 11 Validation Rules

Planning engine must verify:

no duplicate LOT_IDs  
no orphan LOT_IDs  
no simultaneous multi-location lots  

LOT_ID consistency is required
for correct PSI simulation.

---

# 12 Future Extensions

Future versions may attach additional attributes to LOT_ID:

cost  
carbon footprint  
quality attributes  
expiration date  

However, the canonical LOT_ID identity format
must remain stable for compatibility.
