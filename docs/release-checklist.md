# Release Checklist

Use this before publishing a CLI release.

## Preflight

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest
agent-zero-trust --help
agent-zero-trust scan examples/basic-chatbot.yaml
agent-zero-trust scan examples/sales-email-agent.yaml --format markdown --output report.md
agent-zero-trust scan examples/sales-email-agent.yaml --format json --output report.json
```

## Build

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

## GitHub

- Confirm README quick start is accurate.
- Confirm `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md` exist.
- Confirm GitHub Actions pass.
- Create a release tag.

## PyPI

```bash
python -m twine upload dist/*
```

## Post-Release Smoke Test

```bash
python -m pip install agent-zero-trust
agent-zero-trust init
agent-zero-trust scan agent-zero-trust.yaml
```
