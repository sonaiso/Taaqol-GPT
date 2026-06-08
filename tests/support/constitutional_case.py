"""Constitutional test-case schema and assertion helper.

This module is the executable form of
``docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md``. It defines:

* :class:`ConstitutionalTestCase` — the frozen schema every
  constitutional test must declare before it makes any assertion.
* :class:`ConstitutionalChainResult` — the dual of the case: the
  observed result of walking the declared chain.
* :func:`assert_constitutional_case` — the helper that compares a
  case against a result and refuses to silently accept a partial
  pass.

The schema itself is enforced at construction time
(:meth:`ConstitutionalTestCase.__post_init__`). Tests that import
this module *cannot* skip the declarations the constitution
requires; an incomplete or malformed case raises
``ConstitutionalSchemaError`` immediately.

The executable kernel (``SlotGraph``, ``gamma``, ...) is reserved
for PR-2. The harness here works against named verdicts that match
the PR-1 carrier enums (``ClosureState``, ``Rank``, ``FailureCode``,
``ResidualKind``). When PR-2 lands, ``gamma()`` will return a
``GammaResult`` that can be adapted into
:class:`ConstitutionalChainResult` with no schema changes.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank

# Closure states that represent a *licit closure* of the chain. Every
# other state is a refusal and therefore requires a named failure
# code. This split mirrors docs/03_GAMMA_CLOSURE_CONTRACT.md and
# docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md §3.
_CLOSURE_STATES: frozenset[ClosureState] = frozenset(
    {ClosureState.MINIMALLY_CLOSED, ClosureState.PERFORATED_CLOSED}
)


class ConstitutionalSchemaError(AssertionError):
    """Raised when a test case does not satisfy the harness schema.

    Sub-classing :class:`AssertionError` is deliberate: under pytest
    a schema violation is indistinguishable from a constitutional
    test failure, which is exactly the discipline the harness
    enforces.
    """


@dataclass(frozen=True)
class ConstitutionalTestCase:
    """Declared, immutable identity of a constitutional test.

    See ``docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md`` §3 for the
    governing definition. Every field is mandatory; constructing a
    case with a missing or empty declaration raises
    :class:`ConstitutionalSchemaError` before any assertion runs.
    """

    origin_law: str
    branch_name: str
    constitutional_chain: tuple[str, ...]
    expected_state: ClosureState
    expected_failure_code: FailureCode | None
    forbidden_outputs: tuple[str, ...]
    max_rank: Rank
    required_trace: bool
    required_residual_visibility: bool

    def __post_init__(self) -> None:
        # Origin / branch are short identifiers. They must be
        # present so the test can never be orphaned.
        if not isinstance(self.origin_law, str) or not self.origin_law.strip():
            raise ConstitutionalSchemaError(
                "origin_law must be a non-empty string naming the constitutional law"
            )
        if not isinstance(self.branch_name, str) or not self.branch_name.strip():
            raise ConstitutionalSchemaError(
                "branch_name must be a non-empty string naming the branch under test"
            )

        # The constitutional chain must be a non-empty tuple of
        # non-empty string layer names. A single-element chain is
        # legal (e.g. a Law Test), but a zero-element chain is not.
        if not isinstance(self.constitutional_chain, tuple):
            raise ConstitutionalSchemaError(
                "constitutional_chain must be a tuple of layer names"
            )
        if len(self.constitutional_chain) == 0:
            raise ConstitutionalSchemaError(
                "constitutional_chain must contain at least one layer"
            )
        for layer in self.constitutional_chain:
            if not isinstance(layer, str) or not layer.strip():
                raise ConstitutionalSchemaError(
                    "every chain layer must be a non-empty string"
                )

        # Verdict / failure code must use the PR-1 carrier enums.
        if not isinstance(self.expected_state, ClosureState):
            raise ConstitutionalSchemaError(
                "expected_state must be a ClosureState member"
            )
        if self.expected_failure_code is not None and not isinstance(
            self.expected_failure_code, FailureCode
        ):
            raise ConstitutionalSchemaError(
                "expected_failure_code must be a FailureCode member or None"
            )

        # A licit closure must NOT name a failure code; a refusal
        # MUST. This is the test-side projection of
        # ``Every rejection must be named`` (docs/12 §4).
        if self.expected_state in _CLOSURE_STATES:
            if self.expected_failure_code is not None:
                raise ConstitutionalSchemaError(
                    "a closure verdict must not declare a failure code"
                )
        else:
            if self.expected_failure_code is None:
                raise ConstitutionalSchemaError(
                    "a refusal verdict must declare a named FailureCode"
                )

        # forbidden_outputs must be a tuple of non-empty strings.
        # The list may be empty (some chains have no symmetric
        # forbidden surface) but the type is fixed.
        if not isinstance(self.forbidden_outputs, tuple):
            raise ConstitutionalSchemaError(
                "forbidden_outputs must be a tuple of output names"
            )
        for name in self.forbidden_outputs:
            if not isinstance(name, str) or not name.strip():
                raise ConstitutionalSchemaError(
                    "every forbidden output must be a non-empty string"
                )

        if not isinstance(self.max_rank, Rank):
            raise ConstitutionalSchemaError("max_rank must be a Rank member")

        if not isinstance(self.required_trace, bool):
            raise ConstitutionalSchemaError("required_trace must be a bool")
        if not isinstance(self.required_residual_visibility, bool):
            raise ConstitutionalSchemaError(
                "required_residual_visibility must be a bool"
            )


@dataclass(frozen=True)
class ConstitutionalChainResult:
    """Observed result of walking a constitutional chain.

    PR-1 does not yet ship the executable kernel that would
    construct this naturally. The dataclass is here so that the
    harness API is stable across PR-1B and PR-2: when ``gamma()``
    lands, the kernel adapter will populate exactly these fields.
    """

    state: ClosureState
    failure_code: FailureCode | None
    rank: Rank
    residual_visibility: bool
    trace_present: bool
    produced_outputs: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not isinstance(self.state, ClosureState):
            raise ConstitutionalSchemaError(
                "ConstitutionalChainResult.state must be a ClosureState member"
            )
        if self.failure_code is not None and not isinstance(
            self.failure_code, FailureCode
        ):
            raise ConstitutionalSchemaError(
                "ConstitutionalChainResult.failure_code must be a FailureCode or None"
            )
        if not isinstance(self.rank, Rank):
            raise ConstitutionalSchemaError(
                "ConstitutionalChainResult.rank must be a Rank member"
            )
        if not isinstance(self.residual_visibility, bool):
            raise ConstitutionalSchemaError(
                "ConstitutionalChainResult.residual_visibility must be a bool"
            )
        if not isinstance(self.trace_present, bool):
            raise ConstitutionalSchemaError(
                "ConstitutionalChainResult.trace_present must be a bool"
            )
        if not isinstance(self.produced_outputs, frozenset):
            raise ConstitutionalSchemaError(
                "ConstitutionalChainResult.produced_outputs must be a frozenset"
            )
        for name in self.produced_outputs:
            if not isinstance(name, str) or not name.strip():
                raise ConstitutionalSchemaError(
                    "every produced output must be a non-empty string"
                )


def assert_constitutional_case(
    case: ConstitutionalTestCase, result: ConstitutionalChainResult
) -> None:
    """Compare an observed chain result against a declared case.

    The helper walks the assertion chain required by
    ``docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md`` §4 in order. The
    first violated step raises ``AssertionError`` with a message
    that names the law, the branch, and the violated step.

    The helper deliberately refuses to short-circuit on a green
    verdict: a result whose ``state`` matches the case but whose
    rank, trace, residual visibility, or output boundary do not is
    still a failure. That is the entire point of the harness.
    """

    if not isinstance(case, ConstitutionalTestCase):
        raise ConstitutionalSchemaError(
            "assert_constitutional_case requires a ConstitutionalTestCase"
        )
    if not isinstance(result, ConstitutionalChainResult):
        raise ConstitutionalSchemaError(
            "assert_constitutional_case requires a ConstitutionalChainResult"
        )

    prefix = f"[{case.origin_law} / {case.branch_name}]"

    # Step 5 — Verdict matches.
    if result.state is not case.expected_state:
        raise AssertionError(
            f"{prefix} expected ClosureState {case.expected_state.name}, "
            f"got {result.state.name}"
        )

    # Step 10 — Named failure / named closure.
    if result.failure_code is not case.expected_failure_code:
        expected_name = (
            case.expected_failure_code.name
            if case.expected_failure_code is not None
            else "None"
        )
        actual_name = (
            result.failure_code.name if result.failure_code is not None else "None"
        )
        raise AssertionError(
            f"{prefix} expected FailureCode {expected_name}, got {actual_name}"
        )

    # Step 5b — Rank ceiling.
    if result.rank.value > case.max_rank.value:
        raise AssertionError(
            f"{prefix} rank {result.rank.name} exceeds declared ceiling "
            f"{case.max_rank.name}"
        )

    # Step 6 — Residual visibility.
    if case.required_residual_visibility and not result.residual_visibility:
        raise AssertionError(
            f"{prefix} residual visibility was required but not observed"
        )

    # Step 7 — Trace presence.
    if case.required_trace and not result.trace_present:
        raise AssertionError(
            f"{prefix} trace candidate was required but not observed"
        )

    # Step 9 — Forbidden outputs proven absent.
    forbidden_present = sorted(
        set(case.forbidden_outputs) & set(result.produced_outputs)
    )
    if forbidden_present:
        raise AssertionError(
            f"{prefix} forbidden outputs were produced: {forbidden_present}"
        )


__all__: list[str] = [
    "ConstitutionalSchemaError",
    "ConstitutionalTestCase",
    "ConstitutionalChainResult",
    "assert_constitutional_case",
]
