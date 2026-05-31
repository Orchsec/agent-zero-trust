"""Authorization and least-agency rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-AZ-001",
        title="Deny by default missing",
        category="authorization",
        score_category="authorization",
        severity="High",
        description="Permissions are not denied by default.",
        recommendation="Make denied access the default and explicitly grant required actions.",
        predicate=lambda c: not c.authorization.deny_by_default,
        evidence=lambda c: f"authorization.deny_by_default={c.authorization.deny_by_default}",
    ),
    Rule(
        id="AZT-AZ-002",
        title="Least privilege not reviewed",
        category="authorization",
        score_category="authorization",
        severity="Medium",
        description="Agent permissions have not been reviewed for least privilege.",
        recommendation="Review and remove permissions not required for the agent's job.",
        predicate=lambda c: not c.authorization.least_privilege_reviewed,
        evidence=lambda c: (
            f"authorization.least_privilege_reviewed={c.authorization.least_privilege_reviewed}"
        ),
    ),
]
