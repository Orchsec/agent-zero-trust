"""Input and output control rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-IO-001",
        title="Internet access without egress controls",
        category="input_output_controls",
        score_category="input_output_controls",
        severity="High",
        description="Unrestricted egress can leak data or enable unsafe external actions.",
        recommendation="Restrict outbound network access by domain, protocol, and purpose.",
        predicate=lambda c: c.agent.internet_access and not c.input_output_controls.egress_controls,
        evidence=lambda c: (
            f"agent.internet_access={c.agent.internet_access}; "
            f"input_output_controls.egress_controls={c.input_output_controls.egress_controls}"
        ),
    ),
    Rule(
        id="AZT-IO-002",
        title="No prompt injection filtering",
        category="input_output_controls",
        score_category="input_output_controls",
        severity="Medium",
        description="The agent lacks controls for prompt injection attempts.",
        recommendation="Filter and segment untrusted instructions before model/tool use.",
        predicate=lambda c: c.agent.handles_untrusted_input
        and not c.input_output_controls.prompt_injection_filtering,
        evidence=lambda c: (
            "input_output_controls.prompt_injection_filtering="
            f"{c.input_output_controls.prompt_injection_filtering}"
        ),
    ),
    Rule(
        id="AZT-IO-003",
        title="No output filtering for customer data",
        category="input_output_controls",
        score_category="input_output_controls",
        severity="High",
        description="Customer data can leave the system without output filtering.",
        recommendation="Filter, classify, and redact outputs before external delivery.",
        predicate=lambda c: c.agent.handles_customer_data
        and not c.input_output_controls.output_filtering_customer_data,
        evidence=lambda c: (
            "input_output_controls.output_filtering_customer_data="
            f"{c.input_output_controls.output_filtering_customer_data}"
        ),
    ),
]
