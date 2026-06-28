"""GPT-R8 — local audit-integration vocabulary for the GPT reasonableness verdict.

Binding:

* docs/56_GPT_R8_AUDIT_INTEGRATION_LAW.md §1–§10
* docs/01_BLACK_BOX_BOUNDARY.md (no model-internals participate)
* docs/18_ADAPTER_BOUNDARY_LAW.md (no new ``ModelClient`` method)

Scope — strictly local:

* :class:`AuditReasonablenessStatus` — the four-member integration state
  carried alongside the optional reasonableness verdict field on
  :class:`~taaqqul_slot_geometry.audit.answer_audit.AuditedAnswer`. Names
  map 1:1 to the docs/56 §7 local residual vocabulary so a missing
  verdict is always *named*, never silently absent.
* :func:`derive_reasonableness_residual_kind` — pure helper that maps
  an :class:`AuditReasonablenessStatus` value to its docs/56 §7 local
  residual name (or ``None`` for ``NOT_RUN``/``CARRIED``). This is the
  only place the three local residual names appear as data; per
  docs/56 §7 ("may not be used anywhere else"), no other module
  produces these residual names.

This module deliberately does **not** import
``GPTAnswerReasonablenessVerdict`` at runtime: the carrier is passed
in by the audit shell and inspected for its own constitutional
fields. The ``TYPE_CHECKING`` import keeps ``audit/`` from depending
on ``gpt/`` at module-load time (the existing one-way dependency).
"""

from __future__ import annotations

from enum import StrEnum

# docs/56 §7 — three reserved local residual names. These strings may
# not appear anywhere else under ``src/`` (see the negative test in
# ``tests/test_gpt_r8_audit_integration.py``).
RESIDUAL_REASONABLENESS_DEFERRED = "RESIDUAL_REASONABLENESS_DEFERRED"
RESIDUAL_R7_NOT_CONSUMED = "RESIDUAL_R7_NOT_CONSUMED"
NEEDGATE_NOT_OPENED_RESIDUAL_NAME = "RESIDUAL_NEEDGATE_NOT_OPENED"


class AuditReasonablenessStatus(StrEnum):
    """Bounded integration status carried alongside the verdict field.

    The four members partition the integration surface:

    * ``CARRIED`` — a GPT-R7 verdict is present on the audit record.
    * ``NOT_RUN`` — the audit was constructed without consulting
      GPT-R6/R7 at all (the legacy / default audit path).
    * ``DEFERRED`` — an upstream input to R6/R7 (gate report,
      origin binding, evidence contract) was deferred, so the
      verdict could not be produced. Maps to
      :data:`RESIDUAL_REASONABLENESS_DEFERRED`.
    * ``R7_NOT_CONSUMED`` — a GPT-R7 verdict existed but the audit
      shell did not consume it. Maps to
      :data:`RESIDUAL_R7_NOT_CONSUMED`.

    docs/56 §2 B5 requires that absence be *named*; this enum is
    the named surface.
    """

    NOT_RUN = "NOT_RUN"
    CARRIED = "CARRIED"
    DEFERRED = "DEFERRED"
    R7_NOT_CONSUMED = "R7_NOT_CONSUMED"


def derive_reasonableness_residual_kind(
    status: AuditReasonablenessStatus,
) -> str | None:
    """Map an integration status to the docs/56 §7 local residual name.

    Returns the named residual string for ``DEFERRED`` / ``R7_NOT_CONSUMED``,
    or ``None`` for ``NOT_RUN`` / ``CARRIED`` (no residual is implied by
    a verdict that is either absent-by-default or carried in full).
    """

    if not isinstance(status, AuditReasonablenessStatus):
        raise TypeError(
            "derive_reasonableness_residual_kind requires an "
            "AuditReasonablenessStatus member"
        )
    if status is AuditReasonablenessStatus.DEFERRED:
        return RESIDUAL_REASONABLENESS_DEFERRED
    if status is AuditReasonablenessStatus.R7_NOT_CONSUMED:
        return RESIDUAL_R7_NOT_CONSUMED
    return None


__all__ = [
    "NEEDGATE_NOT_OPENED_RESIDUAL_NAME",
    "RESIDUAL_R7_NOT_CONSUMED",
    "RESIDUAL_REASONABLENESS_DEFERRED",
    "AuditReasonablenessStatus",
    "derive_reasonableness_residual_kind",
]
