"""Tool risk rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-TOOL-001",
        title="Agent can read database and send email",
        category="tools",
        score_category="tools_mcp",
        severity="Critical",
        description="The agent can combine sensitive data access with external communication.",
        recommendation="Add approval gates, output filtering, and scoped tool permissions.",
        predicate=lambda c: c.tools.can_read_database and c.tools.can_send_email,
        evidence=lambda c: (
            f"tools.can_read_database={c.tools.can_read_database}; "
            f"tools.can_send_email={c.tools.can_send_email}"
        ),
    ),
    Rule(
        id="AZT-TOOL-002",
        title="Tools lack allowlist",
        category="tools",
        score_category="tools_mcp",
        severity="High",
        description="The agent can use tools without a defined allowlist boundary.",
        recommendation="Create an allowlist of permitted tools and actions.",
        predicate=lambda c: c.tools.uses_tools and not c.tools.tools_allowlist_exists,
        evidence=lambda c: f"tools.tools_allowlist_exists={c.tools.tools_allowlist_exists}",
    ),
    Rule(
        id="AZT-TOOL-003",
        title="High-risk tools without approval",
        category="tools",
        score_category="tools_mcp",
        severity="High",
        description="High-impact actions can occur without human or policy approval.",
        recommendation=(
            "Require approval for email, database writes, code execution, and external actions."
        ),
        predicate=lambda c: (
            c.tools.can_send_email
            or c.tools.can_write_database
            or c.tools.can_execute_code
            or c.tools.can_call_external_apis
        )
        and not c.tools.high_risk_tools_require_approval,
        evidence=lambda c: (
            "tools.high_risk_tools_require_approval="
            f"{c.tools.high_risk_tools_require_approval}"
        ),
    ),
]
