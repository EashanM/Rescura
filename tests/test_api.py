import pytest
from fastapi.testclient import TestClient
from api.fastapi_app import app

client = TestClient(app)

def test_process_emergency_text(monkeypatch):
    # Mock agents and input processing for fast test
    monkeypatch.setattr("api.fastapi_app.transcriber", lambda: None)
    monkeypatch.setattr("api.fastapi_app.triage_agent", lambda *a, **kw: {"severity": 3, "rationale": "test", "immediate_actions": ["rest"]})
    response = client.post("/process-emergency", files={"audio": ("test.wav", b"audio data")})
    assert response.status_code == 200
    assert "assessment" in response.json()
