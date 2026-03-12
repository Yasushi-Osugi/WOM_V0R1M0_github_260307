# WOM — Weekly Operation Model

WOM is a **lot-based supply chain planning engine**.

           WOM — Weekly Operation Model
           Lot-based Supply Chain Planning Engine


        Final Market Demand
                 │
                 │  Demand creates
                 ▼
             LOT_ID Lists
   (NODE + PRODUCT + YYYYWW + SEQUENCE)
                 │
                 │  Backward planning
                 ▼
        Lead-Time Positioned Lots
                 │
                 │
                 ▼
        WOM Planning Engine
        (Lot-based PSI Simulation)
                 │
                 │
                 ▼
        Hybrid Push–Pull Network

     Inbound Supply (PUSH)
           Suppliers
               ↓
          Manufacturing (MOM)
               ↓
         Distribution (DAD)
               ↓ PUSH
       Decoupling Stock Point
               ↓ PULL
           Market Nodes

                 │
                 ▼
        Explainable Planning Results

WOM — Weekly Operation Model
Lot-based Supply Chain Planning Engine

---

WOM (Weekly Operation Model) is a **lot-based supply chain planning engine** designed to simulate global production, logistics, and demand fulfillment using deterministic planning logic.

Unlike traditional planning systems that operate on scalar quantities, WOM operates on **LOT_ID objects**.

This enables:

- demand-anchored planning
- lot-level traceability
- explainable planning behavior
- hybrid push–pull supply chain simulation

WOM is designed as the planning core of a future **economic operating system**.

---

# Core Idea

WOM planning follows a simple principle.


Demand defines the lot.
Lots define the plan.
Supply fulfills the lots.


Instead of planning using quantities, WOM represents supply chain flows using **lists of lot objects**.


quantity = len(lot_id_list)


This makes supply chain behavior transparent and explainable.

---

# WOM Planning Model

The WOM planning model is built on four conceptual layers.


Demand Layer
↓
Planning Engine Layer
↓
Supply Chain Network Layer
↓
Execution / Visualization Layer


---

# Planning Flow

The planning process follows a deterministic pipeline.


Demand generation
↓
LOT_ID creation
↓
Backward lead-time positioning
↓
Forward supply simulation
↓
Shipment allocation


---

# Hybrid Push–Pull Supply Chain

WOM models supply chains using a hybrid push–pull structure.


Inbound Supply Chain (PUSH)
↓
Manufacturing (MOM)
↓
Outbound PUSH
↓
Decoupling Stock Point
↓
Outbound PULL
↓
Market Demand


This structure stabilizes production while allowing flexible demand fulfillment.

---

# LOT_ID — The Planning Unit

The fundamental planning unit in WOM is **LOT_ID**.

Example:


TOKYO_DC-DRUG_A-2026050001


Each LOT_ID represents:

- product
- market node
- consumption week
- lot sequence

LOTS move through the supply chain during simulation.

---

# Repository Structure


WOM
├ main.py
├ pysi/
├ tools/
├ data/
├ docs/

├ WOM_DESIGN_PRINCIPLES.md
├ WOM_PLANNING_THEORY.md
├ WOM_SYSTEM_OVERVIEW.md
├ ARCHITECTURE.md
├ WOM_PIPELINE_SPEC.md
├ LOT_ID_SPEC.md

├ AI_TEAM.md
├ AI_MEETING_PROTOCOL.md
├ DEV_ROADMAP.md
├ AI_SELF_EVOLUTION.md


---

# Documentation Hierarchy

The WOM design documentation is structured as:


Design Philosophy
WOM_DESIGN_PRINCIPLES.md

Planning Theory
WOM_PLANNING_THEORY.md

System Overview
WOM_SYSTEM_OVERVIEW.md

Architecture
ARCHITECTURE.md

Planning Engine Specification
WOM_PIPELINE_SPEC.md

LOT Identity Model
LOT_ID_SPEC.md


---

# Current Capabilities

WOM currently supports:

- lot-based PSI simulation
- multi-node supply chain networks
- hybrid push–pull planning
- scenario simulation
- plugin-based extensions

---

# Future Directions

The WOM architecture enables future extensions including:

- AI-assisted planning
- enterprise planning systems
- economic simulation environments
- global supply chain modeling

WOM may serve as a planning core for a future **economic operating system**.

---

# Development Model

WOM development follows an **AI-assisted research lab model**.

Roles include:

- AI Architect
- AI Engine Developer
- AI Plugin Developer
- AI Scenario Designer
- AI Excel UX Designer
- AI Tester

Collaboration protocols are defined in:


AI_TEAM.md
AI_MEETING_PROTOCOL.md


---

# Running WOM

Basic execution:


python main.py


Example workflows and tools are located in:


tools/
examples/
data/


Detailed instructions are available in:


RUN.md


---

# Why WOM Exists

Traditional supply chain planning systems often suffer from:

- opaque optimization logic
- limited traceability
- unstable planning adjustments

WOM addresses these issues by introducing:

- demand-anchored planning
- lot-based simulation
- explainable planning logic

---

# License

MIT License

---

# Author

Yasushi Osugi

Global Supply Chain Planning Research