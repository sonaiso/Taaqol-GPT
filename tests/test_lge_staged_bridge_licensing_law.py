"""Constitutional acceptance tests for the staged LGE bridge licensing law.

Origin law     : docs/129_LGE_STAGED_SURFACE_TO_DALALAH_BRIDGE_LICENSING_LAW.md
Branch         : LGE-B0 staged surface-to-dalālah bridge licensing
Category       : Category 2 — contract/surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LAW = _ROOT / "docs" / "129_LGE_STAGED_SURFACE_TO_DALALAH_BRIDGE_LICENSING_LAW.md"
_ROADMAP = _ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_DOCS_INDEX = _ROOT / "docs" / "README.md"
_CLAUDE = _ROOT / "CLAUDE.md"
_STAGES = tuple(f"LGE-B{number}" for number in range(1, 10))
_FORBIDDEN = (
    "RuntimeOpening",
    "Bytes -> ArabicLetter",
    "Text / Unicode -> Sound",
    "Syllable -> Root",
    "SurfaceToken / SentenceSlot -> Meaning",
    "DalAloneClosed -> Wad'iMadlulClosed",
)


def _declare(branch_name: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/129_LGE_STAGED_SURFACE_TO_DALALAH_BRIDGE_LICENSING_LAW.md",
        branch_name=f"LGE-B0 ({branch_name})",
        constitutional_chain=("SLGE-SDLC-G0", "LGE-B0"),
        chain_position="LGE-B0 law-only bridge contract",
        origin_law_ref="docs/129_LGE_STAGED_SURFACE_TO_DALALAH_BRIDGE_LICENSING_LAW.md#section-2",
        branch_of_origin="Staged LGE bridge licensing without runtime admission",
        forbidden_shortcut_assertions=_FORBIDDEN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "RuntimeCode",
            "Parser",
            "RootDetector",
            "MorphologyEngine",
            "SyntaxEngine",
            "SemanticEngine",
            "Ifadah",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
        ),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def test_law_declares_nine_staged_bridge_boundaries() -> None:
    _declare("stage registry and bridge contract")
    law = _LAW.read_text(encoding="utf-8")
    for stage in _STAGES:
        assert f"`{stage}`" in law
    for required in (
        "InputContract",
        "EvidenceContract",
        "TraceRef",
        "RankCeiling",
        "RankVector",
        "ResidualPolicy",
        "MinimumCompleteRequirement",
        "BackwardReconstruction",
        "MCE",
        "LGE-B2",
        "LGE-B3",
        "LGE-B4",
        "LGE-B5",
        "LGE-B6",
        "LGE-B7",
        "LGE-B8",
        "LGE-B9",
    ):
        assert required in law


def test_law_preserves_existing_identity_and_semantic_boundaries() -> None:
    _declare("forbidden jumps and independent identity")
    law = _LAW.read_text(encoding="utf-8")
    for shortcut in _FORBIDDEN[1:]:
        assert shortcut in law
    assert "Text alone cannot prove sound" in law
    assert "A G₀ jamid anchor is not a general root certificate" in law
    assert "No direct surface-to-dalālah jump" in law
    assert "finite in-scope exhaustion" in law


def test_law_licenses_bit_values_without_direct_linguistic_inference() -> None:
    _declare("bit values are trace-bound and encoding-dependent")
    law = " ".join(_LAW.read_text(encoding="utf-8").split())
    for marker in (
        "BitObservation",
        "value ∈ {0, 1}",
        "encoding_id",
        "encoding_version",
        "bit_order",
        "every source bit position to be accounted for exactly once",
        "does not exhaust the encoding standard",
        "No bit value",
        "IndependentlyEvidencedSoundCandidate",
    ):
        assert marker in law
    assert "No bit value, byte value, bit pattern" in law


def test_law_requires_separate_letter_and_haraka_mce_before_116_pairs() -> None:
    _declare("29 letters and four marks license a finite product")
    law = " ".join(_LAW.read_text(encoding="utf-8").split())
    for marker in (
        "Letters = (L₁, …, L₂₉)",
        "Harakat = (H₁, H₂, H₃, H₄)",
        "hamza and alif maintained as distinct entries",
        "29/29",
        "4/4",
        "29 × 4 = 116",
        "all and only 116 ordered pairs",
        "each pair appearing exactly once",
        "cannot authorize expanding either set",
    ):
        assert marker in law


def test_law_requires_bounded_proof_obligations_for_each_slot_value_transition() -> None:
    _declare("per-slot value transition proof coverage")
    law = " ".join(_LAW.read_text(encoding="utf-8").split())
    for marker in (
        "ProofObligation(e, s, v)",
        "declared_domain_and_scope",
        "source_slot_ref = s",
        "source_value_ref = v",
        "evidence_refs_and_evidence_rank",
        "proof_object_ref",
        "output_rank_ceiling",
        "inherited_residual_dispositions",
        "countermodel_and_inverse_refs",
        "backward_reconstruction_ref",
        "exactly one obligation record",
        "covered(Dₑ) = Dₑ",
        "no fabricated value, omitted pair, duplicate record, or hidden residual",
        "conditional on its declared premises and evidence",
        "They do not execute transitions, grant runtime admission",
        "slot labels to letter",
    ):
        assert marker in law


def test_law_bounds_algebraic_counting_to_proved_transition_obligations() -> None:
    _declare("conditional count theorem from bits through Dal surface")
    law = " ".join(_LAW.read_text(encoding="utf-8").split()).replace("`", "")
    for marker in (
        "m observed bit positions",
        "at most 2ᵐ possible bitstrings",
        "lineage embedding",
        "Jᵢ: Qᵢ ↪ Qᵢ₊₁",
        "Aᵢ",
        "Rᵢ ⊆ Jᵢ(Qᵢ)",
        "nᵢ₊₁ = nᵢ + Δᵢ⁺ − Δᵢ⁻",
        "nₖ = n₀ + Σᵢ₌₀..k−1 (Δᵢ⁺ − Δᵢ⁻)",
        "injectivity gives",
        "29 · 4 = 116",
        "does not show that each pair is pronounced",
        "every adjacent transition",
        "not runtime admission",
    ):
        assert marker in law
    assert "counting bits or bitstrings does not establish a bit-to-letter" in law
    assert "arithmetic" in law


def test_law_requires_total_arithmetic_accounting_for_stage_outputs() -> None:
    _declare("stage output arithmetic audit")
    law = " ".join(_LAW.read_text(encoding="utf-8").split()).replace("`", "")
    for marker in (
        "every result r ∈ Oᵢ",
        "exactly one arithmetic-accounting disposition",
        "StageOutputArithmetic(Sᵢ, r)",
        "branch_and_chain_position",
        "measure_id_and_unit",
        "operands_and_formula",
        "result_or_not_applicable_reason",
        "proof_or_calculation_ref",
        "rank_ceiling",
        "residual_dispositions",
        "The audit is total over Oᵢ",
        "NOT_APPLICABLE",
        "For every finite output collection, the audit records its cardinality",
        "claims of additive change must satisfy §4C",
        "no cross-layer sum or delta is licensed",
        "does not establish a slot's linguistic identity",
        "without making arithmetic a universal inference rule",
        "does not merge the project-lifecycle branch",
    ):
        assert marker in law


def test_law_defines_path_local_license_increments_without_linguistic_inference() -> None:
    _declare("path-local transition count and encoding-specific bridges")
    law = " ".join(_LAW.read_text(encoding="utf-8").split()).replace("`", "")
    for marker in (
        "n₀(P) = 0",
        "δ(eᵢ) = 1 iff eᵢ has its own valid admission",
        "δ(eᵢ) = 0 for REFUSED or DEFERRED transitions",
        "nᵢ(P) = Σⱼ₌₁..ᵢ δ(eⱼ)",
        "This n counts proved transitions on this declared path",
        "does not increase rank",
        "Existing licenses are reused by reference",
        "path_id, e₁, …, eₖ, nₖ, output_ref",
        "Every declared encoding (UTF-8 or another specifically named encoding and version)",
        "does not map an individual bit or byte directly to an Arabic letter",
        "orthographic grapheme candidate",
        "independently evidenced letter or haraka candidate",
        "Applicable initiation/ibtidāʾ, waṣl, and waqf conditions",
        "not independent permission to create a new mapping",
        "It neither opens runtime nor licenses inference",
    ):
        assert marker in law


def test_law_models_each_declared_transition_inside_each_slot() -> None:
    _declare("slot-local licensed transition proof model")
    law = " ".join(_LAW.read_text(encoding="utf-8").split()).replace("`", "")
    for marker in (
        "E(b,s)",
        "SlotTransitionProof(b, s, e)",
        "branch_id",
        "slot_id",
        "transition_id",
        "predecessor_slot_state_ref",
        "input_value_refs",
        "output_value_refs",
        "transition_contract_ref",
        "proof_object_ref",
        "gate_and_admission_refs",
        "measure_id_and_unit",
        "calculation_or_NOT_APPLICABLE",
        "rank_ceiling_and_check",
        "residual_dispositions",
        "exactly one record is required",
        "disposition is PROVED, REFUSED, or DEFERRED",
        "N(b,s,j) = Σᵢ₌₁..ⱼ δ(b,s,eᵢ)",
        "The transition count δ and a stage-value delta are separate quantities",
        "every transition in the declared finite E(b,s)",
        "does not synthesize a slot value or numeric encoding",
        "join the SLGE-SDLC lifecycle branch to LGE surface geometry",
    ):
        assert marker in law


def test_law_defines_typed_proof_reader_domains_and_induction_prerequisites() -> None:
    _declare("typed proof-reader definitions and bounded induction")
    law = " ".join(_LAW.read_text(encoding="utf-8").split()).replace("`", "")
    for marker in (
        "§4G Algebraic proof-reader definitions and prerequisites",
        "Cℓ = declared carrier identities in layer ℓ",
        "Vℓ = declared mark/value identities in layer ℓ",
        "Pℓ ⊆ Cℓ × Vℓ = declared carrier-mark pairs",
        "Oℓ = source occurrences",
        "Rℓ = declared role identifiers",
        "typed by its layer, coordinate system, unit, source span, and trace",
        "not proof",
        "may be partial or one-to-many",
        "Role(occurrence, context, layer) → role-candidate(s)",
        "A digest may detect record changes but is not proof",
        "Base: the initial state s₀ is evidenced",
        "Step: each eᵢ is proved under its own preconditions",
        "Coverage: E(b,s) contains every in-scope transition exactly once",
        "Conclusion: the result holds only for the declared branch",
        "do not assert that any particular letter, mark, or pair has a grammatical "
        "or semantic role",
    ):
        assert marker in law


def test_law_defines_external_role_reader_and_bidirectional_trace() -> None:
    _declare("external occurrence-scoped role proof reader")
    law = " ".join(_LAW.read_text(encoding="utf-8").split()).replace("`", "")
    for marker in (
        "§4H External role-transition proof reader and bidirectional trace",
        "external, read-only consumer",
        "does not write source files, modify runtime code, execute linguistic transitions",
        "carrier_ref, occurrence_ref, position_ref, context_ref, role_id, transition_id",
        "augmentative-letter analysis",
        "pronoun/reference, demonstrative, vocative, interrogative, conditional",
        "conjunction, coordination, and sequencing",
        "exception, restriction/exclusivity, causation, simile, imperative lām",
        "negation, prohibition, consequence lām",
        "امتنان",
        "not assignments to letters",
        "different occurrences or contexts",
        "Forward evidence path:",
        "Reverse reconstruction:",
        "exact source occurrence",
        "coverage only against an explicitly enumerated finite",
        "not new evidence or authorization",
    ):
        assert marker in law


def test_law_keeps_runtime_closed_and_existing_chain_positions() -> None:
    _declare("law-only and current chain preservation")
    law = _LAW.read_text(encoding="utf-8")
    roadmap = _ROADMAP.read_text(encoding="utf-8")
    for marker in (
        "law-only",
        "does not displace",
        "no runtime code",
        "does not activate any `LGE-B1…LGE-B9` runtime stage",
        "They do not execute transitions",
        "not runtime admission",
        "docs/110",
    ):
        assert marker in law
    assert "SLGE-SDLC-G0" in roadmap
    assert "PR-F  Permit Consumption and Execution Candidate" in roadmap


def test_law_is_synchronized_in_governance_views() -> None:
    _declare("roadmap index and contributor view synchronization")
    assert "Amendment-107 (LGE-B0" in _ROADMAP.read_text(encoding="utf-8")
    assert "129_LGE_STAGED_SURFACE_TO_DALALAH_BRIDGE_LICENSING_LAW.md" in (
        _DOCS_INDEX.read_text(encoding="utf-8")
    )
    claude = _CLAUDE.read_text(encoding="utf-8")
    assert "LGE-B0" in claude
    assert "does not authorize" in claude
    assert "Amendment-108" in _ROADMAP.read_text(encoding="utf-8")
    assert "Amendment-108" in claude
    assert "Amendment-109" in _ROADMAP.read_text(encoding="utf-8")
    assert "Amendment-109" in claude
    assert "Amendment-110" in _ROADMAP.read_text(encoding="utf-8")
    assert "Amendment-110" in claude
    assert "Amendment-111" in _ROADMAP.read_text(encoding="utf-8")
    assert "Amendment-111" in claude
    assert "Amendment-112" in _ROADMAP.read_text(encoding="utf-8")
    assert "Amendment-112" in claude
    assert "Amendment-113" in _ROADMAP.read_text(encoding="utf-8")
    assert "Amendment-113" in claude
    assert "Amendment-114" in _ROADMAP.read_text(encoding="utf-8")
    assert "Amendment-114" in claude
    assert "Amendment-115" in _ROADMAP.read_text(encoding="utf-8")
    assert "Amendment-115" in claude
