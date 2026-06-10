"""Forbidden Straight-Line Registry — PR-5 binding of docs/04 + docs/10 + docs/16 §4.

PR-4 bound the generic :class:`TransitionGate` and hard-coded a single
bar: any ``CERTIFICATE``-layer target is ``FORBIDDEN_STRAIGHT_LINE``.
PR-5 binds the registry that bar belongs to. The constitution states
the contract in ``docs/04_FORBIDDEN_STRAIGHT_LINES.md``:

    The full registry, including all of the above plus the
    technical-terminology cases from docs/10, will be expressed as
    data (not code) and queried by ``is_forbidden_direct(src, tgt)``.

This module is therefore *data plus pure queries* and nothing else:

* :class:`ForbiddenLine` — one row of the registry: a *layer leap*
  ``source → target`` with the reason it is forbidden, the named
  ``required_bridge`` that could ever license it, the document the
  row originates from, and the :class:`FailureCode` it emits until
  that bridge is opened by a future PR (always
  ``FORBIDDEN_STRAIGHT_LINE`` — docs/04, docs/16 §4).
* :class:`TerminologyTransfer` — one row of the technical-terminology
  non-confusion cases (docs/10): a *domain leap within the same
  surface form*, ``(term, source_domain, target_domain,
  required_bridge_gate_name)``. The two row kinds are deliberately
  distinct carriers with distinct queries because docs/10 forbids
  collapsing the two laws into one mechanism.
* :class:`ForbiddenLineRegistry` — the immutable registry value with
  the two query surfaces: :meth:`~ForbiddenLineRegistry.find` /
  :meth:`~ForbiddenLineRegistry.is_forbidden_direct` for layer leaps
  and :meth:`~ForbiddenLineRegistry.find_term_transfer` /
  :meth:`~ForbiddenLineRegistry.is_forbidden_term_transfer` for
  terminology transfers. Name matching is exact after whitespace
  stripping and case folding, so the executable :class:`Layer`
  member names (``"CANDIDATE"``) meet the constitutional row names
  (``"Candidate"``) without a synthesised mapping.
* :data:`FORBIDDEN_STRAIGHT_LINES` — every row of the docs/04
  canonical table, every row of the docs/04 pre-text declared-entry
  table, and the six chain lines of docs/16 §4 that "must be merged
  into the registry that lands in PR-5". Transcription notes:

  - the compound docs/04 row ``Tool/Number/LCNV → Knowledge`` is
    entered as three rows (``Tool``, ``Number``, ``LCNV``) so the
    query contract answers each name, exactly as the governing law
    ("No straight line from Tool / Number / LCNV to Knowledge")
    reads;
  - the docs/04 pre-text table repeats three canonical pairs with
    differently named declared bridges (``Unicode → ArabicLetter``,
    ``CodePoint → Phoneme``, ``Grapheme → FunctionalLetter``); both
    rows are preserved exactly as written and
    :meth:`~ForbiddenLineRegistry.find` returns the first —
    canonical-table — match.
* :data:`TERMINOLOGY_TRANSFERS` — the docs/10 starting cases
  (``cause / sabab / ʿillah`` across physics, fiqh, and philosophy;
  ``qiyās`` across logic, uṣūl al-fiqh, and mathematics) expanded
  into directed ``(term, source_domain, target_domain)`` rows. The
  transliterated Arabic terms are registry *data names*, licensed by
  ``docs/09_ARABIC_APPLICATION_BOUNDARY.md``; no lexicons, no
  glossaries, and no Arabic morphological code enter here.
* :data:`CANONICAL_REGISTRY` — the constitutional registry instance
  the generic gate consults, and :func:`is_forbidden_direct` — the
  docs/04 module-level query contract over it.

Every row emits :attr:`FailureCode.FORBIDDEN_STRAIGHT_LINE` "until
the row's required bridge is opened by a future PR" (docs/16 §4).
No bridge gate is implemented here: the ``CertificationGate`` and
every other named bridge remain declared residuals of their own
future PRs. The module is pure (no I/O, no ledger writes, standard
library only) and a malformed row or registry is a programmer
mistake refused loudly with ``TypeError`` at birth — mirroring the
:class:`TransitionGate` carrier guards — never a constitutional
verdict.

See ``docs/04_FORBIDDEN_STRAIGHT_LINES.md`` — *PR-5 binding*.
"""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode


def _require_text(owner: str, field_name: str, value: object) -> None:
    """Shared birth guard: every registry name is a non-empty string."""

    if not isinstance(value, str) or not value.strip():
        raise TypeError(f"{owner}.{field_name} must be a non-empty string")


@dataclass(frozen=True, slots=True)
class ForbiddenLine:
    """One layer-leap row of the Forbidden Straight-Line Registry.

    The row schema follows the docs/04 tables: the forbidden
    ``source → target`` move, the constitutional reason, the named
    ``required_bridge`` that a future PR must open before the move
    can ever be licensed, the originating document, and the named
    :class:`FailureCode` the row emits until then. A row never
    licenses anything; it only names a refusal.
    """

    source: str
    target: str
    reason: str
    required_bridge: str
    origin_law: str
    failure_code: FailureCode

    def __post_init__(self) -> None:
        _require_text("ForbiddenLine", "source", self.source)
        _require_text("ForbiddenLine", "target", self.target)
        _require_text("ForbiddenLine", "reason", self.reason)
        _require_text("ForbiddenLine", "required_bridge", self.required_bridge)
        _require_text("ForbiddenLine", "origin_law", self.origin_law)
        if not isinstance(self.failure_code, FailureCode):
            raise TypeError("ForbiddenLine.failure_code must be a FailureCode member")


@dataclass(frozen=True, slots=True)
class TerminologyTransfer:
    """One domain-leap row of the terminology non-confusion cases.

    The row schema is exactly the docs/10 entry form ``(term,
    source_domain, target_domain, required_bridge_gate_name)`` plus
    the originating document and the named :class:`FailureCode`.
    A terminology transfer is *not* a layer leap: docs/10 keeps the
    two laws separate "so that future contributors do not collapse
    them into one mechanism", which is why this carrier and its
    query surface are distinct from :class:`ForbiddenLine`.
    """

    term: str
    source_domain: str
    target_domain: str
    required_bridge: str
    origin_law: str
    failure_code: FailureCode

    def __post_init__(self) -> None:
        _require_text("TerminologyTransfer", "term", self.term)
        _require_text("TerminologyTransfer", "source_domain", self.source_domain)
        _require_text("TerminologyTransfer", "target_domain", self.target_domain)
        _require_text("TerminologyTransfer", "required_bridge", self.required_bridge)
        _require_text("TerminologyTransfer", "origin_law", self.origin_law)
        if not isinstance(self.failure_code, FailureCode):
            raise TypeError(
                "TerminologyTransfer.failure_code must be a FailureCode member"
            )


def _normalize(name: str) -> str:
    """Name normalisation for queries: strip whitespace, fold case."""

    return name.strip().casefold()


@dataclass(frozen=True, slots=True)
class ForbiddenLineRegistry:
    """The immutable Forbidden Straight-Line Registry value.

    Holds the layer-leap rows (docs/04 + docs/16 §4) and the
    terminology-transfer rows (docs/10) as two distinct surfaces.
    The registry is a value: queries are pure reads, nothing here
    appends to a ledger or mutates a row.
    """

    lines: tuple[ForbiddenLine, ...]
    term_transfers: tuple[TerminologyTransfer, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.lines, tuple):
            raise TypeError(
                "ForbiddenLineRegistry.lines must be a tuple of ForbiddenLine rows"
            )
        for row in self.lines:
            if not isinstance(row, ForbiddenLine):
                raise TypeError(
                    "every ForbiddenLineRegistry.lines row must be a ForbiddenLine"
                )
        if not isinstance(self.term_transfers, tuple):
            raise TypeError(
                "ForbiddenLineRegistry.term_transfers must be a tuple of "
                "TerminologyTransfer rows"
            )
        for row in self.term_transfers:
            if not isinstance(row, TerminologyTransfer):
                raise TypeError(
                    "every ForbiddenLineRegistry.term_transfers row must be a "
                    "TerminologyTransfer"
                )

    def find(self, source: str, target: str) -> ForbiddenLine | None:
        """Return the first row forbidding ``source → target``, else ``None``.

        Matching is exact after normalisation (strip + casefold), so
        ``find("CANDIDATE", "CERTIFICATE")`` meets the constitutional
        row ``Candidate → Certificate``. Where docs/04 states the
        same pair in both of its tables, the canonical-table row
        precedes the pre-text row. A wrong *type* of argument is a
        programmer mistake refused loudly with ``TypeError``,
        mirroring the gate's domain guard.
        """

        if not isinstance(source, str) or not isinstance(target, str):
            raise TypeError(
                "ForbiddenLineRegistry.find() requires string source and target names"
            )
        src, tgt = _normalize(source), _normalize(target)
        for row in self.lines:
            if _normalize(row.source) == src and _normalize(row.target) == tgt:
                return row
        return None

    def is_forbidden_direct(self, source: str, target: str) -> bool:
        """The docs/04 query contract: is ``source → target`` a
        registered forbidden straight line?"""

        return self.find(source, target) is not None

    def find_term_transfer(
        self, term: str, source_domain: str, target_domain: str
    ) -> TerminologyTransfer | None:
        """Return the row forbidding ``term``'s move from
        ``source_domain`` to ``target_domain``, else ``None``.

        This is the docs/10 surface, deliberately separate from
        :meth:`find`: a domain leap within one surface form is never
        answered by the layer-leap table, and vice versa.
        """

        if (
            not isinstance(term, str)
            or not isinstance(source_domain, str)
            or not isinstance(target_domain, str)
        ):
            raise TypeError(
                "ForbiddenLineRegistry.find_term_transfer() requires string "
                "term and domain names"
            )
        needle = (_normalize(term), _normalize(source_domain), _normalize(target_domain))
        for row in self.term_transfers:
            key = (
                _normalize(row.term),
                _normalize(row.source_domain),
                _normalize(row.target_domain),
            )
            if key == needle:
                return row
        return None

    def is_forbidden_term_transfer(
        self, term: str, source_domain: str, target_domain: str
    ) -> bool:
        """The docs/10 query contract: is moving ``term`` from
        ``source_domain`` to ``target_domain`` a registered forbidden
        terminology transfer?"""

        return self.find_term_transfer(term, source_domain, target_domain) is not None


# ---------------------------------------------------------------------------
# The registry data. Rows are transcribed from the constitutional
# tables; the private entry helpers below only fix each table's
# origin_law and the single FailureCode every row emits (docs/04;
# docs/16 §4) — they add no query logic and synthesise no row.
# ---------------------------------------------------------------------------

_DOCS04_CANONICAL = "docs/04 — canonical forbidden transitions"
_DOCS04_PRE_TEXT = "docs/04 — pre-text declared-entry transitions"
_DOCS16_CHAIN = "docs/16 §4 — the six new forbidden straight lines"
_DOCS10_TERMS = "docs/10 — technical terminology non-confusion cases"


def _canonical(source: str, target: str, reason: str, bridge: str) -> ForbiddenLine:
    return ForbiddenLine(
        source=source,
        target=target,
        reason=reason,
        required_bridge=bridge,
        origin_law=_DOCS04_CANONICAL,
        failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
    )


def _pre_text(source: str, target: str, reason: str, bridge: str) -> ForbiddenLine:
    return ForbiddenLine(
        source=source,
        target=target,
        reason=reason,
        required_bridge=bridge,
        origin_law=_DOCS04_PRE_TEXT,
        failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
    )


def _chain(source: str, target: str, reason: str, bridge: str) -> ForbiddenLine:
    return ForbiddenLine(
        source=source,
        target=target,
        reason=reason,
        required_bridge=bridge,
        origin_law=_DOCS16_CHAIN,
        failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
    )


def _term(
    term: str, source_domain: str, target_domain: str, bridge: str
) -> TerminologyTransfer:
    return TerminologyTransfer(
        term=term,
        source_domain=source_domain,
        target_domain=target_domain,
        required_bridge=bridge,
        origin_law=_DOCS10_TERMS,
        failure_code=FailureCode.FORBIDDEN_STRAIGHT_LINE,
    )


FORBIDDEN_STRAIGHT_LINES: tuple[ForbiddenLine, ...] = (
    # --- docs/04 — canonical forbidden transitions -----------------------
    _canonical("Binary", "Text", "Bytes carry no script identity.", "EncodingIdentityGate"),
    _canonical(
        "Unicode",
        "ArabicLetter",
        "A code point is an encoding trace, not a letter identity.",
        "LetterIdentityGate",
    ),
    _canonical("CodePoint", "Phoneme", "A code point is not a sound.", "PhoneticRealisationGate"),
    _canonical(
        "Grapheme",
        "FunctionalLetter",
        "A graphical mark is not a functional letter.",
        "LetterFunctionGate",
    ),
    _canonical(
        "HarakaMark",
        "CaseFunction",
        "A vowel mark is not a case role without position and syntax.",
        "HarakaFunctionGate",
    ),
    _canonical(
        "Orthography",
        "Pronunciation",
        "Spelling is not pronunciation.",
        "PhoneticRealisationGate",
    ),
    _canonical(
        "Pronunciation",
        "Syllable",
        "Sounds are not syllables without prosodic structure.",
        "SyllableStructureGate",
    ),
    _canonical(
        "Syllable",
        "Word",
        "Syllables are not words without lexical identity.",
        "LexicalIdentityGate",
    ),
    _canonical(
        "Signifier",
        "WordForm",
        "A signifier is not a word-form without morphological law.",
        "MorphologicalRealisationGate",
    ),
    _canonical(
        "WordForm",
        "Meaning",
        "A form is not a meaning without context and convention.",
        "SignificationGate",
    ),
    _canonical(
        "Root",
        "LexicalMeaning",
        "A root is not a meaning; it is a derivational locus.",
        "DerivationGate",
    ),
    _canonical(
        "Weight", "Agency", "A morphological pattern is not a syntactic role.", "RelationRoleGate"
    ),
    _canonical(
        "Pattern",
        "SyntaxRole",
        "Pattern is not role without relation and context.",
        "RelationRoleGate",
    ),
    _canonical(
        "VerbalSignified",
        "PureConcept",
        "A signified is not a pure concept.",
        "ConceptualAbstractionGate",
    ),
    _canonical(
        "Wadʿ",
        "Dalālah",
        "Convention is not signification without a stated domain.",
        "DomainBoundDalalahGate",
    ),
    _canonical(
        "Dalālah",
        "ContextualMeaning",
        "Signification is not contextual meaning without context.",
        "ContextualResolutionGate",
    ),
    _canonical(
        "PureConcept",
        "IntendedMeaning",
        "A concept is not an intended meaning without an utterer.",
        "IntentAttributionGate",
    ),
    _canonical("Context", "Relation", "Context is not a relation.", "RelationDeclarationGate"),
    _canonical("Relation", "Ifādah", "Relation is not informative content.", "IfadahGate"),
    _canonical("Ifādah", "Judgment", "Informative content is not a judgment.", "JudgmentGate"),
    _canonical("Judgment", "Application", "A judgment is not its application.", "ApplicationGate"),
    _canonical(
        "Evidence",
        "Certainty",
        "Evidence has a rank; it never equals certainty.",
        "RankLattice (no auto-promote)",
    ),
    _canonical(
        "LexiconEntry",
        "Candidate",
        "A lexicon entry is a witness, not a generator.",
        "LexiconEvidenceGate",
    ),
    _canonical(
        "Candidate",
        "Certificate",
        "A candidate becomes a certificate only with higher evidence.",
        "CertificationGate",
    ),
    _canonical(
        "ResidualHidden",
        "ApprovedOutput",
        "Hidden residuals block all approved outputs.",
        "ResidualPolicy (visibility)",
    ),
    _canonical(
        "RankBelow",
        "RankAbove",
        "No rank promotion without a gate verdict.",
        "TransitionGate + RankLattice",
    ),
    # The compound docs/04 row ``Tool/Number/LCNV → Knowledge`` is
    # entered as three rows so the query contract answers each name.
    _canonical(
        "Tool", "Knowledge", "An instrument or measurement is not knowledge.", "ToolBoundaryGate"
    ),
    _canonical(
        "Number", "Knowledge", "An instrument or measurement is not knowledge.", "ToolBoundaryGate"
    ),
    _canonical(
        "LCNV", "Knowledge", "An instrument or measurement is not knowledge.", "ToolBoundaryGate"
    ),
    # --- docs/04 — pre-text declared-entry transitions (docs/11 §13) -----
    _pre_text(
        "HumanVoice",
        "ArabicText",
        "A voice event is not a written text without decoding and ASR.",
        "AudioDecodingGate + ASRGate",
    ),
    _pre_text("BinaryAudio", "Text", "Audio bytes carry no text identity.", "AudioDecodingGate"),
    _pre_text(
        "BinaryAudio",
        "UnicodeText",
        "Audio bytes are not code points.",
        "AudioDecodingGate + ASRGate",
    ),
    _pre_text(
        "BinaryAudio",
        "Meaning",
        "Audio bytes are not meaning.",
        "Full pre-text + interpretation chain",
    ),
    _pre_text(
        "BinaryText",
        "Unicode",
        "Bytes are not code points without a stated encoding.",
        "EncodingDecodeGate",
    ),
    _pre_text(
        "BinaryText",
        "ArabicLetter",
        "Bytes are not letters.",
        "EncodingDecodeGate + LetterIdentityGate",
    ),
    _pre_text(
        "Unicode",
        "ArabicText",
        "Code points are an encoding trace, not normalised script.",
        "UnicodeTextNormalizationGate",
    ),
    _pre_text(
        "Unicode",
        "ArabicLetter",
        "A code point is an encoding trace, not a letter identity.",
        "ArabicLetterIdentityGate",
    ),
    _pre_text("CodePoint", "Phoneme", "A code point is not a sound.", "PhonemeEvidenceBridge"),
    _pre_text(
        "Grapheme",
        "FunctionalLetter",
        "A graphical mark is not a functional letter.",
        "FunctionalLetterGate",
    ),
    _pre_text(
        "VocalizedText",
        "ValidAnalysis",
        "A vocalized text is a TextTraceCandidate, not an analysis.",
        "TextEntryValidationGate",
    ),
    _pre_text(
        "DeclaredEntry",
        "OntologicalOrigin",
        "A declared operational entry is not the origin of the trace.",
        "none — refusal is constitutional",
    ),
    # --- docs/16 §4 — the six new forbidden straight lines ---------------
    _chain(
        "Identity",
        "Truth",
        "Identity preservation is not a truth verdict.",
        "Gamma + Gate + Evidence + Rank",
    ),
    _chain("Matching", "Meaning", "Role assignment is not meaning.", "Signification chain + Gate"),
    _chain(
        "Potentiality",
        "Actuality",
        "Admissibility is not filling.",
        "Opening control + Closure + Gate",
    ),
    _chain("Opening", "Closure", "An opening is not its closure without Γ.", "Γ then Gate"),
    _chain(
        "Closure",
        "Certificate",
        "Closure is boundary satisfaction, not truth.",
        "Rank lattice + Gate",
    ),
    _chain(
        "Candidate", "Truth", "A candidate is not a certificate.", "Certification gate + Evidence"
    ),
)


TERMINOLOGY_TRANSFERS: tuple[TerminologyTransfer, ...] = (
    # cause ≠ sabab (سبب) ≠ ʿillah (علة) across physics, fiqh, and
    # philosophy (docs/10) — each surface form is fixed in its own
    # science; every directed move to another listed science is a
    # forbidden transfer until a TerminologyBridgeGate is supplied.
    _term("cause", "physics", "fiqh", "TerminologyBridgeGate"),
    _term("cause", "physics", "philosophy", "TerminologyBridgeGate"),
    _term("sabab", "fiqh", "physics", "TerminologyBridgeGate"),
    _term("sabab", "fiqh", "philosophy", "TerminologyBridgeGate"),
    _term("ʿillah", "philosophy", "physics", "TerminologyBridgeGate"),
    _term("ʿillah", "philosophy", "fiqh", "TerminologyBridgeGate"),
    # qiyās (قياس) in logic ≠ qiyās in uṣūl al-fiqh ≠ qiyās in
    # mathematics (analogy / juristic analogy / measurement) — the
    # same surface form in three sciences; every directed pair is a
    # forbidden transfer (docs/10).
    _term("qiyās", "logic", "uṣūl al-fiqh", "TerminologyBridgeGate"),
    _term("qiyās", "logic", "mathematics", "TerminologyBridgeGate"),
    _term("qiyās", "uṣūl al-fiqh", "logic", "TerminologyBridgeGate"),
    _term("qiyās", "uṣūl al-fiqh", "mathematics", "TerminologyBridgeGate"),
    _term("qiyās", "mathematics", "logic", "TerminologyBridgeGate"),
    _term("qiyās", "mathematics", "uṣūl al-fiqh", "TerminologyBridgeGate"),
)


# The constitutional registry instance: every layer-leap row of
# docs/04 (both tables) and docs/16 §4, plus the docs/10 starting
# terminology cases. This is the value the generic TransitionGate
# consults (docs/08 step 2 — PR-5 binding).
CANONICAL_REGISTRY: ForbiddenLineRegistry = ForbiddenLineRegistry(
    lines=FORBIDDEN_STRAIGHT_LINES,
    term_transfers=TERMINOLOGY_TRANSFERS,
)


def is_forbidden_direct(source: str, target: str) -> bool:
    """The docs/04 query contract over the canonical registry."""

    return CANONICAL_REGISTRY.is_forbidden_direct(source, target)


__all__ = [
    "CANONICAL_REGISTRY",
    "FORBIDDEN_STRAIGHT_LINES",
    "TERMINOLOGY_TRANSFERS",
    "ForbiddenLine",
    "ForbiddenLineRegistry",
    "TerminologyTransfer",
    "is_forbidden_direct",
]
