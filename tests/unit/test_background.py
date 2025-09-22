import pytest
from unittest.mock import AsyncMock, patch
from app.main import summarize_in_background, SummarizerDocument, save_document

@pytest.mark.asyncio
async def test_summarize_in_background(monkeypatch):
    doc_uuid = "test-uuid"
    doc = SummarizerDocument(
        document_uuid=doc_uuid,
        status="PENDING",
        name="Test",
        URL="http://example.com",
        summary=None
    )

    # Mock load_document
    monkeypatch.setattr("app.main.load_document", lambda x: doc)

    # Mock save_document um zu prüfen ob aufgerufen
    saved = {}
    def mock_save(d):
        saved.update(d.dict())
    monkeypatch.setattr("app.main.save_document", mock_save)

    # Mock AsyncClient.generate
    mock_response = {"response": "This is a summary."}
    monkeypatch.setattr("app.main.client.generate", AsyncMock(return_value=mock_response))

    await summarize_in_background(doc_uuid)
    
    assert saved["status"] == "SUCCESS"
    assert saved["summary"] == "This is a summary."
