"""PR-2A — Constitutional construction-refusal tests for SlotGraph.

This module exercises the construction surface tightened in PR-2A
(`docs/17_SLOTGRAPH_GENERATION_LAW.md` §§2–3, §5; `docs/15` §5).
Every test wires through :class:`ConstitutionalChainTestCase` (or
the simpler :class:`ConstitutionalTestCase` where chain context does
not apply) and asserts the named :class:`FailureCode` rather than a
bare :class:`TypeError`. PR-2A removed the previous
``pytest.raises(TypeError)`` shape from the suite because that shape
treated a Python schema error as a constitutional verdict — exactly
what `docs/12 §4` (*every refusal must be named*) and `docs/17 §5
totality` forbid.

Coverage:

1. ``test_slot_boundary_requires_non_empty_refusal_codes``
2. ``test_opening_policy_requires_non_empty_allowed_potentials``
3. ``test_center_requires_identity_claim``
4. ``test_center_requires_trace_ref``
5. ``test_declared_entry_requires_entry_boundary``
6. ``test_non_declared_entry_rejects_entry_boundary``
7. ``test_entry_boundary_requires_representation_status``,
   ``..._ontological_status``, ``..._sound_status``,
   ``..._meaning_status``
8. ``test_entry_boundary_rejects_empty_required_fields``
9. ``test_missing_boundary_returns_named_refusal_not_bare_typeerror``
10. ``test_construction_success_round_trips_through_gamma``
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import (
    Center,
    ClosureState,
    ConstructionResult,
    EntryBoundary,
    FailureCode,
    GenerationSource,
    Layer,
    OpeningPolicy,
    OutputBoundary,
    Rank,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotGraphSchemaError,
    SlotState,
    TraceRef,
    gamma,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

# ---------------------------------------------------------------------------
# Carrier factories — produce constitutionally complete carriers so every
# test isolates exactly one axis of failure.
# ---------------------------------------------------------------------------


def _boundary() -> SlotBoundary:
    return SlotBoundary(
        domain="reasoning",
        scope="slot-test",
        refusal_codes=(FailureCode.BOUNDARY_MISSING,),
    )


def _opening() -> OpeningPolicy:
    return OpeningPolicy(allowed_potentials=frozenset({"yes", "no"}))


def _filled_slot() -> Slot:
    return Slot(
        name="answer",
        value_state=SlotState.FILLED,
        boundary=_boundary(),
        opening=_opening(),
        required=True,
        value="yes",
    )


def _trace_ref() -> TraceRef:
    return TraceRef(anchor="trace://Q1", kind="DECLARED_ENTRY")


def _center() -> Center:
    return Center(
        identity_claim="Q1",
        domain="reasoning",
        scope="slot-test",
        trace_ref=_trace_ref(),
    )


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


def _construct(
    *,
    center: Center | None = None,
    boundary: SlotBoundary | None = None,
    entry_boundary: EntryBoundary | None = None,
    generation_source: GenerationSource = GenerationSource.DECLARED_ENTRY,
    output_boundary: OutputBoundary | None = None,
) -> ConstructionResult:
    """Helper: invoke the named construction surface with sensible defaults.

    Pass ``None`` for the axis a test wants to refuse; all other
    arguments default to constitutionally complete carriers.
    """

    return SlotGraph.construct(
        center=center if center is not None else _center(),
        slots=(_filled_slot(),),
        boundary=boundary if boundary is not None else _boundary(),
        residuals=(),
        rank=Rank.TRACE,
        output_boundary=output_boundary
        if output_boundary is not None
        else _output_within(),
        generation_source=generation_source,
        entry_boundary=entry_boundary
        if entry_boundary is not None
        else _entry_boundary(),
    )


def _chain_case_for_refusal(
    *,
    branch: str,
    code: FailureCode,
    origin_law: str,
    origin_ref: str,
    chain_position: str,
    branch_of_origin: str,
    forbidden_shortcuts: tuple[str, ...] = ("ConstructionRefusal → SilentSuccess",),
) -> ConstitutionalChainTestCase:
    """Shared chain-test scaffold for construction-refusal cases."""

    return ConstitutionalChainTestCase(
        origin_law=origin_law,
        branch_name=branch,
        constitutional_chain=("SlotGraph", "ConstructionSurface", "NamedRefusal"),
        expected_state=ClosureState.INVALID,
        expected_failure_code=code,
        forbidden_outputs=(
            "APPROVED_OUTPUT",
            "MINIMALLY_CLOSED",
            "PERFORATED_CLOSED",
        ),
        max_rank=Rank.TRACE,
        required_trace=False,
        required_residual_visibility=False,
        chain_position=chain_position,
        origin_law_ref=origin_ref,
        branch_of_origin=branch_of_origin,
        forbidden_shortcut_assertions=forbidden_shortcuts,
    )


def _refusal_to_chain_result(result: ConstructionResult) -> ConstitutionalChainResult:
    """Project a :class:`ConstructionResult` refusal onto the harness type."""

    return ConstitutionalChainResult(
        state=ClosureState.INVALID,
        failure_code=result.failure_code,
        rank=Rank.TRACE,
        residual_visibility=False,
        trace_present=False,
    )


# ---------------------------------------------------------------------------
# 1. SlotBoundary requires non-empty refusal_codes (docs/11 §3, docs/17 §3).
# ---------------------------------------------------------------------------


def test_slot_boundary_requires_non_empty_refusal_codes() -> None:
    """A boundary without declared refusals is constitutionally incomplete."""

    with pytest.raises(SlotGraphSchemaError) as excinfo:
        SlotBoundary(
            domain="reasoning",
            scope="slot-test",
            refusal_codes=(),
        )

    message = str(excinfo.value)
    assert FailureCode.BOUNDARY_MISSING.value in message
    assert "non-empty" in message


# ---------------------------------------------------------------------------
# 2. OpeningPolicy requires non-empty allowed_potentials of non-empty strings.
# ---------------------------------------------------------------------------


def test_opening_policy_requires_non_empty_allowed_potentials() -> None:
    """``allowed_potentials`` is the licensed domain — empty is a refusal."""

    with pytest.raises(SlotGraphSchemaError) as empty_excinfo:
        OpeningPolicy(allowed_potentials=frozenset())
    assert FailureCode.UNLICENSED_OPENING.value in str(empty_excinfo.value)

    with pytest.raises(SlotGraphSchemaError) as blank_excinfo:
        OpeningPolicy(allowed_potentials=frozenset({""}))
    assert FailureCode.UNLICENSED_OPENING.value in str(blank_excinfo.value)


# ---------------------------------------------------------------------------
# 3. Center requires a non-empty identity_claim (docs/17 §3).
# ---------------------------------------------------------------------------


def test_center_requires_identity_claim() -> None:
    """A Center without an identity claim is IDENTITY_BROKEN at birth.

    The direct-construction path raises :class:`SlotGraphSchemaError`
    whose message names :attr:`FailureCode.IDENTITY_BROKEN`. The
    named construction surface refuses the matching presence-level
    gap (``center is None``) with :attr:`FailureCode.CENTER_MISSING`,
    proving that no construction path silently promotes a hollow
    identity into a graph.
    """

    with pytest.raises(SlotGraphSchemaError) as excinfo:
        Center(
            identity_claim="",
            domain="reasoning",
            scope="slot-test",
            trace_ref=_trace_ref(),
        )
    assert FailureCode.IDENTITY_BROKEN.value in str(excinfo.value)

    # And the construction surface refuses the presence-level gap as
    # a value, not as an exception.
    refusal = SlotGraph.construct(
        center=None,
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=(),
        rank=Rank.TRACE,
        output_boundary=_output_within(),
        generation_source=GenerationSource.DECLARED_ENTRY,
        entry_boundary=_entry_boundary(),
    )
    case = _chain_case_for_refusal(
        branch="center-missing",
        code=FailureCode.CENTER_MISSING,
        origin_law="docs/17 §3 — Center missing → CENTER_MISSING",
        origin_ref="docs/17_SLOTGRAPH_GENERATION_LAW.md#3-the-constructor-refusal-table",
        chain_position="IdentityChain.link.1.Identity",
        branch_of_origin="No SlotGraph without a Center.",
    )
    assert refusal.is_refusal is True
    assert refusal.graph is None
    assert refusal.failure_code is FailureCode.CENTER_MISSING
    assert_constitutional_case(case, _refusal_to_chain_result(refusal))


# ---------------------------------------------------------------------------
# 4. Center requires a real TraceRef (docs/17 §3 — TRACE_MISSING).
# ---------------------------------------------------------------------------


def test_center_requires_trace_ref() -> None:
    """A Center with ``trace_ref=None`` is refused; so is a hollow anchor."""

    with pytest.raises(SlotGraphSchemaError) as none_excinfo:
        Center(
            identity_claim="Q1",
            domain="reasoning",
            scope="slot-test",
            trace_ref=None,  # type: ignore[arg-type]
        )
    assert FailureCode.TRACE_MISSING.value in str(none_excinfo.value)

    # A TraceRef with an empty anchor cannot be born either, so a
    # Center cannot be smuggled in carrying a hollow trace.
    with pytest.raises(SlotGraphSchemaError) as empty_excinfo:
        TraceRef(anchor="", kind="DECLARED_ENTRY")
    assert FailureCode.TRACE_MISSING.value in str(empty_excinfo.value)


# ---------------------------------------------------------------------------
# 5. DECLARED_ENTRY source requires an EntryBoundary (docs/15 §5).
# ---------------------------------------------------------------------------


def test_declared_entry_requires_entry_boundary() -> None:
    """No declared textual entry without its EntryBoundary."""

    refusal = _construct(
        generation_source=GenerationSource.DECLARED_ENTRY,
        entry_boundary=_entry_boundary(),  # default, then we override below
    )
    # Sanity: the default helper succeeds when entry_boundary is
    # present, so the next call isolates exactly the missing field.
    assert refusal.is_refusal is False

    refusal = SlotGraph.construct(
        center=_center(),
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=(),
        rank=Rank.TRACE,
        output_boundary=_output_within(),
        generation_source=GenerationSource.DECLARED_ENTRY,
        entry_boundary=None,
    )
    case = _chain_case_for_refusal(
        branch="declared-entry-without-entry-boundary",
        code=FailureCode.BOUNDARY_MISSING,
        origin_law="docs/15 §5 — declared textual entry requires EntryBoundary",
        origin_ref="docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md#5-boundary-obligations-on-every-textual-entry",
        chain_position="IdentityChain.link.1.Identity",
        branch_of_origin="A declared textual entry without EntryBoundary is refused.",
    )
    assert refusal.is_refusal is True
    assert refusal.failure_code is FailureCode.BOUNDARY_MISSING
    assert refusal.graph is None
    assert_constitutional_case(case, _refusal_to_chain_result(refusal))

    # Direct dataclass construction refuses the same gap with a
    # named schema error (the Python-level guard, not the value path).
    with pytest.raises(SlotGraphSchemaError) as excinfo:
        SlotGraph(
            center=_center(),
            slots=(_filled_slot(),),
            boundary=_boundary(),
            residuals=(),
            rank=Rank.TRACE,
            output_boundary=_output_within(),
            generation_source=GenerationSource.DECLARED_ENTRY,
            entry_boundary=None,
        )
    assert FailureCode.BOUNDARY_MISSING.value in str(excinfo.value)


def test_non_declared_entry_rejects_entry_boundary() -> None:
    """Non-DECLARED_ENTRY sources must not carry an EntryBoundary."""

    # CANDIDATE is one of the other licensed generation sources
    with pytest.raises(SlotGraphSchemaError) as excinfo:
        SlotGraph(
            center=_center(),
            slots=(_filled_slot(),),
            boundary=_boundary(),
            residuals=(),
            rank=Rank.TRACE,
            output_boundary=_output_within(),
            generation_source=GenerationSource.CANDIDATE,
            entry_boundary=_entry_boundary(),  # forbidden for this source
        )
    assert "entry_boundary must be None unless generation_source is DECLARED_ENTRY" in str(
        excinfo.value
    )
    assert FailureCode.BOUNDARY_MISSING.value in str(excinfo.value)

    # TRANSITION_VERDICT is the third licensed generation source
    with pytest.raises(SlotGraphSchemaError) as excinfo:
        SlotGraph(
            center=_center(),
            slots=(_filled_slot(),),
            boundary=_boundary(),
            residuals=(),
            rank=Rank.TRACE,
            output_boundary=_output_within(),
            generation_source=GenerationSource.TRANSITION_VERDICT,
            entry_boundary=_entry_boundary(),  # forbidden for this source
        )
    assert "entry_boundary must be None unless generation_source is DECLARED_ENTRY" in str(
        excinfo.value
    )
    assert FailureCode.BOUNDARY_MISSING.value in str(excinfo.value)


# ---------------------------------------------------------------------------
# 6. EntryBoundary mandatory fields (docs/15 §5).
# ---------------------------------------------------------------------------


def _entry_boundary_kwargs() -> dict[str, str]:
    return {
        "declared_entry_kind": "ARABIC_VOCALIZED_TEXT",
        "representation_status": "REPRESENTATIONAL_OF_PRIOR",
        "ontological_status": "NOT_AN_ORIGIN",
        "sound_status": "NOT_A_SOUND",
        "meaning_status": "NOT_A_MEANING",
        "prior_trace_status": "OUT_OF_CURRENT_EXECUTION",
        "produces_only": "TEXT_TRACE_CANDIDATE",
    }


def test_entry_boundary_requires_representation_status() -> None:
    """``TextEntry`` is representational — the field must be declared."""

    kwargs = _entry_boundary_kwargs()
    kwargs["representation_status"] = ""
    with pytest.raises(SlotGraphSchemaError) as excinfo:
        EntryBoundary(**kwargs)
    message = str(excinfo.value)
    assert "representation_status" in message
    assert FailureCode.BOUNDARY_MISSING.value in message


def test_entry_boundary_requires_ontological_status() -> None:
    """``TextEntry`` is not an ontological origin — the field must be declared."""

    kwargs = _entry_boundary_kwargs()
    kwargs["ontological_status"] = ""
    with pytest.raises(SlotGraphSchemaError) as excinfo:
        EntryBoundary(**kwargs)
    assert "ontological_status" in str(excinfo.value)


def test_entry_boundary_requires_sound_status() -> None:
    """``TextEntry`` is not a sound — the field must be declared."""

    kwargs = _entry_boundary_kwargs()
    kwargs["sound_status"] = ""
    with pytest.raises(SlotGraphSchemaError) as excinfo:
        EntryBoundary(**kwargs)
    assert "sound_status" in str(excinfo.value)


def test_entry_boundary_requires_meaning_status() -> None:
    """``TextEntry`` is not a meaning — the field must be declared."""

    kwargs = _entry_boundary_kwargs()
    kwargs["meaning_status"] = ""
    with pytest.raises(SlotGraphSchemaError) as excinfo:
        EntryBoundary(**kwargs)
    assert "meaning_status" in str(excinfo.value)


# ---------------------------------------------------------------------------
# 7. Defence in depth — empty/whitespace value on any field is refused.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "field_name",
    sorted(_entry_boundary_kwargs().keys()),
)
def test_entry_boundary_rejects_empty_required_fields(field_name: str) -> None:
    """Every docs/15 §5 field rejects empty *and* whitespace-only values."""

    for blank in ("", "   "):
        kwargs = _entry_boundary_kwargs()
        kwargs[field_name] = blank
        with pytest.raises(SlotGraphSchemaError) as excinfo:
            EntryBoundary(**kwargs)
        message = str(excinfo.value)
        assert field_name in message
        assert FailureCode.BOUNDARY_MISSING.value in message


# ---------------------------------------------------------------------------
# 8. Missing boundary → named refusal, never a bare TypeError.
# ---------------------------------------------------------------------------


def test_missing_boundary_returns_named_refusal_not_bare_typeerror() -> None:
    """docs/17 §5 totality — boundary missing surfaces as a value, not an exception.

    The named construction surface returns a
    :class:`ConstructionResult` carrying
    :attr:`FailureCode.BOUNDARY_MISSING`. PR-2A explicitly removes
    the prior ``pytest.raises(TypeError)`` shape that conflated a
    Python schema error with a constitutional refusal.
    """

    refusal = SlotGraph.construct(
        center=_center(),
        slots=(_filled_slot(),),
        boundary=None,
        residuals=(),
        rank=Rank.TRACE,
        output_boundary=_output_within(),
        generation_source=GenerationSource.DECLARED_ENTRY,
        entry_boundary=_entry_boundary(),
    )

    case = _chain_case_for_refusal(
        branch="boundary-missing-named-refusal",
        code=FailureCode.BOUNDARY_MISSING,
        origin_law="docs/17 §3 — Boundary missing → BOUNDARY_MISSING",
        origin_ref="docs/17_SLOTGRAPH_GENERATION_LAW.md#3-the-constructor-refusal-table",
        chain_position="IdentityChain.link.1.Identity",
        branch_of_origin="No SlotGraph without a Boundary; refusal is a VALUE.",
        forbidden_shortcuts=(
            "ConstructionRefusal → SilentSuccess",
            "BareTypeError → ConstitutionalRefusal",
        ),
    )

    assert isinstance(refusal, ConstructionResult)
    assert refusal.is_refusal is True
    assert refusal.graph is None
    assert refusal.failure_code is FailureCode.BOUNDARY_MISSING
    assert_constitutional_case(case, _refusal_to_chain_result(refusal))


# ---------------------------------------------------------------------------
# 9. Positive: construct + gamma round-trip yields MINIMALLY_CLOSED.
# ---------------------------------------------------------------------------


def test_construction_success_round_trips_through_gamma() -> None:
    """A fully-formed graph constructs cleanly and Γ closes it.

    The construction surface succeeds (``failure_code is None``,
    ``graph`` is a :class:`SlotGraph`), and the resulting graph
    flows through :func:`gamma` to a closure verdict
    (:attr:`ClosureState.MINIMALLY_CLOSED`).
    """

    result = _construct()
    assert isinstance(result, ConstructionResult)
    assert result.is_refusal is False
    assert result.failure_code is None
    assert isinstance(result.graph, SlotGraph)

    verdict = gamma(result.graph)

    case = ConstitutionalChainTestCase(
        origin_law="docs/17 §6 — construction success ⇒ Γ may close",
        branch_name="construction-success-round-trip",
        constitutional_chain=(
            "SlotGraph",
            "ConstructionSurface",
            "Gamma",
            "Closure",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "CERTIFICATE",
            "CANDIDATE_WITH_HIDDEN_RESIDUAL",
        ),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="IdentityChain.link.7.Closure",
        origin_law_ref="docs/17_SLOTGRAPH_GENERATION_LAW.md#6-relationship-to-γ",
        branch_of_origin=(
            "Construction succeeded; Γ then closes minimally."
        ),
        forbidden_shortcut_assertions=(
            "Construction → Truth",
            "Closure → Certificate",
        ),
    )

    chain_result = ConstitutionalChainResult(
        state=verdict.state,
        failure_code=verdict.failure_code,
        rank=verdict.rank,
        residual_visibility=verdict.residual_visibility,
        trace_present=bool(verdict.trace_event_candidate.parent_anchor),
    )
    assert_constitutional_case(case, chain_result)


# ---------------------------------------------------------------------------
# 10/11. EntryBoundary is forbidden for non-DECLARED_ENTRY sources
# (PR-2A-FIX; docs/15 §5, docs/17 §1).
# ---------------------------------------------------------------------------


def test_candidate_source_rejects_entry_boundary() -> None:
    """A CANDIDATE source must not carry a declared textual EntryBoundary.

    docs/15 §5 binds the ``EntryBoundary`` to the declared textual
    entry; a CANDIDATE source carries its boundary in the prior graph
    (docs/17 §1). PR-2A-FIX refuses the forbidden presence at
    construction time so a textual entry can never be conflated with
    a candidate.
    """

    # Sanity: the same CANDIDATE construction succeeds without an
    # entry_boundary, so the refusal below isolates exactly the
    # forbidden presence.
    sane = SlotGraph.construct(
        center=_center(),
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=(),
        rank=Rank.TRACE,
        output_boundary=_output_within(),
        generation_source=GenerationSource.CANDIDATE,
        entry_boundary=None,
    )
    assert sane.is_refusal is False

    result = SlotGraph.construct(
        center=_center(),
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=(),
        rank=Rank.TRACE,
        output_boundary=_output_within(),
        generation_source=GenerationSource.CANDIDATE,
        entry_boundary=_entry_boundary(),
    )
    case = _chain_case_for_refusal(
        branch="candidate-source-rejects-entry-boundary",
        code=FailureCode.BOUNDARY_MISSING,
        origin_law="docs/15 §5 — EntryBoundary belongs to the declared textual entry only",
        origin_ref="docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md#5-boundary-obligations-on-every-textual-entry",
        chain_position="IdentityChain.link.1.Identity",
        branch_of_origin="A CANDIDATE source must not carry an EntryBoundary.",
        forbidden_shortcuts=(
            "ConstructionRefusal → SilentSuccess",
            "DeclaredEntryBoundary → CandidateSource",
        ),
    )
    assert result.is_refusal
    assert result.graph is None
    assert result.failure_code is FailureCode.BOUNDARY_MISSING
    assert_constitutional_case(case, _refusal_to_chain_result(result))

    # Direct dataclass construction refuses the same forbidden
    # presence with a named schema error (the Python-level guard).
    with pytest.raises(
        SlotGraphSchemaError, match="must be None unless generation_source"
    ):
        SlotGraph(
            center=_center(),
            slots=(_filled_slot(),),
            boundary=_boundary(),
            residuals=(),
            rank=Rank.TRACE,
            output_boundary=_output_within(),
            generation_source=GenerationSource.CANDIDATE,
            entry_boundary=_entry_boundary(),
        )


def test_transition_verdict_source_rejects_entry_boundary() -> None:
    """A TRANSITION_VERDICT source must not carry an EntryBoundary.

    The boundary of a TRANSITION_VERDICT source lives in the gate
    verdict (docs/17 §1), never in a declared textual entry boundary
    (docs/15 §5). PR-2A-FIX refuses the forbidden presence at
    construction time so a textual entry can never be conflated with
    a transition verdict.
    """

    # Sanity: the same TRANSITION_VERDICT construction succeeds
    # without an entry_boundary, so the refusal below isolates
    # exactly the forbidden presence.
    sane = SlotGraph.construct(
        center=_center(),
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=(),
        rank=Rank.TRACE,
        output_boundary=_output_within(),
        generation_source=GenerationSource.TRANSITION_VERDICT,
        entry_boundary=None,
    )
    assert sane.is_refusal is False

    result = SlotGraph.construct(
        center=_center(),
        slots=(_filled_slot(),),
        boundary=_boundary(),
        residuals=(),
        rank=Rank.TRACE,
        output_boundary=_output_within(),
        generation_source=GenerationSource.TRANSITION_VERDICT,
        entry_boundary=_entry_boundary(),
    )
    case = _chain_case_for_refusal(
        branch="transition-verdict-source-rejects-entry-boundary",
        code=FailureCode.BOUNDARY_MISSING,
        origin_law="docs/15 §5 — EntryBoundary belongs to the declared textual entry only",
        origin_ref="docs/15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md#5-boundary-obligations-on-every-textual-entry",
        chain_position="IdentityChain.link.1.Identity",
        branch_of_origin="A TRANSITION_VERDICT source must not carry an EntryBoundary.",
        forbidden_shortcuts=(
            "ConstructionRefusal → SilentSuccess",
            "DeclaredEntryBoundary → TransitionVerdictSource",
        ),
    )
    assert result.is_refusal
    assert result.graph is None
    assert result.failure_code is FailureCode.BOUNDARY_MISSING
    assert_constitutional_case(case, _refusal_to_chain_result(result))

    # Direct dataclass construction refuses the same forbidden
    # presence with a named schema error (the Python-level guard).
    with pytest.raises(
        SlotGraphSchemaError, match="must be None unless generation_source"
    ):
        SlotGraph(
            center=_center(),
            slots=(_filled_slot(),),
            boundary=_boundary(),
            residuals=(),
            rank=Rank.TRACE,
            output_boundary=_output_within(),
            generation_source=GenerationSource.TRANSITION_VERDICT,
            entry_boundary=_entry_boundary(),
        )
