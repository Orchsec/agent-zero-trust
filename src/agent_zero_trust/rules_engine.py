"""Deterministic rule evaluation."""

from agent_zero_trust.config_schema import AgentConfig
from agent_zero_trust.constants import SEVERITY_ORDER
from agent_zero_trust.findings import Finding, Rule
from agent_zero_trust.rules import (
    authentication,
    governance,
    identity,
    input_output_controls,
    logging,
    mcp,
    memory,
    permissions,
    rag,
    recovery,
    sandboxing,
    supply_chain,
    tools,
    traceability,
)

RULE_MODULES = [
    identity,
    authentication,
    tools,
    mcp,
    permissions,
    logging,
    traceability,
    memory,
    rag,
    sandboxing,
    input_output_controls,
    recovery,
    governance,
    supply_chain,
]


def all_rules() -> list[Rule]:
    rules: list[Rule] = []
    for module in RULE_MODULES:
        rules.extend(module.RULES)
    return sorted(rules, key=lambda rule: rule.id)


def run_rules(config: AgentConfig) -> list[Finding]:
    findings = [finding for rule in all_rules() if (finding := rule.evaluate(config))]
    severity_rank = {severity: index for index, severity in enumerate(SEVERITY_ORDER)}
    return sorted(findings, key=lambda finding: (severity_rank[finding.severity], finding.id))
