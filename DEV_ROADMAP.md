# WOM Development Roadmap

This document defines the long-term development roadmap for WOM (Weekly Operation Model).

The purpose of this roadmap is to guide the evolution of WOM toward a scalable planning platform capable of supporting global supply chain simulation and AI-assisted planning.

This roadmap is referenced by:

- AI developers
- human contributors
- the AI meeting protocol
- Codex development tasks

---

# 1 Development Philosophy

The WOM project follows several core principles.

Keep the system:

- simple
- modular
- explainable
- reproducible

The most important rule:

**The planning engine must remain transparent and understandable.**

The engine is the intellectual core of the system.

---

# 2 Development Stages

WOM development is organized into several stages.

Stage 1: Planning Engine Stabilization  
Stage 2: Plugin Architecture Expansion  
Stage 3: Scenario Library Expansion  
Stage 4: Excel Interaction Layer  
Stage 5: AI Planning Dialogue  
Stage 6: Economic Simulation Platform

Each stage builds upon the previous one.

---

# 3 Stage 1: Planning Engine Stabilization

Objective:

Stabilize the PSI planning engine and ensure reliable scenario execution.

Key tasks:

- refine planning pipeline
- improve constraint handling
- ensure deterministic outputs
- stabilize scenario execution

Primary modules:


pysi/plan/
pysi/core/


Validation:


python -m tools.run_phone_v0
python -m tools.run_pharma_v0


Success criteria:

- consistent outputs
- reproducible runs
- stable planning pipeline

---

# 4 Stage 2: Plugin Architecture Expansion

Objective:

Enable flexible rule-based planning extensions.

Key tasks:

- standardize plugin interfaces
- introduce allocation plugins
- support capacity-aware planning
- support demand prioritization

Primary modules:


pysi/plugins/


Example plugins:

- capacity_allocator
- demand_priority
- inventory_buffer_control

Success criteria:

- plugins can be added without modifying core engine
- planning behavior can be extended through plugins

---

# 5 Stage 3: Scenario Library Expansion

Objective:

Create a diverse set of reproducible planning scenarios.

Primary areas:


data/
examples/
pysi/scenario/


Example scenarios:

- phone supply chain
- pharmaceutical cold chain
- rice supply chain
- disruption scenarios
- geopolitical supply shocks

Success criteria:

- scenarios demonstrate different planning challenges
- scenarios remain reproducible across versions

---

# 6 Stage 4: Excel Interaction Layer

Objective:

Provide a practical interaction layer for business users.

Responsibilities led by:


AI Excel UX Designer


Key elements:

- Excel scenario templates
- Excel output dashboards
- PSI visualization graphs
- scenario comparison sheets

Data flow:


Excel → WOM Engine → Excel


Success criteria:

- users can run planning scenarios using Excel templates
- results are visible through Excel graphs

---

# 7 Stage 5: AI Planning Dialogue

Objective:

Enable LLM-assisted planning discussions.

Components:

- diagnostic analysis
- planning recommendations
- operator suggestions
- scenario comparison

Typical interaction:


user question
→ LLM diagnosis
→ planning operator suggestion
→ scenario re-execution


Success criteria:

- LLM can explain planning outcomes
- LLM can propose scenario improvements

---

# 8 Stage 6: Economic Simulation Platform

Long-term objective:

Extend WOM from supply chain planning to economic simulation.

Potential extensions:

- multi-industry models
- national supply networks
- macroeconomic demand scenarios
- geopolitical disruptions

Possible applications:

- global supply chain resilience analysis
- economic policy simulation
- long-term infrastructure planning

---

# 9 Short-Term Development Priorities

Current priorities should focus on:

1 planning engine stability  
2 plugin architecture  
3 scenario reproducibility  

Avoid premature expansion of:

- complex GUIs
- distributed infrastructure
- unnecessary abstractions

---

# 10 Role Alignment

Development tasks should follow AI roles defined in:


AI_TEAM.md


Example mapping:

| Development Area | Responsible Role |
|------------------|------------------|
planning engine | AI Engine Developer |
plugins | AI Plugin Developer |
scenarios | AI Scenario Designer |
Excel interaction | AI Excel UX Designer |
validation | AI Tester |
architecture | AI Architect |

---

# 11 Integration with AI Meeting Protocol

Major roadmap changes must be discussed using:


AI_MEETING_PROTOCOL.md


Typical triggers:

- architecture redesign
- major subsystem introduction
- planning algorithm changes

---

# 12 Long-Term Vision

The WOM platform aims to become a **planning OS** capable of supporting:

- supply chain planning
- scenario simulation
- AI-assisted planning dialogue

The roadmap ensures that development remains structured as system complexity grows.
