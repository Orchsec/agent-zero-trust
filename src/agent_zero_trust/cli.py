"""Command line interface for agent-zero-trust."""

from importlib.resources import files
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from agent_zero_trust.loader import ConfigLoadError, load_config
from agent_zero_trust.report import (
    print_terminal_summary,
    render_json_report,
    render_markdown_report,
    write_report,
)
from agent_zero_trust.rules_engine import all_rules
from agent_zero_trust.scanner import scan_config

app = typer.Typer(help="Zero Trust readiness checker for AI agents.")
console = Console()


def _fail(message: str) -> None:
    console.print(f"[red]Error:[/red] {message}")
    raise typer.Exit(1)


@app.command()
def init(
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Path for the generated starter config."),
    ] = Path("agent-zero-trust.yaml"),
) -> None:
    """Create a starter YAML config."""
    template = files("agent_zero_trust").joinpath("examples/basic-chatbot.yaml")
    if not template.is_file():
        _fail("Starter example is missing from the package.")
    output.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    console.print(f"Wrote starter config to [bold]{output}[/bold]")


@app.command()
def validate(config_file: Path) -> None:
    """Validate a YAML or JSON config."""
    try:
        config = load_config(config_file)
    except ConfigLoadError as exc:
        _fail(str(exc))
    except ValidationError as exc:
        _fail(str(exc))
    console.print(f"[green]Valid config:[/green] {config.agent.name}")


@app.command()
def scan(
    config_file: Path,
    output_format: Annotated[
        str,
        typer.Option("--format", "-f", help="Output format: terminal, markdown, json."),
    ] = "terminal",
    output: Annotated[Path | None, typer.Option("--output", "-o")] = None,
) -> None:
    """Scan a config and print or export a report."""
    try:
        result = scan_config(load_config(config_file))
    except ConfigLoadError as exc:
        _fail(str(exc))
    except ValidationError as exc:
        _fail(str(exc))

    if output_format == "terminal":
        print_terminal_summary(result, console)
        return
    if output_format == "markdown":
        content = render_markdown_report(result)
    elif output_format == "json":
        content = render_json_report(result)
    else:
        _fail("--format must be one of: terminal, markdown, json")

    if output:
        write_report(output, content)
        console.print(f"Wrote {output_format} report to [bold]{output}[/bold]")
    else:
        console.print(content)


@app.command("rules")
def list_rules() -> None:
    """List built-in rules."""
    table = Table(title="Agent Zero Trust Rules")
    table.add_column("ID")
    table.add_column("Severity")
    table.add_column("Category")
    table.add_column("Title")
    for rule in all_rules():
        table.add_row(rule.id, rule.severity, rule.category, rule.title)
    console.print(table)


@app.command("examples")
def list_examples() -> None:
    """List bundled example configs."""
    examples_dir = files("agent_zero_trust").joinpath("examples")
    for path in sorted(examples_dir.iterdir(), key=lambda item: item.name):
        if path.suffix != ".yaml":
            continue
        console.print(path.name)
