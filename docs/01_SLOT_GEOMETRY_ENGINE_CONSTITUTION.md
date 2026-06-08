# Slot Geometry Engine Constitution

## Black-box boundary

The engine does not claim to reveal the hidden internal reasoning of GPT or any other model. It provides an external governing layer so that no answer is accepted without trace, bounded closure, and explicit residual handling.

## Governing rules

1. Every knowledge-bearing unit enters the system as a `SlotGraph` with a center, slots, residuals, rank placeholder, and trace.
2. A graph cannot close if required slots remain unfilled.
3. A graph with blocking residuals is blocked.
4. A graph with a broken identity is invalid.
5. A graph cannot produce output above its licensed layer; such an attempt is a `FORBIDDEN_LEAP`.
6. A graph that reaches minimal closure with declared non-blocking residuals is treated as `PERFORATED_CLOSED`, yielding a limited candidate rather than a certificate.
7. No output is valid without a trace reference.

## PR-1 boundary

This repository revision intentionally implements only the foundational core:

- `SlotGraph`
- `Slot`
- `SlotBoundary`
- `Residual`
- `Rank` placeholder
- `TraceRef`
- `GammaClosureState`
- `GammaResult`

Future layers such as rank lattice joins, transition gates, forbidden straight-line registries, and answer audits can be added on top of this closure foundation.
