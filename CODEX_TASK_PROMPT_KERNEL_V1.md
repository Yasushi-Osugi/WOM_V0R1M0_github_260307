# CODEX_TASK_PROMPT_KERNEL_V1

You are working inside the WOM repository.

Your task is to implement the **minimal WOM LOT_ID-based planning kernel**.

Follow the instructions below carefully.

Do not expand scope beyond what is described.

---

# 1. Read These Files First

Before writing any code, read the following files in order:

1. REPO_BOOTSTRAP.md
2. ARCHITECTURE_MAP.md
3. ARCHITECTURE.md
4. INTERFACE_SPEC.md
5. KERNEL_RULES.md
6. WOM_DATA_MODEL.md
7. WOM_MINIMAL_CLASS_MODEL.md
8. WOM_EXECUTION_MODEL.md
9. AGENTS.md
10. CODEX_IMPLEMENT_KERNEL.md

Do not start coding until you understand the architectural rules.

---

# 2. Objective

Implement the **minimal WOM Planning Kernel** that demonstrates the following planning loop:

DemandEvent  
→ FlowEngine.simulate()  
→ FlowEvent stream  
→ derive_state()  
→ detect_trust_events()  
→ Evaluator.score()  
→ Resolver.propose()  
→ apply_operator()  
→ repeat  

This loop must run end-to-end with a small demo scenario.

The implementation must remain minimal.

---

# 3. Required Classes

Implement the following six core classes.

Lot  
DemandEvent  
FlowEvent  
StateView  
Operator  
PlanningKernel  

Use Python dataclasses and type hints.

The class definitions must match the design in `WOM_MINIMAL_CLASS_MODEL.md`.

---

# 4. Supporting Components

Implement the following minimal components:

FlowEngine  
Evaluator  
Resolver  

Keep their logic intentionally simple.

They must only demonstrate the kernel loop clearly.

---

# 5. FlowEngine Requirements

FlowEngine must implement:

simulate(...)  
derive_state(...)  
detect_trust_events(...)

simulate()

Inputs:
- lots
- demand_events
- capacities
- policy

Outputs:
- list of FlowEvent

Minimal behavior is acceptable.

Example:

- generate production events
- generate shipment events
- generate arrival events
- generate sale events

derive_state()

Build StateView from FlowEvents and DemandEvents.

detect_trust_events()

Return simple conditions such as:

stockout risk  
inventory overflow  
capacity overload  

Return a simple structure such as a list of dictionaries.

---

# 6. Evaluator Requirements

Evaluator must implement:

score(state, policy)

Return a dictionary containing metrics such as:

service_level  
inventory_penalty  
total_score  

Example scoring pattern:

total_score = service_level - inventory_penalty

Keep the logic transparent and deterministic.

---

# 7. Resolver Requirements

Resolver must implement:

propose(...)  
apply_operator(...)

propose()

Input:

- lots
- flow_events
- state
- trust_events
- policy

Return an Operator.

Minimal behavior is sufficient.

Example decision rules:

If stockout risk exists → shift production earlier  
If inventory overflow exists → delay shipment  
Otherwise → do_nothing  

apply_operator()

Return updated planning objects.

Do not mutate StateView directly.

Operators should modify:

- lots
- event timing
- event routing
- quantities

---

# 8. PlanningKernel Requirements

PlanningKernel must orchestrate the planning loop.

Responsibilities:

1. run simulation
2. derive state
3. detect trust events
4. evaluate state
5. call resolver
6. apply operator
7. repeat until stable or max iterations reached

PlanningKernel must remain small and readable.

---

# 9. Determinism Rules

The implementation must be deterministic.

Follow these rules:

- avoid random behavior
- avoid unstable ordering
- sort collections when necessary
- avoid relying on dictionary iteration order

The same inputs must produce the same outputs.

---

# 10. File Structure

Place the implementation in a minimal isolated location.

Example structure:

pysi/kernel/minimal_kernel.py  
pysi/kernel/minimal_demo.py  
tests/test_minimal_kernel.py  

If this exact structure does not fit the repository, choose the closest minimal location.

Avoid modifying unrelated files.

---

# 11. Demo Scenario

Provide a small runnable demo.

The demo should:

1. create a few lots
2. create a few demand events
3. define a simple capacity dictionary
4. run PlanningKernel
5. print results

Example output should include:

trust events  
operators selected  
evaluation scores  
final state  

The demo should run with a simple command such as:

python minimal_demo.py

---

# 12. Tests

Provide minimal tests.

Required tests:

1. State derivation is deterministic.
2. Operator does not mutate StateView directly.
3. Flow simulation produces expected event types.
4. Resolver produces a valid Operator.

Keep tests small and readable.

---

# 13. Coding Style

Follow these coding guidelines:

- use dataclasses
- use type hints
- prefer small functions
- prefer explicit logic
- avoid premature abstraction
- add short comments explaining WOM-specific behavior

Prefer clarity over cleverness.

---

# 14. Definition of Success

The implementation is considered successful if:

- the kernel loop runs end-to-end
- the code is small and readable
- state is derived from events
- operators modify planning objects, not state directly
- the demo scenario runs successfully
- the implementation is suitable as the foundation for the WOM planning kernel

---

# 15. Important Constraint

Do not attempt to implement the full WOM system.

This task is only to implement a **minimal working planning kernel**.

If something is unclear, choose the smallest implementation that respects the architecture rules.

---

# Final Instruction

Implement the minimal WOM LOT_ID-based planning kernel according to these instructions.

Keep the implementation minimal, deterministic, and explainable.

Focus on architectural correctness rather than completeness.