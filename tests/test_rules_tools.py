from agent_zero_trust.config_schema import AgentConfig
from agent_zero_trust.rules_engine import run_rules


def test_database_read_and_email_is_critical():
    config = AgentConfig.model_validate(
        {
            "agent": {"name": "agent"},
            "tools": {"uses_tools": True, "can_read_database": True, "can_send_email": True},
        }
    )

    findings = run_rules(config)

    finding = next(finding for finding in findings if finding.id == "AZT-TOOL-001")
    assert finding.severity == "Critical"
