"""Constitutional tests for PR-12: μ chain operations + Ω residual governance.

Origin: docs/20 §§4–11, docs/23_PRE_WEIGHT_CHAIN_OPERATIONS_LAW.md.

Coverage of the 15 required constitutional tests:

1.  Visible residual is not Ω clearance.
2.  PathGateVerdict is required before path-dependent μ steps.
3.  HIDDEN_FORBIDDEN cannot pass silently.
4.  BLOCKING prevents transition.
5.  DEFERRABLE produces deferred bounded candidate only.
6.  NON_BLOCKING may pass visibly.
7.  EXPLANATORY has no transition authority by itself.
8.  μ operations do not produce WeightFitCandidate.
9.  μ operations do not call or define weigh().
10. WeightReadinessCandidate is not LicensedWeight and not WeightFit.
11. Candidate rank cannot be promoted beyond the PR-12 ceiling.
12. TraceRef remains a reference, not an audit ledger commit.
13. No lexical/samāʿ/qiyās/extra-letter licensing appears in PR-12.
14. Every refusal has a named FailureCode or existing refusal taxonomy.
15. Backward analysis hypotheses are not forward transition licenses.
"""

from __future__ import annotations

import ast
import importlib
import importlib.util
import pathlib

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    MU_CHAIN_RANK_CEILING,
    MuStepResult,
    MuStepState,
    OmegaGovernanceState,
    PathCandidate,
    PathGateProof,
    PathGateState,
    PathGateVerdict,
    PathKind,
    PreWeightPathGate,
    PreWeightSurface,
    ResidualGovernanceVerdict,
    RootStemCandidate,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
    mu_boundary,
    mu_ops,
    mu_original_extra,
    mu_root_stem,
    mu_seq,
    mu_weight_readiness,
    mu_word_carrier,
    omega_governance,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.pre_weight import LetterStanding, OriginalExtraMap

_DOC_23 = "docs/23_PRE_WEIGHT_CHAIN_OPERATIONS_LAW.md"


# ---------------------------------------------------------------------------
# Test fixtures — reuse the same carrier factories as test_weight_carriers.py
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr12-mu-chain-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr12/qatala", kind="DECLARED_ENTRY"),
    }


def _syllable() -> SyllableCandidate:
    return SyllableCandidate(**_base("syllable", "syll-qa", "qa"), units=(("q", "a"),))


def _syllables() -> tuple[SyllableCandidate, ...]:
    return (
        _syllable(),
        SyllableCandidate(**_base("syllable", "syll-ta", "ta"), units=(("t", "a"),)),
        SyllableCandidate(**_base("syllable", "syll-la", "la"), units=(("l", "a"),)),
    )


def _sequence() -> SyllableSequenceCandidate:
    return SyllableSequenceCandidate(
        **_base("syllable_sequence", "seq-qatala", "qa-ta-la"),
        syllables=_syllables(),
    )


def _boundary() -> WordBoundaryCandidate:
    return WordBoundaryCandidate(
        **_base("word_boundary", "wb-qatala", "qatala"), sequence=_sequence()
    )


def _word_carrier() -> WordCarrierCandidate:
    return WordCarrierCandidate(
        **_base("word_carrier", "wc-qatala", "qatala"), bounded_surface=_boundary()
    )


def _path(kind: PathKind = PathKind.ROOT) -> PathCandidate:
    return PathCandidate(
        **_base("path", "path-qatala", "root_path"), kind=kind, carrier=_word_carrier()
    )


def _root_stem() -> RootStemCandidate:
    return RootStemCandidate(**_base("root_stem", "root-qtl", "q-t-l"), path=_path())


def _original_extra() -> OriginalExtraMap:
    return OriginalExtraMap(
        **_base("original_extra_map", "oem-qatala", "qatala"),
        underlying_form="qatala",
        assignments=(
            ("q", LetterStanding.ORIGINAL),
            ("t", LetterStanding.ORIGINAL),
            ("l", LetterStanding.ORIGINAL),
        ),
    )


def _surface() -> PreWeightSurface:
    carrier = _word_carrier()
    return PreWeightSurface(
        **_base("pre_weight_surface", "pws-qatala", "qatala"),
        carrier=carrier,
        path=PathCandidate(
            **_base("path", "path-qatala", "root_path"),
            kind=PathKind.ROOT,
            carrier=carrier,
        ),
        original_extra=_original_extra(),
        operations=_operations(),
    )


def _operations():
    from taaqqul_slot_geometry.weight import OperationTraceCandidate
    return OperationTraceCandidate(
        **_base("operation_trace", "ops-qatala", "declared-steps"),
        steps=("declared_seq", "declared_boundary"),
    )


def _granted_governance() -> ResidualGovernanceVerdict:
    """A GRANTED Ω governance verdict with no residuals."""
    return omega_governance((), Rank.CANDIDATE)


def _path_gate_verdict_approved() -> PathGateVerdict:
    """An APPROVED PathGateVerdict."""
    gate = PreWeightPathGate(name="test_gate", gate_rank=Rank.HYPOTHESIS)
    proof = PathGateProof(
        claimed_kind=PathKind.ROOT,
        evidence_surface="trilateral derivation",
        evidence_rank=Rank.HYPOTHESIS,
        domain="arabic_morphophonology",
    )
    return gate.decide(_word_carrier(), proof)


# ---------------------------------------------------------------------------
# 0. The origin law must be present.
# ---------------------------------------------------------------------------


def test_pr12_constitutional_document_is_present() -> None:
    """docs/13 — PR-12 origin law must exist."""
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    path = repo_root / _DOC_23
    assert path.is_file(), f"missing PR-12 origin document: {_DOC_23}"
    assert path.read_text(encoding="utf-8").strip(), f"PR-12 origin document is empty: {_DOC_23}"


# ---------------------------------------------------------------------------
# 1. Visible residual is not Ω clearance.
# ---------------------------------------------------------------------------


def test_visible_residual_is_not_omega_clearance() -> None:
    """docs/23 §2.3.1 — seeing a residual (PR-11) is not clearing it (PR-12).

    A visible NON_BLOCKING residual passes Ω governance (GRANTED),
    but this does NOT mean the residual is cleared — it remains on
    the verdict's residuals tuple.
    """
    residual = Residual(name="visible_remainder", kind=ResidualKind.NON_BLOCKING, visible=True)
    verdict = omega_governance((residual,), Rank.CANDIDATE)
    # Governance is GRANTED (transition may proceed)
    assert verdict.state is OmegaGovernanceState.GRANTED
    # But the residual is still present — not cleared
    assert len(verdict.residuals) == 1
    assert verdict.residuals[0] is residual
    assert verdict.residuals[0].visible is True


# ---------------------------------------------------------------------------
# 2. PathGateVerdict is required before path-dependent μ steps.
# ---------------------------------------------------------------------------


def test_path_gate_verdict_required_before_mu_root_stem() -> None:
    """docs/23 §3.1.2 — μ_root_stem requires a PathGateVerdict."""
    governance = _granted_governance()
    # Without a PathGateVerdict → REFUSED
    result = mu_root_stem(_path(), "not_a_verdict", governance)  # type: ignore[arg-type]
    assert result.state is MuStepState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # With an unapproved verdict → REFUSED
    rejected_verdict = PathGateVerdict(
        state=PathGateState.REJECTED,
        failure_code=FailureCode.DOMAIN_MISSING,
        approved_kind=None,
        granted_rank=Rank.ZERO,
        residuals=(),
        gate_name="test_gate",
    )
    result = mu_root_stem(_path(), rejected_verdict, governance)
    assert result.state is MuStepState.REFUSED


# ---------------------------------------------------------------------------
# 3. HIDDEN_FORBIDDEN cannot pass silently.
# ---------------------------------------------------------------------------


def test_hidden_forbidden_cannot_pass_silently() -> None:
    """docs/23 §2.3.2 — a HIDDEN_FORBIDDEN residual results in REJECTED."""
    hidden = Residual(name="hidden_danger", kind=ResidualKind.HIDDEN_FORBIDDEN, visible=False)
    verdict = omega_governance((hidden,), Rank.CANDIDATE)
    assert verdict.state is OmegaGovernanceState.REJECTED
    assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL


def test_invisible_residual_cannot_pass_silently() -> None:
    """A residual with visible=False is also caught regardless of kind."""
    invisible = Residual(name="invisible", kind=ResidualKind.NON_BLOCKING, visible=False)
    verdict = omega_governance((invisible,), Rank.CANDIDATE)
    assert verdict.state is OmegaGovernanceState.REJECTED
    assert verdict.failure_code is FailureCode.HIDDEN_RESIDUAL


# ---------------------------------------------------------------------------
# 4. BLOCKING prevents transition.
# ---------------------------------------------------------------------------


def test_blocking_prevents_transition() -> None:
    """docs/23 §2.3.3 — BLOCKING results in BLOCKED, never GRANTED."""
    blocking = Residual(name="blocker", kind=ResidualKind.BLOCKING, visible=True)
    verdict = omega_governance((blocking,), Rank.CANDIDATE)
    assert verdict.state is OmegaGovernanceState.BLOCKED
    assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert verdict.granted_rank is Rank.ZERO


# ---------------------------------------------------------------------------
# 5. DEFERRABLE produces deferred bounded candidate only.
# ---------------------------------------------------------------------------


def test_deferrable_produces_deferred_only() -> None:
    """docs/23 §2.3.4 — DEFERRABLE results in DEFERRED, not GRANTED."""
    deferrable = Residual(name="deferred_item", kind=ResidualKind.DEFERRABLE, visible=True)
    verdict = omega_governance((deferrable,), Rank.CANDIDATE)
    assert verdict.state is OmegaGovernanceState.DEFERRED
    assert verdict.failure_code is not None
    assert verdict.granted_rank is Rank.ZERO


def test_mu_step_with_deferred_governance_produces_deferred_result() -> None:
    """A μ step given DEFERRED governance produces a DEFERRED MuStepResult."""
    deferrable = Residual(name="deferred_item", kind=ResidualKind.DEFERRABLE, visible=True)
    deferred_gov = omega_governance((deferrable,), Rank.CANDIDATE)
    result = mu_seq(_syllables(), deferred_gov)
    assert result.state is MuStepState.DEFERRED


# ---------------------------------------------------------------------------
# 6. NON_BLOCKING may pass visibly.
# ---------------------------------------------------------------------------


def test_non_blocking_may_pass_visibly() -> None:
    """docs/23 §2.3.5 — NON_BLOCKING grants transition, residual stays visible."""
    non_blocking = Residual(name="visible_note", kind=ResidualKind.NON_BLOCKING, visible=True)
    verdict = omega_governance((non_blocking,), Rank.CANDIDATE)
    assert verdict.state is OmegaGovernanceState.GRANTED
    assert verdict.failure_code is None
    assert len(verdict.residuals) == 1
    assert verdict.residuals[0].visible is True


# ---------------------------------------------------------------------------
# 7. EXPLANATORY has no transition authority by itself.
# ---------------------------------------------------------------------------


def test_explanatory_has_no_transition_authority() -> None:
    """docs/23 §2.3.6 — EXPLANATORY grants but carries no authority.

    An explanatory residual is audit-only: it doesn't block and doesn't
    add to the governance decision beyond visibility.
    """
    explanatory = Residual(name="audit_note", kind=ResidualKind.EXPLANATORY, visible=True)
    verdict = omega_governance((explanatory,), Rank.CANDIDATE)
    assert verdict.state is OmegaGovernanceState.GRANTED
    # Explanatory is still present in residuals — visible for audit
    assert len(verdict.residuals) == 1
    assert verdict.residuals[0].kind is ResidualKind.EXPLANATORY


# ---------------------------------------------------------------------------
# 8. μ operations do not produce WeightFitCandidate.
# ---------------------------------------------------------------------------


def test_mu_operations_do_not_produce_weight_fit_candidate() -> None:
    """docs/23 §4 — no μ step produces WeightFitCandidate."""
    governance = _granted_governance()

    # Run the full chain
    seq_result = mu_seq(_syllables(), governance)
    assert seq_result.state is MuStepState.LICENSED
    assert seq_result.output.__class__.__name__ != "WeightFitCandidate"

    boundary_result = mu_boundary(seq_result.output, governance)
    assert boundary_result.state is MuStepState.LICENSED
    assert boundary_result.output.__class__.__name__ != "WeightFitCandidate"

    wc_result = mu_word_carrier(boundary_result.output, governance)
    assert wc_result.state is MuStepState.LICENSED
    assert wc_result.output.__class__.__name__ != "WeightFitCandidate"

    # mu_weight_readiness produces WeightReadinessCandidate, not WeightFit
    readiness_result = mu_weight_readiness(_surface(), governance)
    assert readiness_result.state is MuStepState.LICENSED
    assert isinstance(readiness_result.output, WeightReadinessCandidate)
    assert readiness_result.output.__class__.__name__ != "WeightFitCandidate"


# ---------------------------------------------------------------------------
# 9. μ operations do not call or define weigh().
# ---------------------------------------------------------------------------


def test_mu_chain_module_does_not_define_weigh() -> None:
    """docs/23 §4 — no weigh() in the mu_chain module."""
    spec = importlib.util.find_spec("taaqqul_slot_geometry.weight.mu_chain")
    assert spec is not None and spec.origin is not None
    source = pathlib.Path(spec.origin).read_text(encoding="utf-8")
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            assert node.name != "weigh", (
                "mu_chain module defines weigh() — forbidden by docs/23 §4"
            )
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            assert node.id != "weigh", (
                "mu_chain module binds 'weigh' — forbidden by docs/23 §4"
            )


# ---------------------------------------------------------------------------
# 10. WeightReadinessCandidate is not LicensedWeight and not WeightFit.
# ---------------------------------------------------------------------------


def test_weight_readiness_candidate_is_not_licensed_weight_or_fit() -> None:
    """docs/23 §5 — WeightReadinessCandidate is pre-weighing readiness only."""
    governance = _granted_governance()
    result = mu_weight_readiness(_surface(), governance)
    assert result.state is MuStepState.LICENSED
    output = result.output
    assert isinstance(output, WeightReadinessCandidate)
    # It is NOT a weight fit, NOT licensed weight
    assert output.__class__.__name__ == "WeightReadinessCandidate"
    assert not hasattr(output, "fit")
    assert not hasattr(output, "weight_fit")
    assert not hasattr(output, "licensed_weight")


# ---------------------------------------------------------------------------
# 11. Candidate rank cannot be promoted beyond the PR-12 ceiling.
# ---------------------------------------------------------------------------


def test_rank_cannot_exceed_mu_chain_ceiling() -> None:
    """docs/23 §3.2 — MU_CHAIN_RANK_CEILING is HYPOTHESIS."""
    assert MU_CHAIN_RANK_CEILING is Rank.HYPOTHESIS

    # MuStepResult refuses rank above ceiling
    with pytest.raises(WeightCarrierSchemaError):
        MuStepResult(
            state=MuStepState.LICENSED,
            step_name="test",
            failure_code=None,
            output="something",
            rank=Rank.LICENSED,  # above HYPOTHESIS
            residuals=(),
            trace_ref="test/ref",
        )


def test_mu_seq_output_rank_is_bounded() -> None:
    """The mu_seq output rank is always ≤ MU_CHAIN_RANK_CEILING."""
    governance = _granted_governance()
    result = mu_seq(_syllables(), governance)
    assert result.state is MuStepState.LICENSED
    assert result.rank.value <= MU_CHAIN_RANK_CEILING.value


# ---------------------------------------------------------------------------
# 12. TraceRef remains a reference, not an audit ledger commit.
# ---------------------------------------------------------------------------


def test_trace_ref_remains_reference_not_ledger_commit() -> None:
    """docs/23 §3.1.6 — μ steps preserve trace refs without committing."""
    governance = _granted_governance()
    result = mu_seq(_syllables(), governance)
    assert result.state is MuStepState.LICENSED
    # The trace_ref is a string reference, not a ledger object
    assert isinstance(result.trace_ref, str)
    assert result.trace_ref.strip() != ""
    # The output carrier's trace is still a TraceRef
    assert isinstance(result.output.trace, TraceRef)


# ---------------------------------------------------------------------------
# 13. No lexical/samāʿ/qiyās/extra-letter licensing appears in PR-12.
# ---------------------------------------------------------------------------


def test_no_lexical_samaa_qiyas_in_mu_chain_module() -> None:
    """docs/23 §4 — no lexicon, samāʿ, qiyās, or extra-letter licensing."""
    spec = importlib.util.find_spec("taaqqul_slot_geometry.weight.mu_chain")
    assert spec is not None and spec.origin is not None
    source = pathlib.Path(spec.origin).read_text(encoding="utf-8")

    forbidden_terms = {"Lexicon", "PatternTable", "SamaaEvidence", "QiyasEvidence",
                       "ExtraLetterLicense", "lexicon", "samaa", "qiyas"}

    tree = ast.parse(source)
    bound_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            bound_names.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            bound_names.add(node.id)

    leaked = bound_names & forbidden_terms
    assert not leaked, (
        f"mu_chain module binds forbidden lexical/samāʿ/qiyās names: "
        f"{sorted(leaked)} (docs/23 §4)"
    )


# ---------------------------------------------------------------------------
# 14. Every refusal has a named FailureCode or existing refusal taxonomy.
# ---------------------------------------------------------------------------


def test_every_refusal_has_named_failure_code() -> None:
    """docs/23 §3.1.8 — every refusal maps to a named FailureCode."""
    governance = _granted_governance()

    # Refused: empty syllables
    result = mu_seq((), governance)
    assert result.state is MuStepState.REFUSED
    assert isinstance(result.failure_code, FailureCode)

    # Refused: unlicensed input
    result = mu_boundary("not_a_sequence", governance)  # type: ignore[arg-type]
    assert result.state is MuStepState.REFUSED
    assert isinstance(result.failure_code, FailureCode)

    # Refused: omega blocked
    blocking = Residual(name="blocker", kind=ResidualKind.BLOCKING, visible=True)
    blocked_gov = omega_governance((blocking,), Rank.CANDIDATE)
    result = mu_seq(_syllables(), blocked_gov)
    assert result.state is MuStepState.REFUSED
    assert isinstance(result.failure_code, FailureCode)


# ---------------------------------------------------------------------------
# 15. Backward analysis hypotheses are not forward transition licenses.
# ---------------------------------------------------------------------------


def test_backward_hypotheses_are_not_forward_licenses() -> None:
    """docs/23 — a hypothesis (Rank.HYPOTHESIS) from a past step
    does not license forward transition on its own; it needs Ω
    governance to grant transition authority.

    Specifically: even with a HYPOTHESIS-ranked carrier, if
    governance is BLOCKED, no forward movement occurs.
    """
    blocking = Residual(name="blocker", kind=ResidualKind.BLOCKING, visible=True)
    blocked_gov = omega_governance((blocking,), Rank.HYPOTHESIS)

    # Even though the surface_rank is HYPOTHESIS, the blocking residual
    # prevents forward movement
    assert blocked_gov.state is OmegaGovernanceState.BLOCKED
    assert blocked_gov.granted_rank is Rank.ZERO

    # Using this governance in a μ step — transition is refused
    result = mu_seq(_syllables(), blocked_gov)
    assert result.state is MuStepState.REFUSED


# ---------------------------------------------------------------------------
# Additional: Omega governance verdict schema correctness
# ---------------------------------------------------------------------------


def test_omega_governance_granted_on_empty_residuals() -> None:
    """An empty residual tuple → GRANTED (no constraints)."""
    verdict = omega_governance((), Rank.CANDIDATE)
    assert verdict.state is OmegaGovernanceState.GRANTED
    assert verdict.failure_code is None
    assert verdict.residuals == ()
    assert verdict.granted_rank.value <= MU_CHAIN_RANK_CEILING.value


def test_omega_governance_verdict_schema_refuses_inconsistent_state() -> None:
    """A GRANTED verdict with a failure_code is constitutionally invalid."""
    with pytest.raises(WeightCarrierSchemaError):
        ResidualGovernanceVerdict(
            state=OmegaGovernanceState.GRANTED,
            failure_code=FailureCode.HIDDEN_RESIDUAL,
            residuals=(),
            granted_rank=Rank.CANDIDATE,
        )

    # A non-GRANTED verdict without failure_code is also invalid
    with pytest.raises(WeightCarrierSchemaError):
        ResidualGovernanceVerdict(
            state=OmegaGovernanceState.BLOCKED,
            failure_code=None,
            residuals=(),
            granted_rank=Rank.ZERO,
        )


# ---------------------------------------------------------------------------
# Additional: Full μ chain integration test
# ---------------------------------------------------------------------------


def test_full_mu_chain_produces_weight_readiness() -> None:
    """The full μ chain from syllables to weight readiness
    produces a licensed WeightReadinessCandidate when governance
    is GRANTED at every step."""
    gov = _granted_governance()

    # μ_seq
    seq_result = mu_seq(_syllables(), gov)
    assert seq_result.state is MuStepState.LICENSED

    # μ_boundary
    bnd_result = mu_boundary(seq_result.output, gov)
    assert bnd_result.state is MuStepState.LICENSED

    # μ_word_carrier
    wc_result = mu_word_carrier(bnd_result.output, gov)
    assert wc_result.state is MuStepState.LICENSED

    # μ_root_stem (requires path gate verdict)
    carrier = wc_result.output
    gate = PreWeightPathGate(name="test_path_gate", gate_rank=Rank.HYPOTHESIS)
    proof = PathGateProof(
        claimed_kind=PathKind.ROOT,
        evidence_surface="trilateral derivation evidence",
        evidence_rank=Rank.HYPOTHESIS,
        domain="arabic_morphophonology",
    )
    path_verdict = gate.decide(carrier, proof)
    assert path_verdict.state is PathGateState.APPROVED

    path_cand = PathCandidate(
        **{
            "value": carrier.value,
            "type": "path",
            "origin": carrier.origin,
            "identity": f"path-{carrier.identity}",
            "domain": carrier.domain,
            "scope": carrier.scope,
            "rank": path_verdict.granted_rank,
            "residuals": (),
            "trace": carrier.trace,
        },
        kind=path_verdict.approved_kind,
        carrier=carrier,
    )

    root_result = mu_root_stem(path_cand, path_verdict, gov)
    assert root_result.state is MuStepState.LICENSED

    # μ_original_extra
    oem_result = mu_original_extra(
        form="qatala",
        assignments=(("q", "ORIGINAL"), ("t", "ORIGINAL"), ("l", "ORIGINAL")),
        source_carrier=root_result.output,
        governance=gov,
    )
    assert oem_result.state is MuStepState.LICENSED

    # μ_ops
    ops_result = mu_ops(
        steps=("syllable_sequencing", "boundary_marking", "path_gating"),
        source_carrier=oem_result.output,
        governance=gov,
    )
    assert ops_result.state is MuStepState.LICENSED

    # μ_weight_readiness — assemble the surface
    surface = PreWeightSurface(
        value=carrier.value,
        type="pre_weight_surface",
        origin=carrier.origin,
        identity=f"pws-{carrier.identity}",
        domain=carrier.domain,
        scope=carrier.scope,
        rank=Rank.CANDIDATE,
        residuals=(),
        trace=carrier.trace,
        carrier=carrier,
        path=path_cand,
        original_extra=oem_result.output,
        operations=ops_result.output,
    )
    wr_result = mu_weight_readiness(surface, gov)
    assert wr_result.state is MuStepState.LICENSED
    assert isinstance(wr_result.output, WeightReadinessCandidate)
