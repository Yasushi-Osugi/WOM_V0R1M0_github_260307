# WOM Event Store / DB Table Design

Project: Weekly Operation Model (WOM)  
Document Type: Database Design Specification  
Version: 1.0  
Status: Draft  
Date: March 2026

---

# 1. Purpose

This document defines the Event Store and core database table design for WOM.

The WOM database layer must support:

- deterministic event-sourced simulation
- state reconstruction by replay
- scenario persistence
- planning auditability
- distributed planning interoperability
- future multi-agent WOM coordination

The database is not merely a storage layer.

It is the persistent foundation of the WOM Economic OS.

---

# 2. Architectural Role

WOM architecture can be understood as:

Applications / UI
↓
Planning Engine
↓
WOM Kernel
↓
WOM Event Schema
↓
WOM Event Store / DB
↓
Physical Storage

The Event Store is the persistent source of truth.

Derived state may be materialized for performance, but must remain reconstructable from events.

---

# 3. Design Principles

## 3.1 Event-Sourced Persistence

Events are the canonical truth.

State tables are derived views.

---

## 3.2 Deterministic Replay

The database must preserve the fields required for deterministic event replay.

---

## 3.3 Scenario Isolation

Planning runs and scenarios must be separable.

Different scenario branches must coexist safely.

---

## 3.4 Extensibility

The schema must allow future support for:

- distributed nodes
- plugin-generated events
- policy-driven planning
- financial extensions
- multi-agent coordination

---

## 3.5 SQL-First but Engine-Agnostic

The logical model should work with:

- SQLite
- PostgreSQL
- future cloud relational databases

---

# 4. Logical Data Domains

The WOM DB is organized into the following domains:

1. master data
2. scenario data
3. event store
4. derived state
5. planning session / run history
6. policy / plugin / operator history

---

# 5. Core Table Overview

The following logical tables are recommended.

Master Data:
- md_node
- md_product
- md_lane
- md_resource

Scenario Data:
- sc_scenario
- sc_scenario_parameter
- sc_lot
- sc_demand_event

Event Store:
- ev_flow_event
- ev_sale_event
- ev_trust_event
- ev_operator_action

Derived Views / Materialized State:
- st_inventory_snapshot
- st_supply_snapshot
- st_backlog_snapshot
- st_capacity_snapshot
- st_financial_snapshot

Execution / Session Control:
- run_planning_session
- run_iteration_history

Optional Extensions:
- pl_policy_set
- pl_plugin_execution
- ag_agent_action_log

---

# 6. Master Data Tables

# 6.1 md_node

Defines planning nodes.

Examples:

- factories
- DCs
- markets
- suppliers
- legal entities

Suggested columns:

```text
node_id                PK
node_name
node_type
region_code
country_code
parent_node_id         nullable
is_active
attributes_json
created_at
updated_at

Notes:

node_type examples:

factory

dc

market

supplier

virtual

6.2 md_product

Defines products or planning items.

Suggested columns:

product_id             PK
product_name
product_family
base_uom
cpu_conversion_factor  nullable
is_active
attributes_json
created_at
updated_at
6.3 md_lane

Defines transportation or routing lanes.

Suggested columns:

lane_id                PK
from_node_id
to_node_id
lane_type
default_lead_time_weeks
default_capacity_cpu   nullable
cost_class             nullable
is_active
attributes_json
created_at
updated_at
6.4 md_resource

Defines constrained resources.

Suggested columns:

resource_id            PK
resource_name
resource_type
node_id
capacity_uom
is_active
attributes_json
created_at
updated_at

resource_type examples:

production

shipping

storage

handling

7. Scenario Data Tables
7.1 sc_scenario

Defines a planning scenario.

Suggested columns:

scenario_id            PK
scenario_name
scenario_type
parent_scenario_id     nullable
description
version_label          nullable
status
created_by
created_at
updated_at

scenario_type examples:

asis

tobe

canbe

willbe

letitbe

This structure aligns well with your scenario thinking and makes branching natural.

7.2 sc_scenario_parameter

Stores scenario-level parameters.

Suggested columns:

scenario_parameter_id  PK
scenario_id
parameter_name
parameter_value
parameter_type
scope_type             nullable
scope_id               nullable
effective_from_bucket  nullable
effective_to_bucket    nullable
created_at
updated_at

Examples:

lead_time_weeks

capacity_limit

safety_stock

tariff_rate

price_policy

service_target

This table is essential for replacing hard-coded CSV parameter fragments.

7.3 sc_lot

Stores initial or scenario-defined lots.

Suggested columns:

lot_id                 PK
scenario_id
lot_type
product_id
origin_node
destination_node       nullable
final_market_node      nullable
quantity_cpu
uom                    nullable
created_time_bucket
requested_arrival_time_bucket nullable
priority_class         nullable
service_class          nullable
routing_group          nullable
cost_class             nullable
ownership_node         nullable
status                 nullable
attributes_json
created_at
updated_at

This table implements the Lot Header persistence model.

7.4 sc_demand_event

Stores demand-side scenario inputs.

Suggested columns:

demand_id              PK
scenario_id
market_id
product_id
time_bucket
quantity_cpu
price                  nullable
channel_id             nullable
attributes_json
created_at
updated_at

This table is an input domain table, not a runtime event store table.

8. Event Store Tables
8.1 ev_flow_event

This is the central event store table.

Every economic runtime action is recorded here.

Suggested columns:

flow_id                PK
scenario_id
session_id             nullable
iteration_no           nullable
lot_id
event_type
product_id
from_node              nullable
to_node                nullable
time_bucket
quantity_cpu
creation_sequence
event_priority         nullable
causal_event_id        nullable
operator_id            nullable
source_type            nullable
status                 nullable
metadata_json
created_at

Recommended indexes:

(scenario_id, time_bucket)

(lot_id)

(product_id, time_bucket)

(event_type, time_bucket)

(operator_id)

(session_id, iteration_no)

This table must be append-friendly.

Do not design it around heavy in-place mutation.

8.2 ev_sale_event

Two design choices exist:

Option A:
store sale as event_type='sale' inside ev_flow_event only

Option B:
store sale both in ev_flow_event and in a specialized ev_sale_event table

Recommended v1 database design:

Use both, with ev_flow_event as canonical runtime event store and ev_sale_event as an optional analytical convenience table.

Suggested columns:

sale_id                PK
flow_id                unique
scenario_id
session_id             nullable
iteration_no           nullable
market_id
product_id
time_bucket
quantity_cpu
source_node
demand_id              nullable
price                  nullable
revenue_amount         nullable
metadata_json
created_at

Purpose:

analytics

revenue tracking

service evaluation

demand linkage

8.3 ev_trust_event

Stores anomalies detected by the kernel.

Suggested columns:

trust_event_id         PK
scenario_id
session_id             nullable
iteration_no           nullable
event_type
severity
node_id                nullable
product_id             nullable
time_bucket
message
evidence_json
created_at

Recommended indexes:

(scenario_id, time_bucket)

(event_type, time_bucket)

(session_id, iteration_no)

8.4 ev_operator_action

Stores operator actions applied during replanning.

Suggested columns:

operator_id            PK
scenario_id
session_id             nullable
iteration_no           nullable
operator_type
target_json
parameters_json
rationale
selected_flag
created_at

Purpose:

audit trail of intervention

explainability

policy evaluation

future learning systems

9. Session / Execution Control Tables
9.1 run_planning_session

Represents one planning execution session.

Suggested columns:

session_id             PK
scenario_id
engine_version
kernel_version
policy_set_id          nullable
plugin_set_id          nullable
started_at
completed_at           nullable
status
initiated_by
notes                  nullable

status examples:

running

completed

failed

cancelled

This table allows reproducible run management.

9.2 run_iteration_history

Stores iteration-level summary.

Suggested columns:

iteration_history_id   PK
session_id
iteration_no
evaluation_score       nullable
service_level          nullable
inventory_penalty      nullable
risk_penalty           nullable
selected_operator_id   nullable
trust_event_count      nullable
notes                  nullable
created_at

Purpose:

progress tracking

console display

debugging

regression comparison

10. Derived State Tables

These tables are not the canonical truth.

They are derived snapshots for performance and usability.

10.1 st_inventory_snapshot

Suggested columns:

inventory_snapshot_id  PK
scenario_id
session_id             nullable
iteration_no           nullable
node_id
product_id
time_bucket
inventory_cpu
created_at

Recommended unique key:

(scenario_id, session_id, iteration_no, node_id, product_id, time_bucket)

10.2 st_supply_snapshot

Suggested columns:

supply_snapshot_id     PK
scenario_id
session_id             nullable
iteration_no           nullable
node_id
product_id
time_bucket
supply_cpu
created_at
10.3 st_backlog_snapshot

Suggested columns:

backlog_snapshot_id    PK
scenario_id
session_id             nullable
iteration_no           nullable
market_id
product_id
time_bucket
backlog_cpu
created_at
10.4 st_capacity_snapshot

Suggested columns:

capacity_snapshot_id   PK
scenario_id
session_id             nullable
iteration_no           nullable
resource_id
time_bucket
capacity_used_cpu
capacity_limit_cpu     nullable
created_at
10.5 st_financial_snapshot

Optional but strongly recommended for later growth.

Suggested columns:

financial_snapshot_id  PK
scenario_id
session_id             nullable
iteration_no           nullable
node_id                nullable
product_id             nullable
time_bucket
revenue_amount         nullable
cost_amount            nullable
profit_amount          nullable
inventory_value        nullable
created_at

This is the bridge toward the money-side of WOM.

11. Policy / Plugin / Agent Extension Tables
11.1 pl_policy_set

Suggested columns:

policy_set_id          PK
policy_set_name
description
policy_definition_json
created_at
updated_at
11.2 pl_plugin_execution

Suggested columns:

plugin_execution_id    PK
session_id
iteration_no
plugin_name
plugin_version         nullable
input_summary_json     nullable
output_summary_json    nullable
status
created_at
11.3 ag_agent_action_log

Optional future table for multi-agent WOM.

Suggested columns:

agent_action_id        PK
session_id
iteration_no
agent_id
action_type
target_id              nullable
action_payload_json
created_at

This is future-facing but useful to reserve conceptually.

12. Recommended Foreign Key Relationships

Key relationships:

sc_lot.scenario_id → sc_scenario.scenario_id

sc_demand_event.scenario_id → sc_scenario.scenario_id

ev_flow_event.scenario_id → sc_scenario.scenario_id

ev_flow_event.session_id → run_planning_session.session_id

ev_flow_event.lot_id → sc_lot.lot_id

ev_sale_event.flow_id → ev_flow_event.flow_id

ev_trust_event.session_id → run_planning_session.session_id

ev_operator_action.session_id → run_planning_session.session_id

run_iteration_history.session_id → run_planning_session.session_id

In SQLite these may be relaxed operationally, but logically they should be preserved.

13. Replay and Materialization Model

Canonical rule:

Event Store = source of truth
State Snapshot = derived cache / materialized view

Replay process:

load scenario inputs

load runtime events ordered by deterministic key

derive state

optionally persist snapshots

This preserves the event-sourced kernel philosophy.

14. Recommended Deterministic Ordering in DB

For replay, use:

ORDER BY
time_bucket,
COALESCE(event_priority, 999),
creation_sequence,
flow_id

This ordering must be treated as canonical.

15. Example Minimal SQL DDL Skeleton
CREATE TABLE ev_flow_event (
    flow_id TEXT PRIMARY KEY,
    scenario_id TEXT NOT NULL,
    session_id TEXT,
    iteration_no INTEGER,
    lot_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    product_id TEXT NOT NULL,
    from_node TEXT,
    to_node TEXT,
    time_bucket TEXT NOT NULL,
    quantity_cpu REAL NOT NULL,
    creation_sequence INTEGER NOT NULL,
    event_priority INTEGER,
    causal_event_id TEXT,
    operator_id TEXT,
    source_type TEXT,
    status TEXT,
    metadata_json TEXT,
    created_at TEXT NOT NULL
);

Example index:

CREATE INDEX idx_ev_flow_event_scenario_time
ON ev_flow_event (scenario_id, time_bucket, creation_sequence);
16. Recommended Implementation Phasing
Phase 1

Minimal SQL persistence:

sc_scenario

sc_lot

sc_demand_event

ev_flow_event

ev_trust_event

ev_operator_action

run_planning_session

run_iteration_history

This is enough to support Kernel v1.1 and Planning Engine v0.

Phase 2

Add derived state persistence:

st_inventory_snapshot

st_backlog_snapshot

st_capacity_snapshot

Phase 3

Add financial and plugin extensions:

ev_sale_event

st_financial_snapshot

pl_policy_set

pl_plugin_execution

Phase 4

Add multi-agent extensions:

ag_agent_action_log

17. DB Engine Recommendation

For development and local reproducibility:

SQLite is an excellent first engine

For concurrent and scalable planning services:

PostgreSQL is the recommended next step

Suggested path:

CSV
↓
SQLite
↓
PostgreSQL
↓
distributed event architecture

This matches the gradual growth strategy of WOM.

18. Summary

The WOM Event Store / DB design provides the persistent foundation for the WOM Economic OS.

It separates:

scenario inputs

runtime events

trust signals

operator interventions

derived snapshots

planning session history

This design preserves the WOM kernel philosophy:

events are the source of truth
state is derived
planning is reproducible
system behavior is explainable

The Event Store is therefore not just a database.

It is the persistent memory of the WOM system.