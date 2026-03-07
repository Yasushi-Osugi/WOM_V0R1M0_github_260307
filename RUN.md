# RUN Guide

This document explains how to execute WOM for development and testing.

---

# Basic Execution

Run the main entry point:


python main.py


---

# Example Scenario Runs

Phone supply chain demo:


python -m tools.run_phone_v0


Pharmaceutical cold chain demo:


python -m tools.run_pharma_v0


Rice supply chain demo:


python -m tools.run_rice_v0


---

# Typical Development Workflow

1. Modify planning logic in:


pysi/plan/
pysi/core/


2. Run a small scenario:


python -m tools.run_phone_v0


3. Check outputs in:


out/


4. If needed, run GUI visualization.

---

# Scenario Data

Scenario input files are located under:


data/


Example scenario folders:


data/pharma_cold_v0
data/phone_v0
data/rice_v0


---

# Debugging Strategy

When debugging planning logic:

Use the smallest scenario possible.

Recommended order:

1. phone scenario
2. rice scenario
3. pharma scenario

This keeps execution fast.

---

# Output Data

Simulation outputs are written to:


out/
plan_data/


These directories are not tracked by Git.

---

# Notes for Developers

Before modifying core logic:

- confirm the scenario runner works
- avoid modifying historical files
- test changes on a minimal scenario first
