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

Nothing else moves in GPT-K1: no ReasonablenessVerdict, no MaqamGPT,
no MantuqGPT, no MafhumGPT, no pipeline code, no adapter or audit changes
(docs/55 §13, §15).
"""

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
