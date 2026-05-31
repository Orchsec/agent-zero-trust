"""MCP-specific rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-MCP-001",
        title="MCP used without server review",
        category="mcp",
        score_category="tools_mcp",
        severity="High",
        description="MCP servers can expose broad tool, file, or network authority.",
        recommendation="Review MCP server source, permissions, isolation, and update process.",
        predicate=lambda c: c.tools.uses_mcp and not c.tools.mcp_servers_reviewed,
        evidence=lambda c: (
            f"tools.uses_mcp={c.tools.uses_mcp}; "
            f"tools.mcp_servers_reviewed={c.tools.mcp_servers_reviewed}"
        ),
    )
]
