"""Adapter boundary carriers — PR-8 binding of ``docs/18_ADAPTER_BOUNDARY_LAW.md``.

docs/18 §1 fixes the only licensing chain an adapter may travel::

    ModelClient protocol → ConcreteAdapterCandidate → AdapterGuard
        → AuditedAnswer only

*An adapter is a transport, not a judge.* This module binds the
pre-``AnswerAudit`` half of that chain:

* :class:`TransportSurface` — the closed vocabulary of declared
  transports (docs/18 §2). ``IN_MEMORY`` < ``LOCAL_PROCESS`` <
  ``NETWORK`` is an *exposure* order, not a quality order: a
  candidate's declaration is the ceiling of what its completion may
  expose.
* :class:`ConcreteAdapterCandidate` — the §2 declaration surface a
  would-be adapter must fill **at birth**: adapter identity, model
  identity, transport surface, the one required completion slot,
  and constructor-only configuration. No defaults, no synthesis,
  no best-effort mode. The adapter never looks anything up — not
  environment variables, not the filesystem, not the network.
* :class:`AdapterGuard` — the single admission door (docs/18 §1).
  Its :meth:`~AdapterGuard.admit` walks the §3 refusal table in
  order and returns an :class:`AdapterAdmission` value. The guard
  is **pure** and **total** (docs/18 §7): it never calls
  ``complete()``, performs no I/O, and names every expected refusal
  with an existing :class:`FailureCode` — never a bare exception.
  A wrong *type* of argument is a programmer mistake refused loudly
  with ``TypeError``, consistent with the PR-6 audit surface.
* :class:`AdapterAdmission` — the admission verdict value.
  Admission is **not** approval (docs/18 §5): it grants no rank,
  constructs no graph, licenses no output, and writes no trace.
  Everything an admitted client emits still walks the full
  ``AnswerAudit`` chain.

The structural refusals of docs/18 §3 rows 6–10 are detected
against the *named surface registries* below: a completion whose
type or instance exposes a verdict, confidence, ledger, successor,
or rank name is refused before any transport runs. Detection is
deliberately **static** (:func:`inspect.getattr_static`, which
walks the instance ``__dict__`` and the MRO ``__dict__`` mappings
without invoking ``__getattribute__``, ``__getattr__``, or a
descriptor's ``__get__``) so the guard never executes adapter code
— not even adapter-authored lookup machinery — while judging it
(docs/18 §7, PR-8.1 binding).

This module imports exactly two first-party names —
:class:`ModelClient` (the docs/01 boundary) and
:class:`FailureCode` (the named refusal vocabulary) — and the
standard library. No kernel authority (``gamma``, ``SlotGraph``,
``TransitionGate``, ``TraceLedger``, ``Rank``) is reachable from
here; the static guards in ``tests/test_adapter_boundary.py``
prove it.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import IntEnum
from inspect import getattr_static
from types import MappingProxyType

from taaqqul_slot_geometry.audit.model_client import ModelClient
from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode

#: docs/18 §3 row 6 — a completion exposing any of these names offers
#: a verdict surface: it is a judge, not a transport.
VERDICT_SURFACE_NAMES: frozenset[str] = frozenset(
    {"approve", "closure_state", "decide", "transition_state", "verdict"}
)

#: docs/18 §3 row 7 — model internals offered as evidence. A model's
#: confidence in its own answer is never evidence (docs/01).
CONFIDENCE_SURFACE_NAMES: frozenset[str] = frozenset(
    {
        "chain_of_thought",
        "confidence",
        "hidden_state",
        "logits",
        "logprobs",
        "token_probabilities",
    }
)

#: docs/18 §3 row 8 — a trace-ledger write surface. The ``AnswerAudit``
#: shell owns the ledger (docs/07); an adapter that can append has
#: exceeded its layer.
LEDGER_SURFACE_NAMES: frozenset[str] = frozenset(
    {"append", "append_trace", "ledger", "trace_ledger"}
)

#: docs/18 §3 row 9 — a successor-graph surface. Only an ``APPROVED``
#: ``TransitionVerdict`` generates a successor (docs/17 §1, source 3).
SUCCESSOR_SURFACE_NAMES: frozenset[str] = frozenset(
    {"construct_graph", "emit_successor", "slot_graph", "successor", "successor_graph"}
)

#: docs/18 §3 row 10 — a rank claim. No adapter holds rank authority;
#: rank moves only through the gate's bounded meet (docs/05, docs/08).
RANK_SURFACE_NAMES: frozenset[str] = frozenset(
    {"granted_rank", "promote", "promote_rank", "rank"}
)


class TransportSurface(IntEnum):
    """Declared transport vocabulary (docs/18 §2).

    The integer order is an **exposure** order used only as a
    ceiling check: a completion that declares a wider transport
    than its candidate declares is an unlicensed opening
    (docs/18 §3 row 5, §4). It is never a quality or rank order.
    """

    IN_MEMORY = 1
    LOCAL_PROCESS = 2
    NETWORK = 3


@dataclass(frozen=True)
class ConcreteAdapterCandidate:
    """The docs/18 §2 declaration surface, filled at birth.

    Every field is declared by the constructing caller; nothing is
    defaulted, looked up, or synthesised. Wrong *types* are refused
    loudly with ``TypeError`` at construction (a programmer
    mistake); missing or empty *content* — an empty identity, an
    undeclared transport, a completion that is not a
    :class:`ModelClient` — is left for :meth:`AdapterGuard.admit`
    to refuse as a named docs/18 §3 value, because those are
    expected constitutional refusals, not crashes (docs/18 §7).

    ``configuration`` is constructor-args-only (docs/18 §2): it is
    copied and frozen at birth so later mutation of the source
    mapping cannot reach an already-declared candidate.
    """

    adapter_identity: str
    model_identity: str
    transport_surface: TransportSurface | None
    completion: object
    configuration: Mapping[str, str]

    def __post_init__(self) -> None:
        if not isinstance(self.adapter_identity, str):
            raise TypeError("ConcreteAdapterCandidate requires adapter_identity as a str")
        if not isinstance(self.model_identity, str):
            raise TypeError("ConcreteAdapterCandidate requires model_identity as a str")
        if self.transport_surface is not None and not isinstance(
            self.transport_surface, TransportSurface
        ):
            raise TypeError(
                "ConcreteAdapterCandidate requires transport_surface as a "
                "TransportSurface or None"
            )
        if not isinstance(self.configuration, Mapping):
            raise TypeError("ConcreteAdapterCandidate requires configuration as a Mapping")
        for key, value in self.configuration.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise TypeError(
                    "ConcreteAdapterCandidate requires configuration entries as str -> str"
                )
        object.__setattr__(self, "configuration", MappingProxyType(dict(self.configuration)))


@dataclass(frozen=True)
class AdapterAdmission:
    """The admission verdict value :meth:`AdapterGuard.admit` returns.

    Exactly one of ``client`` / ``failure_code`` is set:

    * admitted — ``client`` is the candidate's own completion,
      handed onward to ``AnswerAudit`` unchanged; ``failure_code``
      is ``None``;
    * refused — ``client`` is ``None`` and ``failure_code`` names
      the docs/18 §3 row that fired.

    Admission is not approval (docs/18 §5): this value carries no
    rank, no graph, no output, and no trace entry. Its invariants
    are enforced at birth with ``TypeError`` because an admission
    that is both (or neither) is a programmer mistake, never an
    expected verdict.
    """

    client: ModelClient | None
    failure_code: FailureCode | None
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.message, str) or not self.message.strip():
            raise TypeError("AdapterAdmission requires a non-empty message")
        if (self.client is None) == (self.failure_code is None):
            raise TypeError(
                "AdapterAdmission requires exactly one of client / failure_code "
                "(admitted xor refused)"
            )
        if self.client is not None and not isinstance(self.client, ModelClient):
            raise TypeError("AdapterAdmission requires client to satisfy ModelClient")
        if self.failure_code is not None and not isinstance(self.failure_code, FailureCode):
            raise TypeError("AdapterAdmission requires failure_code as a FailureCode")

    @property
    def is_refusal(self) -> bool:
        """``True`` when the guard refused the candidate."""

        return self.failure_code is not None


#: Sentinel for a name :func:`inspect.getattr_static` finds nowhere on
#: the instance, its class MRO, or its metaclass MRO — distinct from
#: every value an adapter could declare (including ``None``).
_STATIC_MISS: object = object()


def _static_attribute(completion: object, name: str) -> object:
    """Resolve ``name`` on ``completion`` without executing anything.

    :func:`inspect.getattr_static` reads the instance ``__dict__``
    and the MRO ``__dict__`` mappings directly — it never invokes
    ``__getattribute__``, ``__getattr__``, or a descriptor's
    ``__get__`` — so adapter-authored lookup machinery cannot run,
    lie, or detonate while the guard is judging (docs/18 §7). The
    type-level second pass keeps names a metaclass defines visible:
    a surface offered through the type of the type is still a
    surface.
    """

    found = getattr_static(completion, name, _STATIC_MISS)
    if found is _STATIC_MISS:
        found = getattr_static(type(completion), name, _STATIC_MISS)
    return found


def _declared_transport(completion: object) -> TransportSurface | None:
    """Read the transport a completion *declares*, without running it.

    Resolution is static (:func:`_static_attribute`): the value must
    *be* a :class:`TransportSurface` member sitting in the instance
    or MRO ``__dict__``. A property or descriptor that would compute
    one on access is not a declaration — the adapter never looks
    anything up (docs/18 §2) — so it counts as undeclared, and the
    guard never runs it to find out.
    """

    declared = _static_attribute(completion, "transport_surface")
    if isinstance(declared, TransportSurface):
        return declared
    return None


def _exposed_surface(completion: object, names: frozenset[str]) -> tuple[str, ...]:
    """Names from ``names`` the completion structurally exposes.

    Static detection only (:func:`_static_attribute`): a property or
    descriptor object is *seen* but never invoked, and a name
    synthesised only by dynamic lookup hooks is not a structural
    surface. The guard never executes adapter code (docs/18 §7).
    """

    exposed = {
        name for name in names if _static_attribute(completion, name) is not _STATIC_MISS
    }
    return tuple(sorted(exposed))


#: docs/18 §3 rows 6–10, walked in table order by :meth:`AdapterGuard.admit`.
_SURFACE_REFUSALS: tuple[tuple[frozenset[str], FailureCode, str], ...] = (
    (
        VERDICT_SURFACE_NAMES,
        FailureCode.FORBIDDEN_STRAIGHT_LINE,
        "a verdict surface — an adapter is a transport, not a judge (docs/18 §3, §6)",
    ),
    (
        CONFIDENCE_SURFACE_NAMES,
        FailureCode.FORBIDDEN_STRAIGHT_LINE,
        "a confidence / model-internals surface — internals are never evidence "
        "(docs/18 §3; docs/01)",
    ),
    (
        LEDGER_SURFACE_NAMES,
        FailureCode.OUTPUT_EXCEEDS_LAYER,
        "a trace-ledger write surface — the AnswerAudit shell owns the ledger "
        "(docs/18 §3; docs/07)",
    ),
    (
        SUCCESSOR_SURFACE_NAMES,
        FailureCode.GATE_REQUIRED,
        "a successor-graph surface — only an APPROVED TransitionVerdict generates "
        "(docs/18 §3; docs/17 §1)",
    ),
    (
        RANK_SURFACE_NAMES,
        FailureCode.RANK_PROMOTION_WITHOUT_GATE,
        "a rank claim — no adapter holds rank authority (docs/18 §3; docs/05)",
    ),
)


class AdapterGuard:
    """The single admission door of docs/18 §1.

    :meth:`admit` is pure (no I/O, no ``complete()`` call, no
    ledger append, no mutation) and total over its declared domain:
    every expected refusal is an :class:`AdapterAdmission` value
    carrying a named :class:`FailureCode` from the docs/18 §3
    table, in table order. There is no second door and no bypass
    (docs/18 §8): an adapter reaches ``AnswerAudit`` only through
    here.
    """

    @staticmethod
    def admit(candidate: ConcreteAdapterCandidate) -> AdapterAdmission:
        """Walk the docs/18 §3 refusal table over ``candidate``."""

        if not isinstance(candidate, ConcreteAdapterCandidate):
            raise TypeError("AdapterGuard.admit() requires a ConcreteAdapterCandidate")

        if not candidate.adapter_identity.strip():
            return AdapterAdmission(
                client=None,
                failure_code=FailureCode.IDENTITY_BROKEN,
                message=(
                    "AdapterGuard: adapter identity is missing or empty — an unnamed "
                    "transport cannot be admitted (docs/18 §3)."
                ),
            )
        if not candidate.model_identity.strip():
            return AdapterAdmission(
                client=None,
                failure_code=FailureCode.IDENTITY_BROKEN,
                message=(
                    "AdapterGuard: model identity is missing or empty — an adapter "
                    "for an unnamed model cannot be admitted (docs/18 §3)."
                ),
            )
        if candidate.transport_surface is None:
            return AdapterAdmission(
                client=None,
                failure_code=FailureCode.BOUNDARY_MISSING,
                message=(
                    "AdapterGuard: transport surface is undeclared — without a "
                    "declared transport there is no I/O boundary to license "
                    "(docs/18 §2, §3)."
                ),
            )
        if not isinstance(candidate.completion, ModelClient):
            return AdapterAdmission(
                client=None,
                failure_code=FailureCode.REQUIRED_SLOT_EMPTY,
                message=(
                    "AdapterGuard: the completion slot is empty or does not satisfy "
                    "the ModelClient protocol — the one required slot is unfilled "
                    "(docs/18 §2, §3)."
                ),
            )

        declared = _declared_transport(candidate.completion)
        if declared is not None and declared > candidate.transport_surface:
            return AdapterAdmission(
                client=None,
                failure_code=FailureCode.UNLICENSED_OPENING,
                message=(
                    f"AdapterGuard: the completion declares the {declared.name} "
                    f"transport but the candidate licenses only "
                    f"{candidate.transport_surface.name} — I/O beyond the declared "
                    "surface (docs/18 §3, §4)."
                ),
            )

        for names, failure_code, law in _SURFACE_REFUSALS:
            exposed = _exposed_surface(candidate.completion, names)
            if exposed:
                return AdapterAdmission(
                    client=None,
                    failure_code=failure_code,
                    message=(
                        f"AdapterGuard: the completion exposes {', '.join(exposed)} — "
                        f"{law}."
                    ),
                )

        return AdapterAdmission(
            client=candidate.completion,
            failure_code=None,
            message=(
                f"AdapterGuard: admitted {candidate.adapter_identity!r} for model "
                f"{candidate.model_identity!r} on the "
                f"{candidate.transport_surface.name} transport. Admission is not "
                "approval: no rank, no graph, no output, no trace (docs/18 §5)."
            ),
        )


__all__ = [
    "CONFIDENCE_SURFACE_NAMES",
    "LEDGER_SURFACE_NAMES",
    "RANK_SURFACE_NAMES",
    "SUCCESSOR_SURFACE_NAMES",
    "VERDICT_SURFACE_NAMES",
    "AdapterAdmission",
    "AdapterGuard",
    "ConcreteAdapterCandidate",
    "TransportSurface",
]
