"""Bounded reference matrices for USM structural comparison (USM-C2 scope)."""

from __future__ import annotations

from taaqqul_slot_geometry.core import Rank
from taaqqul_slot_geometry.usm.application_contract import ApplicationContract
from taaqqul_slot_geometry.usm.capability_contract import CapabilityContract
from taaqqul_slot_geometry.usm.entity_contract import EntityTypeContract
from taaqqul_slot_geometry.usm.enums import RelationDirection
from taaqqul_slot_geometry.usm.evidence_contract import ScienceEvidenceContract
from taaqqul_slot_geometry.usm.identifiers import (
    ApplicationTypeId,
    CapabilityId,
    CriterionId,
    DomainId,
    EntityTypeId,
    EvidenceTypeId,
    JudgmentTypeId,
    KnowledgeObjectTypeId,
    MatrixId,
    RelationTypeId,
    RuleId,
    ScienceId,
    TraceRef,
    TransformationTypeId,
)
from taaqqul_slot_geometry.usm.judgment_contract import JudgmentContract
from taaqqul_slot_geometry.usm.knowledge_object_contract import KnowledgeObjectContract
from taaqqul_slot_geometry.usm.matrix import UniversalScienceMatrix
from taaqqul_slot_geometry.usm.relation_contract import RelationContract
from taaqqul_slot_geometry.usm.residuals import USMResidual, USMResidualKind
from taaqqul_slot_geometry.usm.transformation_contract import TransformationContract


def _rule(name: str) -> RuleId:
    return RuleId(name)


def _crit(name: str) -> CriterionId:
    return CriterionId(name)


def make_arabic_reference_matrix_v1() -> UniversalScienceMatrix:
    science = ScienceId("ARABIC")
    domain = DomainId("LINGUISTIC_BOUNDARY")
    trace = TraceRef("trace://usm/reference/arabic/v1")
    entities = tuple(
        EntityTypeContract(
            entity_type_id=EntityTypeId(entity),
            science_id=science,
            domain_id=domain,
            identity_criterion=_crit(f"{entity}_IDENTITY"),
            membership_criterion=_crit(f"{entity}_MEMBERSHIP"),
            boundary_rule=_rule(f"{entity}_BOUNDARY"),
            parent_types=(),
            forbidden_confusions=(_rule(f"NO_{entity}_CONFUSION"),),
            trace_ref=TraceRef(f"{trace.value}/entities/{entity.lower()}"),
        )
        for entity in (
            "PHONETIC_TRACE",
            "LETTER",
            "HARAKA",
            "SYLLABLE",
            "ROOT_CANDIDATE",
            "STEM_CANDIDATE",
            "WEIGHT_IMAGE",
            "LEXEME",
            "VERBAL_MADLUL",
            "COMPOSABLE_LEXEME",
            "RELATION_CANDIDATE",
            "CLOSED_COMPOSITION",
            "IFADAH_CANDIDATE",
            "CLAIM_CANDIDATE",
        )
    )
    capabilities = (
        CapabilityContract(
            capability_id=CapabilityId("LETTER_TAKES_LICENSED_HARAKA"),
            science_id=science,
            bearer_type=EntityTypeId("LETTER"),
            permitted_operations=(_rule("ASSIGN_HARAKA"),),
            permitted_relation_roles=(_rule("LETTER_ROLE"),),
            required_conditions=(_rule("HARAKA_LICENSE_PRESENT"),),
            blockers=(_rule("HARAKA_LICENSE_MISSING"),),
            evidence_requirements=(EvidenceTypeId("ATTESTED_USAGE"),),
            rank_ceiling=Rank.CANDIDATE,
            residual_policy_ref=_rule("ARABIC_RESIDUAL_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/capabilities/letter_haraka"),
        ),
        CapabilityContract(
            capability_id=CapabilityId("CLOSED_COMPOSITION_PRODUCES_IFADAH"),
            science_id=science,
            bearer_type=EntityTypeId("CLOSED_COMPOSITION"),
            permitted_operations=(_rule("OPEN_IFADAH"),),
            permitted_relation_roles=(_rule("PREDICATIVE_RELATION"),),
            required_conditions=(_rule("COMPOSITION_CLOSED"),),
            blockers=(_rule("COMPOSITION_OPEN"),),
            evidence_requirements=(EvidenceTypeId("SYNTACTIC_COMPATIBILITY"),),
            rank_ceiling=Rank.CANDIDATE,
            residual_policy_ref=_rule("ARABIC_RESIDUAL_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/capabilities/ifadah"),
        ),
    )
    relations = (
        RelationContract(
            relation_type_id=RelationTypeId("PREDICATION"),
            science_id=science,
            arity=2,
            operand_types=(EntityTypeId("LEXEME"), EntityTypeId("LEXEME")),
            roles=(_rule("SUBJECT"), _rule("PREDICATE")),
            direction=RelationDirection.DIRECTED,
            compatibility_rules=(_rule("SYNTACTIC_COMPATIBILITY_REQUIRED"),),
            saturation_rule=_rule("PREDICATION_SATURATION"),
            scope_rule=_rule("CLAUSAL_SCOPE_ONLY"),
            closure_rule=_rule("CLOSES_IN_COMPOSITION"),
            trace_ref=TraceRef(f"{trace.value}/relations/predication"),
        ),
        RelationContract(
            relation_type_id=RelationTypeId("RESTRICTION"),
            science_id=science,
            arity=2,
            operand_types=(EntityTypeId("LEXEME"), EntityTypeId("LEXEME")),
            roles=(_rule("HEAD"), _rule("RESTRICTOR")),
            direction=RelationDirection.DIRECTED,
            compatibility_rules=(_rule("RESTRICTION_COMPATIBILITY"),),
            saturation_rule=_rule("RESTRICTION_SATURATION"),
            scope_rule=_rule("NOMINAL_SCOPE"),
            closure_rule=_rule("RESTRICTION_CLOSURE"),
            trace_ref=TraceRef(f"{trace.value}/relations/restriction"),
        ),
    )
    transformations = (
        TransformationContract(
            transformation_type_id=TransformationTypeId("TRACE_TO_LETTER_CANDIDATE"),
            science_id=science,
            source_types=(EntityTypeId("PHONETIC_TRACE"),),
            target_types=(EntityTypeId("LETTER"),),
            required_capabilities=(CapabilityId("LETTER_TAKES_LICENSED_HARAKA"),),
            preserved_invariants=(_rule("TRACE_IDENTITY"),),
            declared_changes=(_rule("LETTERIZATION"),),
            required_conditions=(_rule("TRACE_PARSED"),),
            blockers=(_rule("TRACE_AMBIGUOUS"),),
            evidence_requirements=(EvidenceTypeId("ATTESTED_USAGE"),),
            rank_ceiling=Rank.CANDIDATE,
            residual_policy_ref=_rule("ARABIC_RESIDUAL_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/transformations/trace_to_letter"),
        ),
        TransformationContract(
            transformation_type_id=TransformationTypeId("IFADAH_TO_CLAIM_CANDIDATE"),
            science_id=science,
            source_types=(EntityTypeId("IFADAH_CANDIDATE"),),
            target_types=(EntityTypeId("CLAIM_CANDIDATE"),),
            required_capabilities=(CapabilityId("CLOSED_COMPOSITION_PRODUCES_IFADAH"),),
            preserved_invariants=(_rule("CLAIM_TRACEABILITY"),),
            declared_changes=(_rule("CLAIM_READINESS_OPENING"),),
            required_conditions=(_rule("INFORMATIVE_IFADAH"),),
            blockers=(_rule("NON_INFORMATIVE_IFADAH"),),
            evidence_requirements=(EvidenceTypeId("CONTEXTUAL_INDICATION"),),
            rank_ceiling=Rank.CANDIDATE,
            residual_policy_ref=_rule("ARABIC_RESIDUAL_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/transformations/ifadah_to_claim"),
        ),
    )
    evidence = (
        ScienceEvidenceContract(
            evidence_type_id=EvidenceTypeId("ATTESTED_USAGE"),
            science_id=science,
            supported_claim_types=(_rule("USAGE_ATTESTATION_CLAIM"),),
            domain_scope=domain,
            relevance_rule=_rule("USAGE_RELEVANCE"),
            coverage_rule=_rule("USAGE_COVERAGE_BOUNDED"),
            independence_rule=_rule("INDEPENDENT_ATTESTATION_PREFERRED"),
            counterevidence_rule=_rule("COUNTEREVIDENCE_VISIBLE"),
            global_rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(f"{trace.value}/evidence/attested_usage"),
        ),
        ScienceEvidenceContract(
            evidence_type_id=EvidenceTypeId("SYNTACTIC_COMPATIBILITY"),
            science_id=science,
            supported_claim_types=(_rule("STRUCTURAL_COMPATIBILITY_CLAIM"),),
            domain_scope=domain,
            relevance_rule=_rule("STRUCTURAL_RELEVANCE"),
            coverage_rule=_rule("STRUCTURAL_COVERAGE_BOUNDED"),
            independence_rule=_rule("INDEPENDENT_PARSE_CHECK"),
            counterevidence_rule=_rule("PARSE_CONTRADICTION_VISIBLE"),
            global_rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(f"{trace.value}/evidence/syntactic_compatibility"),
        ),
        ScienceEvidenceContract(
            evidence_type_id=EvidenceTypeId("CONTEXTUAL_INDICATION"),
            science_id=science,
            supported_claim_types=(_rule("CONTEXTUAL_INDICATION_CLAIM"),),
            domain_scope=domain,
            relevance_rule=_rule("CONTEXT_RELEVANCE"),
            coverage_rule=_rule("CONTEXT_COVERAGE_BOUNDED"),
            independence_rule=_rule("CONTEXT_SOURCE_DIVERSITY"),
            counterevidence_rule=_rule("CONTEXT_COUNTEREVIDENCE_VISIBLE"),
            global_rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(f"{trace.value}/evidence/contextual_indication"),
        ),
    )
    judgments = (
        JudgmentContract(
            judgment_type_id=JudgmentTypeId("STRUCTURALLY_VALID"),
            science_id=science,
            supported_claim_types=(_rule("STRUCTURAL_COMPATIBILITY_CLAIM"),),
            required_evidence_types=(EvidenceTypeId("SYNTACTIC_COMPATIBILITY"),),
            local_rank_name="STRUCTURAL_RANK",
            global_rank_ceiling=Rank.CANDIDATE,
            conditions=(_rule("SLOT_COMPATIBILITY"),),
            blockers=(_rule("SLOT_CONTRADICTION"),),
            downgrade_rules=(_rule("DOWNGRADE_ON_COUNTEREVIDENCE"),),
            trace_ref=TraceRef(f"{trace.value}/judgments/structural"),
        ),
        JudgmentContract(
            judgment_type_id=JudgmentTypeId("CLAIM_READY_NOT_EXTERNALLY_VERIFIED"),
            science_id=science,
            supported_claim_types=(_rule("CONTEXTUAL_INDICATION_CLAIM"),),
            required_evidence_types=(
                EvidenceTypeId("ATTESTED_USAGE"),
                EvidenceTypeId("CONTEXTUAL_INDICATION"),
            ),
            local_rank_name="CLAIM_READINESS_RANK",
            global_rank_ceiling=Rank.CANDIDATE,
            conditions=(_rule("IFADAH_INFORMATIVE"),),
            blockers=(_rule("EXTERNAL_TRUTH_UNAVAILABLE"),),
            downgrade_rules=(_rule("DEFER_TO_EXTERNAL_EVIDENCE"),),
            trace_ref=TraceRef(f"{trace.value}/judgments/claim_ready"),
        ),
    )
    knowledge_objects = (
        KnowledgeObjectContract(
            knowledge_object_type_id=KnowledgeObjectTypeId("MORPHOLOGICAL_RULE"),
            science_id=science,
            subject_types=(EntityTypeId("ROOT_CANDIDATE"), EntityTypeId("STEM_CANDIDATE")),
            relation_types=(RelationTypeId("PREDICATION"),),
            required_judgments=(JudgmentTypeId("STRUCTURALLY_VALID"),),
            scope_rule=_rule("MORPHOLOGICAL_SCOPE"),
            exception_policy=_rule("MORPHOLOGICAL_EXCEPTION_POLICY"),
            conflict_policy=_rule("MORPHOLOGICAL_CONFLICT_POLICY"),
            revision_policy=_rule("MORPHOLOGICAL_REVISION_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/knowledge/morphological_rule"),
        ),
        KnowledgeObjectContract(
            knowledge_object_type_id=KnowledgeObjectTypeId("COMPOSITION_RULE"),
            science_id=science,
            subject_types=(EntityTypeId("COMPOSABLE_LEXEME"),),
            relation_types=(RelationTypeId("RESTRICTION"),),
            required_judgments=(JudgmentTypeId("CLAIM_READY_NOT_EXTERNALLY_VERIFIED"),),
            scope_rule=_rule("COMPOSITION_SCOPE"),
            exception_policy=_rule("COMPOSITION_EXCEPTION_POLICY"),
            conflict_policy=_rule("COMPOSITION_CONFLICT_POLICY"),
            revision_policy=_rule("COMPOSITION_REVISION_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/knowledge/composition_rule"),
        ),
    )
    applications = (
        ApplicationContract(
            application_type_id=ApplicationTypeId("ANALYZE_NEW_LEXEME"),
            science_id=science,
            knowledge_object_types=(KnowledgeObjectTypeId("MORPHOLOGICAL_RULE"),),
            case_entity_types=(EntityTypeId("LEXEME"),),
            membership_criterion=_crit("LEXEME_MEMBERSHIP"),
            required_conditions=(_rule("LEXEME_INPUT_DECLARED"),),
            blockers=(_rule("OUT_OF_SCOPE_LEXEME"),),
            invalidating_differences=(_rule("UNLICENSED_WEIGHT_PATH"),),
            feedback_policy=_rule("LEXEME_FEEDBACK_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/applications/analyze_lexeme"),
        ),
        ApplicationContract(
            application_type_id=ApplicationTypeId("PRODUCE_CLAIM_CANDIDATE_ONLY"),
            science_id=science,
            knowledge_object_types=(KnowledgeObjectTypeId("COMPOSITION_RULE"),),
            case_entity_types=(EntityTypeId("CLAIM_CANDIDATE"),),
            membership_criterion=_crit("CLAIM_MEMBERSHIP"),
            required_conditions=(_rule("CLAIM_READINESS_ONLY"),),
            blockers=(_rule("EXTERNAL_TRUTH_REQUESTED"),),
            invalidating_differences=(_rule("TRUTH_CERTIFICATION_REQUESTED"),),
            feedback_policy=_rule("CLAIM_FEEDBACK_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/applications/claim_candidate"),
        ),
    )
    residuals = (
        USMResidual(
            residual_id="arabic-capability-algebra-incomplete",
            kind=USMResidualKind.MISSING_CAPABILITY,
            detail="full Bearable(p,x) algebra is incomplete",
            blocking=False,
            visible=True,
            repair_hint="add dedicated capability evaluator branch",
        ),
        USMResidual(
            residual_id="arabic-relation-algebra-incomplete",
            kind=USMResidualKind.UNSPECIFIED_RELATION,
            detail="full relation algebra is incomplete",
            blocking=False,
            visible=True,
            repair_hint="add relation evaluator stage",
        ),
        USMResidual(
            residual_id="arabic-coverage-unproven",
            kind=USMResidualKind.COVERAGE_GAP,
            detail="complete Arabic coverage remains unproven",
            blocking=True,
            visible=True,
            repair_hint="expand bounded coverage matrices",
        ),
        USMResidual(
            residual_id="arabic-irreducibility-unproven",
            kind=USMResidualKind.IRREDUCIBILITY_UNPROVEN,
            detail="final irreducibility proof remains deferred",
            blocking=True,
            visible=True,
            repair_hint="extend mutation-space tests",
        ),
    )
    return UniversalScienceMatrix(
        matrix_id=MatrixId("ArabicReferenceMatrixV1"),
        science_id=science,
        version="1.0",
        declared_scope=(
            "From bounded linguistic carriers through claim readiness, "
            "excluding full Arabic coverage and external truth."
        ),
        entities=entities,
        capabilities=capabilities,
        relations=relations,
        transformations=transformations,
        evidence=evidence,
        judgments=judgments,
        knowledge_objects=knowledge_objects,
        applications=applications,
        residuals=residuals,
        trace_ref=trace,
    )


def make_elementary_mathematics_reference_matrix_v1() -> UniversalScienceMatrix:
    science = ScienceId("ELEMENTARY_MATHEMATICS")
    domain = DomainId("ARITHMETIC_AND_INTRO_ALGEBRA")
    trace = TraceRef("trace://usm/reference/math/v1")
    entities = tuple(
        EntityTypeContract(
            entity_type_id=EntityTypeId(entity),
            science_id=science,
            domain_id=domain,
            identity_criterion=_crit(f"{entity}_IDENTITY"),
            membership_criterion=_crit(f"{entity}_MEMBERSHIP"),
            boundary_rule=_rule(f"{entity}_BOUNDARY"),
            parent_types=(),
            forbidden_confusions=(_rule(f"NO_{entity}_CONFUSION"),),
            trace_ref=TraceRef(f"{trace.value}/entities/{entity.lower()}"),
        )
        for entity in (
            "NATURAL_NUMBER",
            "INTEGER",
            "RATIONAL_NUMBER",
            "QUANTITY",
            "UNIT",
            "EXPRESSION",
            "EQUATION",
            "VARIABLE",
            "FUNCTION_CANDIDATE",
            "SOLUTION_SET",
        )
    )
    capabilities = (
        CapabilityContract(
            capability_id=CapabilityId("EQUIVALENCE_PRESERVING_TRANSFORMATION"),
            science_id=science,
            bearer_type=EntityTypeId("EXPRESSION"),
            permitted_operations=(
                _rule("ADDITION"),
                _rule("SUBTRACTION"),
                _rule("MULTIPLICATION"),
                _rule("CONDITIONAL_DIVISION"),
                _rule("SIMPLIFICATION"),
            ),
            permitted_relation_roles=(_rule("LEFT_SIDE"), _rule("RIGHT_SIDE")),
            required_conditions=(_rule("DOMAIN_CONDITION_HOLDS"),),
            blockers=(_rule("DENOMINATOR_ZERO"),),
            evidence_requirements=(EvidenceTypeId("CALCULATION_TRACE"),),
            rank_ceiling=Rank.CANDIDATE,
            residual_policy_ref=_rule("MATH_RESIDUAL_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/capabilities/equivalence_transform"),
        ),
    )
    relations = (
        RelationContract(
            relation_type_id=RelationTypeId("EQUALITY"),
            science_id=science,
            arity=2,
            operand_types=(EntityTypeId("EXPRESSION"), EntityTypeId("EXPRESSION")),
            roles=(_rule("LEFT_EXPR"), _rule("RIGHT_EXPR")),
            direction=RelationDirection.UNDIRECTED,
            compatibility_rules=(_rule("TYPE_COMPATIBILITY"),),
            saturation_rule=_rule("EQUALITY_SATURATION"),
            scope_rule=_rule("FORMAL_SYSTEM_SCOPE"),
            closure_rule=_rule("EQUIVALENCE_CLOSURE"),
            trace_ref=TraceRef(f"{trace.value}/relations/equality"),
        ),
    )
    transformations = (
        TransformationContract(
            transformation_type_id=TransformationTypeId("EQUATION_TO_EQUIVALENT_EQUATION"),
            science_id=science,
            source_types=(EntityTypeId("EQUATION"),),
            target_types=(EntityTypeId("EQUATION"),),
            required_capabilities=(CapabilityId("EQUIVALENCE_PRESERVING_TRANSFORMATION"),),
            preserved_invariants=(_rule("SOLUTION_SET_PRESERVED"),),
            declared_changes=(_rule("NORMAL_FORM_CHANGE"),),
            required_conditions=(_rule("TRANSFORMATION_RULE_LICENSED"),),
            blockers=(_rule("INVALID_TRANSFORMATION"),),
            evidence_requirements=(EvidenceTypeId("INFERENCE_RULE"),),
            rank_ceiling=Rank.CANDIDATE,
            residual_policy_ref=_rule("MATH_RESIDUAL_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/transformations/equation_equivalent"),
        ),
    )
    evidence = (
        ScienceEvidenceContract(
            evidence_type_id=EvidenceTypeId("DEFINITION"),
            science_id=science,
            supported_claim_types=(_rule("DEFINITIONAL_CLAIM"),),
            domain_scope=domain,
            relevance_rule=_rule("DEFINITION_RELEVANCE"),
            coverage_rule=_rule("DEFINITION_COVERAGE"),
            independence_rule=_rule("AXIOMATIC_INDEPENDENCE"),
            counterevidence_rule=_rule("COUNTEREXAMPLE_PRIORITY"),
            global_rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(f"{trace.value}/evidence/definition"),
        ),
        ScienceEvidenceContract(
            evidence_type_id=EvidenceTypeId("INFERENCE_RULE"),
            science_id=science,
            supported_claim_types=(_rule("DERIVATION_CLAIM"),),
            domain_scope=domain,
            relevance_rule=_rule("RULE_RELEVANCE"),
            coverage_rule=_rule("RULE_COVERAGE"),
            independence_rule=_rule("RULE_INDEPENDENCE"),
            counterevidence_rule=_rule("CONTRADICTION_RULE"),
            global_rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(f"{trace.value}/evidence/inference_rule"),
        ),
        ScienceEvidenceContract(
            evidence_type_id=EvidenceTypeId("CALCULATION_TRACE"),
            science_id=science,
            supported_claim_types=(_rule("COMPUTATIONAL_CLAIM"),),
            domain_scope=domain,
            relevance_rule=_rule("TRACE_RELEVANCE"),
            coverage_rule=_rule("TRACE_COVERAGE"),
            independence_rule=_rule("TRACE_REPRODUCIBILITY"),
            counterevidence_rule=_rule("COUNTEREXAMPLE_TRACE"),
            global_rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(f"{trace.value}/evidence/calculation_trace"),
        ),
    )
    judgments = (
        JudgmentContract(
            judgment_type_id=JudgmentTypeId("PROVED"),
            science_id=science,
            supported_claim_types=(_rule("DERIVATION_CLAIM"),),
            required_evidence_types=(EvidenceTypeId("INFERENCE_RULE"),),
            local_rank_name="PROOF_RANK",
            global_rank_ceiling=Rank.CANDIDATE,
            conditions=(_rule("ASSUMPTIONS_EXPLICIT"),),
            blockers=(_rule("RULE_VIOLATION"),),
            downgrade_rules=(_rule("COUNTEREXAMPLE_DOWNGRADE"),),
            trace_ref=TraceRef(f"{trace.value}/judgments/proved"),
        ),
    )
    knowledge_objects = (
        KnowledgeObjectContract(
            knowledge_object_type_id=KnowledgeObjectTypeId("THEOREM"),
            science_id=science,
            subject_types=(EntityTypeId("EXPRESSION"), EntityTypeId("EQUATION")),
            relation_types=(RelationTypeId("EQUALITY"),),
            required_judgments=(JudgmentTypeId("PROVED"),),
            scope_rule=_rule("FORMAL_SYSTEM_SCOPE"),
            exception_policy=_rule("THEOREM_EXCEPTION_POLICY"),
            conflict_policy=_rule("THEOREM_CONFLICT_POLICY"),
            revision_policy=_rule("THEOREM_REVISION_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/knowledge/theorem"),
        ),
    )
    applications = (
        ApplicationContract(
            application_type_id=ApplicationTypeId("SOLVE_NEW_EQUATION"),
            science_id=science,
            knowledge_object_types=(KnowledgeObjectTypeId("THEOREM"),),
            case_entity_types=(EntityTypeId("EQUATION"),),
            membership_criterion=_crit("EQUATION_MEMBERSHIP"),
            required_conditions=(_rule("ASSUMPTIONS_VERIFIED"),),
            blockers=(_rule("DENOMINATOR_ZERO"),),
            invalidating_differences=(_rule("OUTSIDE_DECLARED_DOMAIN"),),
            feedback_policy=_rule("SOLUTION_FEEDBACK_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/applications/solve_equation"),
        ),
    )
    residuals = (
        USMResidual(
            residual_id="math-geometry-excluded",
            kind=USMResidualKind.COVERAGE_GAP,
            detail="geometry is excluded from ElementaryMathematicsReferenceMatrixV1",
            blocking=True,
            visible=True,
            repair_hint="open dedicated geometry branch",
        ),
        USMResidual(
            residual_id="math-universality-unproven",
            kind=USMResidualKind.IRREDUCIBILITY_UNPROVEN,
            detail="universal mathematical completeness is unclaimed",
            blocking=True,
            visible=True,
            repair_hint="add bounded additional matrices only",
        ),
    )
    return UniversalScienceMatrix(
        matrix_id=MatrixId("ElementaryMathematicsReferenceMatrixV1"),
        science_id=science,
        version="1.0",
        declared_scope="Elementary arithmetic and introductory algebra only.",
        entities=entities,
        capabilities=capabilities,
        relations=relations,
        transformations=transformations,
        evidence=evidence,
        judgments=judgments,
        knowledge_objects=knowledge_objects,
        applications=applications,
        residuals=residuals,
        trace_ref=trace,
    )


def make_elementary_mechanics_reference_matrix_v1() -> UniversalScienceMatrix:
    science = ScienceId("ELEMENTARY_MECHANICS")
    domain = DomainId("CLASSICAL_MECHANICS_MEASUREMENT")
    trace = TraceRef("trace://usm/reference/mechanics/v1")
    entities = tuple(
        EntityTypeContract(
            entity_type_id=EntityTypeId(entity),
            science_id=science,
            domain_id=domain,
            identity_criterion=_crit(f"{entity}_IDENTITY"),
            membership_criterion=_crit(f"{entity}_MEMBERSHIP"),
            boundary_rule=_rule(f"{entity}_BOUNDARY"),
            parent_types=(),
            forbidden_confusions=(_rule(f"NO_{entity}_CONFUSION"),),
            trace_ref=TraceRef(f"{trace.value}/entities/{entity.lower()}"),
        )
        for entity in (
            "BODY",
            "MASS",
            "POSITION",
            "TIME",
            "VELOCITY",
            "ACCELERATION",
            "FORCE",
            "REFERENCE_FRAME",
            "MEASURING_INSTRUMENT",
            "MEASUREMENT",
            "EXPERIMENTAL_SYSTEM",
            "MODEL",
        )
    )
    capabilities = (
        CapabilityContract(
            capability_id=CapabilityId("INSTRUMENT_PRODUCES_CALIBRATED_READING"),
            science_id=science,
            bearer_type=EntityTypeId("MEASURING_INSTRUMENT"),
            permitted_operations=(_rule("READ"), _rule("CALIBRATE")),
            permitted_relation_roles=(_rule("INSTRUMENT_OF"),),
            required_conditions=(_rule("CALIBRATION_VALID"), _rule("UNCERTAINTY_DECLARED")),
            blockers=(_rule("CALIBRATION_EXPIRED"),),
            evidence_requirements=(EvidenceTypeId("CALIBRATED_MEASUREMENT"),),
            rank_ceiling=Rank.CANDIDATE,
            residual_policy_ref=_rule("MECHANICS_RESIDUAL_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/capabilities/instrument"),
        ),
    )
    relations = (
        RelationContract(
            relation_type_id=RelationTypeId("POSITION_RELATIVE_TO_FRAME"),
            science_id=science,
            arity=2,
            operand_types=(EntityTypeId("POSITION"), EntityTypeId("REFERENCE_FRAME")),
            roles=(_rule("POSITION"), _rule("FRAME")),
            direction=RelationDirection.DIRECTED,
            compatibility_rules=(_rule("FRAME_COMPATIBILITY"),),
            saturation_rule=_rule("FRAME_RELATION_SATURATION"),
            scope_rule=_rule("MECHANICS_SCOPE"),
            closure_rule=_rule("FRAME_RELATION_CLOSURE"),
            trace_ref=TraceRef(f"{trace.value}/relations/position_frame"),
        ),
    )
    transformations = (
        TransformationContract(
            transformation_type_id=TransformationTypeId("READING_TO_CALIBRATED_MEASUREMENT"),
            science_id=science,
            source_types=(EntityTypeId("MEASUREMENT"),),
            target_types=(EntityTypeId("MEASUREMENT"),),
            required_capabilities=(CapabilityId("INSTRUMENT_PRODUCES_CALIBRATED_READING"),),
            preserved_invariants=(_rule("TRACE_TO_INSTRUMENT"),),
            declared_changes=(_rule("CALIBRATION_METADATA_ATTACHED"),),
            required_conditions=(_rule("UNCERTAINTY_METADATA_PRESENT"),),
            blockers=(_rule("INSTRUMENT_OUT_OF_SCOPE"),),
            evidence_requirements=(EvidenceTypeId("CALIBRATED_MEASUREMENT"),),
            rank_ceiling=Rank.CANDIDATE,
            residual_policy_ref=_rule("MECHANICS_RESIDUAL_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/transformations/reading_calibrated"),
        ),
    )
    evidence = (
        ScienceEvidenceContract(
            evidence_type_id=EvidenceTypeId("OBSERVATION"),
            science_id=science,
            supported_claim_types=(_rule("OBSERVATIONAL_CLAIM"),),
            domain_scope=domain,
            relevance_rule=_rule("OBSERVATION_RELEVANCE"),
            coverage_rule=_rule("OBSERVATION_COVERAGE"),
            independence_rule=_rule("MULTI_OBSERVER_INDEPENDENCE"),
            counterevidence_rule=_rule("CONTRADICTING_OBSERVATION_VISIBLE"),
            global_rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(f"{trace.value}/evidence/observation"),
        ),
        ScienceEvidenceContract(
            evidence_type_id=EvidenceTypeId("CALIBRATED_MEASUREMENT"),
            science_id=science,
            supported_claim_types=(_rule("MEASUREMENT_CLAIM"),),
            domain_scope=domain,
            relevance_rule=_rule("CALIBRATION_RELEVANCE"),
            coverage_rule=_rule("MEASUREMENT_COVERAGE"),
            independence_rule=_rule("INSTRUMENT_DIVERSITY"),
            counterevidence_rule=_rule("UNCERTAINTY_CONFLICT_VISIBLE"),
            global_rank_ceiling=Rank.CANDIDATE,
            trace_ref=TraceRef(f"{trace.value}/evidence/calibrated_measurement"),
        ),
    )
    judgments = (
        JudgmentContract(
            judgment_type_id=JudgmentTypeId("EXPERIMENTALLY_SUPPORTED"),
            science_id=science,
            supported_claim_types=(_rule("MEASUREMENT_CLAIM"),),
            required_evidence_types=(
                EvidenceTypeId("OBSERVATION"),
                EvidenceTypeId("CALIBRATED_MEASUREMENT"),
            ),
            local_rank_name="EXPERIMENTAL_SUPPORT_RANK",
            global_rank_ceiling=Rank.CANDIDATE,
            conditions=(_rule("VALIDITY_DOMAIN_DECLARED"),),
            blockers=(_rule("OUTSIDE_VALIDITY_DOMAIN"),),
            downgrade_rules=(_rule("DOWNGRADE_ON_CONFLICTING_DATA"),),
            trace_ref=TraceRef(f"{trace.value}/judgments/experimental_support"),
        ),
    )
    knowledge_objects = (
        KnowledgeObjectContract(
            knowledge_object_type_id=KnowledgeObjectTypeId("MODEL"),
            science_id=science,
            subject_types=(
                EntityTypeId("BODY"),
                EntityTypeId("FORCE"),
                EntityTypeId("ACCELERATION"),
            ),
            relation_types=(RelationTypeId("POSITION_RELATIVE_TO_FRAME"),),
            required_judgments=(JudgmentTypeId("EXPERIMENTALLY_SUPPORTED"),),
            scope_rule=_rule("VALIDITY_DOMAIN_RULE"),
            exception_policy=_rule("MODEL_EXCEPTION_POLICY"),
            conflict_policy=_rule("MODEL_CONFLICT_POLICY"),
            revision_policy=_rule("MODEL_REVISION_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/knowledge/model"),
        ),
    )
    applications = (
        ApplicationContract(
            application_type_id=ApplicationTypeId("PREDICT_NEW_BOUNDED_CASE"),
            science_id=science,
            knowledge_object_types=(KnowledgeObjectTypeId("MODEL"),),
            case_entity_types=(EntityTypeId("EXPERIMENTAL_SYSTEM"),),
            membership_criterion=_crit("SYSTEM_MEMBERSHIP"),
            required_conditions=(_rule("VALIDITY_DOMAIN_CONFIRMED"),),
            blockers=(_rule("DOMAIN_MISMATCH"),),
            invalidating_differences=(_rule("UNMEASURED_REQUIRED_VARIABLE"),),
            feedback_policy=_rule("MODEL_FEEDBACK_POLICY"),
            trace_ref=TraceRef(f"{trace.value}/applications/predict_case"),
        ),
    )
    residuals = (
        USMResidual(
            residual_id="mechanics-relativity-excluded",
            kind=USMResidualKind.COVERAGE_GAP,
            detail="relativity is excluded from this elementary mechanics matrix",
            blocking=True,
            visible=True,
            repair_hint="open dedicated relativity matrix branch",
        ),
        USMResidual(
            residual_id="mechanics-causality-not-closed",
            kind=USMResidualKind.APPLICATION_SCOPE_UNRESOLVED,
            detail="causal inference is not closed by temporal succession alone",
            blocking=False,
            visible=True,
            repair_hint="add causal-method gate",
        ),
        USMResidual(
            residual_id="mechanics-universality-unproven",
            kind=USMResidualKind.IRREDUCIBILITY_UNPROVEN,
            detail="final universality claim remains unproven",
            blocking=True,
            visible=True,
            repair_hint="expand bounded reference families",
        ),
    )
    return UniversalScienceMatrix(
        matrix_id=MatrixId("ElementaryMechanicsReferenceMatrixV1"),
        science_id=science,
        version="1.0",
        declared_scope="Elementary classical mechanics and measurement discipline.",
        entities=entities,
        capabilities=capabilities,
        relations=relations,
        transformations=transformations,
        evidence=evidence,
        judgments=judgments,
        knowledge_objects=knowledge_objects,
        applications=applications,
        residuals=residuals,
        trace_ref=trace,
    )


def load_reference_matrices_v1() -> tuple[UniversalScienceMatrix, ...]:
    return (
        make_arabic_reference_matrix_v1(),
        make_elementary_mathematics_reference_matrix_v1(),
        make_elementary_mechanics_reference_matrix_v1(),
    )


__all__ = [
    "load_reference_matrices_v1",
    "make_arabic_reference_matrix_v1",
    "make_elementary_mathematics_reference_matrix_v1",
    "make_elementary_mechanics_reference_matrix_v1",
]
