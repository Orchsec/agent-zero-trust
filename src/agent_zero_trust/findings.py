"""Finding and rule definitions."""

from collections.abc import Callable
from dataclasses import dataclass

from pydantic import BaseModel

from agent_zero_trust.config_schema import AgentConfig


class Finding(BaseModel):
    id: str
    title: str
    category: str
    severity: str
    description: str
    recommendation: str
    evidence: str


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    category: str
    score_category: str
    severity: str
    description: str
    recommendation: str
    predicate: Callable[[AgentConfig], bool]
    evidence: Callable[[AgentConfig], str]

    def evaluate(self, config: AgentConfig) -> Finding | None:
        if not self.predicate(config):
            return None
        return Finding(
            id=self.id,
            title=self.title,
            category=self.category,
            severity=self.severity,
            description=self.description,
            recommendation=self.recommendation,
            evidence=self.evidence(config),
        )
