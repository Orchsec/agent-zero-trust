"""Score and blast-radius calculations."""

from collections import Counter, defaultdict
from typing import Literal

from pydantic import BaseModel

from agent_zero_trust.config_schema import AgentConfig, Environment
from agent_zero_trust.constants import CATEGORY_WEIGHTS, SEVERITY_ORDER, SEVERITY_PENALTIES
from agent_zero_trust.findings import Finding
from agent_zero_trust.rules_engine import all_rules

BlastRadius = Literal["Low", "Medium", "High", "Critical"]


class ScanResult(BaseModel):
    agent_name: str
    environment: str
    score: int
    readiness_level: str
    blast_radius: BlastRadius
    summary: dict[str, int]
    category_scores: dict[str, int]
    findings: list[Finding]


def readiness_level(score: int) -> str:
    if score >= 90:
        return "Strong"
    if score >= 75:
        return "Good"
    if score >= 60:
        return "Needs improvement"
    if score >= 40:
        return "High risk"
    return "Critical risk"


def calculate_category_scores(findings: list[Finding]) -> dict[str, int]:
    rules_by_id = {rule.id: rule for rule in all_rules()}
    penalties: dict[str, int] = defaultdict(int)
    for finding in findings:
        rule = rules_by_id[finding.id]
        penalties[rule.score_category] += SEVERITY_PENALTIES[finding.severity]

    scores: dict[str, int] = {}
    for category, weight in CATEGORY_WEIGHTS.items():
        score = max(0, weight - penalties[category])
        scores[category] = score
    return scores


def calculate_score(findings: list[Finding]) -> int:
    return sum(calculate_category_scores(findings).values())


def calculate_blast_radius(config: AgentConfig) -> BlastRadius:
    points = 0
    if config.agent.environment == Environment.production:
        points += 3
    if config.agent.handles_customer_data:
        points += 2
    if config.agent.handles_untrusted_input:
        points += 1
    if config.agent.internet_access:
        points += 1
    if config.agent.multi_agent_workflow:
        points += 1
    if config.tools.can_read_database:
        points += 2
    if config.tools.can_write_database:
        points += 2
    if config.tools.can_send_email:
        points += 2
    if config.tools.can_execute_code:
        points += 2
    if config.tools.can_call_external_apis:
        points += 1
    if not config.tools.high_risk_tools_require_approval:
        points += 2

    if points >= 10:
        return "Critical"
    if points >= 7:
        return "High"
    if points >= 4:
        return "Medium"
    return "Low"


def summarize_findings(findings: list[Finding]) -> dict[str, int]:
    counts = Counter(finding.severity for finding in findings)
    return {severity: counts.get(severity, 0) for severity in SEVERITY_ORDER}
