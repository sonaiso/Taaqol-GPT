"""Named failure codes — carrier enum (PR-1A).

PR-1A shipped the names of every refusal the engine emits from
``gamma``, the construction surface, the transition gate, or the audit
wrapper. The *decision* that emits each one lives in the
constitutional documents and binds the PR-2+ implementations.

Failures are values, never exceptions. Every refusal verdict must
carry a member of this enum.
"""

from __future__ import annotations

from enum import StrEnum


class FailureCode(StrEnum):
    """Named failure codes referenced by the constitution.

    The enum is intentionally exhaustive across the constitutional
    documents (02, 03, 11). Members are bound by the PR-2+
    implementations (``gamma``, the construction surface, the
    transition gate, the audit wrapper) and must keep their names
    stable.
    """

    # --- Identity / structural failures (doc 02, 11 §2, §3) -------------
    IDENTITY_BROKEN = "IDENTITY_BROKEN"
    CENTER_MISSING = "CENTER_MISSING"
    BOUNDARY_MISSING = "BOUNDARY_MISSING"
    DOMAIN_MISSING = "DOMAIN_MISSING"
    SCOPE_MISSING = "SCOPE_MISSING"
    TRACE_MISSING = "TRACE_MISSING"

    # --- Opening / closure failures (doc 03, 11 §4, §5, §6) -------------
    REQUIRED_SLOT_EMPTY = "REQUIRED_SLOT_EMPTY"
    UNLICENSED_OPENING = "UNLICENSED_OPENING"
    OUTPUT_EXCEEDS_LAYER = "OUTPUT_EXCEEDS_LAYER"

    # --- Residual failures (doc 06, 11 §9) ------------------------------
    HIDDEN_RESIDUAL = "HIDDEN_RESIDUAL"
    BLOCKING_RESIDUAL_PRESENT = "BLOCKING_RESIDUAL_PRESENT"

    # --- Rank / promotion failures (doc 05, 11 §8) ----------------------
    RANK_PROMOTION_WITHOUT_GATE = "RANK_PROMOTION_WITHOUT_GATE"
    RANK_EXCEEDS_CEILING = "RANK_EXCEEDS_CEILING"

    # --- Transition failures (doc 04, 08, 11 §10) -----------------------
    FORBIDDEN_STRAIGHT_LINE = "FORBIDDEN_STRAIGHT_LINE"
    GATE_REQUIRED = "GATE_REQUIRED"


__all__ = ["FailureCode"]
