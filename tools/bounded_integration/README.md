# Bounded imported-evidence readout verifier

An experimental pre-admission review tool, called by the Alghanem integration
runner. It has no dependency on Alghanem and never calls its producer or engine.
It independently reads the supplied CSV bytes, checks the controlled question,
occurrences, roles, case, lexical selections, intermediate payloads and final
answer. Its result does not issue a SlotGraph, Gamma closure, rank, or final
AnswerAudit; it must not be substituted for those APIs.

The caller pins the expected source digest outside the artifact. Tests with an
alternate source pin that source's real digest: semantic failures are therefore
not disguised integrity failures. Imported MASAQ tags remain imported evidence.

Run the cross-repository tests from adjacent pinned checkouts:

```bash
PYTHONPATH=Alghanem/src:Alghanem python -m pytest \
  Alghanem/tests/arabic/test_bounded_path.py -q
```

The engineering contract is governed by evidence-to-claim binding and explicit
rank boundaries (docs/12, docs/16, docs/18, docs/52). This tool does not claim the
constitutional chain is closed. The integration tests live in the producer's
repository and have declared origin/branch/chain; no production kernel or GPT
adapter behavior is changed here.

## Extended admission path

The directory also contains the later fragment, expansion, ontology, acquired
knowledge, and identity verifiers. `admission.py` dispatches these bounded
contracts to their reviewers before using the existing SlotGraph/Gamma APIs.
Its render, serialization and reload entry points revalidate the candidate and
its original question against the supplied trust environment. Acceptance remains
TRACE-scoped; it is not a certificate of external truth or general semantic
derivation from 116. The trusted source adapters, question grammar and some
rendering definitions remain shared, as documented by each verifier.

The cross-repository knowledge and book-reading runners require the companion
Alghanem delivery (book-reading commit c4b38e7), installed as an adjacent checkout.
That delivery records simulated application evidence and an editorial book-rule
policy without human semantic approval. This PR does not embed Alghanem or
silently substitute its definitions. Native Taaqol tests run independently;
companion integration tests must also be run from Alghanem.
