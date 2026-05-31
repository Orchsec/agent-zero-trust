import json

import pytest
from pydantic import ValidationError

from agent_zero_trust.config_schema import AgentConfig
from agent_zero_trust.loader import ConfigLoadError, load_config
from agent_zero_trust.scanner import scan_config


def test_missing_required_agent_section_fails():
    with pytest.raises(ValidationError):
        AgentConfig.model_validate({"project": {"name": "missing-agent"}})


def test_unknown_fields_are_rejected():
    with pytest.raises(ValidationError):
        AgentConfig.model_validate(
            {"agent": {"name": "strict-agent"}, "tools": {"surprise_tool": True}}
        )


def test_invalid_json_fails_clearly(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(ConfigLoadError, match="Invalid .json config"):
        load_config(path)


def test_unsupported_extension_fails(tmp_path):
    path = tmp_path / "agent.txt"
    path.write_text("agent:\n  name: bad", encoding="utf-8")

    with pytest.raises(ConfigLoadError, match="must be YAML"):
        load_config(path)


def test_score_is_deterministic_for_same_input(tmp_path):
    path = tmp_path / "agent.json"
    path.write_text(
        json.dumps(
            {
                "agent": {"name": "deterministic", "environment": "production"},
                "identity": {"unique_identity": False},
            }
        ),
        encoding="utf-8",
    )

    first = scan_config(load_config(path)).model_dump()
    second = scan_config(load_config(path)).model_dump()

    assert first == second
