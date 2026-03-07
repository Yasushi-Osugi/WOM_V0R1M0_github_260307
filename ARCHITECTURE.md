# WOM Architecture

## Overview

WOM (Weekly Operation Model) is a Python-based simulation and planning environment designed to model global supply chain operations.

The system focuses on **Weekly PSI planning**:

- Production / Purchase
- Ship / Sales
- Inventory

The model represents multi-layer supply chains including:

- inbound supply chain (materials → production)
- outbound supply chain (production → market)

The architecture is designed to support:

- simulation
- scenario analysis
- cost / price evaluation
- capacity constraints
- plugin-based planning extensions


---

# High-Level Architecture


WOM architecture

core planning engine
plugin system
network model
scenario system
GUI layer
I/O and persistence layer


Each layer is implemented in the `pysi` package.

---

# Core Planning Engine

Primary location:


pysi/plan/
pysi/core/


Responsibilities:

- PSI planning logic
- lot-based operations
- planning pipeline
- validation and diagnostics

Important modules:


pysi/plan/engines.py
pysi/plan/operations.py
pysi/plan/validators.py
pysi/core/pipeline.py
pysi/core/wom_pipeline.py


This layer contains the **main business logic of WOM**.

Changes to planning behaviour should generally occur here.

---

# Plugin System

Primary location:


pysi/plugins/
pysi/core/plugin_loader.py


Purpose:

Extend planning logic without modifying the core engine.

Examples of plugin functionality:

- capacity allocation
- demand allocation
- urgency handling
- diagnostics
- logging

Plugin structure:


pysi/plugins/<plugin_name>/plugin.py


Many plugin folders also contain:


plugin_OLD.py
plugin_BKxxxx.py


These are historical versions and **should normally not be modified**.

---

# Network Model

Primary location:


pysi/network/


Purpose:

Represent the supply chain structure.

Concepts:

- nodes
- edges
- supply relationships
- tree structures

Important files:


node_base.py
tree.py
network_factory.py


The network layer defines how products and materials flow through the supply chain.

---

# Scenario System

Primary location:


pysi/scenario/
data/
examples/


Purpose:

Define planning scenarios including:

- demand patterns
- capacity
- supply structure
- geopolitical risk
- baseline vs future scenarios

Scenario files include:


JSON scenario definitions
CSV data inputs


Example datasets:


data/pharma_cold_v0
data/phone_v0
data/rice_v0


---

# GUI Layer

Primary location:


pysi/gui/
pysi/app/


Purpose:

Provide interactive visualization and scenario control.

Key components:


cockpit_tk.py
world_map_view.py
network_viewer


GUI functionality is intentionally separated from planning logic.

---

# I/O and Persistence Layer

Primary location:


pysi/io/
pysi/io_adapters/
pysi/db/


Responsibilities:

- CSV loading
- SQL integration
- scenario persistence
- PSI state storage

Example modules:


psi_state_io.py
sql_bridge.py
csv_adapter.py
sqlite.py


---

# Repository Entry Points

Primary execution entry points include:


main.py
pysi/app/entry_csv.py
pysi/app/entry_gui.py
pysi/app/entry_sql.py


Developer utilities exist under:


tools/


Example runner scripts:


run_phone_v0.py
run_pharma_v0.py
run_rice_v0.py


---

# Generated Data (Not Source Code)

The following directories contain runtime outputs and should not be edited:


out/
plan_data/


These are ignored by `.gitignore`.

---

# Development Guidelines

When modifying the code:

Prefer editing:


pysi/plan/
pysi/core/
pysi/network/
pysi/plugins/*/plugin.py


Avoid editing historical files:


*_OLD.py
_BKxxxx.py
Untitled.py


Unless explicitly investigating past implementations.

---

# Design Principles

1. Planning logic should remain independent of GUI code.
2. Storage adapters should remain separate from planning logic.
3. Plugins should extend behaviour rather than modify core code.
4. Scenario execution should remain reproducible.
5. Keep planning models transparent and explainable.

---

# Future Refactoring Direction

Possible improvements:

- unify planning entry point
- clarify active engine modules
- reduce duplicate historical files
- improve plugin lifecycle documentation
- strengthen scenario validation

---

# For Codex Contributors

Before modifying code:

1. Identify the active execution path.
2. Confirm the target file is not a legacy version.
3. Make minimal changes.
4. Preserve scenario reproducibility.
5. Document reasoning for structural changes.