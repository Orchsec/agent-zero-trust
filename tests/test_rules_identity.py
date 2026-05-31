from agent_zero_trust.config_schema import AgentConfig
from agent_zero_trust.rules_engine import run_rules


def test_missing_unique_identity_finds_rule():
    config = AgentConfig.model_validate(
        {"agent": {"name": "agent"}, "identity": {"unique_identity": False}}
    )

    findings = run_rules(config)

    assert any(finding.id == "AZT-ID-001" for finding in findings)
