from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TriadMappingHypothesis:
    entity_mapping: str = "Program Entity ≈ اسم"
    transformation_mapping: str = "Program Transformation ≈ فعل"
    relation_mapping: str = "Program Relation ≈ حرف"
    statement: str = "Triad is a structuring hypothesis, not an acceptance proof."
    is_structuring_hypothesis: bool = True
    acceptance_proof: bool = False
