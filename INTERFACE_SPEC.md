WOM Core Interface Specification
This document defines the stable interface boundaries of the WOM planning kernel.
The purpose of this specification is to:
•	stabilize module responsibilities
•	enable parallel development
•	support deterministic and explainable planning
•	allow AI-assisted extensions without breaking kernel design
This specification intentionally defines interfaces only, not internal algorithms.
________________________________________
1. Architecture Overview
The WOM planning kernel is composed of four core modules:
demand_model.py
flow_engine.py
evaluation.py
resolver.py
Together they implement the WOM decision loop:
Demand Generation
↓
Flow Simulation
↓
State Derivation
↓
Trust Event Detection
↓
Evaluation
↓
Resolver Search
↓
Operator Selection
↓
Flow Update
Each module has a strictly defined responsibility.
________________________________________
2. Design Principles
The WOM kernel follows these architectural principles:
1.	Flow/Event is the source of truth
Inventory and PSI states must always be derived.
2.	Modules must have single responsibility
3.	All module interfaces must be deterministic
4.	All decisions must remain explainable
5.	Modules must communicate via typed interfaces
6.	No module may bypass another module’s responsibility
________________________________________
3. Shared Data Structures
The following types define the shared language between modules.
________________________________________
3.1 DemandEvent
Represents market demand input.
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class DemandEvent:
    demand_id: str
    market_id: str
    product_id: str
    time_bucket: str
    quantity_cpu: float
    price: Optional[float] = None
    channel_id: Optional[str] = None
    metadata: Optional[dict] = None
Demand quantities are expressed in CPU (Common Planning Unit).
________________________________________
3.2 FlowEvent
Represents a physical or logical movement in the supply network.
@dataclass(frozen=True)
class FlowEvent:
    flow_id: str
    lot_id: str
    event_type: str
    product_id: str
    from_node: Optional[str]
    to_node: Optional[str]
    time_bucket: str
    quantity_cpu: float
    metadata: Optional[dict] = None
Typical event_type values:
production
shipment
arrival
sale
inventory_adjustment
Flow events are the primary truth of the system.
________________________________________
3.3 StateView
Represents derived planning state.
@dataclass(frozen=True)
class StateView:
    inventory_by_node_product_time: dict
    demand_by_market_product_time: dict
    supply_by_node_product_time: dict
    capacity_usage_by_resource_time: dict
    backlog_by_market_product_time: dict
    financial_summary: Optional[dict] = None
This structure is derived entirely from flow events.
________________________________________
3.4 TrustEvent
Represents a detected anomaly or constraint violation.
@dataclass(frozen=True)
class TrustEvent:
    trust_event_id: str
    event_type: str
    severity: float
    node_id: Optional[str]
    product_id: Optional[str]
    time_bucket: str
    message: str
    evidence: Optional[dict] = None
Example trust events:
E_STOCKOUT_RISK
E_INVENTORY_CAP_EXCEEDED
E_CAPACITY_OVERLOAD
E_SUPPLY_DELAY
________________________________________
3.5 Operator
Represents a corrective planning action.
@dataclass(frozen=True)
class Operator:
    operator_id: str
    operator_type: str
    target: dict
    parameters: dict
    rationale: Optional[str] = None
Examples:
increase_production
shift_shipment
reroute_flow
change_price
use_buffer_inventory
Operators modify flow events, not state tables.
________________________________________
3.6 EvaluationResult
Represents evaluation results of a planning state.
@dataclass(frozen=True)
class EvaluationResult:
    total_score: float
    service_level: float
    profit: float
    inventory_penalty: float
    risk_penalty: float
    capacity_balance_score: Optional[float] = None
    wellbeing_score: Optional[float] = None
    details: Optional[dict] = None
Evaluation must remain decomposable and explainable.
________________________________________
4. Module: demand_model.py
Responsibility
Generates market demand events.
Must NOT:
•	modify flows
•	simulate supply
•	evaluate plans
•	generate operators
________________________________________
Interface
def generate_demand_events(
    scenario: dict,
    price_state: dict | None = None,
    promotion_state: dict | None = None,
    policy: dict | None = None,
) -> list[DemandEvent]
________________________________________
Output
list[DemandEvent]
________________________________________
Contract
•	deterministic output
•	CPU-based quantities
•	canonical time buckets
•	no side effects
________________________________________
5. Module: flow_engine.py
Responsibility
Simulates supply chain flows and derives system state.
Implements flow conservation across the network.
inflow - outflow = inventory change
________________________________________
Interface
def run_flow(
    network: dict,
    flow_events: list[FlowEvent],
    demand_events: list[DemandEvent],
    capacities: dict,
    policy: dict | None = None,
) -> StateView
________________________________________
Trust Event Detection
def detect_trust_events(
    state: StateView,
    policy: dict | None = None,
) -> list[TrustEvent]
________________________________________
Contract
•	Flow/Event is the primary input truth
•	Inventory must be derived
•	deterministic execution
•	explainable detection logic
________________________________________
6. Module: evaluation.py
Responsibility
Scores a planning state according to business objectives.
Evaluation may include:
•	service level
•	profit
•	inventory penalties
•	risk penalties
•	sustainability metrics
________________________________________
Interface
def evaluate_state(
    state: StateView,
    policy: dict,
    baseline_state: StateView | None = None,
) -> EvaluationResult
________________________________________
Contract
•	must return decomposed metrics
•	total score must be reproducible
•	evaluation weights come from policy
•	evaluation must remain explainable
________________________________________
7. Module: resolver.py
Responsibility
Searches corrective operators to resolve trust events.
Resolver performs:
trust events
↓
operator candidate generation
↓
simulation
↓
evaluation
↓
operator selection
________________________________________
Candidate Generation
def generate_candidates(
    trust_events: list[TrustEvent],
    state: StateView,
    policy: dict,
) -> list[Operator]
________________________________________
Operator Application
def apply_operator(
    flow_events: list[FlowEvent],
    operator: Operator,
) -> list[FlowEvent]
________________________________________
Main Resolver Interface
def resolve(
    network: dict,
    flow_events: list[FlowEvent],
    demand_events: list[DemandEvent],
    capacities: dict,
    trust_events: list[TrustEvent],
    state: StateView,
    policy: dict,
) -> dict
________________________________________
Output
{
    "best_operator": Operator | None,
    "best_flow_events": list[FlowEvent],
    "best_state": StateView,
    "best_evaluation": EvaluationResult,
    "candidate_evaluations": list[dict]
}
________________________________________
Contract
•	search strategy must be replaceable
•	execution must be deterministic
•	decisions must be traceable
•	output must be serializable
________________________________________
8. Allowed Module Dependencies
demand_model.py
        ↓
flow_engine.py
        ↓
evaluation.py

resolver.py → flow_engine.py
resolver.py → evaluation.py
________________________________________
9. Forbidden Dependencies
The following patterns are not allowed:
evaluation → resolver
demand_model → flow_engine
resolver → demand_model
flow_engine → evaluation
Modules must respect architectural boundaries.
________________________________________
10. Execution Loop
A typical WOM execution cycle:
generate_demand_events()
↓
run_flow()
↓
detect_trust_events()
↓
evaluate_state()
↓
resolve()
↓
apply_operator()
↓
run_flow()
↓
evaluate_state()
________________________________________
11. Artifact Outputs
Each run should produce the following artifacts:
demand_events.json
flow_events.json
state_view.json
trust_events.json
evaluation_results.json
operator_candidates.json
operator_spec.json
These artifacts support:
•	reproducibility
•	explainability
•	AI-assisted analysis
________________________________________
12. Policy Interface
All modules receive configuration via policy.
Example:
policy = {
  "time_bucket": "weekly",

  "evaluation_weights": {
      "service": 0.35,
      "profit": 0.30,
      "inventory_penalty": 0.20,
      "risk_penalty": 0.15
  },

  "resolver": {
      "strategy": "beam_search",
      "max_candidates": 20,
      "max_depth": 3
  },

  "demand": {
      "elasticity_model": "linear"
  }
}
No module may hardcode policy values.
________________________________________
13. Scope of This Specification
This document does NOT define:
•	optimization algorithms
•	UI or visualization
•	database persistence
•	plugin system implementation
•	scenario file formats
These topics are handled by separate specifications.
________________________________________
14. Summary
The WOM planning kernel is structured as:
demand_model.py   → market response
flow_engine.py    → supply network physics
evaluation.py     → management objective
resolver.py       → decision/search engine
This architecture enables WOM to function as an AI-assisted planning kernel supporting explainable and reproducible economic decision processes.
