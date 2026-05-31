"""Identity rules."""

from agent_zero_trust.config_schema import Environment
from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-ID-001",
        title="Unique agent identity missing",
        category="identity",
        score_category="identity_authentication",
        severity="High",
        description="The agent does not have a unique identity for access control and audit.",
        recommendation="Assign a unique identity per agent and environment.",
        predicate=lambda c: not c.identity.unique_identity,
        evidence=lambda c: f"identity.unique_identity={c.identity.unique_identity}",
    ),
    Rule(
        id="AZT-ID-002",
        title="Shared service account in use",
        category="identity",
        score_category="identity_authentication",
        severity="High",
        description="Shared service accounts make attribution and revocation difficult.",
        recommendation="Replace shared accounts with per-agent identities.",
        predicate=lambda c: c.identity.shared_service_account,
        evidence=lambda c: f"identity.shared_service_account={c.identity.shared_service_account}",
    ),
    Rule(
        id="AZT-ID-003",
        title="No cryptographic identity for production",
        category="identity",
        score_category="identity_authentication",
        severity="Medium",
        description="Production agents should use cryptographic identity where possible.",
        recommendation=(
            "Use workload identity, mTLS, signed tokens, or equivalent proof of identity."
        ),
        predicate=lambda c: c.agent.environment == Environment.production
        and not c.identity.cryptographic_identity,
        evidence=lambda c: (
            f"agent.environment={c.agent.environment}; "
            f"identity.cryptographic_identity={c.identity.cryptographic_identity}"
        ),
    ),
]
