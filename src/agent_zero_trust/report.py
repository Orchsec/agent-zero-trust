"""Terminal, Markdown, and JSON report rendering."""

import json
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.table import Table

from agent_zero_trust.constants import CATEGORY_WEIGHTS, DISCLAIMER, SEVERITY_ORDER
from agent_zero_trust.scoring import ScanResult


def render_json_report(result: ScanResult) -> str:
    return json.dumps(result.model_dump(), indent=2)


def render_markdown_report(result: ScanResult) -> str:
    env = Environment(
        loader=PackageLoader("agent_zero_trust", "templates"),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("report.md.j2")
    return template.render(result=result, weights=CATEGORY_WEIGHTS, disclaimer=DISCLAIMER)


def write_report(path: str | Path, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")


def print_terminal_summary(result: ScanResult, console: Console | None = None) -> None:
    console = console or Console()
    console.print("[bold]Agent Zero Trust Readiness Assessment[/bold]\n")
    console.print(f"Agent: [bold]{result.agent_name}[/bold]")
    console.print(f"Environment: {result.environment}\n")
    console.print(f"Overall Score: [bold]{result.score}/100[/bold]")
    console.print(f"Readiness Level: [bold]{result.readiness_level}[/bold]")
    console.print(f"Blast Radius: [bold]{result.blast_radius}[/bold]\n")

    table = Table(title="Findings")
    table.add_column("Severity")
    table.add_column("Count", justify="right")
    for severity in SEVERITY_ORDER:
        table.add_row(severity, str(result.summary.get(severity, 0)))
    console.print(table)

    top_findings = result.findings[:5]
    if top_findings:
        console.print("\n[bold]Top Risks:[/bold]")
        for finding in top_findings:
            console.print(f"  [{finding.severity.upper()}] {finding.title}")

    console.print("\n[bold]Recommended Next Steps:[/bold]")
    for index, finding in enumerate(top_findings, start=1):
        console.print(f"  {index}. {finding.recommendation}")
