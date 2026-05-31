import json

import pytest

from agent_zero_trust.loader import ConfigLoadError, load_config


def test_load_yaml_config():
    config = load_config("examples/basic-chatbot.yaml")

    assert config.agent.name == "basic-chatbot"


def test_load_json_config(tmp_path):
    path = tmp_path / "agent.json"
    path.write_text(
        json.dumps({"agent": {"name": "json-agent", "environment": "staging"}}),
        encoding="utf-8",
    )

    config = load_config(path)

    assert config.agent.name == "json-agent"
    assert config.agent.environment == "staging"


def test_invalid_yaml_returns_clear_error(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("agent: [", encoding="utf-8")

    with pytest.raises(ConfigLoadError, match="Invalid .yaml config"):
        load_config(path)
