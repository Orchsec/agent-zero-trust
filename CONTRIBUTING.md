# Contributing

Thanks for helping improve `agent-zero-trust`.

## Development Setup

```bash
git clone https://github.com/<your-org>/agent-zero-trust.git
cd agent-zero-trust
python -m pip install -e ".[dev]"
```

## Local Checks

Run these before opening a pull request:

```bash
python -m ruff check .
python -m pytest
```

## Project Scope

The v0.1 priority is a reliable offline CLI:

- YAML and JSON config loading
- deterministic rule evaluation
- scoring and blast-radius calculation
- terminal, Markdown, and JSON reports
- useful examples and docs

The web app is experimental and should not complicate the CLI package.

## Adding Rules

When adding a rule:

1. Add the rule to the appropriate module in `src/agent_zero_trust/rules/`.
2. Include ID, title, category, severity, description, recommendation, predicate, and evidence.
3. Add the rule ID to `tests/test_rule_inventory.py`.
4. Add or update an example config that exercises the rule.
5. Add tests for edge cases if the predicate has branching logic.

## Reporting Bugs

Please include:

- CLI command used
- config file snippet or minimal reproduction
- expected result
- actual result
- Python version and operating system

## Pull Requests

Keep pull requests focused. Avoid unrelated formatting, generated artifacts, or broad refactors.
