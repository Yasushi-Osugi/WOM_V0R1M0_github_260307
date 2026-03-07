# Codex Development Tasks

This document lists recommended development directions for WOM.

---

# Current Focus Areas

1. Stabilize PSI planning engine
2. Improve plugin visibility
3. Clarify active execution paths
4. Improve scenario reproducibility
5. Reduce legacy file confusion

---

# Immediate Tasks

Possible tasks for Codex contributors:

- identify active planning engine files
- simplify planning pipeline structure
- improve plugin documentation
- add lightweight unit tests
- add scenario validation checks

---

# Medium-Term Tasks

- unify planning entry point
- clean up OLD/BK duplicate files
- create a standard scenario definition format
- improve diagnostics reporting
- modularize GUI components

---

# Long-Term Vision

WOM aims to become:

A **planning OS for global supply chain simulation**.

Potential capabilities include:

- multi-country economic simulation
- geopolitical risk scenario planning
- supply chain digital twin modeling
- LLM-assisted planning dialogue

---

# Development Rules

When working on this repository:

1. Prefer minimal, well-scoped changes.
2. Avoid editing legacy files unless necessary.
3. Preserve compatibility with existing scenarios.
4. Document architectural changes.
5. Keep planning logic explainable.

---

# Codex Editing Guidelines

Before editing code:

1. Identify the active execution path.
2. Verify the file is not an OLD/BK version.
3. Explain the reason for the modification.
4. Avoid unnecessary structural changes.

---

# Suggested Next Refactoring

- define a single canonical run entry
- separate experimental code
- improve architecture documentation
- strengthen plugin lifecycle definitions
