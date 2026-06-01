from fastapi.testclient import TestClient

from web.backend.app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_scan_endpoint_returns_findings():
    response = client.post(
        "/scan",
        json={
            "agent": {
                "name": "web-agent",
                "environment": "production",
                "autonomy_level": "high",
                "handles_customer_data": True,
                "handles_untrusted_input": True,
                "internet_access": True,
            },
            "tools": {
                "uses_tools": True,
                "can_read_database": True,
                "can_send_email": True,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["agent_name"] == "web-agent"
    assert payload["blast_radius"] in {"High", "Critical"}
    assert any(finding["id"] == "AZT-TOOL-001" for finding in payload["findings"])


def test_scan_endpoint_rejects_invalid_payload():
    response = client.post(
        "/scan",
        json={"agent": {"name": "bad", "environment": "production", "internet_access": "yes"}},
    )

    assert response.status_code == 422


def test_report_export_endpoints():
    config = {
        "agent": {"name": "web-agent", "environment": "production"},
        "identity": {"unique_identity": False},
    }

    markdown = client.post("/reports/markdown", json=config)
    json_report = client.post("/reports/json", json=config)

    assert markdown.status_code == 200
    assert "# AI Agent Zero Trust Readiness Report" in markdown.json()["content"]
    assert json_report.status_code == 200
    assert '"agent_name": "web-agent"' in json_report.json()["content"]
