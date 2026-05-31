import pytest
from pydantic import ValidationError

from agent_zero_trust.config_schema import AgentConfig


def test_missing_optional_fields_use_defaults():
    config = AgentConfig.model_validate({"agent": {"name": "minimal"}})

    assert config.agent.environment == "development"
    assert config.tools.high_risk_tools_require_approval is True


def test_environment_must_be_known():
    with pytest.raises(ValidationError):
        AgentConfig.model_validate({"agent": {"name": "bad", "environment": "prod"}})


def test_autonomy_level_must_be_known():
    with pytest.raises(ValidationError):
        AgentConfig.model_validate({"agent": {"name": "bad", "autonomy_level": "root"}})


def test_boolean_fields_must_be_booleans():
    with pytest.raises(ValidationError):
        AgentConfig.model_validate(
            {"agent": {"name": "bad", "handles_customer_data": "yes"}}
        )
