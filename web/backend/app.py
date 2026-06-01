"""FastAPI app for the v2 browser assessment experience."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent_zero_trust.config_schema import AgentConfig
from agent_zero_trust.report import render_json_report, render_markdown_report
from agent_zero_trust.scanner import scan_config

app = FastAPI(
    title="agent-zero-trust API",
    version="0.2.0",
    description="Zero Trust readiness scanning API for AI agent assessments.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/scan")
def scan(config: AgentConfig) -> dict:
    return scan_config(config).model_dump()


@app.post("/reports/markdown")
def markdown_report(config: AgentConfig) -> dict[str, str]:
    return {"content": render_markdown_report(scan_config(config))}


@app.post("/reports/json")
def json_report(config: AgentConfig) -> dict[str, str]:
    return {"content": render_json_report(scan_config(config))}
