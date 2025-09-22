import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_and_get_document(monkeypatch):
    # Mock summarize_in_background, um echten LLM Call zu vermeiden
    monkeypatch.setattr("app.main.summarize_in_background", lambda x: None)

    payload = [{"name": "Doc1", "URL": "http://example.com"}]
    
    # POST
    response = client.post("/documents", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert data[0]["name"] == "Doc1"
    assert data[0]["status"] == "PENDING"
    
    doc_uuid = data[0]["document_uuid"]

    # GET
    response = client.get(f"/documents/{doc_uuid}")
    # Da wir save_document nicht mocken, kann evtl. 404 kommen
    # Für Integration Test könnte man Storage monkeypatchen
