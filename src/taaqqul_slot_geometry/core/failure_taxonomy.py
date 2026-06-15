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

    # --- Ifādah failures (docs/41 §6, docs/42 §7 — PR-20) ----------------
    NO_RELATION_CLOSURE = "NO_RELATION_CLOSURE"
    NO_FORMAL_STYLE = "NO_FORMAL_STYLE"
    NO_SPEECH_FORCE = "NO_SPEECH_FORCE"
    NO_IFADAH_MAQAM = "NO_IFADAH_MAQAM"
    MAQAM_DIVERGENCE = "MAQAM_DIVERGENCE"
    FORMAL_STYLE_CONFLICT = "FORMAL_STYLE_CONFLICT"
    NO_IFADAH_EVIDENCE = "NO_IFADAH_EVIDENCE"
    NO_IFADAH_SCOPE = "NO_IFADAH_SCOPE"

    # --- Hukm failures (docs/43 §7 — PR-21) --------------------------------
    NO_IFADAH = "NO_IFADAH"
    NO_EVALUATION_DOMAIN = "NO_EVALUATION_DOMAIN"
    NO_HUKM_CLAIM = "NO_HUKM_CLAIM"
    NO_HUKM_EVIDENCE = "NO_HUKM_EVIDENCE"
    NO_HUKM_MAQAM = "NO_HUKM_MAQAM"
    AUTHORITY_LEAK = "AUTHORITY_LEAK"
    DOMAIN_LEAP = "DOMAIN_LEAP"  # reserved for extended domain validation

    # --- Manāṭ failures (docs/44 §7 — PR-21M) --------------------------------
    NO_HUKM = "NO_HUKM"
    NO_MANAT_MODE = "NO_MANAT_MODE"
    NO_MANAT_DESCRIPTION = "NO_MANAT_DESCRIPTION"
    NO_EFFECTIVE_ATTRIBUTE = "NO_EFFECTIVE_ATTRIBUTE"
    NO_MANAT_EVIDENCE = "NO_MANAT_EVIDENCE"
    NO_MANAT_DOMAIN = "NO_MANAT_DOMAIN"
    MANAT_MODE_COLLAPSE = "MANAT_MODE_COLLAPSE"
    TAHQIQ_OVERCLAIM = "TAHQIQ_OVERCLAIM"
    REALITY_APPLICATION_FORBIDDEN = "REALITY_APPLICATION_FORBIDDEN"

    # --- Tanzīl failures (docs/45 §7 — PR-22) --------------------------------
    NO_MANAT = "NO_MANAT"
    NO_REALITY_EVIDENCE = "NO_REALITY_EVIDENCE"
    NO_INSTANCE_DESCRIPTOR = "NO_INSTANCE_DESCRIPTOR"
    NO_PRESENTATION_BOUNDARY = "NO_PRESENTATION_BOUNDARY"
    NO_TANZIL_SCOPE = "NO_TANZIL_SCOPE"
    PRESENTATION_WARNING_MISSING = "PRESENTATION_WARNING_MISSING"
    EXECUTION_LEAK = "EXECUTION_LEAK"
    REALITY_APPLICATION_OVERCLAIM = "REALITY_APPLICATION_OVERCLAIM"

    # --- Manṭūq closure failures (docs/48 §6 — PV-A2) ----------------------------
    NO_MANTUQ_SCOPE = "NO_MANTUQ_SCOPE"
    NO_SPOKEN_SURFACE = "NO_SPOKEN_SURFACE"
    NO_MANTUQ_EVIDENCE = "NO_MANTUQ_EVIDENCE"
    NO_MANTUQ_CLOSURE_SCOPE = "NO_MANTUQ_CLOSURE_SCOPE"
    MANTUQ_MAQAM_DIVERGENCE = "MANTUQ_MAQAM_DIVERGENCE"
    MAFHUM_BEFORE_MANTUQ = "MAFHUM_BEFORE_MANTUQ"

    # --- Audit bridge failures (PR-22-AUDIT) -----------------------------------
    NO_TANZIL_VERDICT = "NO_TANZIL_VERDICT"
    AUDIT_PRESENTATION_ENVELOPE_MISSING = "AUDIT_PRESENTATION_ENVELOPE_MISSING"
    AUDIT_PRESENTATION_WARNING_MISSING = "AUDIT_PRESENTATION_WARNING_MISSING"
    AUDIT_RANK_NOT_VISIBLE = "AUDIT_RANK_NOT_VISIBLE"
    AUDIT_RESIDUALS_NOT_VISIBLE = "AUDIT_RESIDUALS_NOT_VISIBLE"
    AUDIT_TRACE_NOT_VISIBLE = "AUDIT_TRACE_NOT_VISIBLE"
    AUDIT_EXECUTION_LEAK = "AUDIT_EXECUTION_LEAK"
    AUDIT_AUTHORITY_LEAK = "AUDIT_AUTHORITY_LEAK"
    AUDIT_CERTIFICATE_LEAK = "AUDIT_CERTIFICATE_LEAK"


__all__ = ["FailureCode"]
