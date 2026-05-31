"""Governance rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-GOV-001",
        title="No risk assessment",
        category="governance",
        score_category="governance",
        severity="Medium",
        description="The agent has not gone through a documented security risk assessment.",
        recommendation="Perform an AI agent risk assessment before production deployment.",
        predicate=lambda c: not c.governance.risk_assessment_done,
        evidence=lambda c: f"governance.risk_assessment_done={c.governance.risk_assessment_done}",
    ),
    Rule(
        id="AZT-GOV-002",
        title="No incident response plan",
        category="governance",
        score_category="governance",
        severity="High",
        description="There is no response plan for agent compromise, tool abuse, or data leakage.",
        recommendation="Create an incident response process for agent-specific failure modes.",
        predicate=lambda c: not c.governance.incident_response_plan_exists,
        evidence=lambda c: (
            "governance.incident_response_plan_exists="
            f"{c.governance.incident_response_plan_exists}"
        ),
    ),
    Rule(
        id="AZT-GOV-003",
        title="No human owner",
        category="governance",
        score_category="governance",
        severity="High",
        description="No accountable human owner is defined for the agent.",
        recommendation="Assign a human owner accountable for the agent.",
        predicate=lambda c: not c.governance.human_owner_defined,
        evidence=lambda c: f"governance.human_owner_defined={c.governance.human_owner_defined}",
    ),
]
