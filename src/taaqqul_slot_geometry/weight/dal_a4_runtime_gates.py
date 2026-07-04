"""DAL-A4 runtime gates for hamza/shadda/tanwin/sukun/madd only.

This module is bounded to DAL-A4 surface gates and does not open DAL-A5,
LAFZI gates, parser/morphology/syntax, or semantic/hukm outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.weight._schema_helpers import (
    require_non_empty as _shared_require_non_empty,
)
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_forbidden_outputs as _shared_validate_forbidden_outputs,
)
from taaqqul_slot_geometry.weight._schema_helpers import (
    validate_rank as _shared_validate_rank,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError

DAL_A4_RANK_CEILING: Rank = Rank.CANDIDATE
DAL_A4_GATE_ORDER: tuple[str, ...] = (
    "HamzaResolutionGate",
    "ShaddaIdghamGate",
    "TanwinTraceGate",
    "SukunCollisionGate",
    "MaddExtensionGate",
)
DAL_A4_FORBIDDEN_OUTPUTS: tuple[str, ...] = (
    "DAL_A5",
    "SyllableLicenseGate",
    "AdjacencyToSequenceGate",
    "S1_S5LicenseGate",
    "WaqfLicenseGate",
    "WaslLicenseGate",
    "UsageBeforeMeaningGate",
    "LoanArabizedGate",
    "DeletionTraceGate",
    "DalAloneClosed",
    "LafziMadlulGate",
    "WordKindGate",
    "RootIdentityGate",
    "WeightPathSelectionGate",
    "ParserRuntime",
    "MorphologyRuntime",
    "SyntaxRuntime",
    "MeaningGate",
    "IfadahGate",
    "MafhumGate",
    "HukmGate",
    "Truth",
    "Certainty",
    "Reality",
)
DAL_A4_RESIDUAL_VOCABULARY: tuple[str, ...] = (
    "DAL_A4_RESIDUAL_RECORDED",
    "HAMZA_UNRESOLVED",
    "SHADDA_UNEXPANDED",
    "SHADDA_IDENTITY_COLLAPSE_BLOCKED",
    "TANWIN_TRACE_DEFERRED",
    "SUKUN_COLLISION_RECORDED",
    "MADD_EXTENSION_MISSING",
    "BLOCKED_DAL_A5_HANDOFF",
    "BLOCKED_LAFZI_HANDOFF",
    "BLOCKED_SEMANTIC_OUTPUT",
)


class DalA4GateName(StrEnum):
    """DAL-A4 gate names."""

    HAMZA_RESOLUTION = "HamzaResolutionGate"
    SHADDA_IDGHAM = "ShaddaIdghamGate"
    TANWIN_TRACE = "TanwinTraceGate"
    SUKUN_COLLISION = "SukunCollisionGate"
    MADD_EXTENSION = "MaddExtensionGate"


class DalA4GateStatus(StrEnum):
    """DAL-A4 local gate status labels."""

    PASSED = "DAL_A4_GATE_PASSED"
    DEFERRED = "DAL_A4_GATE_DEFERRED"
    REFUSED = "DAL_A4_GATE_REFUSED"


class HamzaSurfaceForm(StrEnum):
    """DAL-A4 hamza surface forms."""

    HAMZAT_QAT = "HamzatQat"
    HAMZAT_WASL = "HamzatWasl"
    ALIF_MADD = "AlifMadd"
    SEAT_OF_HAMZA = "SeatOfHamza"
    UNRESOLVED = "HamzaUnresolved"


class ShaddaTraceForm(StrEnum):
    """DAL-A4 shadda/idgham trace forms."""

    DOUBLED_REALIZATION = "DoubledRealization"
    IDGHAM_TRACE = "IdghamTrace"
    UNEXPANDED = "ShaddaUnexpanded"


class TanwinTraceForm(StrEnum):
    """DAL-A4 tanwin trace forms."""

    TERMINAL_NASAL_TRACE = "TerminalNasalTrace"
    NOMINAL_TRACE = "NominalTrace"
    UNRESOLVED = "TanwinUnresolved"


class SukunTraceForm(StrEnum):
    """DAL-A4 sukun surface forms."""

    INTERNAL_SUKUN = "InternalSukun"
    WAQF_SUKUN = "WaqfSukun"
    ORIGINAL_SUKUN = "OriginalSukun"


class MaddTraceForm(StrEnum):
    """DAL-A4 madd trace forms."""

    EXTENSION_TRACE = "MaddExtensionTrace"
    NO_EXTENSION = "MaddNoExtensionEvidence"


@dataclass(frozen=True, slots=True)
class DalA4GateCertificate:
    """Bounded DAL-A4 gate certificate."""

    input_ref: str
    gate_name: DalA4GateName
    status: DalA4GateStatus
    preserved_identity: tuple[str, ...]
    surface_feature: str
    residuals: tuple[str, ...]
    trace_ref: str
    next_allowed_operation: str
    rank: Rank = Rank.CANDIDATE
    forbidden_outputs: tuple[str, ...] = DAL_A4_FORBIDDEN_OUTPUTS

    def __post_init__(self) -> None:
        _require_non_empty(
            self.input_ref,
            "DalA4GateCertificate.input_ref",
            FailureCode.TRACE_MISSING,
        )
        if not isinstance(self.gate_name, DalA4GateName):
            raise WeightCarrierSchemaError(
                "DalA4GateCertificate.gate_name must be DalA4GateName "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.status, DalA4GateStatus):
            raise WeightCarrierSchemaError(
                "DalA4GateCertificate.status must be DalA4GateStatus "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.preserved_identity, tuple) or not self.preserved_identity:
            raise WeightCarrierSchemaError(
                "DalA4GateCertificate.preserved_identity must be non-empty tuple "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        for identity in self.preserved_identity:
            _require_non_empty(
                identity,
                "DalA4GateCertificate.preserved_identity entry",
                FailureCode.IDENTITY_BROKEN,
            )
        _require_non_empty(
            self.surface_feature,
            "DalA4GateCertificate.surface_feature",
            FailureCode.BOUNDARY_MISSING,
        )
        if not isinstance(self.residuals, tuple):
            raise WeightCarrierSchemaError(
                "DalA4GateCertificate.residuals must be tuple "
                f"({FailureCode.HIDDEN_RESIDUAL.value})"
            )
        for residual in self.residuals:
            _require_non_empty(
                residual,
                "DalA4GateCertificate.residuals entry",
                FailureCode.HIDDEN_RESIDUAL,
            )
        _require_non_empty(
            self.trace_ref,
            "DalA4GateCertificate.trace_ref",
            FailureCode.TRACE_MISSING,
        )
        _require_non_empty(
            self.next_allowed_operation,
            "DalA4GateCertificate.next_allowed_operation",
            FailureCode.BOUNDARY_MISSING,
        )
        _validate_rank(self.rank, "DalA4GateCertificate")
        _validate_forbidden_outputs(self.forbidden_outputs, "DalA4GateCertificate")


@dataclass(frozen=True, slots=True)
class DalA4GateResult:
    """DAL-A4 gate result wrapper."""

    certificate: DalA4GateCertificate
    failure_code: FailureCode | None

    def __post_init__(self) -> None:
        if not isinstance(self.certificate, DalA4GateCertificate):
            raise WeightCarrierSchemaError(
                "DalA4GateResult.certificate must be DalA4GateCertificate "
                f"({FailureCode.GATE_REQUIRED.value})"
            )
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise WeightCarrierSchemaError(
                "DalA4GateResult.failure_code must be FailureCode or None "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


def _require_non_empty(value: str, field_name: str, failure_code: FailureCode) -> None:
    _shared_require_non_empty(value, field_name, failure_code)


def _validate_rank(rank: Rank, owner: str) -> None:
    _shared_validate_rank(rank, owner, ceiling=DAL_A4_RANK_CEILING)


def _validate_forbidden_outputs(forbidden_outputs: tuple[str, ...], owner: str) -> None:
    _shared_validate_forbidden_outputs(forbidden_outputs, owner)


_FORBIDDEN_HANDOFF_ALIASES: dict[str, str] = {
    "DAL-A5": "DAL_A5",
    "DAL_A5": "DAL_A5",
    "S1-S5": "S1_S5LicenseGate",
    "LAFZI_MADLUL_GATE": "LafziMadlulGate",
    "IFADAH": "IfadahGate",
    "MAFHUM": "MafhumGate",
    "HUKM": "HukmGate",
    "MEANING": "MeaningGate",
    "ROOT": "RootIdentityGate",
    "PATTERN": "WeightPathSelectionGate",
    "REALITY": "Reality",
}


def _canonical_handoff(handoff: str) -> str:
    stripped = handoff.strip()
    return _FORBIDDEN_HANDOFF_ALIASES.get(stripped, stripped)


def _forbidden_handoff_result(
    *,
    input_ref: str,
    gate_name: DalA4GateName,
    preserved_identity: tuple[str, ...],
    trace_ref: str,
    handoff: str,
) -> DalA4GateResult | None:
    canonical_handoff = _canonical_handoff(handoff)
    if canonical_handoff not in DAL_A4_FORBIDDEN_OUTPUTS:
        return None
    if canonical_handoff == "DAL_A5":
        residual = "BLOCKED_DAL_A5_HANDOFF"
    elif canonical_handoff == "LafziMadlulGate":
        residual = "BLOCKED_LAFZI_HANDOFF"
    else:
        residual = "BLOCKED_SEMANTIC_OUTPUT"
    return DalA4GateResult(
        certificate=DalA4GateCertificate(
            input_ref=input_ref,
            gate_name=gate_name,
            status=DalA4GateStatus.REFUSED,
            preserved_identity=preserved_identity,
            surface_feature=f"FORBIDDEN_HANDOFF:{canonical_handoff}",
            residuals=(residual,),
            trace_ref=trace_ref,
            next_allowed_operation="DAL_A4_LOCAL_ONLY",
        ),
        failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
    )


def evaluate_hamza_resolution_gate(
    *,
    input_ref: str,
    identity: str,
    hamza_form: HamzaSurfaceForm,
    trace_ref: str,
    requested_handoff: str = "ShaddaIdghamGate",
) -> DalA4GateResult:
    """DAL-A4 HamzaResolutionGate."""
    _require_non_empty(
        input_ref,
        "evaluate_hamza_resolution_gate.input_ref",
        FailureCode.TRACE_MISSING,
    )
    _require_non_empty(
        identity,
        "evaluate_hamza_resolution_gate.identity",
        FailureCode.IDENTITY_BROKEN,
    )
    _require_non_empty(
        trace_ref,
        "evaluate_hamza_resolution_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    _require_non_empty(
        requested_handoff,
        "evaluate_hamza_resolution_gate.requested_handoff",
        FailureCode.BOUNDARY_MISSING,
    )
    if not isinstance(hamza_form, HamzaSurfaceForm):
        raise WeightCarrierSchemaError(
            "evaluate_hamza_resolution_gate.hamza_form must be HamzaSurfaceForm "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    forbidden = _forbidden_handoff_result(
        input_ref=input_ref,
        gate_name=DalA4GateName.HAMZA_RESOLUTION,
        preserved_identity=(identity,),
        trace_ref=trace_ref,
        handoff=requested_handoff,
    )
    if forbidden is not None:
        return forbidden

    if hamza_form is HamzaSurfaceForm.UNRESOLVED:
        return DalA4GateResult(
            certificate=DalA4GateCertificate(
                input_ref=input_ref,
                gate_name=DalA4GateName.HAMZA_RESOLUTION,
                status=DalA4GateStatus.DEFERRED,
                preserved_identity=(identity,),
                surface_feature=hamza_form.value,
                residuals=("HAMZA_UNRESOLVED",),
                trace_ref=trace_ref,
                next_allowed_operation="DAL_A4_LOCAL_ONLY",
            ),
            failure_code=FailureCode.BOUNDARY_MISSING,
        )

    return DalA4GateResult(
        certificate=DalA4GateCertificate(
            input_ref=input_ref,
            gate_name=DalA4GateName.HAMZA_RESOLUTION,
            status=DalA4GateStatus.PASSED,
            preserved_identity=(identity,),
            surface_feature=hamza_form.value,
            residuals=("DAL_A4_RESIDUAL_RECORDED",),
            trace_ref=trace_ref,
            next_allowed_operation=_canonical_handoff(requested_handoff),
        ),
        failure_code=None,
    )


def evaluate_shadda_idgham_gate(
    *,
    input_ref: str,
    lead_identity: str,
    tail_identity: str,
    shadda_form: ShaddaTraceForm,
    trace_ref: str,
    requested_handoff: str = "TanwinTraceGate",
) -> DalA4GateResult:
    """DAL-A4 ShaddaIdghamGate."""
    _require_non_empty(
        input_ref,
        "evaluate_shadda_idgham_gate.input_ref",
        FailureCode.TRACE_MISSING,
    )
    _require_non_empty(
        lead_identity,
        "evaluate_shadda_idgham_gate.lead_identity",
        FailureCode.IDENTITY_BROKEN,
    )
    _require_non_empty(
        tail_identity,
        "evaluate_shadda_idgham_gate.tail_identity",
        FailureCode.IDENTITY_BROKEN,
    )
    _require_non_empty(
        trace_ref,
        "evaluate_shadda_idgham_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    _require_non_empty(
        requested_handoff,
        "evaluate_shadda_idgham_gate.requested_handoff",
        FailureCode.BOUNDARY_MISSING,
    )
    if not isinstance(shadda_form, ShaddaTraceForm):
        raise WeightCarrierSchemaError(
            "evaluate_shadda_idgham_gate.shadda_form must be ShaddaTraceForm "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    forbidden = _forbidden_handoff_result(
        input_ref=input_ref,
        gate_name=DalA4GateName.SHADDA_IDGHAM,
        preserved_identity=(lead_identity, tail_identity),
        trace_ref=trace_ref,
        handoff=requested_handoff,
    )
    if forbidden is not None:
        return forbidden

    if lead_identity == tail_identity:
        return DalA4GateResult(
            certificate=DalA4GateCertificate(
                input_ref=input_ref,
                gate_name=DalA4GateName.SHADDA_IDGHAM,
                status=DalA4GateStatus.REFUSED,
                preserved_identity=(lead_identity, tail_identity),
                surface_feature=shadda_form.value,
                residuals=("SHADDA_IDENTITY_COLLAPSE_BLOCKED",),
                trace_ref=trace_ref,
                next_allowed_operation="DAL_A4_LOCAL_ONLY",
            ),
            failure_code=FailureCode.IDENTITY_BROKEN,
        )

    if shadda_form is ShaddaTraceForm.UNEXPANDED:
        return DalA4GateResult(
            certificate=DalA4GateCertificate(
                input_ref=input_ref,
                gate_name=DalA4GateName.SHADDA_IDGHAM,
                status=DalA4GateStatus.DEFERRED,
                preserved_identity=(lead_identity, tail_identity),
                surface_feature=shadda_form.value,
                residuals=("SHADDA_UNEXPANDED",),
                trace_ref=trace_ref,
                next_allowed_operation="DAL_A4_LOCAL_ONLY",
            ),
            failure_code=FailureCode.BOUNDARY_MISSING,
        )

    return DalA4GateResult(
        certificate=DalA4GateCertificate(
            input_ref=input_ref,
            gate_name=DalA4GateName.SHADDA_IDGHAM,
            status=DalA4GateStatus.PASSED,
            preserved_identity=(lead_identity, tail_identity),
            surface_feature=shadda_form.value,
            residuals=("DAL_A4_RESIDUAL_RECORDED",),
            trace_ref=trace_ref,
            next_allowed_operation=_canonical_handoff(requested_handoff),
        ),
        failure_code=None,
    )


def evaluate_tanwin_trace_gate(
    *,
    input_ref: str,
    identity: str,
    tanwin_form: TanwinTraceForm,
    trace_ref: str,
    requested_handoff: str = "SukunCollisionGate",
) -> DalA4GateResult:
    """DAL-A4 TanwinTraceGate."""
    _require_non_empty(input_ref, "evaluate_tanwin_trace_gate.input_ref", FailureCode.TRACE_MISSING)
    _require_non_empty(identity, "evaluate_tanwin_trace_gate.identity", FailureCode.IDENTITY_BROKEN)
    _require_non_empty(trace_ref, "evaluate_tanwin_trace_gate.trace_ref", FailureCode.TRACE_MISSING)
    _require_non_empty(
        requested_handoff,
        "evaluate_tanwin_trace_gate.requested_handoff",
        FailureCode.BOUNDARY_MISSING,
    )
    if not isinstance(tanwin_form, TanwinTraceForm):
        raise WeightCarrierSchemaError(
            "evaluate_tanwin_trace_gate.tanwin_form must be TanwinTraceForm "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    forbidden = _forbidden_handoff_result(
        input_ref=input_ref,
        gate_name=DalA4GateName.TANWIN_TRACE,
        preserved_identity=(identity,),
        trace_ref=trace_ref,
        handoff=requested_handoff,
    )
    if forbidden is not None:
        return forbidden

    if tanwin_form is TanwinTraceForm.UNRESOLVED:
        return DalA4GateResult(
            certificate=DalA4GateCertificate(
                input_ref=input_ref,
                gate_name=DalA4GateName.TANWIN_TRACE,
                status=DalA4GateStatus.DEFERRED,
                preserved_identity=(identity,),
                surface_feature=tanwin_form.value,
                residuals=("TANWIN_TRACE_DEFERRED",),
                trace_ref=trace_ref,
                next_allowed_operation="DAL_A4_LOCAL_ONLY",
            ),
            failure_code=FailureCode.BOUNDARY_MISSING,
        )

    return DalA4GateResult(
        certificate=DalA4GateCertificate(
            input_ref=input_ref,
            gate_name=DalA4GateName.TANWIN_TRACE,
            status=DalA4GateStatus.PASSED,
            preserved_identity=(identity,),
            surface_feature=tanwin_form.value,
            residuals=("DAL_A4_RESIDUAL_RECORDED",),
            trace_ref=trace_ref,
            next_allowed_operation=_canonical_handoff(requested_handoff),
        ),
        failure_code=None,
    )


def evaluate_sukun_collision_gate(
    *,
    input_ref: str,
    identity: str,
    sukun_form: SukunTraceForm,
    has_collision: bool,
    trace_ref: str,
    requested_handoff: str = "MaddExtensionGate",
) -> DalA4GateResult:
    """DAL-A4 SukunCollisionGate."""
    _require_non_empty(
        input_ref,
        "evaluate_sukun_collision_gate.input_ref",
        FailureCode.TRACE_MISSING,
    )
    _require_non_empty(
        identity,
        "evaluate_sukun_collision_gate.identity",
        FailureCode.IDENTITY_BROKEN,
    )
    _require_non_empty(
        trace_ref,
        "evaluate_sukun_collision_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    _require_non_empty(
        requested_handoff,
        "evaluate_sukun_collision_gate.requested_handoff",
        FailureCode.BOUNDARY_MISSING,
    )
    if not isinstance(sukun_form, SukunTraceForm):
        raise WeightCarrierSchemaError(
            "evaluate_sukun_collision_gate.sukun_form must be SukunTraceForm "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(has_collision, bool):
        raise WeightCarrierSchemaError(
            "evaluate_sukun_collision_gate.has_collision must be bool "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    forbidden = _forbidden_handoff_result(
        input_ref=input_ref,
        gate_name=DalA4GateName.SUKUN_COLLISION,
        preserved_identity=(identity,),
        trace_ref=trace_ref,
        handoff=requested_handoff,
    )
    if forbidden is not None:
        return forbidden

    if has_collision:
        return DalA4GateResult(
            certificate=DalA4GateCertificate(
                input_ref=input_ref,
                gate_name=DalA4GateName.SUKUN_COLLISION,
                status=DalA4GateStatus.REFUSED,
                preserved_identity=(identity,),
                surface_feature=sukun_form.value,
                residuals=("SUKUN_COLLISION_RECORDED",),
                trace_ref=trace_ref,
                next_allowed_operation="DAL_A4_LOCAL_ONLY",
            ),
            failure_code=FailureCode.BLOCKING_RESIDUAL_PRESENT,
        )

    return DalA4GateResult(
        certificate=DalA4GateCertificate(
            input_ref=input_ref,
            gate_name=DalA4GateName.SUKUN_COLLISION,
            status=DalA4GateStatus.PASSED,
            preserved_identity=(identity,),
            surface_feature=sukun_form.value,
            residuals=("DAL_A4_RESIDUAL_RECORDED",),
            trace_ref=trace_ref,
            next_allowed_operation=_canonical_handoff(requested_handoff),
        ),
        failure_code=None,
    )


def evaluate_madd_extension_gate(
    *,
    input_ref: str,
    identity: str,
    madd_form: MaddTraceForm,
    extension_evidence: bool,
    trace_ref: str,
    requested_handoff: str = "DAL_A4_LOCAL_ONLY",
) -> DalA4GateResult:
    """DAL-A4 MaddExtensionGate."""
    _require_non_empty(
        input_ref,
        "evaluate_madd_extension_gate.input_ref",
        FailureCode.TRACE_MISSING,
    )
    _require_non_empty(
        identity,
        "evaluate_madd_extension_gate.identity",
        FailureCode.IDENTITY_BROKEN,
    )
    _require_non_empty(
        trace_ref,
        "evaluate_madd_extension_gate.trace_ref",
        FailureCode.TRACE_MISSING,
    )
    _require_non_empty(
        requested_handoff,
        "evaluate_madd_extension_gate.requested_handoff",
        FailureCode.BOUNDARY_MISSING,
    )
    if not isinstance(madd_form, MaddTraceForm):
        raise WeightCarrierSchemaError(
            "evaluate_madd_extension_gate.madd_form must be MaddTraceForm "
            f"({FailureCode.GATE_REQUIRED.value})"
        )
    if not isinstance(extension_evidence, bool):
        raise WeightCarrierSchemaError(
            "evaluate_madd_extension_gate.extension_evidence must be bool "
            f"({FailureCode.GATE_REQUIRED.value})"
        )

    forbidden = _forbidden_handoff_result(
        input_ref=input_ref,
        gate_name=DalA4GateName.MADD_EXTENSION,
        preserved_identity=(identity,),
        trace_ref=trace_ref,
        handoff=requested_handoff,
    )
    if forbidden is not None:
        return forbidden

    if madd_form is MaddTraceForm.NO_EXTENSION or not extension_evidence:
        return DalA4GateResult(
            certificate=DalA4GateCertificate(
                input_ref=input_ref,
                gate_name=DalA4GateName.MADD_EXTENSION,
                status=DalA4GateStatus.DEFERRED,
                preserved_identity=(identity,),
                surface_feature=madd_form.value,
                residuals=("MADD_EXTENSION_MISSING",),
                trace_ref=trace_ref,
                next_allowed_operation="DAL_A4_LOCAL_ONLY",
            ),
            failure_code=FailureCode.BOUNDARY_MISSING,
        )

    return DalA4GateResult(
        certificate=DalA4GateCertificate(
            input_ref=input_ref,
            gate_name=DalA4GateName.MADD_EXTENSION,
            status=DalA4GateStatus.PASSED,
            preserved_identity=(identity,),
            surface_feature=madd_form.value,
            residuals=("DAL_A4_RESIDUAL_RECORDED",),
            trace_ref=trace_ref,
            next_allowed_operation=_canonical_handoff(requested_handoff),
        ),
        failure_code=None,
    )


__all__ = [
    "DAL_A4_FORBIDDEN_OUTPUTS",
    "DAL_A4_GATE_ORDER",
    "DAL_A4_RANK_CEILING",
    "DAL_A4_RESIDUAL_VOCABULARY",
    "DalA4GateCertificate",
    "DalA4GateName",
    "DalA4GateResult",
    "DalA4GateStatus",
    "HamzaSurfaceForm",
    "MaddTraceForm",
    "ShaddaTraceForm",
    "SukunTraceForm",
    "TanwinTraceForm",
    "evaluate_hamza_resolution_gate",
    "evaluate_madd_extension_gate",
    "evaluate_shadda_idgham_gate",
    "evaluate_sukun_collision_gate",
    "evaluate_tanwin_trace_gate",
]
