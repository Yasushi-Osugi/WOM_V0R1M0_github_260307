# WOM System Design Index

## Overview

This document provides a **navigation map of the WOM system design documents**.

The WOM repository contains several architectural documents that describe different aspects of the system:

- conceptual architecture
- planning engine structure
- runtime execution model
- core data model
- development workflow
- AI-assisted development environment

This index explains how these documents relate to each other and how they should be used.

The goal is to allow:

- developers
- AI agents
- researchers

to quickly understand the structure of the WOM planning system.

---

# 1 WOM Architecture Stack

The WOM system can be understood as a layered architecture.


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


The documents in this repository correspond to different layers of this stack.

---

# 2 Core Architecture Documents

These documents define the conceptual architecture of WOM.

## ARCHITECTURE.md

The main architecture document.

Defines:

- overall WOM architecture
- planning kernel concept
- modular structure
- design principles

Recommended reading order:

1. Read this document first.

---

## WOM_META_ARCHITECTURE.md

Describes the **meta-level architecture** of WOM.

Focus areas:

- architecture layers
- AI research lab model
- relationship between theory and implementation
- economic operating system concept

This document explains **why WOM exists and what it aims to become**.

---

# 3 Planning Engine Architecture

These documents explain the **internal structure of the planning engine**.

## WOM_PLANNING_ENGINE_ARCHITECTURE.md

Defines the core planning engine.

Topics:

- demand generation
- flow simulation
- evaluation
- resolver search

Key idea:

WOM operates as a **closed-loop planning engine**.

---

## WOM_EXECUTION_MODEL.md

Defines the runtime behavior of the planning engine.

Topics:

- planning cycle
- event processing
- simulation loop
- operator application
- termination conditions

This document explains **how WOM actually runs**.

---

# 4 Data Model

## WOM_DATA_MODEL.md

Defines the core data structures used by WOM.

Key entities:

- Lot
- Event
- Flow
- State
- TrustEvent
- Operator
- EvaluationResult

This document ensures **consistent data structures across the system**.

---

# 5 Interface and Kernel Rules

## INTERFACE_SPEC.md

Defines module interfaces.

Main modules:

- demand_model
- flow_engine
- evaluation
- resolver

Purpose:

- maintain modular boundaries
- ensure compatibility across implementations

---

## KERNEL_RULES.md

Defines constraints for the WOM kernel.

Examples:

- kernel must remain deterministic
- state must be derived from events
- operators must modify flows, not state

Purpose:

Prevent architectural drift.

---

# 6 Development Workflow

## DEV_ROADMAP.md

Defines the development priorities of the WOM project.

Topics:

- short-term goals
- medium-term architecture improvements
- long-term vision

This document guides development decisions.

---

## AGENTS.md

Defines AI development rules.

Topics:

- AI roles
- code generation guidelines
- repository conventions
- safe modification practices

This document allows AI agents to collaborate effectively.

---

# 7 Repository Orientation

## ARCHITECTURE_MAP.md

A simplified architecture map for quick understanding.

Purpose:

- show key components
- explain module relationships

Recommended for new contributors.

---

## REPO_BOOTSTRAP.md

Provides onboarding guidance.

Topics:

- repository structure
- first steps for developers
- reading order of documents

This is the **entry point for new contributors**.

---

# 8 Recommended Reading Order

For new readers:


REPO_BOOTSTRAP.md

ARCHITECTURE_MAP.md

ARCHITECTURE.md

WOM_META_ARCHITECTURE.md

WOM_PLANNING_ENGINE_ARCHITECTURE.md

WOM_EXECUTION_MODEL.md

WOM_DATA_MODEL.md

INTERFACE_SPEC.md

KERNEL_RULES.md


For developers implementing features:


ARCHITECTURE.md
→ INTERFACE_SPEC.md
→ WOM_DATA_MODEL.md
→ WOM_EXECUTION_MODEL.md


---

# 9 Conceptual Summary

The WOM system integrates several layers of abstraction.


CPU demand model
↓
Supply chain flow simulation
↓
State derivation
↓
Evaluation
↓
Resolver decision search
↓
Operator application
↓
Re-simulation


This architecture transforms WOM into:

- a supply chain planning engine
- a simulation-based decision system
- a research platform for economic planning models

---

# 10 Future Documents

Additional documents may be added in the future.

Examples:

- WOM_FIELD_THEORY.md
- WOM_KNOWLEDGE_GRAPH.md
- WOM_GLOBAL_ECONOMIC_MODEL.md
- WOM_AI_NATION_MODEL.md

These documents may expand WOM beyond supply chain planning into broader economic simulation.

---

# 11 Summary

The WOM repository combines:

architecture design  
planning engine implementation  
economic modeling  
AI-assisted development  

into a unified framework.

The documents referenced in this index collectively define the **WOM planning system**.

---

# End of Document