"""RAG rules."""

from agent_zero_trust.findings import Rule

RULES = [
    Rule(
        id="AZT-RAG-001",
        title="RAG uses untrusted sources",
        category="rag",
        score_category="memory_rag",
        severity="Medium",
        description=(
            "Untrusted retrieval sources can introduce prompt injection or poisoned content."
        ),
        recommendation="Classify sources, isolate indexes, and filter retrieved content.",
        predicate=lambda c: c.rag.uses_rag and c.rag.untrusted_sources,
        evidence=lambda c: f"rag.untrusted_sources={c.rag.untrusted_sources}",
    ),
    Rule(
        id="AZT-RAG-002",
        title="Document uploads allowed without ingestion validation",
        category="rag",
        score_category="memory_rag",
        severity="High",
        description="Uploaded documents can carry malicious instructions or sensitive content.",
        recommendation="Validate, scan, classify, and sanitize documents before ingestion.",
        predicate=lambda c: c.rag.uses_rag
        and c.rag.document_uploads
        and not c.rag.ingestion_validation,
        evidence=lambda c: (
            f"rag.document_uploads={c.rag.document_uploads}; "
            f"rag.ingestion_validation={c.rag.ingestion_validation}"
        ),
    ),
]
