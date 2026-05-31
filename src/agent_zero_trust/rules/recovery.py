"""Recovery rules."""

from agent_zero_trust.config_schema import Environment
from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-REC-001",
        title="No rollback plan",
        category="recovery",
        score_category="recovery",
        severity="Medium",
        description="The team lacks a rollback path for unsafe agent behavior or release issues.",
        recommendation="Create and test a rollback plan for agent prompts, tools, and deployments.",
        predicate=lambda c: not c.recovery.rollback_plan_exists,
        evidence=lambda c: f"recovery.rollback_plan_exists={c.recovery.rollback_plan_exists}",
    ),
    Rule(
        id="AZT-REC-002",
        title="No kill switch in production",
        category="recovery",
        score_category="recovery",
        severity="High",
        description="The production agent cannot be disabled quickly during an incident.",
        recommendation="Add a kill switch to disable the agent quickly during incidents.",
        predicate=lambda c: c.agent.environment == Environment.production
        and not c.recovery.kill_switch_exists,
        evidence=lambda c: (
            f"agent.environment={c.agent.environment}; "
            f"recovery.kill_switch_exists={c.recovery.kill_switch_exists}"
        ),
    ),
]
