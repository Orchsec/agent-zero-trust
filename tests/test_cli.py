from pathlib import Path

from typer.testing import CliRunner

from agent_zero_trust.cli import app

runner = CliRunner()


def test_cli_validate_smoke():
    result = runner.invoke(app, ["validate", "examples/basic-chatbot.yaml"])

    assert result.exit_code == 0
    assert "Valid config" in result.output


def test_cli_markdown_output(tmp_path):
    output = tmp_path / "report.md"

    result = runner.invoke(
        app,
        [
            "scan",
            "examples/sales-email-agent.yaml",
            "--format",
            "markdown",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert Path(output).exists()
    assert "AI Agent Zero Trust Readiness Report" in output.read_text(encoding="utf-8")


def test_cli_json_output(tmp_path):
    output = tmp_path / "report.json"

    result = runner.invoke(
        app,
        [
            "scan",
            "examples/sales-email-agent.yaml",
            "--format",
            "json",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert '"agent_name": "sales-email-agent"' in output.read_text(encoding="utf-8")


def test_cli_init_rules_and_examples(tmp_path):
    starter = tmp_path / "agent-zero-trust.yaml"

    init_result = runner.invoke(app, ["init", "--output", str(starter)])
    rules_result = runner.invoke(app, ["rules"])
    examples_result = runner.invoke(app, ["examples"])

    assert init_result.exit_code == 0
    assert starter.exists()
    assert rules_result.exit_code == 0
    assert "AZT-TOOL-001" in rules_result.output
    assert examples_result.exit_code == 0
    assert "high-risk-agent.yaml" in examples_result.output


def test_cli_invalid_format_fails():
    result = runner.invoke(
        app,
        ["scan", "examples/basic-chatbot.yaml", "--format", "xml"],
    )

    assert result.exit_code == 1
    assert "--format must be one of" in result.output
