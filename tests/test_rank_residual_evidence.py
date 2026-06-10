"""Constitutional tests for the PR-3 rank / residual / evidence contracts.

Coverage mirrors the PR-3 acceptance list:

1.  RankLattice — bounded ``meet`` / ``join`` algebra: the meet never
    promotes, the join never invents a rank above every input, the
    bounds are ``ZERO`` / ``CERTIFICATE``, and empty or ill-typed
    calls refuse loudly (programmer mistake, not a verdict).
2.  ResidualPolicy — the per-kind rank-cap table of docs/06, the
    ``ResidualCeiling`` meet of docs/11 §9 (empty surface = vacuous
    lattice top, not a promotion), and ``evaluate`` naming
    ``HIDDEN_RESIDUAL`` before ``BLOCKING_RESIDUAL_PRESENT`` in the
    order of the closure law.
3.  EvidenceContract — named schema refusals (``IDENTITY_BROKEN``,
    ``DOMAIN_MISSING``, ``TRACE_MISSING``) and the aggregation law:
    empty pool → lattice bottom; a single source never licenses
    ``CERTIFICATE`` (docs/11 §8 anti-straight-line); a pool is as
    strong as its strongest member, never stronger.
4.  ``Γ`` step 9 — the rank-ceiling binding: a carried rank above
    ``ResidualCeiling`` is refused ``INVALID``/``RANK_EXCEEDS_CEILING``;
    a rank at the cap still closes; the vacuous ceiling never raises
    a carried rank; and step 8 (required slots) still precedes step 9.
5.  PR-3-FIX — the ``Residual`` birth guard (docs/11 §12): the
    carrier cannot be born malformed, so neither
    ``ResidualPolicy.ceiling`` nor ``Γ`` step 9 can ever meet a
    residual whose fields would turn a named refusal into a bare
    ``TypeError``.

Verdict-producing tests declare themselves through
:class:`ConstitutionalChainTestCase` (docs/12 §9) and are checked by
:func:`assert_constitutional_case`. Pure-algebra and schema-guard
tests follow the construction-surface precedent: ``pytest.raises``
plus the named ``FailureCode`` value asserted inside the message.
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import (
    SINGLE_SOURCE_EVIDENCE_CEILING,
    Center,
    ClosureState,
    EntryBoundary,
    EvidenceContract,
    EvidenceSource,
    FailureCode,
    GenerationSource,
    Layer,
    OpeningPolicy,
    OutputBoundary,
    Rank,
    RankLattice,
    Residual,
    ResidualKind,
    ResidualPolicy,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotGraphSchemaError,
    SlotState,
    TraceRef,
    gamma,
)
from taaqqul_slot_geometry.core.gamma import GammaResult
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

# ---------------------------------------------------------------------------
# Carrier factories — identical in shape to the Γ kernel tests; each
# step-9 test varies only the single axis it exercises.
# ---------------------------------------------------------------------------


def _boundary() -> SlotBoundary:
    return SlotBoundary(
        domain="reasoning",
        scope="rank-test",
        refusal_codes=(FailureCode.BOUNDARY_MISSING,),
    )


def _opening() -> OpeningPolicy:
    return OpeningPolicy(allowed_potentials=frozenset({"yes", "no"}))


def _filled_slot(name: str = "answer") -> Slot:
    return Slot(
        name=name,
        value_state=SlotState.FILLED,
        boundary=_boundary(),
        opening=_opening(),
        required=True,
        value="yes",
    )


def _empty_slot(name: str = "answer") -> Slot:
    return Slot(
        name=name,
        value_state=SlotState.EMPTY,
        boundary=_boundary(),
        opening=_opening(),
        required=True,
    )


def _center() -> Center:
    return Center(
        identity_claim="Q1",
        domain="reasoning",
        scope="rank-test",
        trace_ref=_trace_ref(),
    )


def _trace_ref() -> TraceRef:
    return TraceRef(anchor="trace://Q1", kind="DECLARED_ENTRY")


def _output_within() -> OutputBoundary:
    return OutputBoundary(declared_layer=Layer.CANDIDATE, output_layer=Layer.SLOT)


def _entry_boundary() -> EntryBoundary:
    return EntryBoundary(
        declared_entry_kind="ARABIC_VOCALIZED_TEXT",
        representation_status="REPRESENTATIONAL_OF_PRIOR",
        ontological_status="NOT_AN_ORIGIN",
        sound_status="NOT_A_SOUND",
        meaning_status="NOT_A_MEANING",
        prior_trace_status="OUT_OF_CURRENT_EXECUTION",
        produces_only="TEXT_TRACE_CANDIDATE",
    )


def _build_graph(
    *,
    slots: tuple[Slot, ...] | None = None,
    residuals: tuple[Residual, ...] = (),
    rank: Rank = Rank.TRACE,
) -> SlotGraph:
    return SlotGraph(
        center=_center(),
        slots=slots if slots is not None else (_filled_slot(),),
        boundary=_boundary(),
        residuals=residuals,
        rank=rank,
        output_boundary=_output_within(),
        generation_source=GenerationSource.DECLARED_ENTRY,
        entry_boundary=_entry_boundary(),
    )


def _result_from(verdict: GammaResult) -> ConstitutionalChainResult:
    return ConstitutionalChainResult(
        state=verdict.state,
        failure_code=verdict.failure_code,
        rank=verdict.rank,
        residual_visibility=verdict.residual_visibility,
        trace_present=bool(verdict.trace_event_candidate.parent_anchor),
    )


def _deferrable(name: str = "open-question") -> Residual:
    return Residual(name=name, kind=ResidualKind.DEFERRABLE, visible=True)


def _evidence(name: str, rank: Rank) -> EvidenceSource:
    return EvidenceSource(
        name=name,
        kind="declared-observation",
        rank=rank,
        trace_ref=_trace_ref(),
    )


# ---------------------------------------------------------------------------
# 1. RankLattice — bounded meet / join algebra (docs/05, docs/11 §8).
# ---------------------------------------------------------------------------


def test_rank_lattice_meet_never_promotes() -> None:
    """docs/11 §8 — the meet can only keep or lower, never raise."""

    for a in Rank:
        for b in Rank:
            bound = RankLattice.meet(a, b)
            assert bound == min(a, b)
            assert bound <= a and bound <= b
            assert bound in (a, b), "meet must be one of its inputs, never invented"


def test_rank_lattice_join_is_strongest_member_never_stronger() -> None:
    """docs/05 — a pool is as strong as its strongest member, never stronger."""

    for a in Rank:
        for b in Rank:
            bound = RankLattice.join(a, b)
            assert bound == max(a, b)
            assert bound >= a and bound >= b
            assert bound in (a, b), "join must be one of its inputs, never invented"


def test_rank_lattice_bounds_are_zero_and_certificate() -> None:
    assert RankLattice.BOTTOM is Rank.ZERO
    assert RankLattice.TOP is Rank.CERTIFICATE
    for rank in Rank:
        assert RankLattice.meet(rank, RankLattice.BOTTOM) is RankLattice.BOTTOM
        assert RankLattice.join(rank, RankLattice.TOP) is RankLattice.TOP


def test_rank_lattice_refuses_empty_and_ill_typed_calls_loudly() -> None:
    """docs/11 §12 — no synthesis: an empty meet/join is a programmer
    mistake refused with ``TypeError``, mirroring ``gamma``'s domain
    guard, never a silently synthesised bound."""

    with pytest.raises(TypeError):
        RankLattice.meet()
    with pytest.raises(TypeError):
        RankLattice.join()
    with pytest.raises(TypeError):
        RankLattice.meet(Rank.STRONG, 3)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        RankLattice.join("CERTIFICATE")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 2. ResidualPolicy — rank caps, ceiling, evaluate (docs/06, docs/11 §9).
# ---------------------------------------------------------------------------


def test_rank_cap_table_matches_the_constitution() -> None:
    """docs/06 — per-kind caps; the table is total over ResidualKind."""

    assert ResidualPolicy.rank_cap(ResidualKind.BLOCKING) is Rank.ZERO
    assert ResidualPolicy.rank_cap(ResidualKind.HIDDEN_FORBIDDEN) is Rank.ZERO
    assert ResidualPolicy.rank_cap(ResidualKind.DEFERRABLE) is Rank.HYPOTHESIS
    assert ResidualPolicy.rank_cap(ResidualKind.NON_BLOCKING) is RankLattice.TOP
    assert ResidualPolicy.rank_cap(ResidualKind.EXPLANATORY) is RankLattice.TOP
    for kind in ResidualKind:
        assert isinstance(ResidualPolicy.rank_cap(kind), Rank)
    with pytest.raises(TypeError):
        ResidualPolicy.rank_cap("BLOCKING")  # type: ignore[arg-type]


def test_residual_ceiling_is_the_meet_of_per_kind_caps() -> None:
    """docs/11 §9 — ``ResidualCeiling(G) = meet over δ of rank-cap``.

    The empty surface yields the lattice top: vacuously no residual
    constraint. It is *not* a promotion — the value only ever enters
    a meet downstream.
    """

    assert ResidualPolicy.ceiling(()) is RankLattice.TOP
    assert ResidualPolicy.ceiling((_deferrable(),)) is Rank.HYPOTHESIS
    assert (
        ResidualPolicy.ceiling(
            (
                _deferrable(),
                Residual(name="halt", kind=ResidualKind.BLOCKING, visible=True),
            )
        )
        is Rank.ZERO
    )
    assert (
        ResidualPolicy.ceiling(
            (Residual(name="aside", kind=ResidualKind.NON_BLOCKING, visible=True),)
        )
        is RankLattice.TOP
    )


def test_evaluate_names_hidden_before_blocking() -> None:
    """docs/03 ordered law — the hidden refusal (``Γ`` step 6)
    precedes the blocking refusal (``Γ`` step 7), and every refusal
    is a named ``FailureCode``, never an exception."""

    hidden = Residual(name="buried", kind=ResidualKind.HIDDEN_FORBIDDEN, visible=True)
    blocking = Residual(name="halt", kind=ResidualKind.BLOCKING, visible=True)

    both = ResidualPolicy.evaluate((hidden, blocking))
    assert both.failure_code is FailureCode.HIDDEN_RESIDUAL
    assert both.all_visible is False
    assert both.ceiling is Rank.ZERO

    blocked = ResidualPolicy.evaluate((blocking,))
    assert blocked.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert blocked.all_visible is True
    assert blocked.perforating is False

    invisible = Residual(name="unsaid", kind=ResidualKind.NON_BLOCKING, visible=False)
    assert ResidualPolicy.evaluate((invisible,)).failure_code is (
        FailureCode.HIDDEN_RESIDUAL
    )


def test_evaluate_admissible_surfaces() -> None:
    empty = ResidualPolicy.evaluate(())
    assert empty.failure_code is None
    assert empty.all_visible is True  # vacuously — no hidden surface to expose
    assert empty.perforating is False
    assert empty.ceiling is RankLattice.TOP

    perforated = ResidualPolicy.evaluate((_deferrable(),))
    assert perforated.failure_code is None
    assert perforated.all_visible is True
    assert perforated.perforating is True
    assert perforated.ceiling is Rank.HYPOTHESIS


# ---------------------------------------------------------------------------
# 3. EvidenceContract — named schema refusals + aggregation law
#    (docs/05, docs/08 preconditions, docs/11 §8).
# ---------------------------------------------------------------------------


def test_evidence_source_schema_refusals_are_named() -> None:
    """docs/11 §12 — missing means refuse, and every refusal carries
    its constitutional name inside the schema error message."""

    with pytest.raises(SlotGraphSchemaError) as broken_name:
        EvidenceSource(name="  ", kind="observation", rank=Rank.TRACE, trace_ref=_trace_ref())
    assert FailureCode.IDENTITY_BROKEN.value in str(broken_name.value)

    with pytest.raises(SlotGraphSchemaError) as missing_kind:
        EvidenceSource(name="e1", kind="", rank=Rank.TRACE, trace_ref=_trace_ref())
    assert FailureCode.DOMAIN_MISSING.value in str(missing_kind.value)

    with pytest.raises(SlotGraphSchemaError) as missing_trace:
        EvidenceSource(name="e1", kind="observation", rank=Rank.TRACE, trace_ref=None)  # type: ignore[arg-type]
    assert FailureCode.TRACE_MISSING.value in str(missing_trace.value)

    with pytest.raises(SlotGraphSchemaError):
        EvidenceSource(name="e1", kind="observation", rank=5, trace_ref=_trace_ref())  # type: ignore[arg-type]


def test_evidence_contract_schema_guards() -> None:
    with pytest.raises(SlotGraphSchemaError):
        EvidenceContract(sources=[_evidence("e1", Rank.TRACE)])  # type: ignore[arg-type]
    with pytest.raises(SlotGraphSchemaError):
        EvidenceContract(sources=("not-evidence",))  # type: ignore[arg-type]


def test_evidence_rank_aggregation_law() -> None:
    """docs/11 §8 — *a single evidence source may never license
    CERTIFICATE*; absent evidence licenses nothing; a pool is as
    strong as its strongest member, never stronger."""

    assert EvidenceContract().evidence_rank is RankLattice.BOTTOM

    single_cert = EvidenceContract(sources=(_evidence("e1", Rank.CERTIFICATE),))
    assert SINGLE_SOURCE_EVIDENCE_CEILING is Rank.STRONG
    assert single_cert.evidence_rank is Rank.STRONG
    assert single_cert.evidence_rank < Rank.CERTIFICATE

    single_low = EvidenceContract(sources=(_evidence("e1", Rank.LICENSED),))
    assert single_low.evidence_rank is Rank.LICENSED  # the cap only binds above it

    pool = EvidenceContract(
        sources=(_evidence("e1", Rank.TRACE), _evidence("e2", Rank.CERTIFICATE))
    )
    assert pool.evidence_rank is Rank.CERTIFICATE  # join — no corroboration bonus
    for a in Rank:
        for b in Rank:
            aggregate = EvidenceContract(
                sources=(_evidence("e1", a), _evidence("e2", b))
            ).evidence_rank
            assert aggregate == max(a, b), "a pool never exceeds its strongest member"


# ---------------------------------------------------------------------------
# 4. Γ step 9 — the rank-ceiling binding (docs/03 step 9, docs/11 §9).
# ---------------------------------------------------------------------------


def test_gamma_refuses_rank_above_residual_ceiling() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §9 Residual visibility law — rank ceiling",
        branch_name="carried-rank-above-deferrable-cap",
        constitutional_chain=("SlotGraph", "Gamma", "ResidualCeiling", "Rank"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=FailureCode.RANK_EXCEEDS_CEILING,
        forbidden_outputs=("MINIMALLY_CLOSED", "PERFORATED_CLOSED", "CERTIFICATE"),
        max_rank=Rank.LICENSED,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.8.Implication",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#9-residual-visibility-law",
        branch_of_origin="Implication above the residual ceiling is refused, not promoted.",
        forbidden_shortcut_assertions=("Implication → Truth",),
    )
    graph = _build_graph(residuals=(_deferrable(),), rank=Rank.LICENSED)

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.rank is Rank.LICENSED, "Γ reports the carried rank, never edits it"


def test_gamma_closes_perforated_at_the_residual_cap() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §9 Residual visibility law — rank at the cap",
        branch_name="carried-rank-at-deferrable-cap",
        constitutional_chain=("SlotGraph", "Gamma", "ResidualCeiling", "Closure"),
        expected_state=ClosureState.PERFORATED_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE", "APPROVED_OUTPUT"),
        max_rank=Rank.HYPOTHESIS,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.8.Implication",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#9-residual-visibility-law",
        branch_of_origin="A rank at the ceiling closes perforated; the residual stays visible.",
        forbidden_shortcut_assertions=("Implication → Truth",),
    )
    graph = _build_graph(residuals=(_deferrable(),), rank=Rank.HYPOTHESIS)

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))


def test_gamma_vacuous_ceiling_never_raises_the_carried_rank() -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §8 Rank lattice law — non-promotion",
        branch_name="empty-residual-surface-vacuous-top",
        constitutional_chain=("SlotGraph", "Gamma", "ResidualCeiling", "Closure"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("CERTIFICATE",),
        max_rank=Rank.STRONG,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.8.Implication",
        origin_law_ref="docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#8-rank-lattice-law",
        branch_of_origin="The vacuous ceiling licenses nothing; the carried rank passes through.",
        forbidden_shortcut_assertions=("Evidence → Certainty",),
    )
    graph = _build_graph(rank=Rank.STRONG)

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.rank is Rank.STRONG, "the vacuous top is not a promotion"


def test_gamma_step8_required_slots_precede_step9_ceiling() -> None:
    """docs/03 — the ordered closure law: a refusal at step 8
    (required slot empty) short-circuits step 9 even when the carried
    rank also exceeds the residual ceiling."""

    case = ConstitutionalChainTestCase(
        origin_law="docs/03 The ordered closure law — step 8 before step 9",
        branch_name="empty-slot-and-rank-above-ceiling",
        constitutional_chain=("SlotGraph", "Gamma", "Opening", "ResidualCeiling"),
        expected_state=ClosureState.OPEN,
        expected_failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
        forbidden_outputs=("MINIMALLY_CLOSED", "PERFORATED_CLOSED"),
        max_rank=Rank.LICENSED,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.6.Opening",
        origin_law_ref="docs/03_GAMMA_CLOSURE_CONTRACT.md#the-ordered-closure-law",
        branch_of_origin="Opening is consulted before the rank ceiling; the order is load-bearing.",
        forbidden_shortcut_assertions=("Opening → Closure",),
    )
    graph = _build_graph(
        slots=(_empty_slot(),), residuals=(_deferrable(),), rank=Rank.LICENSED
    )

    verdict = gamma(graph)

    assert_constitutional_case(case, _result_from(verdict))
    assert verdict.failure_code is not FailureCode.RANK_EXCEEDS_CEILING


# ---------------------------------------------------------------------------
# 5. PR-3-FIX — Residual birth guard (docs/11 §12 — missing means
#    refuse). Residual carrier cannot be born malformed; no malformed
#    residual reaches Γ step 9.
# ---------------------------------------------------------------------------


def test_residual_carrier_cannot_be_born_malformed() -> None:
    """PR-3-FIX — *Residual carrier cannot be born malformed.*

    ``ResidualPolicy.ceiling`` and ``Γ`` step 9 consume the carrier
    as-is, so every field is guarded at birth (docs/11 §12 — missing
    means refuse). The refusal is a loud ``TypeError`` naming the
    field — a programmer mistake, not a constitutional verdict —
    mirroring the ``rank_cap`` / ``RankLattice`` domain guards. No
    new ``FailureCode`` is minted: the guard keeps malformed
    residuals out of the constitutional surface entirely.
    """

    with pytest.raises(TypeError, match="Residual.name"):
        Residual(name="", kind=ResidualKind.DEFERRABLE, visible=True)
    with pytest.raises(TypeError, match="Residual.name"):
        Residual(name="   ", kind=ResidualKind.DEFERRABLE, visible=True)
    with pytest.raises(TypeError, match="Residual.kind"):
        Residual(name="r", kind="BLOCKING", visible=True)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="Residual.visible"):
        Residual(name="r", kind=ResidualKind.DEFERRABLE, visible="yes")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="Residual.note"):
        Residual(name="r", kind=ResidualKind.DEFERRABLE, visible=True, note=7)  # type: ignore[arg-type]

    born = Residual(name="r", kind=ResidualKind.DEFERRABLE, visible=True)
    assert born.note == ""  # a valid birth is untouched; the default stays a str


def test_residual_policy_ceiling_never_receives_a_malformed_residual() -> None:
    """PR-3-FIX — birth prevents a malformed residual from reaching
    ``ResidualPolicy.ceiling``.

    ``ceiling`` assumes every ``residual.kind`` is a ``ResidualKind``
    before calling ``rank_cap``; the birth guard is what makes that
    assumption sound. The carrier that would have made ``rank_cap``
    raise inside the policy engine cannot be constructed at all, and
    every validly born kind has a computable cap.
    """

    with pytest.raises(TypeError):
        Residual(name="malformed", kind="BLOCKING", visible=True)  # type: ignore[arg-type]

    for kind in ResidualKind:
        surface = (Residual(name="declared", kind=kind, visible=True),)
        assert ResidualPolicy.ceiling(surface) is ResidualPolicy.rank_cap(kind)


def test_no_malformed_residual_reaches_gamma_step_9() -> None:
    """PR-3-FIX — *No malformed residual reaches Gamma step 9.*

    The exact malformed carrier from the PR-3 review —
    ``Residual(name="", kind="BLOCKING", visible="yes")`` — is
    refused at birth, so the bare ``TypeError`` it would have raised
    inside step 9's ceiling computation is unreachable and ``Γ``'s
    named-refusal discipline is preserved. A validly born surface
    then walks the full chain to a *named* verdict — never an
    exception.
    """

    with pytest.raises(TypeError):
        Residual(name="", kind="BLOCKING", visible="yes")  # type: ignore[arg-type]

    case = ConstitutionalChainTestCase(
        origin_law="docs/11 §12 Implementation obligations — Residual birth guard",
        branch_name="valid-residual-surface-walks-step-9-without-typeerror",
        constitutional_chain=("Residual", "SlotGraph", "Gamma", "ResidualCeiling"),
        expected_state=ClosureState.PERFORATED_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("TypeError", "CERTIFICATE"),
        max_rank=Rank.HYPOTHESIS,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.8.Implication",
        origin_law_ref=(
            "docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md#12-implementation-obligations"
        ),
        branch_of_origin=(
            "A residual is well-formed at birth or it is never born; "
            "step 9 only ever meets well-formed kinds."
        ),
        forbidden_shortcut_assertions=("Malformed Residual → Gamma step 9",),
    )
    graph = _build_graph(residuals=(_deferrable(),), rank=Rank.HYPOTHESIS)

    verdict = gamma(graph)  # must return a named verdict, never raise

    assert isinstance(verdict, GammaResult)
    assert_constitutional_case(case, _result_from(verdict))
