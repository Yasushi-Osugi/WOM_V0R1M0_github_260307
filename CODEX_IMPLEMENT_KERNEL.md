# CODEX_IMPLEMENT_KERNEL.md

# starter memo
1. Read CODEX_IMPLEMENT_KERNEL.md and implement the minimal WOM LOT_ID-based planning kernel exactly within that scope.
2. Keep the implementation small, deterministic, and runnable.
3. Do not expand beyond the requested scope.


## Objective

Implement the **minimal WOM Planning Kernel** based on the repository design documents.

The implementation must be:

- minimal
- deterministic
- explainable
- extensible
- compatible with the WOM architecture

This task is **not** to implement the full WOM system.
This task is to implement the smallest useful LOT_ID-based planning kernel.

---

# 1. Required Reading

Before writing code, read these files in order:

1. `REPO_BOOTSTRAP.md`
2. `ARCHITECTURE_MAP.md`
3. `ARCHITECTURE.md`
4. `INTERFACE_SPEC.md`
5. `KERNEL_RULES.md`
6. `WOM_DATA_MODEL.md`
7. `WOM_MINIMAL_CLASS_MODEL.md`
8. `WOM_EXECUTION_MODEL.md`
9. `AGENTS.md`

Do not start implementation until you understand:

- Flow/Event is the source of truth
- State is derived
- Operators modify lots/events, not state directly
- The kernel must remain deterministic

---

# 2. Scope

Implement the minimal LOT_ID-based WOM planning kernel using these six classes:

- `Lot`
- `DemandEvent`
- `FlowEvent`
- `StateView`
- `Operator`
- `PlanningKernel`

Also implement the minimum required supporting components:

- a minimal `FlowEngine`
- a minimal `Evaluator`
- a minimal `Resolver`
- a tiny runnable demo

Do **not** implement:

- Excel integration
- plugins
- database persistence
- UI
- advanced pricing models
- advanced search algorithms
- full ERP integration

Keep scope intentionally small.

---

# 3. Implementation Goal

The resulting implementation must support this loop:

```text
DemandEvent
↓
FlowEngine.simulate()
↓
FlowEvent stream
↓
derive_state()
↓
detect_trust_events()
↓
Evaluator.score()
↓
Resolver.propose()
↓
apply_operator()
↓
repeat

A small demo should run end-to-end without external dependencies beyond Python standard library.

NumPy is optional, not required.

4. Architectural Constraints

The following rules are mandatory.

Rule 1 — FlowEvent is the source of truth

Do not treat inventory tables as primary truth.

Do not mutate StateView directly as part of planning logic.

Rule 2 — StateView is derived

StateView must always be rebuilt from FlowEvent and DemandEvent.

Rule 3 — Operators modify lots/events only

Operators may modify:

lot attributes

event timing

event routing

event quantities

Operators must not directly change StateView.

Rule 4 — Deterministic execution

The same inputs must produce the same outputs.

Avoid:

hidden randomness

unstable ordering

nondeterministic dictionary iteration assumptions

Use explicit sorting where needed.

Rule 5 — Minimal design

Do not over-engineer.

Implement the smallest version that demonstrates the WOM kernel logic clearly.

5. Suggested File Layout

Implement under a small isolated module path.

Recommended example:

pysi/kernel/minimal_kernel.py
pysi/kernel/minimal_demo.py
tests/test_minimal_kernel.py

If this path does not fit the current repository structure, choose the nearest equivalent minimal location.

Avoid touching unrelated files.

6. Class Definitions to Implement

Implement these classes closely following WOM_MINIMAL_CLASS_MODEL.md.

Lot
@dataclass(frozen=True)
class Lot:
    lot_id: str
    product_id: str
    quantity_cpu: float
    origin_node: str
    due_week: str
    destination_node: str | None = None
    priority: int = 0
    attributes: dict = field(default_factory=dict)
DemandEvent
@dataclass(frozen=True)
class DemandEvent:
    demand_id: str
    market_node: str
    product_id: str
    week: str
    quantity_cpu: float
    price: float | None = None
    channel_id: str | None = None
    attributes: dict = field(default_factory=dict)
FlowEvent
@dataclass(frozen=True)
class FlowEvent:
    event_id: str
    lot_id: str
    event_type: str
    product_id: str
    week: str
    quantity_cpu: float
    from_node: str | None = None
    to_node: str | None = None
    sequence: int = 0
    attributes: dict = field(default_factory=dict)
StateView
@dataclass
class StateView:
    inventory_by_node_product_week: dict = field(default_factory=dict)
    demand_by_node_product_week: dict = field(default_factory=dict)
    supply_by_node_product_week: dict = field(default_factory=dict)
    backlog_by_node_product_week: dict = field(default_factory=dict)
    capacity_usage_by_node_week: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
Operator
@dataclass(frozen=True)
class Operator:
    operator_id: str
    operator_type: str
    target_lot_id: str | None = None
    target_event_id: str | None = None
    parameters: dict = field(default_factory=dict)
    rationale: str = ""
PlanningKernel

Implement a small orchestrator class that coordinates simulation, evaluation, trust detection, and operator application.

7. Supporting Components
7.1 FlowEngine

Implement a minimal FlowEngine with these methods:

simulate(...)
derive_state(...)
detect_trust_events(...)
simulate()

Input:

lots

demand_events

capacities

policy

Output:

list of FlowEvent

Minimal behavior is enough.
For example:

generate production events for lots

generate shipment events toward market

generate arrival events

generate sale events if demand exists

Keep logic simple and explicit.

derive_state()

Rebuild StateView from the event list.

Must at least derive:

inventory

supply

demand

backlog

capacity usage

detect_trust_events()

Generate simple trust events such as:

stockout risk

inventory overflow

capacity overload

Return a simple serializable structure or a minimal trust-event dataclass if convenient.

7.2 Evaluator

Implement a minimal evaluator with:

score(state, policy) -> dict

Return decomposed metrics such as:

service_level

inventory_penalty

total_score

Simple scoring is enough.

Example pattern:

total_score = service_level - inventory_penalty

Keep it deterministic and transparent.

7.3 Resolver

Implement a minimal resolver with:

propose(...)
apply_operator(...)
propose()

Given:

lots

flow_events

state

trust_events

policy

Return a single Operator.

Minimal behavior is enough.

Example logic:

if stockout risk exists → shift production earlier or increase supply

if inventory overflow exists → delay production or shipment

otherwise → do_nothing

apply_operator()

Return a new list of lots or modified planning objects.
Do not mutate state directly.

If modifying lots is simpler than modifying events in the first version, that is acceptable.

8. Minimal Demo

Provide a runnable demo script.

Suggested behavior:

Create a tiny scenario

one product

one factory

one market

one or two lots

one or two demand events

Run the planning kernel for a few iterations

Print:

trust events

chosen operators

evaluation scores

final derived state

The goal is not realism.
The goal is to demonstrate the WOM kernel loop clearly.

9. Tests

Add minimal tests.

Required tests:

Test 1 — State derivation is deterministic

Same inputs produce same state.

Test 2 — Operator does not mutate StateView directly

State changes only through re-simulation.

Test 3 — Flow simulation produces expected event types

At least production / shipment / arrival / sale when appropriate.

Test 4 — Resolver returns a valid Operator

For a simple trust event.

Keep tests small and readable.

10. Coding Conventions

Use Python dataclasses

Use type hints

Prefer pure functions where possible

Keep comments concise and useful

Prefer clarity over abstraction

Prefer explicitness over cleverness

Use readable names such as:

derive_state

detect_trust_events

apply_operator

run

Avoid vague names like:

process

handle

update_data

11. Deliverables

Expected deliverables:

Minimal kernel module with the six core classes

Minimal FlowEngine

Minimal Evaluator

Minimal Resolver

Runnable demo

Small test file

Optional but helpful:

a short module-level docstring

simple inline comments explaining WOM-specific rules

12. Definition of Success

This task is successful if:

the code runs end-to-end

the kernel loop is visible and understandable

state is derived from events

operators do not mutate state directly

the implementation is small and clear

the code can serve as a foundation for the full WOM kernel

13. Final Instruction

When uncertain, choose the smaller and clearer implementation.

Preserve these priorities in order:

architectural correctness

determinism

explainability

minimal scope

extensibility

Do not optimize for completeness.
Optimize for a correct minimal WOM kernel.