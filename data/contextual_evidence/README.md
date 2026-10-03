# Contextual Certificate Fixtures

This directory contains bounded fixtures for replayable certification from
source bytes to a word-in-context verdict.

Current fixture:
- `canonical116_contextual_cases.json`

Design notes:
- `canonical116.ready` and `unit_count=116` are checked as a separate layer.
- Phrase existence (A), uniqueness (B), and dataset-origin linkage (C) are
  evaluated as separate claims.
- Claim C is never inferred from A/B; it requires an explicit origin link.
- Missing origin linkage yields a suspended context-resolution layer.
- Source identity preserves source/version/hash/extraction policy/normalization policy.
