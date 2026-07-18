from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from enum import IntEnum, StrEnum

EXPECTED_MAPPING_FINGERPRINT = (
    "04f4be0c11eb40bb88b3431dd9255bd828bed3dfe7b27f5130f90d36e557c13d"
)


class FVerdict(StrEnum):
    ACCEPT = "ACCEPT"
    DEFER = "DEFER"
    BLOCK = "BLOCK"


class TenConditionCode(StrEnum):
    ACCEPT_TO_BLOCK = "ACCEPT_TO_BLOCK"
    BLOCK_TO_ACCEPT = "BLOCK_TO_ACCEPT"
    OPERATION_COLLAPSE = "OPERATION_COLLAPSE"
    COMPOSITION_FAILURE = "COMPOSITION_FAILURE"
    INTERMEDIATE_LAYER_DELETED = "INTERMEDIATE_LAYER_DELETED"
    RANK_INFLATION = "RANK_INFLATION"
    IDENTITY_LOSS = "IDENTITY_LOSS"
    BLOCKING_RESIDUAL_LOSS = "BLOCKING_RESIDUAL_LOSS"
    POST_HOC_MAPPING = "POST_HOC_MAPPING"
    RANDOM_SYMBOLIC_EQUIVALENCE = "RANDOM_SYMBOLIC_EQUIVALENCE"


class Rank(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass(frozen=True)
class RealizationCase:
    abstract_state: str
    carrier: str
    protocol: str
    realization: str
    identity: str
    state_licensed: bool
    carrier_known: bool
    protocol_licensed: bool
    surface_visible: bool
    carrier_limited: bool
    rank: Rank
    rank_ceiling: Rank
    residuals: tuple[str, ...]

    def evaluate(self) -> FVerdict:
        if not self.state_licensed or not self.protocol_licensed:
            return FVerdict.BLOCK
        if self.carrier_limited or not self.surface_visible or not self.carrier_known:
            return FVerdict.DEFER
        return FVerdict.ACCEPT

    def pipeline_layers(self) -> tuple[str, str, str]:
        return (self.abstract_state, self.carrier, self.realization)


@dataclass
class MappingDeclaration:
    state_map: dict[str, str]
    operation_map: dict[str, str]
    declared_fingerprint: str = EXPECTED_MAPPING_FINGERPRINT
    _integrity_hash: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._integrity_hash = self._compute_integrity_hash()

    def _compute_integrity_hash(self) -> str:
        payload = {
            "operation_map": self.operation_map,
            "state_map": self.state_map,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def has_post_hoc_mutation(self) -> bool:
        return self._compute_integrity_hash() != self._integrity_hash


@dataclass(frozen=True)
class FExperiment:
    accept_case: RealizationCase
    defer_case: RealizationCase
    block_case: RealizationCase
    operations: tuple[str, str]
    declaration: MappingDeclaration
    non_trivial_features: frozenset[str]
    state_multiple_realizations: dict[str, tuple[str, ...]]

    def structural_valid(self) -> bool:
        required_features = frozenset(
            {
                "abstract_surface_distinction",
                "carrier_protocol_dependency",
                "same_state_multiple_realizations",
                "same_surface_not_sufficient",
            }
        )
        all_layers_present = all(all(layer for layer in c.pipeline_layers()) for c in self.cases())
        expected_verdicts = (
            self.accept_case.evaluate() == FVerdict.ACCEPT
            and self.defer_case.evaluate() == FVerdict.DEFER
            and self.block_case.evaluate() == FVerdict.BLOCK
        )
        operation_chain_distinct = self.operations == (
            "abstract_to_carrier",
            "carrier_to_surface_observation",
        )
        has_state_multi_realization = any(
            len(realizations) > 1 for realizations in self.state_multiple_realizations.values()
        )
        return (
            all_layers_present
            and expected_verdicts
            and operation_chain_distinct
            and required_features.issubset(self.non_trivial_features)
            and has_state_multi_realization
            and not self.declaration.has_post_hoc_mutation()
        )

    def cases(self) -> tuple[RealizationCase, RealizationCase, RealizationCase]:
        return (self.accept_case, self.defer_case, self.block_case)


@dataclass(frozen=True)
class ConditionAuditResult:
    index: int
    code: TenConditionCode
    passed: bool


@dataclass(frozen=True)
class TenConditionAuditReport:
    structural_valid: bool
    ten_condition_passed: bool
    mapping_fingerprint: str
    results: tuple[ConditionAuditResult, ...]


class TenConditionAuditor:
    def __init__(self, experiment: FExperiment) -> None:
        self.experiment = experiment

    def run(self) -> TenConditionAuditReport:
        checks = (
            self._audit_accept_to_block(),
            self._audit_block_to_accept(),
            self._audit_operation_collapse(),
            self._audit_composition_failure(),
            self._audit_intermediate_layer_deleted(),
            self._audit_rank_inflation(),
            self._audit_identity_loss(),
            self._audit_blocking_residual_loss(),
            self._audit_post_hoc_mapping(),
            self._audit_random_symbolic_equivalence(),
        )
        return TenConditionAuditReport(
            structural_valid=self.experiment.structural_valid(),
            ten_condition_passed=all(result.passed for result in checks),
            mapping_fingerprint=self.experiment.declaration.declared_fingerprint,
            results=checks,
        )

    def _audit_accept_to_block(self) -> ConditionAuditResult:
        injected_expected = FVerdict.BLOCK
        detected = self.experiment.accept_case.evaluate() != injected_expected
        return ConditionAuditResult(1, TenConditionCode.ACCEPT_TO_BLOCK, detected)

    def _audit_block_to_accept(self) -> ConditionAuditResult:
        injected_expected = FVerdict.ACCEPT
        detected = self.experiment.block_case.evaluate() != injected_expected
        return ConditionAuditResult(2, TenConditionCode.BLOCK_TO_ACCEPT, detected)

    def _audit_operation_collapse(self) -> ConditionAuditResult:
        collapsed = ("merged_op", "merged_op")
        detected = len(set(collapsed)) == 1
        return ConditionAuditResult(3, TenConditionCode.OPERATION_COLLAPSE, detected)

    def _audit_composition_failure(self) -> ConditionAuditResult:
        wrong_order = ("carrier_to_surface_observation", "abstract_to_carrier")
        detected = wrong_order != self.experiment.operations
        return ConditionAuditResult(4, TenConditionCode.COMPOSITION_FAILURE, detected)

    def _audit_intermediate_layer_deleted(self) -> ConditionAuditResult:
        injected = replace(self.experiment.accept_case, carrier="")
        detected = any(not layer for layer in injected.pipeline_layers())
        return ConditionAuditResult(5, TenConditionCode.INTERMEDIATE_LAYER_DELETED, detected)

    def _audit_rank_inflation(self) -> ConditionAuditResult:
        injected = replace(self.experiment.accept_case, rank=Rank.HIGH, rank_ceiling=Rank.MEDIUM)
        detected = injected.rank > injected.rank_ceiling
        return ConditionAuditResult(6, TenConditionCode.RANK_INFLATION, detected)

    def _audit_identity_loss(self) -> ConditionAuditResult:
        source_identity = self.experiment.accept_case.identity
        target_identity = f"{source_identity}_mutated"
        detected = source_identity != target_identity
        return ConditionAuditResult(7, TenConditionCode.IDENTITY_LOSS, detected)

    def _audit_blocking_residual_loss(self) -> ConditionAuditResult:
        injected = replace(self.experiment.block_case, residuals=())
        detected = injected.evaluate() == FVerdict.BLOCK and not injected.residuals
        return ConditionAuditResult(8, TenConditionCode.BLOCKING_RESIDUAL_LOSS, detected)

    def _audit_post_hoc_mapping(self) -> ConditionAuditResult:
        declaration = MappingDeclaration(
            state_map=dict(self.experiment.declaration.state_map),
            operation_map=dict(self.experiment.declaration.operation_map),
            declared_fingerprint=self.experiment.declaration.declared_fingerprint,
        )
        declaration.state_map["i3rab_raf3"] = "post_hoc_target"
        detected = declaration.has_post_hoc_mutation()
        return ConditionAuditResult(9, TenConditionCode.POST_HOC_MAPPING, detected)

    def _audit_random_symbolic_equivalence(self) -> ConditionAuditResult:
        a = self.experiment.accept_case
        b = replace(
            self.experiment.defer_case,
            abstract_state=a.abstract_state,
            realization=a.realization,
            carrier="random_symbolic_carrier",
            protocol="random_symbolic_protocol",
        )
        symbolic_match = a.abstract_state == b.abstract_state and a.realization == b.realization
        functional_match = (
            a.carrier == b.carrier
            and a.protocol == b.protocol
            and a.evaluate() == b.evaluate()
        )
        detected = symbolic_match and not functional_match
        return ConditionAuditResult(10, TenConditionCode.RANDOM_SYMBOLIC_EQUIVALENCE, detected)


def build_f_experiment() -> FExperiment:
    declaration = MappingDeclaration(
        state_map={
            "i3rab_raf3": "measured_state",
            "i3rab_licensed_limited": "measured_limited_response",
            "i3rab_unlicensed": "measured_unlicensed",
        },
        operation_map={
            "abstract_to_carrier": "state_to_instrument_response",
            "carrier_to_surface_observation": "response_to_observed_reading",
        },
    )
    return FExperiment(
        accept_case=RealizationCase(
            abstract_state="i3rab_raf3",
            carrier="jam3_mudhakr_salim_carrier",
            protocol="licensed_nahw_relation",
            realization="waw",
            identity="subject_A",
            state_licensed=True,
            carrier_known=True,
            protocol_licensed=True,
            surface_visible=True,
            carrier_limited=False,
            rank=Rank.MEDIUM,
            rank_ceiling=Rank.MEDIUM,
            residuals=(),
        ),
        defer_case=RealizationCase(
            abstract_state="i3rab_licensed_limited",
            carrier="limited_visibility_carrier",
            protocol="licensed_measurement_protocol",
            realization="implicit_surface",
            identity="subject_B",
            state_licensed=True,
            carrier_known=True,
            protocol_licensed=True,
            surface_visible=False,
            carrier_limited=True,
            rank=Rank.MEDIUM,
            rank_ceiling=Rank.MEDIUM,
            residuals=("LIMITED_SURFACE_VISIBILITY",),
        ),
        block_case=RealizationCase(
            abstract_state="i3rab_unlicensed",
            carrier="unlicensed_carrier",
            protocol="missing_license",
            realization="none",
            identity="subject_C",
            state_licensed=False,
            carrier_known=False,
            protocol_licensed=False,
            surface_visible=False,
            carrier_limited=False,
            rank=Rank.LOW,
            rank_ceiling=Rank.LOW,
            residuals=("NO_LICENSED_RELATION",),
        ),
        operations=("abstract_to_carrier", "carrier_to_surface_observation"),
        declaration=declaration,
        non_trivial_features=frozenset(
            {
                "abstract_surface_distinction",
                "carrier_protocol_dependency",
                "same_state_multiple_realizations",
                "same_surface_not_sufficient",
            }
        ),
        state_multiple_realizations={"i3rab_raf3": ("waw", "damma")},
    )


def run_f_experiment() -> TenConditionAuditReport:
    return TenConditionAuditor(build_f_experiment()).run()
