from agent_zero_trust.loader import load_config
from agent_zero_trust.scanner import scan_config
from agent_zero_trust.scoring import readiness_level


def test_low_risk_example_scores_high():
    result = scan_config(load_config("examples/basic-chatbot.yaml"))

    assert result.score >= 90
    assert result.blast_radius in {"Low", "Medium"}


def test_high_risk_example_scores_critical():
    result = scan_config(load_config("examples/high-risk-agent.yaml"))

    assert result.score <= 39
    assert result.blast_radius == "Critical"
    assert result.summary["Critical"] >= 1


def test_readiness_levels():
    assert readiness_level(95) == "Strong"
    assert readiness_level(80) == "Good"
    assert readiness_level(65) == "Needs improvement"
    assert readiness_level(45) == "High risk"
    assert readiness_level(20) == "Critical risk"
