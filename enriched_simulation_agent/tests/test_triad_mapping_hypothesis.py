from sim_agent.laws import check_triad_mapping_hypothesis
from sim_agent.triad import TriadMappingHypothesis


def test_triad_mapping_hypothesis_accepts_structuring_hypothesis() -> None:
    hypothesis = TriadMappingHypothesis()

    result = check_triad_mapping_hypothesis(hypothesis, treat_as_acceptance_proof=False)

    assert result.passed
    assert result.law_name == "TriadMappingHypothesisBoundary"


def test_triad_mapping_hypothesis_rejects_when_treated_as_proof() -> None:
    hypothesis = TriadMappingHypothesis(acceptance_proof=True)

    result = check_triad_mapping_hypothesis(hypothesis, treat_as_acceptance_proof=True)

    assert not result.passed
    assert "TRIAD_MAPPING_TREATED_AS_PROOF" in result.violations
