WOM Kernel v1.1 – Next Action TODO

Project: Weekly Operation Model (WOM)
Component: WOM Planning Kernel
Current Version: v1
Next Target: v1.1
Date: March 2026

1. Purpose of Kernel v1.1

The objective of WOM Kernel v1.1 is to strengthen the semantic foundation of the WOM execution model while preserving the minimal and deterministic architecture established in Kernel v1.

Kernel v1 successfully demonstrated that:

Economic planning can be executed as an event-sourced simulation

The execution loop can be deterministic

Planning can operate as a self-correcting control loop

Kernel v1.1 focuses on completing the minimal economic event semantics and strengthening runtime trust detection, enabling the kernel to serve as a stable foundation for the upcoming Planning Engine layer.

Kernel v1.1 is therefore not a feature expansion, but a semantic stabilization step.

2. Design Philosophy

Kernel development follows the principles defined in the WOM Development Roadmap:

Simplicity first

Deterministic execution

Event-sourced architecture

Explainable planning behavior

Reproducible simulation runs

Kernel v1.1 must not introduce unnecessary complexity such as:

complex UI layers

distributed execution

heavy optimization frameworks

premature AI integration

These capabilities belong to the Planning Engine layer, not the Kernel.

3. Kernel vs Planning Engine Responsibilities
WOM Kernel Responsibilities

The Kernel defines the execution semantics of economic flows.

Responsibilities include:

Event ordering

Flow simulation

State derivation

Trust event detection

Operator application

Deterministic re-simulation loop

The Kernel behaves similarly to a runtime engine.

Planning Engine Responsibilities

The Planning Engine will operate above the Kernel and implement planning intelligence.

Responsibilities include:

scenario management

plugin execution

operator candidate generation

policy control

planning heuristics

optimization strategies

user interaction

Conceptually:

Planning Engine
      ↑
WOM Kernel

Kernel = economic execution model
Planning Engine = planning intelligence

4. Kernel v1.1 Target Improvements

Kernel v1.1 focuses on four core improvements.

4.1 Explicit Sale Event
Current Situation

Demand processing currently reduces inventory directly:

DemandEvent → inventory reduction

This results in an implicit sale process.

Improvement

Introduce an explicit event:

DemandEvent
     ↓
SaleEvent
     ↓
Inventory change

Possible structure:

DemandEvent
   ↓
SaleEvent
   ↓
UnmetDemandEvent (optional)
Benefits

Complete economic event chain

Production
Shipment
Arrival
Sale

Stronger event sourcing semantics

Better explainability

Easier financial modeling in later stages

4.2 Backlog / Unmet Demand Event Semantics
Current Situation

Backlog is stored as a derived state:

backlog_by_market_product_time

However it is not represented as an explicit event.

Improvement

Introduce an explicit record for unmet demand:

Possible options:

UnmetDemandEvent
BacklogEvent
Benefits

Clearer demand fulfillment history

Enables service level explanation

Supports later revenue-loss modeling

Improves auditability of planning results

4.3 Runtime Integrity Trust Events

Kernel v1 currently detects:

stockout risk

capacity overload

However execution integrity violations are not yet monitored.

New Trust Events

Kernel v1.1 should detect:

E_NEGATIVE_INVENTORY

Inventory becomes negative.

E_INVALID_SHIPMENT

Shipment exceeds available inventory.

E_INVALID_SALE

Sale event executed without available inventory.

Benefits

Kernel becomes a runtime validator

Planning errors become observable

System robustness improves

Supports debugging and validation

4.4 Improved Iteration History

Kernel v1 already records iteration history.

Kernel v1.1 should extend this with clearer traceability.

Each iteration should include:

iteration
state
trust_events
evaluation
selected_operator

Optional additional metadata:

score_delta
backlog_change
inventory_change
Benefits

Planning runs become explainable

Easier debugging

Enables future visualization tools

Supports regression testing

5. Optional Support Feature
Kernel Console / Observer

Kernel behavior is currently mostly silent.

A lightweight Kernel Observer may be introduced outside the kernel core.

Possible outputs:

trust event summary

operator decisions

iteration summaries

evaluation metrics

Example:

Iteration 1
Stockout detected: market_TYO
Operator applied: add_production(factory_A)

Iteration 2
Backlog reduced
Capacity overload detected

This observer layer should remain separate from kernel execution logic.

6. What Kernel v1.1 Must NOT Do

The following capabilities belong to the Planning Engine, not the Kernel.

Kernel v1.1 must NOT implement:

complex operator search

multi-scenario branching

optimization algorithms

distributed planning nodes

deep AI integration

plugin execution frameworks

These will be implemented in later stages.

7. Relationship to Development Roadmap

Kernel v1.1 directly supports:

Stage 1 – Planning Engine Stabilization

Key roadmap requirements:

reproducible runs

consistent outputs

stable simulation pipeline

Kernel v1.1 provides the semantic stability required for the Planning Engine.

8. Development Priority

Recommended implementation order:

1️⃣ Explicit Sale Event
2️⃣ Unmet Demand / Backlog Event
3️⃣ Runtime Integrity Trust Events
4️⃣ Improved Iteration History
5️⃣ Optional Kernel Observer

9. Expected Result

After Kernel v1.1 is complete, WOM will have:

a deterministic economic simulation kernel

a complete minimal economic event chain

runtime integrity monitoring

traceable planning iterations

This provides a solid foundation for the next stage:

WOM Kernel v1
        ↓
WOM Kernel v1.1
        ↓
Planning Engine v0
        ↓
Plugin Architecture
        ↓
WOM Economic Operating System
10. Summary

Kernel v1 proved that the WOM architecture can run as executable code.

Kernel v1.1 will ensure that the economic execution semantics are complete, observable, and robust, allowing the Planning Engine to evolve on top of a stable foundation.

The kernel remains intentionally minimal, deterministic, and explainable.