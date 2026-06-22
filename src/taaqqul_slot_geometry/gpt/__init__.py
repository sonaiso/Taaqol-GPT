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

GPT-R1 remains carrier-only: no MaqamGPT verdict, no extraction, no gates,
no reasonableness verdict, and no pipeline code.
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

__all__ = [
    "GPTAnswerInput",
    "InputContractSchemaError",
    "InputEvidenceNeed",
    "InputRiskLevel",
    "InputTimeSensitivity",
    "AttributeEventOrigin",
    "BindingVerdict",
    "EntityGenusOrigin",
    "EvidenceDirection",
    "EvidenceOrigin",
    "OriginBinding",
    "OriginCarrierSchemaError",
    "OriginRank",
    "OriginResidual",
    "OriginResidualKind",
    "OriginStability",
    "ReferenceOrigin",
    "RelationOperatorOrigin",
    "ResolutionType",
]
