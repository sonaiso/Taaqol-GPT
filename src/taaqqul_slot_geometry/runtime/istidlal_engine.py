from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.runtime.corpus_runner import (
    CorpusRunResult,
    run_native_corpus,
)
from taaqqul_slot_geometry.runtime.report_builder import (
    NativeCorpusReport,
    build_native_report,
)


@dataclass(frozen=True, slots=True)
class IstidlalRuntimeResult:
    corpus_result: CorpusRunResult
    report: NativeCorpusReport
    tokens: tuple[str, ...]
    source_text: str | None


class IstidlalEngine:
    def tokenize(self, text: str) -> tuple[str, ...]:
        if not isinstance(text, str):
            raise TypeError("IstidlalEngine.tokenize() requires text as a string")
        tokens = tuple(token for token in text.split() if token.strip())
        if not tokens:
            raise ValueError("IstidlalEngine.tokenize() requires at least one token")
        return tokens

    def run_text(self, corpus_id: str, text: str) -> IstidlalRuntimeResult:
        tokens = self.tokenize(text)
        return self.run_tokens(corpus_id, tokens, source_text=text)

    def run_tokens(
        self,
        corpus_id: str,
        tokens: tuple[str, ...],
        *,
        source_text: str | None = None,
    ) -> IstidlalRuntimeResult:
        if not isinstance(corpus_id, str):
            raise TypeError("IstidlalEngine.run_tokens() requires corpus_id as a string")
        if not corpus_id.strip():
            raise ValueError("IstidlalEngine.run_tokens() requires a non-empty corpus_id")
        if not isinstance(tokens, tuple):
            raise TypeError("IstidlalEngine.run_tokens() requires tokens as a tuple[str, ...]")
        if not tokens:
            raise ValueError("IstidlalEngine.run_tokens() requires at least one token")
        for token in tokens:
            if not isinstance(token, str):
                raise TypeError("IstidlalEngine.run_tokens() requires every token as a string")
            if not token.strip():
                raise ValueError(
                    "IstidlalEngine.run_tokens() refuses empty/blank token surfaces"
                )
        if source_text is not None and not isinstance(source_text, str):
            raise TypeError(
                "IstidlalEngine.run_tokens() requires source_text as a string or None"
            )

        corpus_result = run_native_corpus(corpus_id, tokens)
        report = build_native_report(corpus_result)
        return IstidlalRuntimeResult(
            corpus_result=corpus_result,
            report=report,
            tokens=tokens,
            source_text=source_text,
        )


__all__ = ["IstidlalEngine", "IstidlalRuntimeResult"]
