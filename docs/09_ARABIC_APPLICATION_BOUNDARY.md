# 09 — Arabic Application Boundary

> **Status:** Boundary declaration only. No Arabic code in this
> repository before the core (PR-1 through PR-4) is stable.

This document fixes a deliberate scope boundary: Arabic linguistic
content — phonology, morphology, syntax, lexicons, root/pattern
systems, recitation rules — is **out of scope** until after the
constitutional core and the forbidden-transition registry are landed
and tested.

## Why the boundary exists

The repository's value is not "another Arabic NLP toolkit." It is a
governance layer that prevents *any* claim — Arabic, English, or
numeric — from travelling without an audit trail. If Arabic content
were added before the core is stable, the temptation would be to wire
shortcuts:

- `HarakaMark → CaseFunction` directly,
- `Weight → Agency` directly,
- `LexiconEntry → Candidate` directly.

Every one of those is a forbidden straight line (see
[`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md)).
The discipline of building the core first guarantees that when Arabic
content is finally added, it can only enter as `SlotGraph`s passing
through gates, never as direct value transformations.

## What this boundary forbids in the current PRs

Until the core is stable, the repository must not contain:

- Arabic-script test data treated as semantic input.
- Lexicon files, root tables, pattern tables, or morphological tries.
- Any function whose signature or docstring claims to translate,
  pronounce, parse, or interpret Arabic text.
- Any import of Arabic NLP libraries.

## What this boundary permits

- Mentioning Arabic terms (e.g., *Dalālah*, *Ifādah*, *Wadʿ*, *Qiyās*)
  in *documentation* as examples of layers and forbidden transitions.
- Using transliterated Arabic terms as the *names* of forbidden
  transitions in the PR-4 registry, since the registry is data, not
  linguistic code.

## When the boundary will be reconsidered

After PR-5 ships and the `AnswerAudit` wrapper is in use, a separate
proposal may open the door to a first Arabic application. That
proposal must declare which gates it implements, which forbidden
transitions it explicitly does *not* shortcut, and what evidence
sources it consults. No application code lands before that proposal is
accepted.
