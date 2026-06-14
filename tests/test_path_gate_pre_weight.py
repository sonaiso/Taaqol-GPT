"""Constitutional tests for PR-11 — the pre-weight path gate (docs/22).

PR-10 gave the carrier.
PR-10B forbade the carrier from claiming a verdict.
PR-11 establishes the path court.

This test file proves:

1. **PathGateProof birth guards** — a proof without evidence, wrong
   kind, or missing domain is refused at birth.
2. **PathGateVerdict invariants** — approved iff no failure code,
   refusals carry named FailureCode and grant nothing.
3. **PreWeightPathGate.decide** — the full seven-step decision:
   type guard, domain match, evidence presence, preventer check,
   residual check, rank bound, approval.
4. **Negative constitutional tests** — PathKind ≠ PathGateProof,
   carrier declaration ≠ gate verdict, no weighing, no meaning,
   no Ω judgment, no forbidden fields on gate structures.
5. **All seven PathKind members through the gate** — each path kind
   is independently decidable.
6. **Forbidden path jumps** — carrier-as-verdict, missing evidence,
   domain mismatch, competing preventers.
7. **docs/22 origin document is present** — static guard.

Disciplines: these are negative-shape tests and birth-guard tests
under the PR-2 construction-test discipline (``pytest.raises`` for
birth refusals, field-set assertions for forbidden-field checks, and
verdict-state assertions for gate decisions).
"""

from __future__ import annotations

import dataclasses
import pathlib

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    BIRTH_RANK_CEILING,
    PathKind,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.path_gate import (
    PATH_GATE_RANK_CEILING,
    PathGateProof,
    PathGateState,
    PathGateVerdict,
    PreWeightPathGate,
)

# ---------------------------------------------------------------------------
# Carrier factories (reused from test_carrier_not_verdict.py shape)
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr11-path-gate-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr11/qatala", kind="DECLARED_ENTRY"),
    }


def _syllable() -> SyllableCandidate:
    return SyllableCandidate(**_base("syllable", "syll-qa", "qa"), units=(("q", "a"),))


def _sequence() -> SyllableSequenceCandidate:
    return SyllableSequenceCandidate(
        **_base("syllable_sequence", "seq-qatala", "qa-ta-la"),
        syllables=(
            _syllable(),
            SyllableCandidate(**_base("syllable", "syll-ta", "ta"), units=(("t", "a"),)),
            SyllableCandidate(**_base("syllable", "syll-la", "la"), units=(("l", "a"),)),
        ),
    )


def _boundary() -> WordBoundaryCandidate:
    return WordBoundaryCandidate(
        **_base("word_boundary", "wb-qatala", "qatala"), sequence=_sequence()
    )


def _word_carrier(
    domain: str = "arabic_morphophonology",
    residuals: tuple[Residual, ...] = (),
) -> WordCarrierCandidate:
    base = _base("word_carrier", "wc-qatala", "qatala")
    base["domain"] = domain
    base["residuals"] = residuals
    return WordCarrierCandidate(**base, bounded_surface=_boundary())


def _gate(
    name: str = "pre_weight_path_gate",
    gate_rank: Rank = Rank.HYPOTHESIS,
) -> PreWeightPathGate:
    return PreWeightPathGate(name=name, gate_rank=gate_rank)


def _proof(
    kind: PathKind = PathKind.ROOT,
    evidence: str = "root morphological evidence",
    rank: Rank = Rank.CANDIDATE,
    domain: str = "arabic_morphophonology",
) -> PathGateProof:
    return PathGateProof(
        claimed_kind=kind,
        evidence_surface=evidence,
        evidence_rank=rank,
        domain=domain,
    )


# ===================================================================
# 1. PathGateProof birth guards
# ===================================================================


class TestPathGateProofBirth:
    """docs/22 §4 — PathGateProof birth guards."""

    def test_proof_with_valid_inputs(self) -> None:
        proof = _proof()
        assert proof.claimed_kind is PathKind.ROOT
        assert proof.evidence_surface == "root morphological evidence"
        assert proof.evidence_rank is Rank.CANDIDATE
        assert proof.domain == "arabic_morphophonology"

    def test_proof_with_empty_evidence_surface_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="evidence_surface"):
            PathGateProof(
                claimed_kind=PathKind.ROOT,
                evidence_surface="  ",
                evidence_rank=Rank.CANDIDATE,
                domain="arabic_morphophonology",
            )

    def test_proof_with_non_pathkind_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="claimed_kind"):
            PathGateProof(
                claimed_kind="ROOT",  # type: ignore[arg-type]
                evidence_surface="evidence",
                evidence_rank=Rank.CANDIDATE,
                domain="arabic_morphophonology",
            )

    def test_proof_with_non_rank_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="evidence_rank"):
            PathGateProof(
                claimed_kind=PathKind.ROOT,
                evidence_surface="evidence",
                evidence_rank="HIGH",  # type: ignore[arg-type]
                domain="arabic_morphophonology",
            )

    def test_proof_with_empty_domain_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="domain"):
            PathGateProof(
                claimed_kind=PathKind.ROOT,
                evidence_surface="evidence",
                evidence_rank=Rank.CANDIDATE,
                domain="",
            )


# ===================================================================
# 2. PathGateVerdict invariants
# ===================================================================


class TestPathGateVerdictInvariants:
    """docs/22 §5 — PathGateVerdict invariants."""

    def test_approved_verdict_valid(self) -> None:
        v = PathGateVerdict(
            state=PathGateState.APPROVED,
            failure_code=None,
            approved_kind=PathKind.ROOT,
            granted_rank=Rank.CANDIDATE,
            residuals=(),
            gate_name="test_gate",
        )
        assert v.state is PathGateState.APPROVED
        assert v.failure_code is None
        assert v.approved_kind is PathKind.ROOT

    def test_approved_verdict_with_failure_code_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="APPROVED.*FailureCode"):
            PathGateVerdict(
                state=PathGateState.APPROVED,
                failure_code=FailureCode.GATE_REQUIRED,
                approved_kind=PathKind.ROOT,
                granted_rank=Rank.CANDIDATE,
                residuals=(),
                gate_name="test_gate",
            )

    def test_approved_verdict_without_kind_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="approved_kind"):
            PathGateVerdict(
                state=PathGateState.APPROVED,
                failure_code=None,
                approved_kind=None,
                granted_rank=Rank.CANDIDATE,
                residuals=(),
                gate_name="test_gate",
            )

    def test_refusal_verdict_without_failure_code_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="named FailureCode"):
            PathGateVerdict(
                state=PathGateState.REJECTED,
                failure_code=None,
                approved_kind=None,
                granted_rank=Rank.ZERO,
                residuals=(),
                gate_name="test_gate",
            )

    def test_refusal_verdict_with_approved_kind_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="approved_kind"):
            PathGateVerdict(
                state=PathGateState.REJECTED,
                failure_code=FailureCode.DOMAIN_MISSING,
                approved_kind=PathKind.ROOT,
                granted_rank=Rank.ZERO,
                residuals=(),
                gate_name="test_gate",
            )

    def test_refusal_verdict_with_nonzero_rank_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="Rank.ZERO"):
            PathGateVerdict(
                state=PathGateState.REJECTED,
                failure_code=FailureCode.DOMAIN_MISSING,
                approved_kind=None,
                granted_rank=Rank.CANDIDATE,
                residuals=(),
                gate_name="test_gate",
            )

    def test_unnamed_gate_refused(self) -> None:
        with pytest.raises(WeightCarrierSchemaError, match="gate_name"):
            PathGateVerdict(
                state=PathGateState.APPROVED,
                failure_code=None,
                approved_kind=PathKind.ROOT,
                granted_rank=Rank.CANDIDATE,
                residuals=(),
                gate_name="",
            )


# ===================================================================
# 3. PreWeightPathGate birth guards
# ===================================================================


class TestPreWeightPathGateBirth:
    """docs/22 — gate birth guards."""

    def test_gate_with_valid_inputs(self) -> None:
        gate = _gate()
        assert gate.name == "pre_weight_path_gate"
        assert gate.gate_rank is Rank.HYPOTHESIS

    def test_gate_unnamed_refused(self) -> None:
        with pytest.raises(TypeError, match="name"):
            PreWeightPathGate(name="", gate_rank=Rank.HYPOTHESIS)

    def test_gate_exceeding_ceiling_refused(self) -> None:
        with pytest.raises(TypeError, match="PATH_GATE_RANK_CEILING"):
            PreWeightPathGate(name="test", gate_rank=Rank.LICENSED)

    def test_gate_non_rank_refused(self) -> None:
        with pytest.raises(TypeError, match="gate_rank"):
            PreWeightPathGate(name="test", gate_rank="HIGH")  # type: ignore[arg-type]


# ===================================================================
# 4. PreWeightPathGate.decide — the seven steps
# ===================================================================


class TestPreWeightPathGateDecide:
    """docs/22 §5 — the full seven-step decision."""

    # Step 1 — type guard
    def test_decide_non_carrier_raises(self) -> None:
        gate = _gate()
        with pytest.raises(TypeError, match="WordCarrierCandidate"):
            gate.decide("not a carrier", _proof())  # type: ignore[arg-type]

    def test_decide_non_proof_raises(self) -> None:
        gate = _gate()
        with pytest.raises(TypeError, match="PathGateProof"):
            gate.decide(_word_carrier(), "not a proof")  # type: ignore[arg-type]

    # Step 2 — domain match
    def test_decide_domain_mismatch_rejected(self) -> None:
        gate = _gate()
        carrier = _word_carrier(domain="arabic_morphophonology")
        proof = _proof(domain="persian_morphophonology")
        verdict = gate.decide(carrier, proof)
        assert verdict.state is PathGateState.REJECTED
        assert verdict.failure_code is FailureCode.DOMAIN_MISSING
        assert verdict.approved_kind is None
        assert verdict.granted_rank is Rank.ZERO

    # Step 3 — evidence presence (zero-rank evidence)
    def test_decide_zero_rank_evidence_deferred(self) -> None:
        gate = _gate()
        carrier = _word_carrier()
        proof = _proof(rank=Rank.ZERO)
        verdict = gate.decide(carrier, proof)
        assert verdict.state is PathGateState.DEFERRED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED
        assert verdict.approved_kind is None
        assert verdict.granted_rank is Rank.ZERO

    # Step 4 — preventer check
    def test_decide_competing_preventer_blocks(self) -> None:
        gate = _gate()
        carrier = _word_carrier()
        proof = _proof(kind=PathKind.ROOT)
        verdict = gate.decide(
            carrier, proof, preventers=(PathKind.JAMID,)
        )
        assert verdict.state is PathGateState.BLOCKED
        assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
        assert verdict.approved_kind is None
        assert verdict.granted_rank is Rank.ZERO
        # The preventer residual is visible
        assert len(verdict.residuals) == 1
        assert verdict.residuals[0].kind is ResidualKind.BLOCKING
        assert verdict.residuals[0].visible is True

    def test_decide_same_kind_preventer_does_not_block(self) -> None:
        """A preventer of the same kind as the claimed path does not block."""
        gate = _gate()
        carrier = _word_carrier()
        proof = _proof(kind=PathKind.ROOT)
        verdict = gate.decide(
            carrier, proof, preventers=(PathKind.ROOT,)
        )
        # same kind → not a competing path → approval
        assert verdict.state is PathGateState.APPROVED

    # Step 5 — blocking residuals on the carrier
    def test_decide_blocking_residual_blocks(self) -> None:
        blocker = Residual(
            name="unresolved_vowel",
            kind=ResidualKind.BLOCKING,
            visible=True,
            note="unresolved vowel issue",
        )
        carrier = _word_carrier(residuals=(blocker,))
        gate = _gate()
        proof = _proof()
        verdict = gate.decide(carrier, proof)
        assert verdict.state is PathGateState.BLOCKED
        assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
        assert verdict.residuals == (blocker,)

    def test_decide_non_blocking_residual_passes(self) -> None:
        non_blocker = Residual(
            name="optional_note",
            kind=ResidualKind.NON_BLOCKING,
            visible=True,
            note="informational",
        )
        carrier = _word_carrier(residuals=(non_blocker,))
        gate = _gate()
        proof = _proof()
        verdict = gate.decide(carrier, proof)
        assert verdict.state is PathGateState.APPROVED

    # Step 6 — rank bound: carrier rank above BIRTH_RANK_CEILING is rejected
    def test_decide_carrier_rank_above_ceiling_rejected(self) -> None:
        """A carrier whose rank exceeds BIRTH_RANK_CEILING is rejected.

        Carriers normally cannot be born with rank > CANDIDATE, but if
        one is synthetically promoted (bypassing birth guards), the gate
        must still refuse it.
        """
        carrier = _word_carrier()
        # Bypass the frozen birth guard to set a rank above BIRTH_RANK_CEILING
        object.__setattr__(carrier, "rank", Rank.HYPOTHESIS)
        gate = _gate()
        proof = _proof()
        verdict = gate.decide(carrier, proof)
        assert verdict.state is PathGateState.REJECTED
        assert verdict.failure_code is FailureCode.RANK_PROMOTION_WITHOUT_GATE

    # Step 7 — approval with bounded meet
    def test_decide_approved_root_path(self) -> None:
        gate = _gate(gate_rank=Rank.HYPOTHESIS)
        carrier = _word_carrier()
        proof = _proof(kind=PathKind.ROOT, rank=Rank.CANDIDATE)
        verdict = gate.decide(carrier, proof)
        assert verdict.state is PathGateState.APPROVED
        assert verdict.failure_code is None
        assert verdict.approved_kind is PathKind.ROOT
        # meet(CANDIDATE, CANDIDATE, HYPOTHESIS) = CANDIDATE
        assert verdict.granted_rank is Rank.CANDIDATE
        assert verdict.residuals == ()
        assert verdict.gate_name == "pre_weight_path_gate"

    def test_decide_meet_bounds_rank(self) -> None:
        """The meet always keeps or lowers — never raises."""
        gate = _gate(gate_rank=Rank.CANDIDATE)
        carrier = _word_carrier()
        proof = _proof(rank=Rank.HYPOTHESIS)
        verdict = gate.decide(carrier, proof)
        assert verdict.state is PathGateState.APPROVED
        # meet(HYPOTHESIS, CANDIDATE, CANDIDATE) = CANDIDATE
        assert verdict.granted_rank is Rank.CANDIDATE


# ===================================================================
# 5. All seven PathKind members through the gate
# ===================================================================


@pytest.mark.parametrize("kind", list(PathKind))
class TestAllPathKindsDecidable:
    """docs/22 §6 — every PathKind is independently decidable."""

    def test_path_kind_approved(self, kind: PathKind) -> None:
        gate = _gate()
        carrier = _word_carrier()
        proof = _proof(kind=kind)
        verdict = gate.decide(carrier, proof)
        assert verdict.state is PathGateState.APPROVED
        assert verdict.approved_kind is kind
        assert verdict.failure_code is None

    def test_path_kind_deferred_on_zero_evidence(self, kind: PathKind) -> None:
        gate = _gate()
        carrier = _word_carrier()
        proof = _proof(kind=kind, rank=Rank.ZERO)
        verdict = gate.decide(carrier, proof)
        assert verdict.state is PathGateState.DEFERRED
        assert verdict.failure_code is FailureCode.GATE_REQUIRED


# ===================================================================
# 6. Negative constitutional tests — forbidden identities
# ===================================================================


class TestPathKindIsNotPathGateProof:
    """docs/22 §2 — PathKind ≠ PathGateProof."""

    def test_path_kind_has_no_proof_fields(self) -> None:
        """PathKind is a StrEnum; PathGateProof is a frozen dataclass.
        They share no interface."""
        for kind in PathKind:
            assert not hasattr(kind, "evidence_surface")
            assert not hasattr(kind, "evidence_rank")
            assert not hasattr(kind, "claimed_kind")

    def test_path_gate_proof_has_no_enum_methods(self) -> None:
        proof = _proof()
        assert not hasattr(proof, "value")  # StrEnum attribute
        assert not hasattr(proof, "name")  # Enum.name

    def test_path_kind_is_not_instance_of_proof(self) -> None:
        for kind in PathKind:
            assert not isinstance(kind, PathGateProof)


class TestCarrierDeclarationIsNotVerdict:
    """docs/21 + docs/22 — carrier declaration ≠ gate verdict."""

    def test_word_carrier_has_no_verdict_fields(self) -> None:
        carrier = _word_carrier()
        field_names = {f.name for f in dataclasses.fields(carrier)}
        verdict_fields = {
            "verdict", "approved_kind", "failure_code", "gate_result",
            "proof", "gate_name", "path_gate_state",
        }
        leaked = field_names & verdict_fields
        assert not leaked, (
            f"WordCarrierCandidate carries verdict fields: {sorted(leaked)} — "
            "carrier declaration ≠ gate verdict (docs/21)"
        )

    def test_path_gate_verdict_has_no_carrier_fields(self) -> None:
        verdict = PathGateVerdict(
            state=PathGateState.APPROVED,
            failure_code=None,
            approved_kind=PathKind.ROOT,
            granted_rank=Rank.CANDIDATE,
            residuals=(),
            gate_name="test",
        )
        field_names = {f.name for f in dataclasses.fields(verdict)}
        carrier_fields = {
            "bounded_surface", "sequence", "syllables", "units",
            "value", "type", "origin", "identity", "domain", "scope",
            "trace",
        }
        leaked = field_names & carrier_fields
        assert not leaked, (
            f"PathGateVerdict carries carrier fields: {sorted(leaked)} — "
            "gate verdict ≠ carrier declaration (docs/22 §2)"
        )


class TestPathGateVerdictIsNotMeaning:
    """docs/22 §1 — a path gate verdict is not a meaning."""

    def test_verdict_has_no_meaning_fields(self) -> None:
        verdict = PathGateVerdict(
            state=PathGateState.APPROVED,
            failure_code=None,
            approved_kind=PathKind.ROOT,
            granted_rank=Rank.CANDIDATE,
            residuals=(),
            gate_name="test",
        )
        field_names = {f.name for f in dataclasses.fields(verdict)}
        meaning_fields = {
            "meaning", "hukm", "agency", "patienthood", "reality",
            "event", "knowledge", "semantics",
        }
        leaked = field_names & meaning_fields
        assert not leaked, (
            f"PathGateVerdict carries meaning fields: {sorted(leaked)} — "
            "a path gate verdict is not a meaning (docs/22 §1)"
        )


class TestPathGateVerdictIsNotWeight:
    """docs/22 §1 — a path gate verdict is not a weight."""

    def test_verdict_has_no_weight_fields(self) -> None:
        verdict = PathGateVerdict(
            state=PathGateState.APPROVED,
            failure_code=None,
            approved_kind=PathKind.ROOT,
            granted_rank=Rank.CANDIDATE,
            residuals=(),
            gate_name="test",
        )
        field_names = {f.name for f in dataclasses.fields(verdict)}
        weight_fields = {
            "weight", "fit", "weight_fit", "scored", "alignment",
            "pattern", "weight_image", "mizan", "mawzun",
        }
        leaked = field_names & weight_fields
        assert not leaked, (
            f"PathGateVerdict carries weight fields: {sorted(leaked)} — "
            "a path gate verdict is not a weight (docs/22 §1)"
        )


class TestPathGateHasNoOmegaJudgment:
    """docs/22 §7 — no Ω judgment, no μ chain, no extraction."""

    def test_gate_has_no_omega_fields(self) -> None:
        gate = _gate()
        assert not hasattr(gate, "omega_judgment")
        assert not hasattr(gate, "weight_opening")
        assert not hasattr(gate, "functional_closure")

    def test_verdict_has_no_omega_fields(self) -> None:
        verdict = PathGateVerdict(
            state=PathGateState.APPROVED,
            failure_code=None,
            approved_kind=PathKind.ROOT,
            granted_rank=Rank.CANDIDATE,
            residuals=(),
            gate_name="test",
        )
        assert not hasattr(verdict, "omega_judgment")
        assert not hasattr(verdict, "weight_opening")

    def test_proof_has_no_omega_fields(self) -> None:
        proof = _proof()
        assert not hasattr(proof, "omega_judgment")
        assert not hasattr(proof, "weight_opening")


class TestCandidateRankIsNotGateRank:
    """docs/21 + docs/22 — CandidateRank ≠ GateRank."""

    def test_birth_rank_ceiling_is_candidate(self) -> None:
        assert BIRTH_RANK_CEILING is Rank.CANDIDATE

    def test_path_gate_rank_ceiling_is_hypothesis(self) -> None:
        assert PATH_GATE_RANK_CEILING is Rank.HYPOTHESIS

    def test_candidate_below_gate_ceiling(self) -> None:
        assert Rank.CANDIDATE.value < PATH_GATE_RANK_CEILING.value


class TestFailureCodeSurfaceStability:
    """FailureCode surface remains stable except for explicitly ratified additions.

    PR-20 additions are ratified by docs/41 and docs/42.
    """

    def test_failure_codes_unchanged(self) -> None:
        # FailureCode surface remains stable except for explicitly
        # ratified additions. PR-20 additions are ratified by
        # docs/41 (Ifādah Boundary Law) and docs/42 (SpeechForce/
        # FormalStyle Bridge Law).
        expected = {
            "IDENTITY_BROKEN", "CENTER_MISSING", "BOUNDARY_MISSING",
            "DOMAIN_MISSING", "SCOPE_MISSING", "TRACE_MISSING",
            "REQUIRED_SLOT_EMPTY", "UNLICENSED_OPENING",
            "OUTPUT_EXCEEDS_LAYER", "HIDDEN_RESIDUAL",
            "BLOCKING_RESIDUAL_PRESENT", "RANK_PROMOTION_WITHOUT_GATE",
            "RANK_EXCEEDS_CEILING", "FORBIDDEN_STRAIGHT_LINE",
            "GATE_REQUIRED",
            # PR-20: Ifādah failures (docs/41 §6, docs/42 §7)
            "NO_RELATION_CLOSURE", "NO_FORMAL_STYLE",
            "NO_SPEECH_FORCE", "NO_IFADAH_MAQAM",
            "MAQAM_DIVERGENCE", "FORMAL_STYLE_CONFLICT",
            "NO_IFADAH_EVIDENCE", "NO_IFADAH_SCOPE",
        }
        actual = {member.name for member in FailureCode}
        assert actual == expected, (
            f"FailureCode members changed unexpectedly. "
            f"added: {actual - expected}, removed: {expected - actual}"
        )


class TestNoNewRuntimeDeps:
    """docs/22 §7 — no new runtime dependencies."""

    def test_path_gate_imports_only_stdlib_and_weight(self) -> None:
        """The path_gate module imports only from stdlib and the
        taaqqul_slot_geometry package — no pip-installed external deps."""
        import ast
        import importlib.util

        spec = importlib.util.find_spec("taaqqul_slot_geometry.weight.path_gate")
        assert spec is not None and spec.origin is not None
        source = pathlib.Path(spec.origin).read_text(encoding="utf-8")
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    assert top in {
                        "taaqqul_slot_geometry", "__future__",
                        "dataclasses", "enum",
                    }, f"path_gate imports external package: {alias.name}"
            elif isinstance(node, ast.ImportFrom) and node.module:
                top = node.module.split(".")[0]
                assert top in {
                    "taaqqul_slot_geometry", "__future__",
                    "dataclasses", "enum",
                }, f"path_gate imports from external package: {node.module}"


# ===================================================================
# 7. Static guard: docs/22 origin document exists
# ===================================================================


class TestConstitutionalDocumentPresent:
    """docs/13 — a PR's origin law must exist in the repository."""

    def test_pr11_constitutional_document_is_present(self) -> None:
        repo_root = pathlib.Path(__file__).resolve().parent.parent
        doc = "docs/22_PRE_WEIGHT_PATH_GATE_LAW.md"
        path = repo_root / doc
        assert path.is_file(), f"missing PR-11 origin document: {doc}"
        assert path.read_text(encoding="utf-8").strip(), (
            f"PR-11 origin document is empty: {doc}"
        )

    def test_pr10b_law_still_present(self) -> None:
        """docs/21 must still exist — PR-11 builds on it."""
        repo_root = pathlib.Path(__file__).resolve().parent.parent
        doc = "docs/21_CARRIER_DECLARATION_IS_NOT_VERDICT_LAW.md"
        path = repo_root / doc
        assert path.is_file(), f"missing PR-10B origin document: {doc}"


# ===================================================================
# 8. Forbidden path jumps — specific scenarios
# ===================================================================


class TestForbiddenPathJumps:
    """docs/22 §7 — forbidden forms."""

    def test_carrier_declaration_as_verdict_is_refused(self) -> None:
        """PathKind on a carrier is not a gate verdict — the carrier
        must still go through the gate to get a PathGateVerdict."""
        carrier = _word_carrier()
        # The carrier has no verdict field — this is structural
        assert not hasattr(carrier, "verdict")
        assert not hasattr(carrier, "approved_kind")

    def test_multiple_preventers_first_blocks(self) -> None:
        gate = _gate()
        carrier = _word_carrier()
        proof = _proof(kind=PathKind.ROOT)
        verdict = gate.decide(
            carrier, proof,
            preventers=(PathKind.JAMID, PathKind.MABNI),
        )
        assert verdict.state is PathGateState.BLOCKED
        assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT

    @pytest.mark.parametrize(
        "kind_a,kind_b",
        [
            (PathKind.ROOT, PathKind.JAMID),
            (PathKind.JAMID, PathKind.ROOT),
            (PathKind.ROOT, PathKind.MABNI),
            (PathKind.OPERATOR, PathKind.BORROWED),
            (PathKind.PROPER_NAME, PathKind.RESIDUAL),
        ],
    )
    def test_competing_paths_block_each_other(
        self, kind_a: PathKind, kind_b: PathKind
    ) -> None:
        """When kind_b is a preventer and kind_a is claimed, the gate blocks."""
        gate = _gate()
        carrier = _word_carrier()
        proof = _proof(kind=kind_a)
        verdict = gate.decide(carrier, proof, preventers=(kind_b,))
        assert verdict.state is PathGateState.BLOCKED
        assert verdict.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT

    def test_hidden_residual_on_verdict_carried_visibly(self) -> None:
        """A hidden residual on a verdict is accepted at gate level.

        The gate carries residuals as-is; Ω judgment governance (PR-12)
        will catch HIDDEN_FORBIDDEN residuals at the chain level.

        PR-11B clarification: this test proves *visible carry, no silent
        pass* — it does NOT prove Ω clearance. The gate sees and carries;
        it does not judge or clear.
        """
        hidden = Residual(
            name="hidden_test",
            kind=ResidualKind.HIDDEN_FORBIDDEN,
            visible=False,
        )
        # The verdict accepts Residual tuples; the gate never
        # produces hidden residuals (the gate produces only BLOCKING
        # visible residuals). But if someone tries to construct one
        # with a hidden residual, the Residual itself is valid —
        # the governance that catches HIDDEN_FORBIDDEN is the Ω
        # judgment (PR-12 surface). The verdict just carries them
        # visibly.
        verdict = PathGateVerdict(
            state=PathGateState.APPROVED,
            failure_code=None,
            approved_kind=PathKind.ROOT,
            granted_rank=Rank.CANDIDATE,
            residuals=(hidden,),
            gate_name="test",
        )
        assert verdict.residuals[0].kind is ResidualKind.HIDDEN_FORBIDDEN
