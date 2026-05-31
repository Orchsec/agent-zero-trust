from agent_zero_trust.loader import load_config
from agent_zero_trust.rules_engine import all_rules, run_rules

REQUIRED_RULE_IDS = {
    "AZT-ID-001",
    "AZT-ID-002",
    "AZT-ID-003",
    "AZT-AUTH-001",
    "AZT-AUTH-002",
    "AZT-AUTH-003",
    "AZT-TOOL-001",
    "AZT-TOOL-002",
    "AZT-TOOL-003",
    "AZT-MCP-001",
    "AZT-AZ-001",
    "AZT-AZ-002",
    "AZT-LOG-001",
    "AZT-LOG-002",
    "AZT-TRACE-001",
    "AZT-TRACE-002",
    "AZT-MEM-001",
    "AZT-MEM-002",
    "AZT-RAG-001",
    "AZT-RAG-002",
    "AZT-SBX-001",
    "AZT-IO-001",
    "AZT-IO-002",
    "AZT-IO-003",
    "AZT-REC-001",
    "AZT-REC-002",
    "AZT-GOV-001",
    "AZT-GOV-002",
    "AZT-GOV-003",
    "AZT-SC-001",
    "AZT-SC-002",
}


def test_all_documented_rule_ids_exist():
    rule_ids = {rule.id for rule in all_rules()}

    assert rule_ids == REQUIRED_RULE_IDS


def test_high_risk_example_triggers_all_required_rule_categories():
    config = load_config("examples/high-risk-agent.yaml")
    finding_ids = {finding.id for finding in run_rules(config)}

    assert finding_ids == REQUIRED_RULE_IDS


def test_rule_metadata_is_report_ready():
    for rule in all_rules():
        assert rule.title
        assert rule.category
        assert rule.severity in {"Critical", "High", "Medium", "Low"}
        assert rule.description
        assert rule.recommendation
