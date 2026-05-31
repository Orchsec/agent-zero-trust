# Real Project Validation: OpenHands

This validation target maps public OpenHands documentation into an `agent-zero-trust` config.
It is a product validation fixture, not a formal security audit of OpenHands.

## Target

- Project: OpenHands
- Config: `validation-targets/openhands-doc-validated.yaml`
- Scenario: self-hosted/local coding-agent usage

## Public Evidence Used

- OpenHands README says the project includes a REST API and single-page React app.
- OpenHands runtime/sandbox docs define the sandbox as where commands are run, files are edited,
  and servers are started.
- OpenHands docs list Docker sandbox as recommended, with process sandbox described as unsafe.
- OpenHands FAQ states code runs in an isolated Docker sandbox but notes potential risks:
  internet access from the container, credentials can be used if provided, mounted files can be
  modified or deleted, and external network requests can be made.

## Mapping Notes

| Schema field | Value | Rationale |
| --- | --- | --- |
| `autonomy_level` | `high` | Coding agent can execute multi-step software tasks. |
| `handles_untrusted_input` | `true` | User tasks, repos, issues, files, and code can be adversarial. |
| `internet_access` | `true` | Docs explicitly mention internet access from the sandbox. |
| `can_execute_code` | `true` | Sandbox exists to run commands/code. |
| `can_call_external_apis` | `true` | Docs mention external network requests and integrations. |
| `sandbox_for_untrusted_input` | `true` | Docker sandbox is recommended for isolation. |
| `egress_controls` | `false` | Public docs confirm internet access, but this fixture does not assume an egress allowlist. |
| `risk_assessment_done` | `false` | No deployment-specific risk assessment evidence in public docs. |
| `ai_bom_exists` | `false` | No deployment-specific AI-BOM evidence in public docs. |

## Run

```bash
agent-zero-trust scan validation-targets/openhands-doc-validated.yaml
```
