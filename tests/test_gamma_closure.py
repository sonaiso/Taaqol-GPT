import unittest

from taaqqul_slot_geometry import (
    GammaClosureState,
    Residual,
    ResidualKind,
    Slot,
    SlotGraph,
    SlotState,
    TraceRef,
    close_slot_graph,
)


class GammaClosureTests(unittest.TestCase):
    def test_open_graph_without_required_slots(self) -> None:
        graph = SlotGraph(
            center="claim",
            layer=1,
            trace=TraceRef("trace-open"),
            slots=(Slot(name="subject", required=True),),
        )

        result = close_slot_graph(graph)

        self.assertEqual(result.state, GammaClosureState.OPEN)
        self.assertEqual(result.missing_required_slots, ("subject",))

    def test_minimally_closed_graph_with_required_slots(self) -> None:
        graph = SlotGraph(
            center="claim",
            layer=1,
            trace=TraceRef("trace-closed"),
            slots=(
                Slot(
                    name="subject",
                    required=True,
                    state=SlotState.FILLED,
                    value="evidence-backed subject",
                ),
            ),
        )

        result = close_slot_graph(graph)

        self.assertEqual(result.state, GammaClosureState.MINIMALLY_CLOSED)
        self.assertFalse(result.limited_candidate)

    def test_perforated_closed_graph_with_non_blocking_residuals(self) -> None:
        graph = SlotGraph(
            center="claim",
            layer=1,
            trace=TraceRef("trace-perforated"),
            slots=(Slot(name="subject", required=True, state=SlotState.FILLED),),
            residuals=(
                Residual(
                    code="missing-context",
                    kind=ResidualKind.NON_BLOCKING,
                    message="Context is declared but not fully resolved.",
                ),
            ),
        )

        result = close_slot_graph(graph)

        self.assertEqual(result.state, GammaClosureState.PERFORATED_CLOSED)
        self.assertTrue(result.limited_candidate)
        self.assertEqual(result.residuals[0].code, "missing-context")

    def test_blocked_graph_with_blocking_residual(self) -> None:
        graph = SlotGraph(
            center="claim",
            layer=1,
            trace=TraceRef("trace-blocked"),
            slots=(Slot(name="subject", required=True, state=SlotState.FILLED),),
            residuals=(
                Residual(
                    code="contradiction",
                    kind=ResidualKind.BLOCKING,
                    message="Conflicting evidence prevents closure.",
                ),
            ),
        )

        result = close_slot_graph(graph)

        self.assertEqual(result.state, GammaClosureState.BLOCKED)
        self.assertEqual(result.residuals[0].code, "contradiction")

    def test_invalid_graph_with_identity_break(self) -> None:
        graph = SlotGraph(
            center="claim",
            layer=1,
            trace=TraceRef("trace-invalid"),
            slots=(Slot(name="subject", required=True, state=SlotState.FILLED),),
            identity_ok=False,
        )

        result = close_slot_graph(graph)

        self.assertEqual(result.state, GammaClosureState.INVALID)

    def test_forbidden_leap_when_output_exceeds_layer(self) -> None:
        graph = SlotGraph(
            center="claim",
            layer=1,
            trace=TraceRef("trace-leap"),
            slots=(Slot(name="subject", required=True, state=SlotState.FILLED),),
        )

        result = close_slot_graph(graph, requested_output_layer=2)

        self.assertEqual(result.state, GammaClosureState.FORBIDDEN_LEAP)
        self.assertEqual(result.output_layer, 2)


if __name__ == "__main__":
    unittest.main()
