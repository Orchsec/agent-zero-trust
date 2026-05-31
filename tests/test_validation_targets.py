from pathlib import Path

from agent_zero_trust.loader import load_config
from agent_zero_trust.scanner import scan_config


def test_public_validation_targets_scan_successfully():
    target_dir = Path("validation-targets")
    targets = sorted(target_dir.glob("*.yaml"))

    assert len(targets) >= 5

    results = [scan_config(load_config(target)) for target in targets]
    levels = {result.readiness_level for result in results}

    assert "Strong" in levels
    assert "Good" in levels
    assert "Needs improvement" in levels
    assert "Critical risk" in levels
