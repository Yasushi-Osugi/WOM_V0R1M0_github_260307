# WOM Minimal Class Model

This document defines the **minimal class architecture** required to implement the WOM planning kernel.

The goal is to provide a **small, deterministic, and extensible core model** that:

- represents supply objects using LOT_ID
- represents system activity as flow events
- derives system state from events
- allows decision operators to modify planning outcomes

This minimal model forms the foundation of the **WOM Planning Kernel**.

---

# Core Principle

WOM follows a strict architectural principle:

Flow/Event = source of truth  
State = derived view

This means:

- inventory is not stored as primary state
- system state is always derived from flow events
- operators modify lots or events, not state directly

---

# Minimal Class Set

The minimal WOM kernel uses six classes.


Lot
DemandEvent
FlowEvent
StateView
Operator
PlanningKernel


These classes represent the minimal structure required to simulate and optimize planning flows.

---

# Class Relationship


DemandEvent
↓
Lot
↓
FlowEvent
↓
StateView
↓
Operator
↓
PlanningKernel


PlanningKernel orchestrates the interaction between all other classes.

---

# 1 Lot

## Purpose

Represents the **basic supply object** handled by the planning system.

In WOM, planning is performed on **lots rather than quantities**.

## Definition

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class Lot:
    lot_id: str
    product_id: str
    quantity_cpu: float
    origin_node: str
    due_week: str
    destination_node: Optional[str] = None
    priority: int = 0
    attributes: dict = field(default_factory=dict)
Notes

lot_id must be globally unique

lots should be immutable objects

operators may replace lots but should not mutate them

2 DemandEvent
Purpose

Represents market demand signals entering the planning system.

Definition
from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class DemandEvent:
    demand_id: str
    market_node: str
    product_id: str
    week: str
    quantity_cpu: float
    price: Optional[float] = None
    channel_id: Optional[str] = None
    attributes: dict = field(default_factory=dict)
Notes

Demand events are inputs to the planning kernel.

They are not flow events.

3 FlowEvent
Purpose

Represents actual movement or transformation of supply lots.

Flow events are the primary source of truth for system activity.

Definition
from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class FlowEvent:
    event_id: str
    lot_id: str
    event_type: str
    product_id: str
    week: str
    quantity_cpu: float
    from_node: Optional[str] = None
    to_node: Optional[str] = None
    sequence: int = 0
    attributes: dict = field(default_factory=dict)
Typical Event Types

production
shipment
arrival
sale
inventory_adjustment

4 StateView
Purpose

Represents a derived view of the system state.

StateView must always be reconstructed from FlowEvents.

Definition
from dataclasses import dataclass, field

@dataclass
class StateView:
    inventory_by_node_product_week: dict = field(default_factory=dict)
    demand_by_node_product_week: dict = field(default_factory=dict)
    supply_by_node_product_week: dict = field(default_factory=dict)
    backlog_by_node_product_week: dict = field(default_factory=dict)
    capacity_usage_by_node_week: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
Notes

StateView is never directly mutated by operators.

5 Operator
Purpose

Represents a corrective planning action proposed by the resolver.

Operators modify lots or flow events.

Definition
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Operator:
    operator_id: str
    operator_type: str
    target_lot_id: str | None = None
    target_event_id: str | None = None
    parameters: dict = field(default_factory=dict)
    rationale: str = ""
Example Operator Types

shift_production_week
shift_shipment_week
reroute_lot
split_lot
change_price
do_nothing

6 PlanningKernel
Purpose

Coordinates the entire planning loop.

The kernel performs:

flow simulation

state derivation

evaluation

decision search

operator application

Definition
from dataclasses import dataclass, field
from typing import List

@dataclass
class PlanningKernel:

    demand_model: object
    flow_engine: object
    evaluator: object
    resolver: object
    max_iterations: int = 10
    history: list = field(default_factory=list)

    def run(
        self,
        lots: List[Lot],
        demand_events: List[DemandEvent],
        capacities: dict,
        policy: dict | None = None,
    ) -> dict:

        current_lots = lots
        current_flow_events: List[FlowEvent] = []

        for step in range(self.max_iterations):

            current_flow_events = self.flow_engine.simulate(
                lots=current_lots,
                demand_events=demand_events,
                capacities=capacities,
                policy=policy or {},
            )

            state = self.flow_engine.derive_state(
                flow_events=current_flow_events,
                demand_events=demand_events,
                capacities=capacities,
                policy=policy or {},
            )

            trust_events = self.flow_engine.detect_trust_events(
                state=state,
                capacities=capacities,
                policy=policy or {},
            )

            evaluation = self.evaluator.score(
                state=state,
                policy=policy or {},
            )

            self.history.append({
                "step": step,
                "state": state,
                "trust_events": trust_events,
                "evaluation": evaluation,
            })

            if not trust_events:
                break

            operator = self.resolver.propose(
                lots=current_lots,
                flow_events=current_flow_events,
                state=state,
                trust_events=trust_events,
                policy=policy or {},
            )

            current_lots = self.resolver.apply_operator(
                lots=current_lots,
                flow_events=current_flow_events,
                operator=operator,
                policy=policy or {},
            )

        return {
            "lots": current_lots,
            "flow_events": current_flow_events,
            "state": state,
            "evaluation": evaluation,
            "history": self.history,
        }
Kernel Loop

The WOM planning kernel follows this loop.


DemandEvent
↓
FlowEngine.simulate()
↓
FlowEvent stream
↓
StateView.derive()
↓
Evaluation.score()
↓
Resolver.propose()
↓
Operator.apply()
↓
Repeat

Architectural Rules

The following rules must always hold.

FlowEvent is the source of truth.

StateView must be derived from FlowEvents.

Operators modify lots or events.

StateView must never be directly mutated.

The planning kernel must remain deterministic.

Summary

The WOM minimal model represents planning as an event-driven system.


Lot           = identity of supply
DemandEvent   = market input
FlowEvent     = system activity
StateView     = derived observation
Operator      = corrective action
PlanningKernel = closed-loop orchestrator


This model forms the minimal core of the WOM Planning Kernel.