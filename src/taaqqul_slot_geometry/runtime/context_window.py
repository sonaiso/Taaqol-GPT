from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TokenCarrier:
    token_id: str
    surface: str
    index: int


@dataclass(frozen=True, slots=True)
class MultiTokenSpanCarrier:
    span_id: str
    token_ids: tuple[str, ...]
    surface: str


@dataclass(frozen=True, slots=True)
class CompositionReadinessCandidate:
    span: MultiTokenSpanCarrier
    contracted_unit_ids: tuple[str, ...]
    candidate_link_operator: str | None
    identity_compatible: bool
    bearability_compatible: bool
    reference_ready: bool
    relation_kind_candidate: str | None
    evidence_refs: tuple[str, ...]
    residuals: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ContextWindow:
    corpus_id: str
    tokens: tuple[TokenCarrier, ...]

    def span(self, start: int, end: int) -> MultiTokenSpanCarrier:
        if start < 0 or end > len(self.tokens) or start >= end:
            raise ValueError("invalid span bounds")
        items = self.tokens[start:end]
        return MultiTokenSpanCarrier(
            span_id=f"{self.corpus_id}:span:{start}-{end}",
            token_ids=tuple(t.token_id for t in items),
            surface=" ".join(t.surface for t in items),
        )
