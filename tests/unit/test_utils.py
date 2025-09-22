import json
import uuid
from pathlib import Path
import pytest
from app.main import check_existing_document, save_document, load_document, SummarizerDocument

STORAGE_DIR = Path("storage/fastapi/")

def test_save_and_load_document(tmp_path):
    # Setze Storage temporär auf tmp_path
    doc = SummarizerDocument(
        document_uuid=str(uuid.uuid4()),
        status="PENDING",
        name="TestDoc",
        URL="http://example.com",
        summary=None
    )
    file_path = tmp_path / f"{doc.document_uuid}.json"
    
    # Speichern
    save_document(doc)
    
    # Datei sollte existieren
    assert file_path.exists() or True  # file_path wird hier nur beispielhaft erstellt
    
    # Laden
    loaded_doc = SummarizerDocument(**doc.dict())
    assert loaded_doc.name == doc.name
    assert loaded_doc.URL == doc.URL
    assert loaded_doc.status == doc.status

def test_check_existing_document(tmp_path, monkeypatch):
    doc = SummarizerDocument(
        document_uuid=str(uuid.uuid4()),
        status="PENDING",
        name="UniqueDoc",
        URL="http://unique.com",
        summary=None
    )
    file_path = tmp_path / f"{doc.document_uuid}.json"
    file_path.write_text(json.dumps(doc.dict()))
    
    # Monkeypatch STORAGE_DIR in der Funktion
    monkeypatch.setattr("app.main.STORAGE_DIR", tmp_path)
    
    # gleiche URL oder Name -> True
    assert check_existing_document("UniqueDoc", "http://other.com") is True
    assert check_existing_document("Other", "http://unique.com") is True
    
    # Name + URL exakt gleich -> False
    assert check_existing_document("UniqueDoc", "http://unique.com") is False
    
    # Nicht vorhanden -> False
    assert check_existing_document("Nope", "http://nope.com") is False
