"""Sandboxing rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-SBX-001",
        title="No sandbox for untrusted input",
        category="sandboxing",
        score_category="sandboxing",
        severity="High",
        description="The agent handles untrusted input without sandbox isolation.",
        recommendation="Run risky execution, parsing, and tool use in a constrained sandbox.",
        predicate=lambda c: c.agent.handles_untrusted_input
        and not c.sandboxing.sandbox_for_untrusted_input,
        evidence=lambda c: (
            f"agent.handles_untrusted_input={c.agent.handles_untrusted_input}; "
            f"sandboxing.sandbox_for_untrusted_input={c.sandboxing.sandbox_for_untrusted_input}"
        ),
    )
]
