# Validation Targets

These targets are public-profile configs derived from open-source project documentation. They are
useful for validating rule coverage against realistic agent shapes, but they are not formal audits
of any live deployment.

## Real-World Public Profiles

| Target | Why it is useful | Local config |
| --- | --- | --- |
| OpenHands | Coding agent with REST API, local GUI, sandboxed development workflows, hosted/cloud variants, and integrations. | `validation-targets/openhands-public-profile.yaml` |
| Microsoft AutoGen / Magentic-One | Multi-agent framework with web browsing, code execution, and file handling. | `validation-targets/autogen-magentic-one-public-profile.yaml` |
| LangChain Open Agent Platform | Agent builder with tools, RAG, MCP tools, supervisor/multi-agent orchestration, and auth/access control. | `validation-targets/langchain-open-agent-platform-public-profile.yaml` |
| AutoGPT | Autonomous agent pattern with web browsing, file management, API keys, internet access, and memory. | `validation-targets/autogpt-public-profile.yaml` |
| CrewAI | Multi-agent orchestration framework with tool use, memory, and knowledge/RAG workflows. | `validation-targets/crewai-public-profile.yaml` |

## How to Run

```bash
agent-zero-trust scan validation-targets/openhands-public-profile.yaml
agent-zero-trust scan validation-targets/autogen-magentic-one-public-profile.yaml
agent-zero-trust scan validation-targets/langchain-open-agent-platform-public-profile.yaml
agent-zero-trust scan validation-targets/autogpt-public-profile.yaml
agent-zero-trust scan validation-targets/crewai-public-profile.yaml
```

## Interpretation Rules

- Treat these as calibration fixtures, not verdicts on the projects.
- Keep findings tied to the local YAML evidence, not broad claims about the upstream project.
- When validating a real deployment, replace assumptions with observed evidence from IAM, network
  policy, logs, runtime config, secrets management, MCP server manifests, and approval workflows.
