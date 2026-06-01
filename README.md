# agent-zero-trust

Open-source Zero Trust readiness checker and blast-radius calculator for AI agents.

`agent-zero-trust` is CLI-first, offline, deterministic, and designed for pre-production
self-assessment.

## Why this exists

AI agents can use tools, access APIs, persist memory, call external services, and perform
multi-step actions. Traditional AppSec checklists do not fully capture these risks.

`agent-zero-trust` helps teams identify security gaps before production.

## Install

```bash
pip install agent-zero-trust
```

For local development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```bash
agent-zero-trust init
agent-zero-trust scan agent-zero-trust.yaml
```

Export reports:

```bash
agent-zero-trust scan examples/sales-email-agent.yaml --format markdown --output report.md
agent-zero-trust scan examples/sales-email-agent.yaml --format json --output report.json
```

## What It Checks

- Agent identity and credential posture
- Short-lived credentials and revocation
- Tool permissions and high-risk tool chaining
- MCP server review status
- Least agency and deny-by-default authorization
- Memory, RAG, and ingestion controls
- Logging and traceability
- Sandboxing and egress controls
- Recovery, governance, and supply-chain readiness

## Example Output

```text
Agent Zero Trust Readiness Assessment

Agent: sales-email-agent
Environment: production

Overall Score: 37/100
Readiness Level: Critical risk
Blast Radius: Critical

      Findings
+------------------+
| Severity | Count |
|----------+-------|
| Critical |     1 |
| High     |    13 |
| Medium   |     4 |
| Low      |     0 |
+------------------+

Top Risks:
  [CRITICAL] Agent can read database and send email
  [HIGH] Static API keys used
  [HIGH] No credential revocation
  [HIGH] No incident response plan
  [HIGH] No human owner

Recommended Next Steps:
  1. Add approval gates, output filtering, and scoped tool permissions.
  2. Use short-lived scoped tokens or workload identity.
  3. Add a tested credential revocation path.
  4. Create an incident response process for agent-specific failure modes.
  5. Assign a human owner accountable for the agent.
```

## Example Config

```yaml
agent:
  name: sales-email-agent
  environment: production
  autonomy_level: high
  handles_customer_data: true
  handles_untrusted_input: true
  internet_access: true
tools:
  uses_tools: true
  can_read_database: true
  can_send_email: true
  high_risk_tools_require_approval: false
identity:
  unique_identity: false
authentication:
  static_api_keys: true
```

## Commands

```bash
agent-zero-trust init
agent-zero-trust validate <config-file>
agent-zero-trust scan <config-file>
agent-zero-trust scan <config-file> --format markdown --output report.md
agent-zero-trust scan <config-file> --format json --output report.json
agent-zero-trust rules
agent-zero-trust examples
```

## Open Source Development

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/release-checklist.md](docs/release-checklist.md).

## Version 2 Web App

The v2 branch includes an experimental local web app for browser-based assessments.

```bash
python -m pip install -e ".[web,dev]"
python -m uvicorn web.backend.app:app --reload --host 127.0.0.1 --port 8000

cd web/frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

## Disclaimer

This tool is a self-assessment aid, not a formal audit, certification, or penetration test.
