"""Assessment orchestration."""

from agent_zero_trust.config_schema import AgentConfig
from agent_zero_trust.rules_engine import run_rules
from agent_zero_trust.scoring import (
    ScanResult,
    calculate_blast_radius,
    calculate_category_scores,
    calculate_score,
    readiness_level,
    summarize_findings,
)


def scan_config(config: AgentConfig) -> ScanResult:
    findings = run_rules(config)
    score = calculate_score(findings)
    return ScanResult(
        agent_name=config.agent.name,
        environment=config.agent.environment.value,
        score=score,
        readiness_level=readiness_level(score),
        blast_radius=calculate_blast_radius(config),
        summary=summarize_findings(findings),
        category_scores=calculate_category_scores(findings),
        findings=findings,
    )
