"""``taaqqul_slot_geometry.gpt`` — the GPT reasonableness branch.

GPT-K1 carrier surface — binding ``docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md``
under the docs/14 chain row *GPT-K1 — Origin Schema Carriers*. That row licenses
**carriers only**: frozen dataclasses representing the five Knowledge Origins,
OriginBinding, and OriginResidual — no verdicts, no gates, no full pipeline.

The five Knowledge Origins:

* :class:`EntityGenusOrigin` — what an entity IS (genus, bearing capacity).
* :class:`AttributeEventOrigin` — what a predicate REQUIRES (conditions).
* :class:`RelationOperatorOrigin` — what a relation/operator MEANS (binding).
* :class:`ReferenceOrigin` — what a reference expression POINTS TO.
* :class:`EvidenceOrigin` — what SUPPORTS or REFUTES a claim.

Plus the binding and residual carriers:

* :class:`OriginBinding` — connects a MantuqGPT claim to origin(s).
* :class:`OriginResidualKind` — the nine typed residual kinds (docs/55 §8.3).
* :class:`OriginResidual` — a single residual from an incomplete binding.

GPT-R1 adds the input-envelope carrier:

* :class:`GPTAnswerInput` — request/answer envelope and pre-boundary hints.

GPT-R2 adds the maqam boundary:

* :class:`MaqamGPT` — preserved question context and constraints.
* :class:`MaqamCommunicationMode` — structural ikhbar/insha maqām label.

GPT-R3 adds the mantuq boundary:

* :class:`MantuqGPT` — explicit GPT claims only, with trace.
* :class:`ExplicitClaim` / :class:`ClaimBoundary` — explicit claim surfaces.

GPT-R4 adds the mafhum boundary:

* :class:`MafhumGPT` — licensed implication candidate derived from MantuqGPT.
* Restriction, scope, non-mention, type, and preventer surfaces.

GPT-R5 adds the origin binding gate:

* :class:`OriginBindingClaim` — selected MantuqGPT / MafhumGPT claim surface.
* :class:`OriginBindingGateResult` — bounded origin-binding gate result.

GPT-R6 adds reasonableness gates:

* :class:`ReasonablenessGateDecision` — one bounded gate decision.
* :class:`ReasonablenessGateReport` — aggregate gate report (pre-verdict).
* :func:`run_reasonableness_gates` — evaluates six licensed gates only.

GPT-R7 adds the bounded verdict surface:

* :class:`GPTAnswerReasonablenessVerdict` — verdict-state mapping from R6.
* :func:`prove_gpt_answer_reasonableness_verdict` — consumes R6 reports only.

The GPT surface still has no audit integration and no pipeline code.
"""

from taaqqul_slot_geometry.gpt.input_contract import (
    GPTAnswerInput,
    InputContractSchemaError,
    InputEvidenceNeed,
    InputRiskLevel,
    InputTimeSensitivity,
)
from taaqqul_slot_geometry.gpt.knowledge_origins import (
    AttributeEventOrigin,
    BindingVerdict,
    EntityGenusOrigin,
    EvidenceDirection,
    EvidenceOrigin,
    OriginBinding,
    OriginCarrierSchemaError,
    OriginRank,
    OriginResidual,
    OriginResidualKind,
    OriginStability,
    ReferenceOrigin,
    RelationOperatorOrigin,
    ResolutionType,
)
from taaqqul_slot_geometry.gpt.mafhum_boundary import (
    GPT_MAFHUM_TRANSITION_CONTRACT,
    ExplicitRestriction,
    MafhumGPT,
    MafhumGPTResult,
    MafhumGPTSchemaError,
    MafhumGPTState,
    MafhumType,
    PreventerGateResult,
    PreventerKind,
    RestrictionKind,
    ScopeBoundary,
    SilenceNonMention,
    build_mafhum_gpt,
)
from taaqqul_slot_geometry.gpt.mantuq_boundary import (
    ClaimBoundary,
    ExplicitClaim,
    MantuqGPT,
    MantuqGPTSchemaError,
    build_mantuq_gpt,
)
from taaqqul_slot_geometry.gpt.maqam_boundary import (
    MaqamCommunicationMode,
    MaqamGPT,
    MaqamGPTSchemaError,
    build_maqam_gpt,
    classify_maqam_communication_mode,
)
from taaqqul_slot_geometry.gpt.origin_binding_gate import (
    GPT_ORIGIN_BINDING_TRANSITION_CONTRACT,
    KnowledgeOrigin,
    OriginBindingClaim,
    OriginBindingGateResult,
    OriginBindingGateSchemaError,
    OriginBindingGateState,
    OriginBindingRequiredOriginType,
    OriginBindingSourceKind,
    bind_origin_to_claim,
    claim_from_mafhum,
    claim_from_mantuq_boundary,
)
from taaqqul_slot_geometry.gpt.reasonableness_gates import (
    GPT_REASONABLENESS_GATES_TRANSITION_CONTRACT,
    ReasonablenessGateDecision,
    ReasonablenessGateKind,
    ReasonablenessGateReport,
    ReasonablenessGateReportState,
    ReasonablenessGateSchemaError,
    ReasonablenessGateState,
    run_reasonableness_gates,
)
from taaqqul_slot_geometry.gpt.reasonableness_verdict import (
    GPT_REASONABLENESS_VERDICT_TRANSITION_CONTRACT,
    GPTAnswerReasonablenessVerdict,
    ReasonablenessVerdictSchemaError,
    ReasonablenessVerdictState,
    prove_gpt_answer_reasonableness_verdict,
)

__all__ = [
    "ClaimBoundary",
    "ExplicitClaim",
    "ExplicitRestriction",
    "GPT_MAFHUM_TRANSITION_CONTRACT",
    "GPT_ORIGIN_BINDING_TRANSITION_CONTRACT",
    "GPTAnswerInput",
    "InputContractSchemaError",
    "InputEvidenceNeed",
    "InputRiskLevel",
    "InputTimeSensitivity",
    "KnowledgeOrigin",
    "MafhumGPT",
    "MafhumGPTResult",
    "MafhumGPTSchemaError",
    "MafhumGPTState",
    "MafhumType",
    "MaqamCommunicationMode",
    "MaqamGPT",
    "MaqamGPTSchemaError",
    "MantuqGPT",
    "MantuqGPTSchemaError",
    "PreventerGateResult",
    "PreventerKind",
    "RestrictionKind",
    "ScopeBoundary",
    "SilenceNonMention",
    "build_mafhum_gpt",
    "build_maqam_gpt",
    "build_mantuq_gpt",
    "bind_origin_to_claim",
    "classify_maqam_communication_mode",
    "claim_from_mafhum",
    "claim_from_mantuq_boundary",
    "AttributeEventOrigin",
    "BindingVerdict",
    "EntityGenusOrigin",
    "EvidenceDirection",
    "EvidenceOrigin",
    "OriginBinding",
    "OriginBindingClaim",
    "OriginBindingGateResult",
    "OriginBindingGateSchemaError",
    "OriginBindingGateState",
    "OriginBindingRequiredOriginType",
    "OriginBindingSourceKind",
    "OriginCarrierSchemaError",
    "OriginRank",
    "OriginResidual",
    "OriginResidualKind",
    "OriginStability",
    "ReferenceOrigin",
    "RelationOperatorOrigin",
    "ResolutionType",
    "GPT_REASONABLENESS_GATES_TRANSITION_CONTRACT",
    "GPT_REASONABLENESS_VERDICT_TRANSITION_CONTRACT",
    "GPTAnswerReasonablenessVerdict",
    "ReasonablenessGateDecision",
    "ReasonablenessGateKind",
    "ReasonablenessGateReport",
    "ReasonablenessGateReportState",
    "ReasonablenessGateSchemaError",
    "ReasonablenessGateState",
    "ReasonablenessVerdictSchemaError",
    "ReasonablenessVerdictState",
    "prove_gpt_answer_reasonableness_verdict",
    "run_reasonableness_gates",
]
