"""Authentication and credential rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-AUTH-001",
        title="Static API keys used",
        category="authentication",
        score_category="identity_authentication",
        severity="High",
        description=(
            "Static API keys increase exposure if leaked or copied into prompts, "
            "logs, or memory."
        ),
        recommendation="Use short-lived scoped tokens or workload identity.",
        predicate=lambda c: c.authentication.static_api_keys,
        evidence=lambda c: f"authentication.static_api_keys={c.authentication.static_api_keys}",
    ),
    Rule(
        id="AZT-AUTH-002",
        title="Token lifetime too long",
        category="authentication",
        score_category="identity_authentication",
        severity="Medium",
        description="Long-lived tokens expand the window for abuse.",
        recommendation="Use short-lived scoped credentials and rotate them automatically.",
        predicate=lambda c: (not c.authentication.short_lived_tokens)
        or c.authentication.token_lifetime_minutes > 60,
        evidence=lambda c: (
            f"authentication.short_lived_tokens={c.authentication.short_lived_tokens}; "
            f"authentication.token_lifetime_minutes={c.authentication.token_lifetime_minutes}"
        ),
    ),
    Rule(
        id="AZT-AUTH-003",
        title="No credential revocation",
        category="authentication",
        score_category="identity_authentication",
        severity="High",
        description="Credentials cannot be revoked quickly during compromise or misuse.",
        recommendation="Add a tested credential revocation path.",
        predicate=lambda c: not c.authentication.credential_revocation_exists,
        evidence=lambda c: (
            "authentication.credential_revocation_exists="
            f"{c.authentication.credential_revocation_exists}"
        ),
    ),
]
