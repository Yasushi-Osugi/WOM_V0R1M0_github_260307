# WOM Design Principles

This document defines the core design philosophy of WOM (Weekly Operation Model).

These principles guide all architectural and implementation decisions across the WOM system.

They are referenced by:

- ARCHITECTURE.md
- DEV_ROADMAP.md
- AI_MEETING_PROTOCOL.md
- AI_TEAM.md

The goal is to ensure that WOM evolves consistently as system complexity grows.

---

# 1 Core Vision

WOM aims to become a **planning OS** capable of supporting:

- global supply chain planning
- scenario simulation
- AI-assisted planning dialogue
- economic system modeling

The system must remain transparent, explainable, and extensible.

---

# 2 Planning Engine First

The **planning engine is the core intellectual asset** of WOM.

All development decisions must prioritize:

- engine clarity
- algorithm transparency
- reproducible planning outcomes

User interfaces and auxiliary tools must not complicate the planning engine.

---

# 3 Network-Based Planning

WOM models supply chains as **network systems**.

Nodes represent:

- factories
- distribution centers
- markets

Edges represent:

- transportation flows
- supply relationships

Planning must always operate on a **network representation** rather than isolated tables.

---

# 4 Lot and Flow Based Planning

Planning must be based on:

- lot-level quantities
- physical product flows
- time-series PSI logic

Key variables:


Production / Purchase
Shipment / Sales
Inventory


Planning algorithms must maintain the **physical consistency of flows**.

---

# 5 Explainable Planning

All planning outcomes must be explainable.

The system should avoid:

- opaque algorithms
- hidden optimization behavior
- non-transparent heuristics

Users must be able to understand:

- why a decision was made
- what constraints influenced it
- how flows propagate across the network

Explainability is a fundamental requirement for AI-assisted planning.

---

# 6 Modular Architecture

The WOM system must remain modular.

Major components:


planning engine
plugin system
scenario system
interaction layer


Each component should evolve independently.

The planning engine must remain isolated from UI and external integrations.

---

# 7 Plugin-Based Extension

Planning behavior must be extendable through plugins.

Examples:

- allocation rules
- prioritization rules
- capacity management
- disruption response

Plugins must be able to modify planning behavior **without modifying core engine logic**.

---

# 8 Scenario Reproducibility

All scenarios must be reproducible.

Requirements:

- deterministic execution
- fixed input datasets
- version-controlled scenarios

This enables:

- planning comparison
- regression testing
- AI-assisted scenario analysis

---

# 9 Human + AI Collaboration

WOM is designed for **collaborative planning between humans and AI systems**.

The system should support:

- human strategic thinking
- AI diagnostic analysis
- AI planning suggestions

AI must assist human planners rather than replace decision-making authority.

---

# 10 Practical Interaction Layer

User interaction should prioritize practicality.

For business environments, preferred interaction tools include:


Excel templates
scenario dashboards
visualization sheets


Complex GUI frameworks should not be introduced unless clearly necessary.

The planning engine must remain independent from any specific UI technology.

---

# 11 Simplicity Over Complexity

When design alternatives exist, choose the solution that keeps the system:

- simpler
- easier to understand
- easier to maintain

Avoid:

- premature optimization
- unnecessary abstraction
- complex frameworks

The WOM system should remain **conceptually simple even as it grows**.

---

# 12 Long-Term Evolution

WOM development progresses through stages:

1 Planning engine stabilization  
2 Plugin architecture expansion  
3 Scenario library growth  
4 Excel interaction layer  
5 AI planning dialogue  
6 Economic simulation platform

The system evolves gradually toward a **planning OS for economic systems**.

---

# Guiding Principle

When facing design choices, always ask:

**Does this change make the planning engine clearer, simpler, and more explainable?**

If not, reconsider the design.
