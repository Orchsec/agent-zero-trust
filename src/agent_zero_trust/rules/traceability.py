"""Traceability rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-TRACE-001",
        title="Request IDs missing",
        category="traceability",
        score_category="logging_traceability",
        severity="High",
        description="Requests cannot be correlated across prompts, tool calls, and outputs.",
        recommendation="Propagate request IDs through all agent actions and logs.",
        predicate=lambda c: not c.traceability.request_ids,
        evidence=lambda c: f"traceability.request_ids={c.traceability.request_ids}",
    ),
    Rule(
        id="AZT-TRACE-002",
        title="Cannot trace user request to agent action",
        category="traceability",
        score_category="logging_traceability",
        severity="High",
        description="The system cannot connect user requests to downstream agent actions.",
        recommendation="Add trace links from user request to planner step, tool call, and output.",
        predicate=lambda c: not c.traceability.trace_user_request_to_agent_action,
        evidence=lambda c: (
            "traceability.trace_user_request_to_agent_action="
            f"{c.traceability.trace_user_request_to_agent_action}"
        ),
    ),
]
