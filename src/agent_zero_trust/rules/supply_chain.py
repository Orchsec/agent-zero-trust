"""Supply-chain rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-SC-001",
        title="No AI-BOM",
        category="supply_chain",
        score_category="supply_chain",
        severity="Low",
        description=(
            "The project lacks an inventory of model, tools, datasets, APIs, "
            "and dependencies."
        ),
        recommendation=(
            "Create an AI-BOM covering model, tools, datasets, MCP servers, APIs, "
            "and dependencies."
        ),
        predicate=lambda c: not c.supply_chain.ai_bom_exists,
        evidence=lambda c: f"supply_chain.ai_bom_exists={c.supply_chain.ai_bom_exists}",
    ),
    Rule(
        id="AZT-SC-002",
        title="Model source not verified",
        category="supply_chain",
        score_category="supply_chain",
        severity="Medium",
        description="Model source, provider posture, or update mechanism has not been verified.",
        recommendation="Verify model source, provider security posture, and update mechanism.",
        predicate=lambda c: not c.supply_chain.model_source_verified,
        evidence=lambda c: (
            f"supply_chain.model_source_verified={c.supply_chain.model_source_verified}"
        ),
    ),
]
