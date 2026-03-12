# WOM Architecture

This document describes the architecture of WOM (Weekly Operation Model).

WOM is designed as a modular planning platform capable of supporting:

- global supply chain planning
- scenario simulation
- AI-assisted planning
- future economic system modeling

The architecture follows the principles defined in:

- WOM_DESIGN_PRINCIPLES.md
- DEV_ROADMAP.md
- AI_TEAM.md
- AI_MEETING_PROTOCOL.md

---

# 1 Architectural Overview

The WOM system consists of five major layers.

Scenario Layer  
Network Model Layer  
Planning Kernel  
Plugin System  
Interaction Layer  

Overall flow:

Scenario  
↓  
Network Construction  
↓  
Planning Kernel  
↓  
Plugin Stages  
↓  
Result Generation  
↓  
Interaction Layer  

---

# 2 Scenario Layer

The scenario layer defines the planning context.

Responsibilities:

- demand input
- supply configuration
- network structure
- scenario parameters

Primary locations:

data/  
examples/  
pysi/scenario/

Scenarios must be:

- reproducible
- version-controlled
- deterministic

Scenarios are used for:

- development testing
- regression validation
- AI diagnostics

---

# 3 Network Model Layer

The network layer constructs the supply chain model.

Nodes represent:

- factories
- distribution centers
- markets

Edges represent:

- transport flows
- supply relationships

Primary modules:

pysi/network/

Responsibilities:

- node creation
- edge creation
- capacity definitions
- lead time modeling

The network model forms the structural foundation for planning.

---

# 4 Planning Kernel

The planning kernel performs the PSI planning calculation.

Unlike a simple pipeline, the WOM kernel operates as a **closed-loop planning engine**.

Kernel stages include:

Demand Generation  
Flow Simulation  
State Derivation  
Trust Event Detection  
Evaluation  
Resolver Decision  
Operator Application  

Kernel execution loop:

Network Model  
↓  
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
Resolver Decision  
↓  
Operator Application  
↓  
Re-simulation  

Primary modules:

pysi/plan/  
pysi/core/

The kernel must remain:

- deterministic
- explainable
- modular

---

# 5 Plugin System

The plugin system enables extensible planning behavior.

Plugins modify planning behavior without changing core engine logic.

Plugin directory:

pysi/plugins/

Example plugins:

- capacity_allocator
- demand_priority
- inventory_buffer_control

Standard plugin interface:


def apply_plugin(state, context):
return modified_state


Plugin execution points are defined within the planning kernel.

---

# 6 Interaction Layer

The interaction layer provides user access to the planning system.

Two interaction modes exist.

Developer interaction:

- matplotlib visualization
- debug tools

Business interaction:

- Excel templates
- Excel dashboards
- scenario comparison sheets

Preferred interaction model:

Excel → WOM Engine → Excel

This provides a practical interface for business users.

---

# 7 Result Generation

Planning results include:

- PSI time series
- inventory levels
- capacity utilization
- service level metrics

Results are used for:

- scenario evaluation
- visualization
- AI diagnostic analysis

---

# 8 Testing and Validation

Planning results must be validated through reproducible scenarios.

Example executions:

python -m tools.run_phone_v0  
python -m tools.run_pharma_v0  

Validation checks include:

- execution success
- reproducibility
- output stability

Regression scenarios must be maintained.

---

# 9 Integration with AI Development Model

The WOM architecture integrates with the AI development framework.

Development roles:

- AI Architect
- AI Engine Developer
- AI Plugin Developer
- AI Scenario Designer
- AI Excel UX Designer
- AI Tester

Architectural decisions are governed by:

AI_MEETING_PROTOCOL.md

System evolution follows:

DEV_ROADMAP.md

---

# 10 Architectural Principles

The architecture must follow these rules:

Planning kernel clarity is prioritized over feature complexity.

Plugins must extend behavior without modifying core engine logic.

Scenarios must remain reproducible.

User interaction must not introduce architectural coupling.

---

# 11 Long-Term Evolution

The WOM architecture will evolve toward a planning platform capable of supporting:

- global supply chain simulation
- AI planning dialogue
- economic network modeling

The architecture must remain stable while enabling gradual expansion.