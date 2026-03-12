WOM Kernel Protection Rules
This document defines non-negotiable architectural rules for the WOM planning kernel.
These rules protect the integrity of the WOM architecture.
AI coding agents and human developers must follow these rules when modifying this repository.
Violating these rules can break:
•	determinism
•	explainability
•	reproducibility
•	architectural extensibility
________________________________________
1. Kernel Definition
The WOM kernel consists of the following components:
flow_engine
event_model
state_derivation
These components define the physical behavior of the planning system.
They are equivalent to physics laws of the planning world.
Kernel components must remain:
•	deterministic
•	stateless
•	explainable
•	policy-independent
________________________________________
2. Source of Truth Rule
Flow/Event data is the only source of truth.
Inventory, PSI tables, and derived states must always be computed from events.
Flow Events → Derived State
Never treat inventory tables as primary data.
Forbidden pattern:
inventory[node] += quantity
Correct pattern:
create FlowEvent(type="inventory_adjustment")
________________________________________
3. State Mutation Rule
No module is allowed to directly mutate derived state.
State must only change through:
Flow Events
Allowed:
FlowEvent → flow_engine → new StateView
Forbidden:
modify StateView directly
________________________________________
4. Resolver Boundary Rule
The resolver must never modify system state directly.
Resolver may only:
generate operators
apply operators to flow events
re-run simulation
evaluate results
Resolver must never:
modify inventory tables
change state structures
bypass flow_engine
Resolver output must always be expressed as:
Operator → FlowEvent modifications
________________________________________
5. Flow Conservation Rule
The planning engine must always satisfy flow conservation.
inflow − outflow = inventory change
No module may violate this rule.
Violations indicate a kernel bug.
________________________________________
6. Determinism Rule
Kernel execution must be deterministic.
Given identical inputs:
same scenario
same events
same policy
The engine must produce identical results.
Avoid:
•	non-seeded randomness
•	unstable iteration order
•	parallel race conditions
________________________________________
7. Event Ordering Rule
All events must follow a deterministic ordering.
Required ordering keys:
time_bucket
event_priority
creation_sequence
Event ordering must never depend on:
Python dictionary order
system clock
thread timing
________________________________________
8. Kernel Independence Rule
The kernel must remain independent of:
business policies
UI logic
economic models
pricing models
Kernel modules must not contain:
pricing logic
profit calculations
scenario-specific rules
These belong in higher layers.
________________________________________
9. Layer Separation Rule
WOM architecture consists of layers:
Application Layer
Decision Layer
Economic Layer
Kernel Layer
Dependency direction must always be:
Application → Decision → Economic → Kernel
Reverse dependencies are forbidden.
________________________________________
10. Event Immutability Rule
Flow events must be treated as immutable.
Preferred structure:
@dataclass(frozen=True)
Events should never be modified in-place.
Instead:
create new event
This supports reproducibility and event sourcing.
________________________________________
11. Artifact Transparency Rule
Every decision must leave an artifact trail.
Required artifacts:
flow_events.json
state_view.json
trust_events.json
operator_candidates.json
operator_spec.json
evaluation_results.json
Artifacts enable:
debugging
AI analysis
decision traceability
________________________________________
12. Time Consistency Rule
The system must use a canonical time representation.
Example:
YYYYWW
Time conversions must be centralized.
Forbidden patterns:
mix weekly and monthly logic inside kernel
________________________________________
13. Kernel Modification Policy
Kernel code must be modified only when:
a correctness bug exists
a performance improvement is required
a new event type is introduced
Kernel must NOT be modified for:
business experiments
scenario variations
policy changes
Those belong in higher layers.
________________________________________
14. AI Agent Safety Rule
AI coding agents must:
1.	Read these files before coding
ARCHITECTURE.md
INTERFACE_SPEC.md
KERNEL_RULES.md
2.	Respect module responsibilities.
3.	Avoid refactoring kernel structure unless explicitly instructed.
4.	Prefer minimal code changes.
________________________________________
15. Examples
Correct approach
Resolver decides to increase production.
Operator → create FlowEvent(production)
Simulation updates inventory.
flow_engine → derive new StateView
________________________________________
Incorrect approach
Resolver updates inventory directly.
state.inventory[node] += 100
This violates kernel rules.
________________________________________
16. Philosophy
The WOM kernel should behave like physics of an economic world.
Events = physical reality
State = observation
Decision = policy
Kernel rules ensure that this physical model remains stable.
________________________________________
17. Summary
The WOM kernel must guarantee:
Flow-first architecture
Event sourcing
Deterministic execution
Layer separation
Explainable decisions
Maintaining these principles ensures that WOM can evolve toward:
AI-assisted planning
economic simulation
AI management operating systems
without breaking the core architecture.
________________________________________
Final Note
If a change conflicts with these rules:
do not change the kernel.
Instead extend the system through:
plugins
policies
scenario configuration
decision layer
The kernel must remain stable.
