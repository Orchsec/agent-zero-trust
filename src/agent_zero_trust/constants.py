"""Shared constants for scoring and reporting."""

CATEGORY_WEIGHTS: dict[str, int] = {
    "identity_authentication": 15,
    "tools_mcp": 15,
    "authorization": 15,
    "logging_traceability": 15,
    "memory_rag": 10,
    "sandboxing": 10,
    "input_output_controls": 8,
    "recovery": 5,
    "governance": 5,
    "supply_chain": 2,
}

SEVERITY_PENALTIES: dict[str, int] = {
    "Critical": 18,
    "High": 10,
    "Medium": 6,
    "Low": 3,
}

SEVERITY_ORDER = ["Critical", "High", "Medium", "Low"]

DISCLAIMER = (
    "This is a self-assessment tool, not a formal audit, certification, "
    "or penetration test."
)
