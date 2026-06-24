# 15 — Rejected Runtime Patterns (Embargo Guard)

> **Status:** Active embargo guard.
> These patterns are rejected and blocked from runtime surfaces until Runtime Embargo is explicitly lifted.

---

## Rejected runtime anti-patterns

1. `binding_kernel.py` before embargo lift.
2. `decision_engine.py` before embargo lift.
3. `coverage_matrix_v0.1.yaml` before computed schema + embargo lift.
4. MRK proof booleans:
   - `domain_proved`
   - `unit_proved`
   - `identity_preserved`
   - `trace_preserved`
   - `gate_passed`
5. `identity_preserved=True` or `is_preserved=True` defaults.
6. Evidence list as proof.
7. `Rank.CERTIFICATE` / `Rank.REJECTED` as runtime verdict outputs.
   Reason: they collapse audit-only policy intent into runtime verdict
   claims and bypass embargoed proof discipline.
8. `SlotGeometry.transform(operation: str): pass`
9. `Gate.condition` as free text.
10. `Bridge.translator` as free text.
11. Manual `ComputedVerdict` injection.
12. `mrk_defaults` all-true presets.

---

## Embargo law

A rejected pattern may appear only inside this documentation file as a quoted anti-pattern.
It may not appear in `src/`, `schemas/`, or runtime-facing tests.

Runtime Embargo remains active.
FailureAlignment remains `AUDIT_ONLY`.
Proof policy alignment remains audit-only.
No kernel. No engine. No runtime.
