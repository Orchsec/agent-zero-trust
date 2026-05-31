"""Logging rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-LOG-001",
        title="Tool calls not logged",
        category="logging",
        score_category="logging_traceability",
        severity="High",
        description="Tool use is not recorded for investigation or accountability.",
        recommendation="Log tool name, arguments metadata, result status, actor, and request ID.",
        predicate=lambda c: c.tools.uses_tools and not c.logging.logs_tool_calls,
        evidence=lambda c: f"logging.logs_tool_calls={c.logging.logs_tool_calls}",
    ),
    Rule(
        id="AZT-LOG-002",
        title="Data access not logged",
        category="logging",
        score_category="logging_traceability",
        severity="High",
        description="Access to data stores is not logged.",
        recommendation="Log data access decisions and sensitive resource identifiers.",
        predicate=lambda c: (c.tools.can_read_database or c.tools.can_write_database)
        and not c.logging.logs_data_access,
        evidence=lambda c: f"logging.logs_data_access={c.logging.logs_data_access}",
    ),
]
