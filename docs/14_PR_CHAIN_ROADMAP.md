# 14 — PR Chain Roadmap

> **Status:** Constitutional law. Ratified in PR-1B. This file is the
> authoritative chain of pull requests. The
> [Constitutional PR Geometry](13_CONSTITUTIONAL_PR_GEOMETRY.md) binds
> every PR to declare its position in this chain. A PR that
> implements work belonging to a later position is a
> `FORBIDDEN_LEAP`, regardless of CI status.

The chain is intentionally narrow. Each step exists to make the next
step reviewable, not to deliver standalone value.

```text
PR-0    Scaffold + Constitution                            ✓ done
PR-1A   Mathematical Slot Geometry Constitution            ✓ done
        + minimum carrier enums
PR-1B   Constitutional Test Geometry                       ✓ done
        + Constitutional PR Geometry
        + PR template + roadmap
PR-1C   Pre-SlotGraph constitutional closure               ✓ done
        + docs 15 (Textual Communication Entry Law)
        + docs 16 (Identity-to-Truth Licensing Chain)
        + docs 17 (SlotGraph Generation Law)
        + ConstitutionalChainTestCase (schema only)
PR-2    SlotGraph + GammaClosure minimal implementation    ✓ done
        (Rank / Residual carriers wired into the kernel)
PR-2A   Harden SlotGraph construction against              ✓ done
        constitutional gaps (corrective PR;
        Copilot review on PR-2 — no new layer)
PR-3    RankLattice + ResidualPolicy + EvidenceContract    ✓ done
PR-4    TransitionGate + FailureTaxonomy bindings          ✓ done
PR-5    Forbidden Straight-Line Registry                   ✓ done
        (+ technical-terminology non-confusion cases)
PR-6    AnswerAudit wrapper                                ← current
        (ModelClient protocol only — no adapters)
```

## 1. Per-step boundary summary

```text
PR-0
    Origin   : "A repository must declare its laws before its code."
    Output   : repository scaffold, top-level constitutional docs.
    Forbidden: any executable kernel.

PR-1A
    Origin   : "SlotGeometry is a constitutional mathematical object."
    Output   : docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md
               + minimum carrier enums (ClosureState, FailureCode,
               Rank, Residual, ResidualKind).
    Forbidden: SlotGraph, gamma, TraceLedger, TransitionGate.

PR-1B
    Origin   : "No PR without origin/branch/chain;
                no test without origin/branch/chain."
    Output   : docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md,
               docs/13_CONSTITUTIONAL_PR_GEOMETRY.md,
               docs/14_PR_CHAIN_ROADMAP.md,
               tests/support/constitutional_case.py,
               minimal harness tests proving schema rules,
               .github/pull_request_template.md,
               CLAUDE.md updates.
    Forbidden: any new runtime behavior; SlotGraph; gamma;
               TransitionGate; LLM adapters; Arabic code.

PR-1C (this PR)
    Origin   : "No SlotGraph from a raw value;
                no text without a communicative entry boundary;
                no internal processing without the
                identity-to-truth licensing chain;
                no partial test pass is a constitutional pass."
    Output   : docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md,
               docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md,
               docs/17_SLOTGRAPH_GENERATION_LAW.md,
               docs/12 § 9 (ChainTestCase),
               tests/support/constitutional_case.py
                   (ConstitutionalChainTestCase, schema only),
               CLAUDE.md and PR template updates that bind PR-2
               to these laws.
    Forbidden: any executable kernel; SlotGraph; Slot; gamma;
               TransitionGate; EvidenceContract; TraceLedger;
               any new src/ module beyond what already exists;
               new src/taaqqul_slot_geometry/ logic;
               LLM adapters; lexicons; Arabic linguistic code;
               new runtime dependencies.
    Binding  : Any PR-2 attempt opened before this PR is merged,
               or that does not honor docs 15, 16, 17, is a
               FORBIDDEN_LEAP regardless of CI status.

PR-2
    Origin   : Mathematical Slot Geometry Laws sections 1–4.
    Output   : SlotGraph, Slot, Center, Boundary, gamma()
               returning a GammaResult with a TraceEntryCandidate.
    Forbidden: TransitionGate emission; rank promotion;
               forbidden-line registry; LLM adapters; Arabic code.

PR-2A
    Origin   : "Construction refusals must be named and complete"
               — docs/17 §§2–3 + §5 totality, docs/15 §5, docs/12.
    Output   : SlotBoundary refuses empty refusal_codes;
               OpeningPolicy refuses empty allowed_potentials;
               TraceRef refuses empty anchor;
               Center requires non-empty identity_claim + real
               TraceRef; EntryBoundary carries the full docs/15 §5
               surface (representation/ontological/sound/meaning
               status + prior_trace_status + produces_only);
               SlotGraph.center mandatory; entry_boundary required
               when generation_source is DECLARED_ENTRY; named
               construction surface SlotGraph.construct(...) →
               ConstructionResult with FailureCode for every
               presence-level row of docs/17 §3.
    Forbidden: RankLattice policy; ResidualPolicy engine;
               EvidenceContract; TransitionGate; Forbidden
               Straight-Line Registry; AnswerAudit; Arabic code;
               lexicons; LLM adapters; new FailureCode members;
               changes to gamma's verdict semantics; gamma side
               effects; TraceLedger imports from gamma; TypeError
               as a constitutional refusal.

PR-3
    Origin   : Mathematical Slot Geometry Laws sections 5–7
               (Rank, Residual, Evidence).
    Output   : RankLattice with bounded meet/join;
               ResidualPolicy enforcing visibility;
               EvidenceContract carriers.
    Forbidden: TransitionGate emission; forbidden-line registry;
               LLM adapters; Arabic code.

PR-4
    Origin   : Mathematical Slot Geometry Laws section 8 + docs/08.
    Output   : TransitionGate; FailureTaxonomy bindings;
               named refusals everywhere previously promised.
    Forbidden: forbidden-line registry; LLM adapters; Arabic code.

PR-5
    Origin   : docs/04 + docs/10.
    Output   : Forbidden Straight-Line Registry; technical
               terminology non-confusion cases.
    Forbidden: LLM adapters; Arabic code beyond the constitutional
               cases listed in docs/09.

PR-6
    Origin   : docs/01 (black-box boundary).
    Output   : AnswerAudit wrapper that consumes the kernel
               via a ModelClient protocol.
    Forbidden: any concrete adapter (OpenAI, Anthropic, local).
               Concrete adapters require a separate post-PR-6
               milestone.
```

## 2. Amendment discipline

```text
The only licit way to change this chain is an Amendment PR
whose entire branch is the chain change itself.
```

An Amendment PR is bound by
[`13_CONSTITUTIONAL_PR_GEOMETRY.md`](13_CONSTITUTIONAL_PR_GEOMETRY.md)
exactly like any other PR. Its `origin_law` is "this roadmap" and
its `branch_name` is the specific step being added, split, merged,
or retired.

## 3. Reading order for reviewers

```text
1. CLAUDE.md
2. docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md
3. docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md
4. docs/13_CONSTITUTIONAL_PR_GEOMETRY.md
5. docs/14_PR_CHAIN_ROADMAP.md
6. docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md
7. docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md
8. docs/17_SLOTGRAPH_GENERATION_LAW.md
9. The PR description, checked against (4), (5), (6), (7), (8).
```

A reviewer who skips (4), (5), (6), (7), or (8) cannot tell whether
the PR is a constitutional branch or a leap. CI cannot tell either.
