# CODEX_DEVELOPMENT_PROTOCOL.md

This document defines the **development protocol for collaborating with Codex (AI coding agents)** in the WOM repository.

The goal is to enable **fast, safe, and reproducible AI-assisted development**.

This protocol ensures:

- architectural integrity
- deterministic behavior
- minimal code drift
- explainable development history

---

# 1. Development Philosophy

WOM development follows an **AI Research Lab model**.

Human designers define:

- architecture
- mathematical model
- planning theory

AI developers (Codex) implement:

- modules
- tests
- refactoring
- documentation

The collaboration rule is:

Human defines **what and why**  
AI implements **how**

---

# 2. Development Layers

WOM development is divided into layers.


Theory Layer
Architecture Layer
Interface Layer
Kernel Implementation
Extensions
Applications


Codex must **not modify higher layers when implementing lower layers**.

Example:

Kernel implementation must not change:

- architecture
- interface definitions
- mathematical assumptions

---

# 3. Required Reading for Codex

Before implementing code, Codex must read:

1. REPO_BOOTSTRAP.md
2. ARCHITECTURE_MAP.md
3. ARCHITECTURE.md
4. INTERFACE_SPEC.md
5. KERNEL_RULES.md
6. WOM_MINIMAL_CLASS_MODEL.md
7. WOM_EXECUTION_MODEL.md
8. CODEX_IMPLEMENT_KERNEL.md
9. CODEX_TASK_PROMPT_KERNEL_V1.md

These files define the design constraints.

---

# 4. Codex Development Workflow

Codex must follow this workflow when implementing features.


1 Read architecture
2 Confirm scope
3 Implement minimal version
4 Write tests
5 Run example
6 Commit changes
7 Explain reasoning


Codex must **not skip these steps**.

---

# 5. Pull Request Rules

Every Codex implementation must:

- remain small
- affect only the intended module
- avoid unnecessary refactoring
- preserve deterministic behavior

Pull requests must include:

- description of changes
- explanation of reasoning
- test results
- example run output

---

# 6. Kernel Protection Rules

The following files are **architectural core**.

They must **not be modified by Codex unless explicitly instructed**.


ARCHITECTURE.md
INTERFACE_SPEC.md
KERNEL_RULES.md
WOM_DATA_MODEL.md
WOM_MINIMAL_CLASS_MODEL.md


These files define the WOM planning kernel.

Changing them can break the architecture.

---

# 7. Allowed Changes

Codex is allowed to modify:


kernel implementation files
tests
demo scenarios
internal helper functions
documentation comments


Codex must **not modify repository structure** without approval.

---

# 8. Minimal Implementation Principle

Codex must follow the rule:

**Implement the smallest working version first.**

Avoid:

- premature optimization
- unnecessary abstraction
- large frameworks
- heavy dependencies

Small, clear code is preferred.

---

# 9. Determinism Requirement

WOM planning must remain deterministic.

Codex must avoid:

- hidden randomness
- unstable sorting
- implicit ordering
- time-dependent behavior

The same inputs must produce the same outputs.

---

# 10. Explainability Requirement

All planning decisions must be explainable.

Codex implementations must preserve:

- trust events
- operator selection
- evaluation metrics
- decision trace

Planning decisions must be reproducible.

---

# 11. Architecture Safety Rules

Codex must not violate these principles:

FlowEvent = source of truth

StateView = derived

Operators modify events or lots

StateView must not be mutated directly.

---

# 12. Code Style

Use:

- Python dataclasses
- type hints
- explicit function names
- readable control flow

Prefer:

clear code > clever code

---

# 13. Debugging Procedure

If something fails:

1. inspect FlowEvents
2. inspect derived StateView
3. inspect trust events
4. inspect evaluation output
5. inspect resolver decision

Debugging must follow the **planning loop order**.

---

# 14. Versioning

Each kernel change must include:


version note
behavior description
test update


Breaking changes require explicit approval.

---

# 15. AI Safety Rule

Codex must **not rewrite large parts of the system without request**.

If large changes appear necessary:

Codex must first propose the change before implementing it.

---

# 16. Human Review

Human maintainers review:

- architecture
- algorithms
- mathematical models
- kernel rules

Codex implements the agreed design.

---

# 17. Final Principle

The WOM system must evolve as:


Theory → Architecture → Interface → Kernel → Applications


Codex development must **respect this order**.

Breaking the order will produce unstable systems.

---

# Summary

The Codex development protocol ensures:

- architectural stability
- minimal kernel
- deterministic planning
- explainable decisions
- safe AI collaboration

The purpose is to allow **AI and humans to co-develop the WOM planning system efficiently and safely.**