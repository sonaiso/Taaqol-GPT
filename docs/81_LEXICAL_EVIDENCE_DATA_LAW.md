# 81 — Lexical Evidence Data Law (LEX-DATA-1)

> Status: data declaration.
> Scope: fixture + schema + constitutional tests only; no runtime gate opening.
> Snapshot date: 2026-07-09.

## §1 Constitutional positioning

```text
LEXICON_ROLE = LINGUISTIC_ATTESTATION_WITNESS
LEXICON_NOT_EQUAL = {Meaning, Hukm, Truth, Certainty, Reality}
LEXICON_OUTPUT_ROLE = CandidateOnly
```

A lexical source in this stage is a witness for lexical attestation and usage validity,
not a producer of final meaning, hukm, truth, certainty, or reality.

## §2 LEX-DATA-1 surface

```text
LEX_DATA_1_SCOPE = data/lexical_evidence/*
LEX_DATA_1_COUNTS = {
  jamid_genus_anchors: 25,
  attribute_source_anchors: 50,
  genus_attribute_compatibility_links: 100
}
LEX_DATA_1_ALLOWED_OUTPUTS = {
  LexicalEvidenceCandidate,
  AttributeSourceCandidate,
  GenusAttributeCompatibilityCandidate
}
LEX_DATA_1_FORBIDDEN_OUTPUTS = {
  Meaning,
  FinalMeaning,
  Hukm,
  Truth,
  Certainty,
  Reality,
  EssentialAttributeTruth
}
```

## §3 Source and quotation discipline

```text
LEX_DATA_1_ALLOWED_SOURCES = {Maqayis, Wasit}
LEX_DATA_1_QUOTE_POLICY = NO_LONG_QUOTE
LEX_DATA_1_SOURCE_USE = citation_attestation_only
```

LEX-DATA-1 stores source attestations and trace references only.
It must not store copied long lexical definitions.

## §4 Rank and residual discipline

```text
LINK_COMPATIBILITY_STATUS = CANDIDATE
LINK_RANK_CEILING = HYPOTHESIS
RESIDUAL_VISIBILITY = REQUIRED
```

Compatibility links are bounded candidate links.
They are not essential-truth assertions and not final semantic closure.

## §5 Runtime embargo

```text
RUNTIME_NOT_OPENED = {
  parser,
  morphology_runtime,
  semantic_runtime,
  truth_engine,
  lexical_meaning_runtime,
  lexical_evidence_gate
}
```

LEX-DATA-1 is data-only preparation for future licensed gates.
