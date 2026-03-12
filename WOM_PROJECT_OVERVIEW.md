# WOM Project Overview

## What is WOM?

WOM (Weekly Operation Model) is a planning framework designed to model and simulate economic activity through supply chain flows.

At its core, WOM is a **planning kernel** that integrates:

- demand modeling
- supply chain flow simulation
- evaluation of system performance
- decision search and corrective actions

The project explores how **complex economic systems can be represented as flow-based planning models**.

---

# Core Idea

Traditional planning systems focus on static planning tables.

WOM instead models economic activity as **flows of supply through a network over time**.

The core principle is:


Flow/Event = source of truth
State = derived view


This means that:

- production
- shipment
- arrival
- sale

are recorded as **events**, and planning states such as inventory are **derived from those events**.

---

# Core Planning Loop

The WOM engine operates as a closed-loop planning system.


Demand
↓
Flow Simulation
↓
State Derivation
↓
Evaluation
↓
Resolver Decision
↓
Operator Application
↓
Re-Simulation


This loop allows WOM to move beyond simple planning tools and function as a **simulation-based decision engine**.

---

# Key Concepts

The WOM planning model is built around six core concepts.


CPU
Price
Lot
Flow
Resolver
Evaluation


### CPU (Common Planning Unit)

Represents the fundamental unit of demand.

Examples include household consumption units or market demand groups.

---

### Price

Acts as the market signal that influences demand and supply behavior.

---

### Lot

The basic supply object handled by the planning engine.

Lots represent production batches, shipment units, or supply allocations.

---

### Flow

Flows represent the movement of lots through the supply network.

Examples include production flows, shipment flows, and sales flows.

---

### Resolver

The resolver is the decision engine of the system.

It detects issues in the system and proposes corrective operators.

---

### Evaluation

Evaluation functions measure system performance.

Typical metrics include:

- profit
- service level
- inventory stability
- risk exposure

---

# Architecture Overview

The WOM system is organized into several layers.


Human Objectives
↓
AI Research Design
↓
Software Architecture
↓
Planning Kernel
↓
Mathematical Model
↓
Economic System Model


This layered structure allows WOM to serve both as:

- a supply chain planning engine
- a research platform for economic planning models

---

# Planning Engine Modules

The core planning engine is composed of four modules.


demand_model.py
flow_engine.py
evaluation.py
resolver.py


Each module handles a specific responsibility.

| Module | Responsibility |
|------|------|
| demand_model | demand generation |
| flow_engine | supply chain simulation |
| evaluation | system scoring |
| resolver | decision search |

---

# Data Model

The WOM system uses a flow-oriented data model.

Key entities include:

- Lot
- Event
- Flow
- State
- TrustEvent
- Operator

Events represent system truth, while states are derived from event streams.

---

# AI-Assisted Development

WOM is designed to be developed using **AI-assisted workflows**.

The repository includes documents that guide collaboration between:

- human architects
- AI design agents
- code generation systems

Examples include:

- AGENTS.md
- DEV_ROADMAP.md
- INTERFACE_SPEC.md

---

# Why WOM Exists

The WOM project explores a key question:

Can economic planning systems be designed as **simulation engines with explicit decision loops**?

If successful, this approach may provide a new way to model:

- supply chain planning
- resource allocation
- economic system dynamics

---

# Current Scope

The current implementation focuses on:

- weekly supply chain planning
- event-based flow simulation
- explainable planning artifacts
- deterministic simulation behavior

Future work may explore broader economic modeling.

---

# Repository Structure

Key documents in the repository include:


ARCHITECTURE.md
WOM_META_ARCHITECTURE.md
WOM_PLANNING_ENGINE_ARCHITECTURE.md
WOM_EXECUTION_MODEL.md
WOM_DATA_MODEL.md
WOM_SYSTEM_DESIGN_INDEX.md


These documents collectively describe the design of the WOM planning system.

---

# Project Status

WOM is an experimental research and development project.

The current focus is on:

- stabilizing the planning engine
- improving modular architecture
- enabling AI-assisted development workflows

---

# Summary

WOM combines:

- flow-based supply chain simulation
- deterministic planning engines
- decision search mechanisms
- structured planning artifacts

into a unified planning framework.

The project aims to explore how **planning systems can evolve from static planning tools into dynamic simulation-driven decision engines**.

---

# End of Document