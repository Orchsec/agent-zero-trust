import json

from agent_zero_trust.loader import load_config
from agent_zero_trust.report import render_json_report, render_markdown_report
from agent_zero_trust.scanner import scan_config


def test_markdown_report_contains_required_sections():
    result = scan_config(load_config("examples/sales-email-agent.yaml"))

    report = render_markdown_report(result)

    assert "# AI Agent Zero Trust Readiness Report" in report
    assert "## Findings" in report
    assert "## Disclaimer" in report


def test_json_report_is_machine_readable():
    result = scan_config(load_config("examples/sales-email-agent.yaml"))

    payload = json.loads(render_json_report(result))

    assert payload["agent_name"] == "sales-email-agent"
    assert "findings" in payload
