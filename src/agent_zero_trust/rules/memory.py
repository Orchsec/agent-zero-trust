"""Memory rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-MEM-001",
        title="Memory used without isolation",
        category="memory",
        score_category="memory_rag",
        severity="High",
        description="Shared memory can leak data across users, tenants, or tasks.",
        recommendation="Isolate memory by tenant, user, environment, and purpose.",
        predicate=lambda c: c.memory.uses_memory and not c.memory.memory_isolated,
        evidence=lambda c: f"memory.memory_isolated={c.memory.memory_isolated}",
    ),
    Rule(
        id="AZT-MEM-002",
        title="Sensitive data can be stored in memory without expiration",
        category="memory",
        score_category="memory_rag",
        severity="High",
        description="Sensitive memory without expiration increases privacy and breach impact.",
        recommendation="Avoid storing sensitive data or enforce retention limits and deletion.",
        predicate=lambda c: c.memory.uses_memory
        and c.memory.sensitive_data_allowed
        and not c.memory.expiration_exists,
        evidence=lambda c: (
            f"memory.sensitive_data_allowed={c.memory.sensitive_data_allowed}; "
            f"memory.expiration_exists={c.memory.expiration_exists}"
        ),
    ),
]
