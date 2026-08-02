from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.forbidden_lines import CANONICAL_REGISTRY
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight import (
    assemble_chain_report,
    bind_dal_madlul,
    build_word_class_registry,
    prove_contractable_unit,
    prove_dal,
    prove_hukm_candidate,
    prove_ifadah_candidate,
    prove_manat_candidate,
    prove_mufrad_dalalah_closure,
    prove_relation_candidate,
    prove_relation_closure,
    prove_tanzil_candidate,
    prove_verbal_madlul,
)


class PathId(StrEnum):
    ROOT_STEM_PATH = "RootStemPath"
    JAMID_PATH = "JamidPath"
    MUSHTAQ_PATH = "MushtaqPath"
    MABNI_VERB_PATH = "MabniVerbPath"
    BUILT_NOUN_PATH = "BuiltNounPath"
    PARTICLE_OPERATOR_PATH = "ParticleOperatorPath"
    PRONOUN_PATH = "PronounPath"
    DEMONSTRATIVE_PATH = "DemonstrativePath"
    RELATIVE_REFERENCE_PATH = "RelativeReferencePath"
    DEICTIC_REFERENCE_PATH = "DeicticReferencePath"
    CONDITIONAL_OPERATOR_PATH = "ConditionalOperatorPath"
    NEGATION_OPERATOR_PATH = "NegationOperatorPath"
    COORDINATION_OPERATOR_PATH = "CoordinationOperatorPath"
    RESIDUAL_PATH = "ResidualPath"


@dataclass(frozen=True, slots=True)
class PathEvidence:
    path_id: PathId
    evidence: tuple[str, ...]
    confidence: float


@dataclass(frozen=True, slots=True)
class StageSpec:
    stage_id: str
    canonical_name: str
    input_carrier_types: tuple[str, ...]
    output_carrier_types: tuple[str, ...]
    required_predecessors: tuple[str, ...]
    alternative_predecessors: tuple[str, ...]
    allowed_predecessors: tuple[str, ...]
    allowed_successors: tuple[str, ...]
    applicability_predicate: Callable[[tuple[PathEvidence, ...]], bool]
    execution_callable: Callable[..., object] | None
    required_evidence_types: tuple[str, ...]
    minimum_rank: Rank
    blocking_residual_families: tuple[str, ...]
    identity_invariants: tuple[str, ...]
    context_requirement: str
    failure_codes: tuple[FailureCode, ...]
    constitutional_document_refs: tuple[str, ...]
    runtime_implemented: bool
    corpus_enabled: bool


def _all_paths(_: tuple[PathEvidence, ...]) -> bool:
    return True


def _content_path_only(paths: tuple[PathEvidence, ...]) -> bool:
    content = {
        PathId.ROOT_STEM_PATH,
        PathId.JAMID_PATH,
        PathId.MUSHTAQ_PATH,
        PathId.MABNI_VERB_PATH,
    }
    return any(p.path_id in content for p in paths)


def _non_content_path(paths: tuple[PathEvidence, ...]) -> bool:
    non_content = {
        PathId.PARTICLE_OPERATOR_PATH,
        PathId.PRONOUN_PATH,
        PathId.DEMONSTRATIVE_PATH,
        PathId.RELATIVE_REFERENCE_PATH,
        PathId.DEICTIC_REFERENCE_PATH,
        PathId.CONDITIONAL_OPERATOR_PATH,
        PathId.NEGATION_OPERATOR_PATH,
        PathId.COORDINATION_OPERATOR_PATH,
        PathId.BUILT_NOUN_PATH,
    }
    return any(p.path_id in non_content for p in paths)


def classify_token_paths(surface: str) -> tuple[PathEvidence, ...]:
    token = surface.strip()
    if not token:
        return (
            PathEvidence(
                path_id=PathId.RESIDUAL_PATH,
                evidence=("empty_token",),
                confidence=1.0,
            ),
        )

    mapping: dict[str, tuple[PathEvidence, ...]] = {
        "يا": (
            PathEvidence(
                PathId.PARTICLE_OPERATOR_PATH,
                ("nidā operator surface",),
                0.96,
            ),
        ),
        "أيها": (
            PathEvidence(PathId.BUILT_NOUN_PATH, ("built form marker",), 0.85),
            PathEvidence(
                PathId.DEMONSTRATIVE_PATH,
                ("deictic demonstrative signal",),
                0.73,
            ),
        ),
        "الذين": (
            PathEvidence(
                PathId.RELATIVE_REFERENCE_PATH,
                ("relative-reference surface",),
                0.95,
            ),
        ),
        "الذي": (
            PathEvidence(
                PathId.RELATIVE_REFERENCE_PATH,
                ("relative-reference surface",),
                0.95,
            ),
        ),
        "إذا": (
            PathEvidence(
                PathId.CONDITIONAL_OPERATOR_PATH,
                ("conditional operator surface",),
                0.94,
            ),
        ),
        "إلى": (
            PathEvidence(
                PathId.PARTICLE_OPERATOR_PATH,
                ("jarr/link operator surface",),
                0.91,
            ),
            PathEvidence(
                PathId.DEICTIC_REFERENCE_PATH,
                ("boundary-bridge directional signal",),
                0.51,
            ),
        ),
        "أن": (
            PathEvidence(
                PathId.PARTICLE_OPERATOR_PATH,
                ("particle/operator surface",),
                0.92,
            ),
        ),
        "كما": (
            PathEvidence(
                PathId.PARTICLE_OPERATOR_PATH,
                ("comparative-link operator surface",),
                0.87,
            ),
        ),
        "ولا": (
            PathEvidence(PathId.NEGATION_OPERATOR_PATH, ("negation marker",), 0.9),
            PathEvidence(
                PathId.COORDINATION_OPERATOR_PATH,
                ("coordination marker",),
                0.78,
            ),
        ),
        "عليه": (
            PathEvidence(PathId.PRONOUN_PATH, ("attached pronoun evidence",), 0.86),
        ),
        "بينكم": (
            PathEvidence(
                PathId.PRONOUN_PATH,
                ("attached pronoun cluster",),
                0.74,
            ),
            PathEvidence(
                PathId.DEICTIC_REFERENCE_PATH,
                ("interlocutor-space reference",),
                0.66,
            ),
        ),
    }

    if token in mapping:
        return mapping[token]
    if token.startswith("ال"):
        return (PathEvidence(PathId.JAMID_PATH, ("definite lexical surface",), 0.62),)
    return (
        PathEvidence(
            PathId.ROOT_STEM_PATH,
            ("default lexical-content fallback",),
            0.55,
        ),
    )


def _stage(
    *,
    stage_id: str,
    canonical_name: str,
    input_carrier_types: tuple[str, ...],
    output_carrier_types: tuple[str, ...],
    required_predecessors: tuple[str, ...],
    alternative_predecessors: tuple[str, ...] = (),
    allowed_successors: tuple[str, ...],
    applicability_predicate: Callable[[tuple[PathEvidence, ...]], bool],
    execution_callable: Callable[..., object] | None,
    required_evidence_types: tuple[str, ...],
    context_requirement: str,
    refs: tuple[str, ...],
    runtime_implemented: bool,
    corpus_enabled: bool,
) -> StageSpec:
    allowed_predecessors = required_predecessors + tuple(
        predecessor
        for predecessor in alternative_predecessors
        if predecessor not in required_predecessors
    )
    return StageSpec(
        stage_id=stage_id,
        canonical_name=canonical_name,
        input_carrier_types=input_carrier_types,
        output_carrier_types=output_carrier_types,
        required_predecessors=required_predecessors,
        alternative_predecessors=alternative_predecessors,
        allowed_predecessors=allowed_predecessors,
        allowed_successors=allowed_successors,
        applicability_predicate=applicability_predicate,
        execution_callable=execution_callable,
        required_evidence_types=required_evidence_types,
        minimum_rank=Rank.CANDIDATE,
        blocking_residual_families=("BLOCKING",),
        identity_invariants=("identity_preserved",),
        context_requirement=context_requirement,
        failure_codes=(FailureCode.GATE_REQUIRED,),
        constitutional_document_refs=refs,
        runtime_implemented=runtime_implemented,
        corpus_enabled=corpus_enabled,
    )


def get_native_stage_registry() -> tuple[StageSpec, ...]:
    return (
        StageSpec(
            stage_id="PATH_CLASSIFICATION",
            canonical_name="Path Classification",
            input_carrier_types=("TokenCarrier",),
            output_carrier_types=("PathEvidence",),
            required_predecessors=(),
            alternative_predecessors=(),
            allowed_predecessors=(),
            allowed_successors=("PRE_WEIGHT_CAPACITY_AUDIT", "FORMAL_SHAPE"),
            applicability_predicate=_all_paths,
            execution_callable=classify_token_paths,
            required_evidence_types=("token_surface",),
            minimum_rank=Rank.ZERO,
            blocking_residual_families=(),
            identity_invariants=("token_surface_identity_preserved",),
            context_requirement="NONE",
            failure_codes=(FailureCode.GATE_REQUIRED,),
            constitutional_document_refs=(
                "docs/14_PR_CHAIN_ROADMAP.md",
                "docs/20_PRE_WEIGHT_LICENSING_LAW.md",
            ),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="PRE_WEIGHT_CAPACITY_AUDIT",
            canonical_name="PreWeightCapacityAudit",
            input_carrier_types=("PathEvidence",),
            output_carrier_types=("PreWeightCapacityAudit",),
            required_predecessors=("PATH_CLASSIFICATION",),
            allowed_successors=("DAL_ONLY", "NON_CONTENT_FORMAL_ROUTE"),
            applicability_predicate=_all_paths,
            execution_callable=None,
            required_evidence_types=("path_family_classification",),
            context_requirement="NONE",
            refs=("docs/20_PRE_WEIGHT_LICENSING_LAW.md",),
            runtime_implemented=False,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="DAL_ONLY",
            canonical_name="DalOnlyCandidate",
            input_carrier_types=("LicensingBoundaryVerdict",),
            output_carrier_types=("DalBoundaryVerdict",),
            required_predecessors=("PRE_WEIGHT_CAPACITY_AUDIT",),
            allowed_successors=("VERBAL_MADLUL",),
            applicability_predicate=_content_path_only,
            execution_callable=prove_dal,
            required_evidence_types=("license_boundary", "trace_ref"),
            context_requirement="LICENSING_BOUNDARY_REQUIRED",
            refs=("docs/26_DAL_ONLY_CANDIDATE_BOUNDARY_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="VERBAL_MADLUL",
            canonical_name="VerbalMadlulCandidate",
            input_carrier_types=("DalOnlyCandidate",),
            output_carrier_types=("VerbalMadlulBoundaryVerdict",),
            required_predecessors=("DAL_ONLY",),
            allowed_successors=("DAL_MADLUL_BINDING",),
            applicability_predicate=_content_path_only,
            execution_callable=prove_verbal_madlul,
            required_evidence_types=("dal_candidate",),
            context_requirement="DAL_ONLY_REQUIRED",
            refs=("docs/27_VERBAL_MADLUL_CANDIDATE_BOUNDARY_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="DAL_MADLUL_BINDING",
            canonical_name="DalMadlulBindingCandidate",
            input_carrier_types=(
                "VerbalMadlulCandidate",
                "RegistryLookupResult",
                "RegistryLookupResult",
            ),
            output_carrier_types=("DalMadlulBindingVerdict",),
            required_predecessors=("VERBAL_MADLUL",),
            allowed_successors=("CONTRACTABLE_UNIT",),
            applicability_predicate=_content_path_only,
            execution_callable=bind_dal_madlul,
            required_evidence_types=("dal_registry", "madlul_registry"),
            context_requirement="REGISTRY_PROOF_REQUIRED",
            refs=("docs/31_DAL_MADLUL_BINDING_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="CONTRACTABLE_UNIT",
            canonical_name="ContractableUnitGeometry",
            input_carrier_types=("DalMadlulBindingCandidate",),
            output_carrier_types=("ContractableUnitVerdict",),
            required_predecessors=("DAL_MADLUL_BINDING",),
            allowed_successors=("RELATION",),
            applicability_predicate=_all_paths,
            execution_callable=prove_contractable_unit,
            required_evidence_types=("binding_candidate",),
            context_requirement="BINDING_REQUIRED",
            refs=("docs/32_CONTRACTABLE_UNIT_GEOMETRY_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="RELATION",
            canonical_name="RelationCandidate",
            input_carrier_types=(
                "ContractableUnitGeometry",
                "ContractableUnitGeometry",
            ),
            output_carrier_types=("RelationVerdict",),
            required_predecessors=("CONTRACTABLE_UNIT",),
            allowed_successors=("FORMAL_SHAPE",),
            applicability_predicate=_all_paths,
            execution_callable=prove_relation_candidate,
            required_evidence_types=("governor", "dependent"),
            context_requirement="PAIR_REQUIRED",
            refs=("docs/33_RELATION_CANDIDATE_BOUNDARY_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="FORMAL_SHAPE",
            canonical_name="FormalShapeRegistry",
            input_carrier_types=("RelationCandidate",),
            output_carrier_types=("FormalShapeRegistry",),
            required_predecessors=(),
            alternative_predecessors=("RELATION", "PATH_CLASSIFICATION"),
            allowed_successors=("MUFRAD_DALALAH",),
            applicability_predicate=_all_paths,
            execution_callable=build_word_class_registry,
            required_evidence_types=("formal_domain",),
            context_requirement="FORMAL_ONLY",
            refs=("docs/34_FORMAL_SHAPE_REGISTRY_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="MUFRAD_DALALAH",
            canonical_name="MufradDalalahClosure",
            input_carrier_types=("DalalahCandidateVerdict",),
            output_carrier_types=("MufradDalalahClosureVerdict",),
            required_predecessors=("FORMAL_SHAPE",),
            allowed_successors=("RELATION_CLOSURE",),
            applicability_predicate=_content_path_only,
            execution_callable=prove_mufrad_dalalah_closure,
            required_evidence_types=("dalalah_candidates",),
            context_requirement="DALALAH_CANDIDATE_REQUIRED",
            refs=("docs/39_MUFRAD_DALALAH_CLOSURE_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="RELATION_CLOSURE",
            canonical_name="RelationClosure",
            input_carrier_types=("RelationCandidate",),
            output_carrier_types=("RelationClosureVerdict",),
            required_predecessors=("MUFRAD_DALALAH",),
            allowed_successors=("IFADAH",),
            applicability_predicate=_all_paths,
            execution_callable=prove_relation_closure,
            required_evidence_types=("relation_candidate",),
            context_requirement="RELATION_CANDIDATE_REQUIRED",
            refs=("docs/40_RELATION_CLOSURE_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="IFADAH",
            canonical_name="IfadahCandidate",
            input_carrier_types=(
                "RelationClosureVerdict",
                "FormalStyleVerdict",
                "MaqamContextBoundaryVerdict",
            ),
            output_carrier_types=("IfadahVerdict",),
            required_predecessors=("RELATION_CLOSURE",),
            allowed_successors=("HUKM",),
            applicability_predicate=_all_paths,
            execution_callable=prove_ifadah_candidate,
            required_evidence_types=("speech_force", "maqam", "ifadah_evidence"),
            context_requirement="SPAN_AND_CONTEXT_REQUIRED",
            refs=(
                "docs/41_IFADAH_BOUNDARY_LAW.md",
                "docs/42_SPEECH_FORCE_FORMAL_STYLE_BRIDGE_LAW.md",
            ),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="HUKM",
            canonical_name="HukmCandidate",
            input_carrier_types=("IfadahVerdict",),
            output_carrier_types=("HukmVerdict",),
            required_predecessors=("IFADAH",),
            allowed_successors=("MANAT",),
            applicability_predicate=_all_paths,
            execution_callable=prove_hukm_candidate,
            required_evidence_types=("hukm_claim", "hukm_evidence", "hukm_maqam"),
            context_requirement="IFADAH_REQUIRED",
            refs=("docs/43_HUKM_DOMAIN_BOUNDARY_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="MANAT",
            canonical_name="ManatCandidate",
            input_carrier_types=("HukmVerdict",),
            output_carrier_types=("ManatVerdict",),
            required_predecessors=("HUKM",),
            allowed_successors=("TANZIL",),
            applicability_predicate=_all_paths,
            execution_callable=prove_manat_candidate,
            required_evidence_types=("manat_evidence", "manat_domain"),
            context_requirement="HUKM_REQUIRED",
            refs=("docs/44_MANAT_BOUNDARY_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        StageSpec(
            stage_id="TANZIL",
            canonical_name="TanzilCandidate",
            input_carrier_types=("HukmVerdict", "ManatVerdict"),
            output_carrier_types=("TanzilVerdict",),
            required_predecessors=("MANAT",),
            alternative_predecessors=(),
            allowed_predecessors=("MANAT",),
            allowed_successors=("ANSWER_AUDIT",),
            applicability_predicate=_all_paths,
            execution_callable=prove_tanzil_candidate,
            required_evidence_types=("reality_evidence", "presentation_envelope"),
            minimum_rank=Rank.CANDIDATE,
            blocking_residual_families=("BLOCKING",),
            identity_invariants=("tanzil_not_execution",),
            context_requirement="HUKM_AND_MANAT_REQUIRED",
            failure_codes=(
                FailureCode.GATE_REQUIRED,
                FailureCode.NO_HUKM,
                FailureCode.NO_MANAT,
            ),
            constitutional_document_refs=("docs/45_TANZIL_PRESENTATION_BOUNDARY_LAW.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
        _stage(
            stage_id="ANSWER_AUDIT",
            canonical_name="AnswerAudit",
            input_carrier_types=("TanzilVerdict",),
            output_carrier_types=("AuditedAnswer",),
            required_predecessors=("TANZIL",),
            allowed_successors=(),
            applicability_predicate=_all_paths,
            execution_callable=None,
            required_evidence_types=("model_answer",),
            context_requirement="MODEL_CLIENT_REQUIRED",
            refs=("docs/46_VERTICAL_PATH_CLOSURE_LAW.md",),
            runtime_implemented=False,
            corpus_enabled=False,
        ),
        _stage(
            stage_id="NON_CONTENT_FORMAL_ROUTE",
            canonical_name="NonContentFormalRoute",
            input_carrier_types=("TokenCarrier", "PathEvidence"),
            output_carrier_types=("PreSemanticChainReport",),
            required_predecessors=("PRE_WEIGHT_CAPACITY_AUDIT",),
            allowed_successors=("FORMAL_SHAPE",),
            applicability_predicate=_non_content_path,
            execution_callable=assemble_chain_report,
            required_evidence_types=("path_evidence",),
            context_requirement="VERBAL_MADLUL_REQUIRED",
            refs=("docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md",),
            runtime_implemented=True,
            corpus_enabled=True,
        ),
    )


def registry_version() -> str:
    return "native-registry-v1"


def registry_hash() -> str:
    payload = []
    for spec in get_native_stage_registry():
        payload.append(
            {
                "stage_id": spec.stage_id,
                "canonical_name": spec.canonical_name,
                "input_carrier_types": spec.input_carrier_types,
                "output_carrier_types": spec.output_carrier_types,
                "required_predecessors": spec.required_predecessors,
                "alternative_predecessors": spec.alternative_predecessors,
                "allowed_predecessors": spec.allowed_predecessors,
                "allowed_successors": spec.allowed_successors,
                "required_evidence_types": spec.required_evidence_types,
                "minimum_rank": spec.minimum_rank.name,
                "blocking_residual_families": spec.blocking_residual_families,
                "identity_invariants": spec.identity_invariants,
                "context_requirement": spec.context_requirement,
                "failure_codes": tuple(fc.name for fc in spec.failure_codes),
                "constitutional_document_refs": spec.constitutional_document_refs,
                "runtime_implemented": spec.runtime_implemented,
                "corpus_enabled": spec.corpus_enabled,
            }
        )
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def validate_no_forbidden_jump(specs: tuple[StageSpec, ...]) -> None:
    stage_ids = {spec.stage_id for spec in specs}
    for spec in specs:
        for successor in spec.allowed_successors:
            if successor not in stage_ids:
                continue
            if CANONICAL_REGISTRY.is_forbidden_direct(spec.stage_id, successor):
                msg = (
                    "forbidden straight-line jump in registry: "
                    f"{spec.stage_id} -> {successor}"
                )
                raise ValueError(msg)


def declared_runtime_stage_ids() -> tuple[str, ...]:
    return tuple(spec.stage_id for spec in get_native_stage_registry())
