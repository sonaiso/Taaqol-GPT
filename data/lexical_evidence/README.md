# LEX-DATA-1 Lexical Evidence Fixtures

This directory contains data-only lexical evidence fixtures for bounded constitutional measurement.

Scope:
- 25 jamid genus anchors
- 50 attribute-source anchors
- 100 genus-attribute compatibility links

Allowed outputs:
- LexicalEvidenceCandidate
- AttributeSourceCandidate
- GenusAttributeCompatibilityCandidate

Forbidden outputs:
- Meaning
- FinalMeaning
- Hukm
- Truth
- Certainty
- Reality
- EssentialAttributeTruth

Data policy:
- Sources are limited to Maqayis and Wasit in LEX-DATA-1.
- No long copied definitions are stored.
- Attestation is source-reference only, not semantic closure.

## LEX-DATA-2 Arabic WordNet witness fixtures

This repository also carries a bounded external lexical witness fixture set
for Arabic WordNet under:

- `lex_data_2_arabic_wordnet_samples.json`

Boundary notes:
- WordNet rows are candidate-only lexical evidence.
- WordNet is not final meaning, hukm, truth, certainty, or reality authority.
- Multi-sense ambiguity remains visible and is never silently collapsed.
- Every row preserves provenance (`source_id`, `source_version`, `synset_id`,
  query identity, trace, and retrieval metadata).
