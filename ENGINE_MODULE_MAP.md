# ENGINE MODULE MAP

This document explains the code-level structure of WOM
(Weekly Operation Model).

Its purpose is to help:

- Codex agents
- ChatGPT development sessions
- human contributors

understand where the core logic lives and how the main modules interact.

---
                 WOM ENGINE

           ┌───────────────────┐
           │     Scenario      │
           └────────┬──────────┘
                    │
                    ▼
           ┌───────────────────┐
           │     Network       │
           └────────┬──────────┘
                    │
                    ▼
           ┌───────────────────┐
           │ Planning Pipeline │
           └────────┬──────────┘
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Plugins     PSI      Cost
                   Engine   Model
                    │
                    ▼
           ┌───────────────────┐
           │ Visualization / IO│
           └───────────────────┘

---

# 1 Top-Level View

At a high level, WOM consists of:

```text
main.py
   │
   ▼
Application / Entry Layer
   │
   ▼
Planning Engine Core
   │
   ├── Scenario System
   ├── Network Model
   ├── Planning Pipeline
   ├── Plugin System
   └── I/O / Persistence
   │
   ▼
Output / Visualization Layer
2 Repository Code Map
WOM
├ main.py
├ pysi/
│  ├ app/
│  ├ core/
│  ├ plan/
│  ├ network/
│  ├ plugins/
│  ├ scenario/
│  ├ io/
│  ├ io_adapters/
│  ├ db/
│  ├ gui/
│  ├ evaluate/
│  ├ tutorial/
│  └ utils/
├ tools/
├ data/
├ examples/
└ docs/
3 Main Code Responsibilities
3.1 main.py

Primary top-level entry point.

Responsibilities:

start WOM execution

route to application flow

provide a simple execution entry

Use this when explaining the project at the highest level.

3.2 pysi/app/

Application entry layer.

Typical responsibilities:

CSV entry execution

GUI entry execution

SQL entry execution

orchestration

Representative files:

pysi/app/entry_csv.py
pysi/app/entry_gui.py
pysi/app/entry_sql.py
pysi/app/orchestrator.py

Use this layer when changing execution flow or application startup behavior.

3.3 pysi/core/

Planning orchestration and pipeline management.

Typical responsibilities:

planning pipeline execution

plugin loading / hook management

engine orchestration

Representative files:

pysi/core/pipeline.py
pysi/core/wom_pipeline.py
pysi/core/plugin_loader.py

This is one of the most important areas of the system.

If the question is:

How does WOM run the engine?

the answer usually starts here.

3.4 pysi/plan/

Core planning engine logic.

Typical responsibilities:

PSI logic

lot-flow behavior

operations

validators

demand generation

Representative files:

pysi/plan/engines.py
pysi/plan/operations.py
pysi/plan/validators.py
pysi/plan/demand_generate.py

This is the primary location for:

planning behavior changes

lot handling rules

PSI logic updates

If the question is:

Where is WOM's core planning intelligence?

the answer is:

pysi/plan/
3.5 pysi/network/

Supply chain network model.

Typical responsibilities:

node definitions

tree construction

network factories

structural representation of supply chains

Representative files:

pysi/network/node_base.py
pysi/network/tree.py
pysi/network/network_factory.py

This layer defines:

inbound structures

outbound structures

parent / child relationships

lead-time and structural flow context

Use this layer when changing the physical or logical supply chain structure.

3.6 pysi/plugins/

Extension layer for planning logic.

Typical responsibilities:

capacity allocation

urgency logic

diagnostics

rule extensions

demand / capacity provider logic

Representative structure:

pysi/plugins/<plugin_name>/plugin.py

Examples:

pysi/plugins/capacity_allocator/plugin.py
pysi/plugins/capacity_clip/plugin.py
pysi/plugins/diagnostics/plugin.py

Important note:

Prefer editing:

plugin.py

Avoid by default:

plugin_OLD.py
plugin_BK*.py

This layer is the main path for extending WOM behavior without rewriting the core engine.

3.7 pysi/scenario/

Scenario definition and scenario loading layer.

Typical responsibilities:

define scenarios

load scenario configurations

manage baseline / risk / what-if structures

Representative files:

pysi/scenario/loader.py
pysi/scenario/store.py
pysi/scenario/index.py

Use this layer when creating:

baseline scenarios

disruption scenarios

risk simulations

future-state models

3.8 pysi/io/ and pysi/io_adapters/

Data input / output layer.

Responsibilities:

PSI state persistence

SQL bridges

CSV adapters

tree writeback

state loading

Representative files:

pysi/io/psi_state_io.py
pysi/io/sql_bridge.py
pysi/io_adapters/csv_adapter.py
pysi/io_adapters/sql_adapter.py

Use this layer when changing how WOM reads or writes data.

3.9 pysi/db/

Database utilities and schema support.

Responsibilities:

SQLite integration

schema setup

calendar sync

DB verification

seed / migration logic

Representative files:

pysi/db/sqlite.py
pysi/db/schema.sql
pysi/db/apply_schema.py

Use this layer when moving WOM from CSV-based storage toward SQL-based persistence.

3.10 pysi/gui/

Visualization / GUI layer.

Responsibilities:

developer-facing visualization

cockpit views

network viewers

world map views

Representative files:

pysi/gui/cockpit_tk.py
pysi/gui/world_map_view.py
pysi/gui/network_viewer_patched.py

Important design note:

In WOM, GUI is not the core asset.

The planning engine must remain independent of GUI technology.

3.11 pysi/evaluate/

Evaluation and cost / price analysis layer.

Responsibilities:

cost attachment

offering price logic

revenue / margin propagation

evaluation support

Representative files:

pysi/evaluate/cost_attach.py
pysi/evaluate/offering_price.py
pysi/evaluate/evaluate_cost_models_v2.py

Use this layer when extending WOM from physical PSI into profit / value evaluation.

3.12 pysi/tutorial/

Scenario adapters and learning / demo utilities.

Responsibilities:

tutorial adapters

demo plotting

lightweight examples

Use this layer for:

education

demonstrations

quick experiments

3.13 tools/

Execution and maintenance utilities.

Typical responsibilities:

scenario runners

schema checks

migration helpers

validation tools

Representative files:

tools/run_phone_v0.py
tools/run_pharma_v0.py
tools/run_rice_v0.py

This layer is best understood as:

developer utilities

not core engine logic.

4 Core Execution Path

The most important conceptual execution path in WOM is:

Scenario Input
   ↓
Network Construction
   ↓
Planning Pipeline
   ↓
Plugin Hooks
   ↓
PSI / LOT Processing
   ↓
Result Generation
   ↓
Visualization / Export

Mapped to modules:

pysi/scenario/
   ↓
pysi/network/
   ↓
pysi/core/
   ↓
pysi/plugins/
   ↓
pysi/plan/
   ↓
pysi/io/ , pysi/evaluate/ , pysi/gui/
5 Most Important Edit Targets

When making meaningful engine changes, the most likely target directories are:

pysi/plan/
pysi/core/
pysi/network/
pysi/plugins/

Typical usage:

planning logic change → pysi/plan/

pipeline / orchestration change → pysi/core/

supply chain structure change → pysi/network/

extend behavior safely → pysi/plugins/

6 Safe Editing Guidance

Prefer editing:

main current files
plugin.py
engines.py
operations.py
pipeline.py
wom_pipeline.py

Avoid unless explicitly needed:

*_OLD.py
*_BK*.py
Untitled*.py
temporary files

Generated / runtime outputs should not be edited:

out/
plan_data/
__pycache__/
7 Relationship to Core Design Documents

This module map should be read together with:

WOM_DESIGN_PRINCIPLES.md

WOM_PLANNING_THEORY.md

WOM_SYSTEM_OVERVIEW.md

ARCHITECTURE.md

WOM_PIPELINE_SPEC.md

LOT_ID_SPEC.md

Those documents define:

why WOM exists

how WOM is modeled

how the planning engine works

This document defines:

where those ideas live in the codebase

8 Simplified Mental Model

A simple way to understand the codebase is:

Scenario defines the problem
Network defines the structure
Plan defines the logic
Core runs the flow
Plugins extend the behavior
IO stores the state
GUI shows the result
9 Final Summary

If you need to understand WOM quickly:

What is WOM?            → README.md
How does WOM work?      → WOM_SYSTEM_OVERVIEW.md
What is the theory?     → WOM_PLANNING_THEORY.md
What is the architecture? → ARCHITECTURE.md
How does the pipeline work? → WOM_PIPELINE_SPEC.md
How is lot identity defined? → LOT_ID_SPEC.md
Where is the code?      → ENGINE_MODULE_MAP.md