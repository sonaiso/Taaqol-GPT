"""GPT-K2 — Minimal Golden Origins Dataset loader.

Binding:
- docs/54 §6 (GPT-K2 roadmap declaration)
- docs/55 §13, §16 (golden dataset shape; test/calibration only)
- docs/14 chain row GPT-K2 (dataset only, no verdict/gate/pipeline behavior)

This module ships immutable dataset carriers and a deterministic loader for the
minimal golden dataset used by constitutional verification tests.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from taaqqul_slot_geometry.gpt.knowledge_origins import (
    AttributeEventOrigin,
    EntityGenusOrigin,
    EvidenceDirection,
    EvidenceOrigin,
    OriginRank,
    OriginStability,
    ReferenceOrigin,
    RelationOperatorOrigin,
    ResolutionType,
)

_DATA_DIR = Path(__file__).resolve().parent / "data"
_DEFAULT_DATA_PATH = _DATA_DIR / "coverage_matrix_v2.json"


class GoldenOriginsDatasetError(ValueError):
    """Dataset content does not match the GPT-K2 contract surface."""


@dataclass(frozen=True, slots=True)
class GoldenCoverageCase:
    """A single calibration/verification case from coverage_matrix_v2."""

    case_id: str
    text: str
    expected_path: str
    expected_result: str
    expected_stage: str
    rationale: str


@dataclass(frozen=True, slots=True)
class GoldenOriginsDataset:
    """Immutable in-memory GPT-K2 dataset surface."""

    schema_version: str
    origin_law: str
    branch_name: str
    entities: tuple[EntityGenusOrigin, ...]
    attributes: tuple[AttributeEventOrigin, ...]
    relations: tuple[RelationOperatorOrigin, ...]
    references: tuple[ReferenceOrigin, ...]
    evidence_entries: tuple[EvidenceOrigin, ...]
    coverage_matrix: tuple[GoldenCoverageCase, ...]


def default_coverage_matrix_path() -> Path:
    """Return the repository path of the bundled GPT-K2 dataset."""

    return _DEFAULT_DATA_PATH


def load_golden_origins_dataset(path: Path | None = None) -> GoldenOriginsDataset:
    """Load the GPT-K2 minimal golden dataset from JSON."""

    data_path = path or _DEFAULT_DATA_PATH
    try:
        payload = json.loads(data_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise GoldenOriginsDatasetError(f"failed to read dataset: {data_path}") from exc
    except json.JSONDecodeError as exc:
        raise GoldenOriginsDatasetError(f"invalid JSON in dataset: {data_path}") from exc

    entities = tuple(
        EntityGenusOrigin(
            entity_id=item["entity_id"],
            genus=item["genus"],
            essential_properties=tuple(item["essential_properties"]),
            bearing_capacity=tuple(item["bearing_capacity"]),
            bearing_refusal=tuple(item["bearing_refusal"]),
            domain=item["domain"],
            stability=OriginStability(item["stability"]),
            source_ref=item["source_ref"],
            rank=OriginRank(item["rank"]),
            residuals=tuple(item["residuals"]),
        )
        for item in payload["entities"]
    )
    attributes = tuple(
        AttributeEventOrigin(
            attribute_id=item["attribute_id"],
            required_conditions=tuple(item["required_conditions"]),
            contradicting_conditions=tuple(item["contradicting_conditions"]),
            typical_bearers=tuple(item["typical_bearers"]),
            impossible_bearers=tuple(item["impossible_bearers"]),
            domain=item["domain"],
            stability=OriginStability(item["stability"]),
            source_ref=item["source_ref"],
            rank=OriginRank(item["rank"]),
            residuals=tuple(item["residuals"]),
        )
        for item in payload["attributes"]
    )
    relations = tuple(
        RelationOperatorOrigin(
            relation_id=item["relation_id"],
            argument_structure=item["argument_structure"],
            presuppositions=tuple(item["presuppositions"]),
            binding_semantics=item["binding_semantics"],
            domain=item["domain"],
            stability=OriginStability(item["stability"]),
            source_ref=item["source_ref"],
            rank=OriginRank(item["rank"]),
            residuals=tuple(item["residuals"]),
        )
        for item in payload["relations"]
    )
    references = tuple(
        ReferenceOrigin(
            reference_id=item["reference_id"],
            referent=item["referent"],
            resolution_type=ResolutionType(item["resolution_type"]),
            confidence=OriginRank(item["confidence"]),
            domain=item["domain"],
            maqam_dependency=OriginRank(item["maqam_dependency"]),
            residuals=tuple(item["residuals"]),
        )
        for item in payload["references"]
    )
    evidence_entries = tuple(
        EvidenceOrigin(
            claim_ref=item["claim_ref"],
            evidence_type=item["evidence_type"],
            evidence_direction=EvidenceDirection(item["evidence_direction"]),
            evidence_content=item["evidence_content"],
            source=item["source"],
            source_rank=OriginRank(item["source_rank"]),
            recency=OriginStability(item["recency"]),
            domain=item["domain"],
            stability=OriginStability(item["stability"]),
            residuals=tuple(item["residuals"]),
            contradiction_with=tuple(item["contradiction_with"]),
        )
        for item in payload["evidence_entries"]
    )
    coverage_matrix = tuple(
        GoldenCoverageCase(
            case_id=item["case_id"],
            text=item["text"],
            expected_path=item["expected_path"],
            expected_result=item["expected_result"],
            expected_stage=item["expected_stage"],
            rationale=item["rationale"],
        )
        for item in payload["coverage_matrix"]
    )

    dataset = GoldenOriginsDataset(
        schema_version=payload["schema_version"],
        origin_law=payload["origin_law"],
        branch_name=payload["branch_name"],
        entities=entities,
        attributes=attributes,
        relations=relations,
        references=references,
        evidence_entries=evidence_entries,
        coverage_matrix=coverage_matrix,
    )
    _assert_gpt_k2_counts(dataset)
    return dataset


def _assert_gpt_k2_counts(dataset: GoldenOriginsDataset) -> None:
    if len(dataset.entities) != 50:
        raise GoldenOriginsDatasetError("GPT-K2 requires 50 entities")
    if len(dataset.attributes) != 50:
        raise GoldenOriginsDatasetError("GPT-K2 requires 50 attributes")
    if len(dataset.relations) != 30:
        raise GoldenOriginsDatasetError("GPT-K2 requires 30 relations")
    if len(dataset.references) != 20:
        raise GoldenOriginsDatasetError("GPT-K2 requires 20 references")
    if len(dataset.evidence_entries) != 50:
        raise GoldenOriginsDatasetError("GPT-K2 requires 50 evidence entries")
    if len(dataset.coverage_matrix) != 50:
        raise GoldenOriginsDatasetError("GPT-K2 requires 50 coverage cases")


__all__ = [
    "GoldenCoverageCase",
    "GoldenOriginsDataset",
    "GoldenOriginsDatasetError",
    "default_coverage_matrix_path",
    "load_golden_origins_dataset",
]
