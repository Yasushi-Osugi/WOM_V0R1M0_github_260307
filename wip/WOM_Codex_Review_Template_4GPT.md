# WOM_Codex_Review_Template_4GPT.md

You are reviewing code produced by an AI coding agent (Codex).

Project: WOM Planning Kernel

Architecture principles:

1. Flow/Event is the source of truth
2. StateView is a derived view
3. StateView must never be directly mutated
4. Operators modify planning objects (FlowEvents or Lots)
5. Kernel must remain deterministic

----------------------------------------------------
INPUT
----------------------------------------------------

Below is the Codex implementation.

[PASTE CODEX OUTPUT HERE]

----------------------------------------------------
REVIEW TASK
----------------------------------------------------

Analyze the code according to the following checklist.

1. Architecture compliance

Check whether the implementation respects WOM architecture:

- Flow/Event = source of truth
- StateView = derived view
- Operator does NOT mutate StateView
- PlanningKernel only orchestrates logic

Return:

Architecture status:
PASS / FAIL

Explain violations if any.

----------------------------------------------------

2. Determinism check

Verify the system produces identical results with identical inputs.

Look for:

- explicit event ordering
- sorted flow processing
- deterministic operator selection

Return:

Determinism status:
PASS / FAIL

Explain risks if present.

----------------------------------------------------

3. Minimal kernel scope

Verify the implementation remains minimal.

Check:

- no unnecessary framework
- no plugins implemented
- no external dependencies
- no large abstraction layers

Return:

Minimality status:
PASS / FAIL

Explain if scope expanded.

----------------------------------------------------

4. Kernel runtime loop verification

Verify that the following loop exists:

DemandEvent generation
↓
Flow simulation
↓
State derivation
↓
Trust event detection
↓
Evaluation
↓
Resolver
↓
Operator application
↓
Re-simulation

Return:

Loop implementation:
COMPLETE / PARTIAL / MISSING

Explain missing steps.

----------------------------------------------------

5. Code quality

Evaluate:

- readability
- class responsibility clarity
- testability
- deterministic data flow

Score:

Code quality score: 1–10

----------------------------------------------------

6. Risk detection

Identify any:

- architecture violations
- hidden state mutation
- nondeterministic behavior
- logic errors

List risks clearly.

----------------------------------------------------

7. Final verdict

Return one of the following:

APPROVE – implementation matches WOM architecture

REVISE – implementation mostly correct but needs fixes

REJECT – architecture broken

Explain reasoning in 3–5 sentences.