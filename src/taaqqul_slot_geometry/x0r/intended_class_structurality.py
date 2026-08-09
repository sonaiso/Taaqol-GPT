"""V0.29a Intended-Class Structurality Attack runtime surface.

This module defines a fragment-local structural intended class ``K_i`` as
``Mod(T_i)`` over a structural signature ``Σ_K`` and enforces an executable
anti-smuggling boundary:

- Membership is structural only.
- Claim/checker/extractor/cutoff vocabulary is forbidden in ``Σ_K`` and ``T_K``.
- Non-membership must produce structural violation witnesses.
- Claim-independence is testable on extended models by projection to ``Σ_K``.

Scope is intentionally narrow: this module does not define any claim equivalence,
representation theorem, FRP, finite quotient, cutoff, candidate completeness, or
context completeness.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Callable, Iterable


@dataclass(frozen=True)
class StructuralNode:
    """Smallest structural unit in the V0.29a selected fragment."""

    node_id: str
    boundary_id: str
    domain_id: str
    scope_id: str
    trace_ref: str


@dataclass(frozen=True)
class StructuralFragmentModel:
    """Finite model over the selected fragment signature ``Σ_K``."""

    model_id: str
    nodes: tuple[StructuralNode, ...]


@dataclass(frozen=True)
class EvaluationOverlay:
    """Downstream/non-structural fields excluded from ``Σ_K`` and ``T_K``."""

    claim_truth_value: bool | None = None
    checker_output: str | None = None
    extractor_output: str | None = None
    b_min_candidate: str | None = None
    cutoff_result: str | None = None
    contextual_equivalence_result: str | None = None
    algorithm_success: bool | None = None


@dataclass(frozen=True)
class ExtendedFragmentModel:
    """Model + non-structural overlay for claim-independence checks."""

    structural: StructuralFragmentModel
    overlay: EvaluationOverlay


@dataclass(frozen=True)
class StructuralViolationWitness:
    """Executable witness for ``Violation_K(M, w)``."""

    model_id: str
    axiom_id: str
    locus: str
    observed: str
    expected: str


@dataclass(frozen=True)
class IntendedClassMembership:
    """Membership verdict and witness set for V0.29a."""

    in_intended_class: bool
    witnesses: tuple[StructuralViolationWitness, ...]


AxiomValidator = Callable[[StructuralFragmentModel], tuple[StructuralViolationWitness, ...]]


@dataclass(frozen=True)
class StructuralAxiom:
    """Axiom in ``T_K`` with an executable local validator."""

    axiom_id: str
    symbols: frozenset[str]
    validator: AxiomValidator


@dataclass(frozen=True)
class StructuralTheory:
    """Fragment-local intended-class theory ``T_i`` over ``Σ_K``."""

    fragment_id: str
    signature_sigma_k: frozenset[str]
    axioms: tuple[StructuralAxiom, ...]


ANTI_SMUGGLING_FORBIDDEN_TOKENS: frozenset[str] = frozenset(
    {
        "psi",
        "correct",
        "accept",
        "checker",
        "extractor",
        "b_min",
        "bmin",
        "cutoff",
        "contextual",
        "equivalence",
        "algorithm_success",
        "claim_truth",
        "representation_adequacy",
    }
)

# Selected smallest fragment (already aligned with repository architecture):
# finite carrier-node structure with explicit boundary/domain/scope/trace fields.
SIGMA_K_S0: frozenset[str] = frozenset(
    {
        "Node",
        "node_id",
        "boundary_id",
        "domain_id",
        "scope_id",
        "trace_ref",
    }
)


@dataclass(frozen=True)
class AntiSmugglingViolation:
    locus: str
    symbol: str
    forbidden_token: str


def _tokenize(symbol: str) -> tuple[str, ...]:
    return tuple(re.findall(r"[a-z0-9_]+", symbol.lower()))


def _non_empty(value: str) -> bool:
    return bool(value and value.strip())


def _axiom_non_empty_node_set(
    model: StructuralFragmentModel,
) -> tuple[StructuralViolationWitness, ...]:
    if model.nodes:
        return ()
    return (
        StructuralViolationWitness(
            model_id=model.model_id,
            axiom_id="TK_S0_A1_NON_EMPTY_NODE_SET",
            locus="model.nodes",
            observed="empty",
            expected="at least one StructuralNode",
        ),
    )


def _axiom_unique_node_ids(
    model: StructuralFragmentModel,
) -> tuple[StructuralViolationWitness, ...]:
    seen: set[str] = set()
    witnesses: list[StructuralViolationWitness] = []
    for idx, node in enumerate(model.nodes):
        if node.node_id in seen:
            witnesses.append(
                StructuralViolationWitness(
                    model_id=model.model_id,
                    axiom_id="TK_S0_A2_UNIQUE_NODE_IDS",
                    locus=f"nodes[{idx}].node_id",
                    observed=node.node_id,
                    expected="globally unique node_id within the model",
                )
            )
        seen.add(node.node_id)
    return tuple(witnesses)


def _axiom_node_fields_non_empty(
    model: StructuralFragmentModel,
) -> tuple[StructuralViolationWitness, ...]:
    witnesses: list[StructuralViolationWitness] = []
    for idx, node in enumerate(model.nodes):
        required = {
            "node_id": node.node_id,
            "boundary_id": node.boundary_id,
            "domain_id": node.domain_id,
            "scope_id": node.scope_id,
            "trace_ref": node.trace_ref,
        }
        for field_name, value in required.items():
            if _non_empty(value):
                continue
            witnesses.append(
                StructuralViolationWitness(
                    model_id=model.model_id,
                    axiom_id="TK_S0_A3_TOTAL_STRUCTURAL_FIELDS",
                    locus=f"nodes[{idx}].{field_name}",
                    observed=repr(value),
                    expected="non-empty structural field",
                )
            )
    return tuple(witnesses)


def _axiom_trace_refs_injective_over_nodes(
    model: StructuralFragmentModel,
) -> tuple[StructuralViolationWitness, ...]:
    seen: set[str] = set()
    witnesses: list[StructuralViolationWitness] = []
    for idx, node in enumerate(model.nodes):
        if node.trace_ref in seen:
            witnesses.append(
                StructuralViolationWitness(
                    model_id=model.model_id,
                    axiom_id="TK_S0_A4_TRACE_REF_INJECTIVE",
                    locus=f"nodes[{idx}].trace_ref",
                    observed=node.trace_ref,
                    expected="trace_ref injective over nodes in this fragment",
                )
            )
        seen.add(node.trace_ref)
    return tuple(witnesses)


T_K_S0 = StructuralTheory(
    fragment_id="K_S0_CARRIER_NODE_FRAGMENT",
    signature_sigma_k=SIGMA_K_S0,
    axioms=(
        StructuralAxiom(
            axiom_id="TK_S0_A1_NON_EMPTY_NODE_SET",
            symbols=frozenset({"Node", "node_id"}),
            validator=_axiom_non_empty_node_set,
        ),
        StructuralAxiom(
            axiom_id="TK_S0_A2_UNIQUE_NODE_IDS",
            symbols=frozenset({"Node", "node_id"}),
            validator=_axiom_unique_node_ids,
        ),
        StructuralAxiom(
            axiom_id="TK_S0_A3_TOTAL_STRUCTURAL_FIELDS",
            symbols=frozenset(
                {"Node", "node_id", "boundary_id", "domain_id", "scope_id", "trace_ref"}
            ),
            validator=_axiom_node_fields_non_empty,
        ),
        StructuralAxiom(
            axiom_id="TK_S0_A4_TRACE_REF_INJECTIVE",
            symbols=frozenset({"Node", "trace_ref"}),
            validator=_axiom_trace_refs_injective_over_nodes,
        ),
    ),
)

FRAGMENT_THEORIES: dict[str, StructuralTheory] = {
    T_K_S0.fragment_id: T_K_S0,
}


def anti_smuggling_violations(
    theory: StructuralTheory,
    forbidden_tokens: frozenset[str] = ANTI_SMUGGLING_FORBIDDEN_TOKENS,
) -> tuple[AntiSmugglingViolation, ...]:
    """Return all anti-smuggling violations in ``Σ_K`` and ``T_K``."""

    violations: list[AntiSmugglingViolation] = []

    def _scan_symbol(locus: str, symbol: str) -> None:
        tokens = _tokenize(symbol)
        for token in forbidden_tokens:
            if token in tokens:
                violations.append(
                    AntiSmugglingViolation(
                        locus=locus,
                        symbol=symbol,
                        forbidden_token=token,
                    )
                )

    for symbol in theory.signature_sigma_k:
        _scan_symbol("signature_sigma_k", symbol)

    for axiom in theory.axioms:
        _scan_symbol(f"axiom_id:{axiom.axiom_id}", axiom.axiom_id)
        for symbol in axiom.symbols:
            _scan_symbol(f"axiom_symbol:{axiom.axiom_id}", symbol)

    return tuple(violations)


def anti_smuggling_holds(
    theory: StructuralTheory,
    forbidden_tokens: frozenset[str] = ANTI_SMUGGLING_FORBIDDEN_TOKENS,
) -> bool:
    return not anti_smuggling_violations(theory, forbidden_tokens=forbidden_tokens)


def violation_k(
    model: StructuralFragmentModel,
    witness: StructuralViolationWitness,
    *,
    theory: StructuralTheory = T_K_S0,
) -> bool:
    """Executable predicate for ``Violation_K(M, w)``."""

    return witness in classify_membership(model, theory=theory).witnesses


def classify_membership(
    model: StructuralFragmentModel,
    *,
    theory: StructuralTheory = T_K_S0,
) -> IntendedClassMembership:
    """Compute ``M ∈ K_i`` or return explicit structural violation witnesses."""

    witnesses: list[StructuralViolationWitness] = []
    for axiom in theory.axioms:
        witnesses.extend(axiom.validator(model))

    return IntendedClassMembership(
        in_intended_class=not witnesses,
        witnesses=tuple(witnesses),
    )


def in_intended_class(
    model: StructuralFragmentModel,
    *,
    theory: StructuralTheory = T_K_S0,
) -> bool:
    """Membership predicate for ``K_i := Mod(T_i)``."""

    return classify_membership(model, theory=theory).in_intended_class


def models_of(
    theory: StructuralTheory,
    candidates: Iterable[StructuralFragmentModel],
) -> tuple[StructuralFragmentModel, ...]:
    """Finite realization of ``Mod(T_i)`` over a candidate pool."""

    return tuple(model for model in candidates if in_intended_class(model, theory=theory))


def project_to_sigma_k(
    model: ExtendedFragmentModel | StructuralFragmentModel,
) -> StructuralFragmentModel:
    """Forget non-structural overlay and keep only ``Σ_K`` structure."""

    if isinstance(model, StructuralFragmentModel):
        return model
    return model.structural


def structurality_theorem_holds(
    left: ExtendedFragmentModel,
    right: ExtendedFragmentModel,
    *,
    theory: StructuralTheory = T_K_S0,
) -> bool:
    """Claim-independence theorem for the selected fragment.

    If two extended models agree on their ``Σ_K`` projection, then
    intended-class membership is equal.
    """

    if project_to_sigma_k(left) != project_to_sigma_k(right):
        raise ValueError("structurality theorem requires equal Σ_K projections")
    return in_intended_class(left.structural, theory=theory) == in_intended_class(
        right.structural, theory=theory
    )


def non_membership_has_witness(
    model: StructuralFragmentModel,
    *,
    theory: StructuralTheory = T_K_S0,
) -> bool:
    """Falsifiability condition: ``M ∉ K_i => ∃w Violation_K(M,w)``."""

    verdict = classify_membership(model, theory=theory)
    if verdict.in_intended_class:
        return True
    return len(verdict.witnesses) > 0


__all__ = [
    "ANTI_SMUGGLING_FORBIDDEN_TOKENS",
    "SIGMA_K_S0",
    "T_K_S0",
    "FRAGMENT_THEORIES",
    "AntiSmugglingViolation",
    "EvaluationOverlay",
    "ExtendedFragmentModel",
    "IntendedClassMembership",
    "StructuralAxiom",
    "StructuralFragmentModel",
    "StructuralNode",
    "StructuralTheory",
    "StructuralViolationWitness",
    "anti_smuggling_holds",
    "anti_smuggling_violations",
    "classify_membership",
    "in_intended_class",
    "models_of",
    "non_membership_has_witness",
    "project_to_sigma_k",
    "structurality_theorem_holds",
    "violation_k",
]
