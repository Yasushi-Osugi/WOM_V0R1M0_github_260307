# WOM AI Research Lab Model

This document defines the AI collaboration structure used to develop WOM.

The WOM repository is designed to support **AI-assisted collaborative development**, where multiple AI roles contribute to different aspects of the system.

The goal is to enable a structured workflow where AI and human developers cooperate efficiently.

---

# AI Development Roles

The WOM AI team consists of the following roles.

## 1. AI Architect

Responsibilities:

- Maintain overall system architecture
- Update ARCHITECTURE.md when design changes
- Define module boundaries
- Review major structural changes

Primary areas:


ARCHITECTURE.md
repo structure
pysi/core
pysi/network


Key decisions:

- planning engine structure
- plugin architecture
- module separation
- system evolution strategy

---

## 2. AI Engine Developer

Responsibilities:

- Improve the PSI planning engine
- Implement lot-flow logic
- Maintain planning pipeline

Primary areas:


pysi/plan/
pysi/core/


Typical work:

- planning algorithm improvements
- constraint handling
- performance improvements

---

## 3. AI Plugin Developer

Responsibilities:

- Implement and extend planning plugins
- Add rule-based planning behaviors

Primary areas:


pysi/plugins/


Typical work:

- capacity allocation
- demand prioritization
- diagnostics
- rule extensions

---

## 4. AI Scenario Designer

Responsibilities:

- Create reproducible planning scenarios
- Maintain scenario datasets

Primary areas:


data/
pysi/scenario/
examples/


Typical work:

- baseline scenarios
- demand shock scenarios
- geopolitical risk scenarios
- educational examples

---

## 5. AI Tester

Responsibilities:

- Verify scenario execution
- Detect regressions
- Validate outputs

Primary areas:


tools/
RUN.md


Typical work:

- regression checks
- scenario validation
- output consistency checks

---

## 6. AI Excel UX Designer

Responsibilities:

- Design Excel interaction layer
- Define user-facing visualization

Primary areas:


Excel templates
Python ↔ Excel interface
Graph templates


Typical work:

- Excel scenario templates
- PSI visualization graphs
- scenario comparison sheets
- planning dashboards

This role focuses on **business usability**, not graphical frameworks.

---

# AI Coordination Model

The WOM development process follows a collaborative model where different AI roles coordinate their contributions.

Typical flow:


Scenario Designer → Engine Developer → Plugin Developer → Tester → Architect


UX improvements are coordinated with:


Excel UX Designer


---

# AI Development Process

The recommended development workflow is:

### Step 1: Identify development task

Tasks originate from:


TODO_Codex.md
bug reports
performance improvements
new scenario needs


---

### Step 2: Assign AI role

Determine the responsible role.

Example:

| Task | Role |
|-----|------|
planning logic change | Engine Developer |
new plugin | Plugin Developer |
scenario creation | Scenario Designer |
visualization | Excel UX Designer |

---

### Step 3: Implement minimal change

The responsible AI role:

- identifies active execution path
- proposes smallest safe modification
- preserves existing scenarios

---

### Step 4: Execute test scenario

Use:


RUN.md


Example:


python -m tools.run_phone_v0


Verify:

- execution success
- output consistency
- no regression

---

### Step 5: Code review

All non-trivial changes require review by:


AI Architect


The review verifies:

- architecture consistency
- module boundaries
- maintainability

---

# AI Code Review Rules

When reviewing code:

1. Confirm the active execution path.
2. Ensure legacy files are not modified.
3. Prefer minimal patches.
4. Confirm scenarios remain reproducible.
5. Ensure architecture remains consistent.

---

# AI Meeting Model

Regular coordination occurs through structured discussions.

Recommended cadence:

### Weekly Architecture Meeting

Participants:


AI Architect
AI Engine Developer
AI Plugin Developer


Agenda:

- architecture evolution
- engine improvements
- plugin integration

---

### Scenario Review Meeting

Participants:


AI Scenario Designer
AI Tester


Agenda:

- scenario coverage
- regression tests
- dataset improvements

---

### UX Review Meeting

Participants:


AI Excel UX Designer
AI Architect


Agenda:

- Excel interaction design
- visualization improvements
- business usability

---

# Long-Term Vision

The WOM AI Research Lab aims to create a planning platform capable of:

- global supply chain simulation
- economic scenario analysis
- planning dialogue with LLM systems

Ultimately evolving toward a **planning OS for economic systems**.

---

# Guiding Principle

The most important rule:

**Keep the planning engine simple, transparent, and explainable.**

The engine is the core intellectual asset of WOM.
