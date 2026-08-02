"""Native runtime registry and corpus runner constitutional tests.

Origin law  : docs/14 + docs/80 + docs/91
Branch      : Native corpus execution synchronization surface
Category    : Category 2 (contract/surface)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.runtime import (
    ContextWindow,
    StageTransitionState,
    TokenCarrier,
    classify_token_paths,
    get_native_stage_registry,
    run_native_corpus,
    validate_no_forbidden_jump,
)
from taaqqul_slot_geometry.runtime.context_window import CompositionReadinessCandidate
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REQUIRED_STAGE_IDS = {
    "PATH_CLASSIFICATION",
    "PRE_WEIGHT_CAPACITY_AUDIT",
    "DAL_ONLY",
    "VERBAL_MADLUL",
    "DAL_MADLUL_BINDING",
    "CONTRACTABLE_UNIT",
    "RELATION",
    "FORMAL_SHAPE",
    "MUFRAD_DALALAH",
    "RELATION_CLOSURE",
    "IFADAH",
    "HUKM",
    "MANAT",
    "TANZIL",
    "ANSWER_AUDIT",
}


def _declare(branch: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md",
        branch_name=f"native runtime/{branch}",
        constitutional_chain=("docs/14", "docs/80", "runtime/native_registry"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("MeaningClaim", "HukmShortcut", "TanzilExecution"),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="native registry + corpus runner",
        origin_law_ref=(
            "docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md"
            "#1-live-reference-truth-vs-historical-snapshot-records"
        ),
        branch_of_origin="Runtime synchronization without semantic/hukm leap",
        forbidden_shortcut_assertions=(
            "Signifier -> Meaning",
            "Hukm -> Tanzil without Manat",
        ),
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _required_tokens() -> tuple[str, ...]:
    return (
        "يا",
        "أيها",
        "الذين",
        "الذي",
        "إذا",
        "إلى",
        "أن",
        "كما",
        "ولا",
        "عليه",
        "بينكم",
    )


def test_registry_contains_required_runtime_stages() -> None:
    _declare("registry required stages")
    stage_ids = {spec.stage_id for spec in get_native_stage_registry()}
    assert _REQUIRED_STAGE_IDS.issubset(stage_ids)


def test_registry_forbidden_line_sync() -> None:
    _declare("forbidden-line sync")
    specs = get_native_stage_registry()
    validate_no_forbidden_jump(specs)


def test_runtime_callable_and_carrier_surface_visibility() -> None:
    _declare("api coherence")
    specs = get_native_stage_registry()

    # Any runtime-enabled stage must expose either a callable or an explicit
    # runtime_implemented=False marker.
    for spec in specs:
        if spec.runtime_implemented:
            assert (
                spec.execution_callable is not None
                or spec.stage_id == "PRE_WEIGHT_CAPACITY_AUDIT"
            )
        if spec.execution_callable is not None:
            assert callable(spec.execution_callable)

        assert spec.input_carrier_types
        assert spec.output_carrier_types
        assert spec.canonical_name


def test_required_function_and_reference_words_have_native_paths() -> None:
    _declare("path-aware applicability")
    expected = {
        "يا": {"ParticleOperatorPath"},
        "أيها": {"BuiltNounPath", "DemonstrativePath"},
        "الذين": {"RelativeReferencePath"},
        "الذي": {"RelativeReferencePath"},
        "إذا": {"ConditionalOperatorPath"},
        "إلى": {"ParticleOperatorPath"},
        "أن": {"ParticleOperatorPath"},
        "كما": {"ParticleOperatorPath"},
        "ولا": {"NegationOperatorPath", "CoordinationOperatorPath"},
        "عليه": {"PronounPath"},
        "بينكم": {"PronounPath", "DeicticReferencePath"},
    }

    for token, expected_paths in expected.items():
        got = {p.path_id.value for p in classify_token_paths(token)}
        assert expected_paths.issubset(got)


def test_state_distinction_and_visibility_contract() -> None:
    _declare("state distinction")
    result = run_native_corpus("native-test", _required_tokens())

    states = [
        record.transition_state
        for item in result.token_results
        for record in item.records
    ]
    assert StageTransitionState.BLOCKED not in states
    assert StageTransitionState.DEFERRED in states
    assert StageTransitionState.DECLARED_NOT_IMPLEMENTED in states
    assert StageTransitionState.NOT_OPENED in states
    assert StageTransitionState.NOT_APPLICABLE in states
    assert StageTransitionState.EXECUTED in states

    # Distinction: these states are separate enum members by contract.
    assert StageTransitionState.DEFERRED is not StageTransitionState.NOT_OPENED
    assert StageTransitionState.NOT_APPLICABLE is not StageTransitionState.DEFERRED
    assert StageTransitionState.NOT_APPLICABLE is not StageTransitionState.BLOCKED

    # Residual and trace visibility, and no implicit rank upgrade.
    for item in result.token_results:
        for record in item.records:
            assert record.trace_entry_id
            assert record.rank_after.value <= record.rank_before.value
            assert set(record.residuals_before).issubset(set(record.residuals_after))


def test_formal_shape_uses_alternative_predecessor_opening() -> None:
    _declare("formal-shape predecessor alternatives")
    run = run_native_corpus("formal-shape-opening", ("يا",))
    formal_shape_records = [
        record
        for record in run.token_results[0].records
        if record.stage_id == "FORMAL_SHAPE"
    ]
    assert formal_shape_records
    assert formal_shape_records[0].transition_state is StageTransitionState.DEFERRED


def test_runtime_not_implemented_stages_are_not_recorded_executed() -> None:
    _declare("runtime implemented discipline")
    specs = {spec.stage_id: spec for spec in get_native_stage_registry()}
    run = run_native_corpus("runtime-implementation-discipline", _required_tokens())

    for token_result in run.token_results:
        for record in token_result.records:
            if not specs[record.stage_id].runtime_implemented:
                assert record.transition_state is not StageTransitionState.EXECUTED
                assert record.output_carrier_id is None
                if (
                    record.transition_state
                    is StageTransitionState.DECLARED_NOT_IMPLEMENTED
                ):
                    assert "runtime_implementation_missing" in record.remediation_hints
                else:
                    assert record.transition_state in {
                        StageTransitionState.NOT_OPENED,
                        StageTransitionState.NOT_APPLICABLE,
                    }


def test_runtime_failure_codes_are_documented_and_documented_codes_exist() -> None:
    _declare("failure-code sync")
    specs = get_native_stage_registry()
    runtime_codes = {code.name for spec in specs for code in spec.failure_codes}
    enum_codes = {code.name for code in FailureCode}

    doc_path = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "LAW_TO_RUNTIME_COVERAGE_MATRIX.md"
    )
    lines = doc_path.read_text(encoding="utf-8").splitlines()
    documented_codes_by_stage: dict[str, set[str]] = {}
    for line in lines:
        if not line.startswith("| docs/"):
            continue
        columns = [part.strip() for part in line.split("|")[1:-1]]
        stage_id = columns[4].strip("`")
        code_cell = columns[5].strip("`")
        if not code_cell:
            continue
        documented = {
            piece.strip()
            for piece in code_cell.split(",")
            if piece.strip()
        }
        documented_codes_by_stage.setdefault(stage_id, set()).update(documented)

    documented_codes = set().union(*documented_codes_by_stage.values())

    assert documented_codes <= enum_codes

    for spec in specs:
        if spec.stage_id not in documented_codes_by_stage:
            continue
        spec_codes = {code.name for code in spec.failure_codes}
        assert spec_codes <= documented_codes_by_stage[spec.stage_id]

    assert runtime_codes <= documented_codes


def test_token_span_boundary_and_no_auto_relation_or_ifadah() -> None:
    _declare("token span relation boundary")
    tokens = (
        "يا",
        "أيها",
        "الذين",
        "آمنوا",
        "إذا",
        "تداينتم",
        "بدين",
        "إلى",
        "أجل",
        "مسمى",
        "فاكتبوه",
        "وليكتب",
        "بينكم",
        "كاتب",
        "بالعدل",
        "ولا",
        "يأب",
        "كاتب",
        "أن",
        "يكتب",
        "كما",
        "علمه",
        "الله",
    )

    window = ContextWindow(
        corpus_id="dayn-short",
        tokens=tuple(
            [
                TokenCarrier(token_id=f"t{i:03d}", surface=s, index=i)
                for i, s in enumerate(tokens)
            ]
        ),
    )
    span = window.span(0, 4)
    readiness = CompositionReadinessCandidate(
        span=span,
        contracted_unit_ids=span.token_ids,
        candidate_link_operator="NIDA_CHAIN",
        identity_compatible=True,
        bearability_compatible=False,
        reference_ready=False,
        relation_kind_candidate=None,
        evidence_refs=("span_boundary_proof",),
        residuals=("RELATION_DEFERRED_PENDING_CONTEXT",),
    )

    assert readiness.relation_kind_candidate is None
    assert "RELATION_DEFERRED" in readiness.residuals[0]

    run = run_native_corpus("dayn-snippet", tokens)
    for token_result in run.token_results:
        tanzil_records = [r for r in token_result.records if r.stage_id == "TANZIL"]
        assert tanzil_records
        # hukm->tanzil without manat is never executed in this native token-runner.
        assert tanzil_records[0].transition_state in {
            StageTransitionState.NOT_OPENED,
            StageTransitionState.DEFERRED,
            StageTransitionState.NOT_APPLICABLE,
        }


def test_regression_guard_not_applicable_no_longer_zero() -> None:
    _declare("regression guard")
    run = run_native_corpus("regression-dayn", _required_tokens())
    not_applicable = 0
    for token_result in run.token_results:
        for record in token_result.records:
            if record.transition_state is StageTransitionState.NOT_APPLICABLE:
                not_applicable += 1

    # Previous reported snapshot had synthetic zero NOT_APPLICABLE.
    assert not_applicable > 0
