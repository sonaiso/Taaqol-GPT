# 96 — AUX-ESA-2 SOURCE_BLOCKER_UNMAPPED Translation Contract

> Status: auxiliary contract hardening record for blocker translation.
> Scope: `enriched_simulation_agent/**` plus constitutional record/tests only.
> Snapshot date: 2026-07-18.

## §1 Scope and quarantine

This step is limited to the auxiliary simulation kernel and its contract tests.
It does not open constitutional chain movement and does not alter core runtime.

## §2 Contract statement

If a blocking source condition exists and no licensed target translation exists,
the composed simulation may defer with `DEFER + SOURCE_BLOCKER_UNMAPPED` or
escalate to `BLOCK`.

## §3 Allowed outcomes

A source blocker may be:

1. preserved as the same blocker code in target,
2. translated by explicit mapping to a licensed target blocker code,
3. deferred as `DEFER + SOURCE_BLOCKER_UNMAPPED`,
4. or escalate to `BLOCK`.

## §4 Forbidden outcome

A source blocker that is unmapped must never resolve to `ACCEPT`.
`BLOCK(source) -> ACCEPT(target)` is forbidden.

## §5 Minimal runtime obligations

The auxiliary runtime contract for this step is:

- mapped source blocker must stay visible as preserved or translated blocker,
- unmapped blocking source blocker must not pass as `ACCEPT`,
- unexplained target blocker must yield `BLOCK`,
- unmapped nonblocking source residual must defer, not accept.

## §6 Constitutional non-admission statement

This step does not admit AUX-ESA into `docs/14_PR_CHAIN_ROADMAP.md`.
It does not license any Arabic/programming or linguistic/knowledge bridge.
It does not mutate `src/taaqqul_slot_geometry/**`.
