# Taaqol-GPT

A constitutional slot-geometry engine for traceable reasoning outputs.

This repository does not claim to expose the hidden internal reasoning of GPT or any language model. Instead, it builds a constitutional slot-geometry layer around generated answers. Every input, claim, transition, and output must pass through SlotGraph construction, Gamma minimal closure, rank boundaries, residual visibility, and trace preservation.

## Current scope

The initial implementation focuses on the first foundation slice:

- `SlotGraph`
- `GammaClosure`
- minimal residual handling
- trace-preserving closure results
- focused tests for open, minimal, perforated, blocked, invalid, and forbidden-leap states

## Run tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
