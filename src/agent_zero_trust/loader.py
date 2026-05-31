"""Config loading for YAML and JSON files."""

import json
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from agent_zero_trust.config_schema import AgentConfig


class ConfigLoadError(Exception):
    """Raised when a config file cannot be read or parsed."""


def load_raw_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigLoadError(f"Config file not found: {config_path}")

    try:
        text = config_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigLoadError(f"Could not read config file: {exc}") from exc

    try:
        if config_path.suffix.lower() == ".json":
            data = json.loads(text)
        elif config_path.suffix.lower() in {".yaml", ".yml"}:
            data = yaml.safe_load(text)
        else:
            raise ConfigLoadError("Config file must be YAML (.yaml/.yml) or JSON (.json)")
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ConfigLoadError(f"Invalid {config_path.suffix.lower()} config: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigLoadError("Config root must be an object")
    return data


def load_config(path: str | Path) -> AgentConfig:
    try:
        return AgentConfig.model_validate(load_raw_config(path))
    except ValidationError:
        raise
