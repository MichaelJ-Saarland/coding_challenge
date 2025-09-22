import os
import uuid
import json
from pathlib import Path
from typing import Optional, List
from ollama import AsyncClient
from pydantic import BaseModel, Field
from fastapi import FastAPI, BackgroundTasks, HTTPException

# Pydantic models
class SummarizerInput(BaseModel):
    name: str = Field(..., example="A name for this document")
    URL: str = Field(..., example="https://some.url/to/an/article")

class SummarizerDocument(BaseModel):
    document_uuid: str = Field(..., example="generated-uuid")
    status: str = Field(..., example="PENDING")
    name: str = Field(..., example="A name for this document")
    URL: str = Field(..., example="https://some.url/to/an/article")
    summary: Optional[str] = None

# FastAPI app
app = FastAPI()

# Storage directory
STORAGE_DIR = Path("storage/fastapi/")
STORAGE_DIR.mkdir(exist_ok=True, parents=True)

# Ollama client
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = AsyncClient(OLLAMA_HOST)

# Helper functions
def check_existing_document(name: str, URL: str):
    for json_file in STORAGE_DIR.glob("*.json"):
        content = json.loads(json_file.read_text())
        doc = SummarizerDocument(**content)
        if doc.name == name and doc.URL == URL:
            return False
        elif doc.name == name or doc.URL == URL:
            return True
    return False

def load_document(doc_uuid: str):
    STORAGE_FILE = STORAGE_DIR / f"{doc_uuid}.json"
    try:
        content = json.loads(STORAGE_FILE.read_text())
    except FileNotFoundError: 
        raise HTTPException(status_code=404, detail="Document does not exist.")
    return SummarizerDocument(**content)

def save_document(doc):
    doc_uuid = doc.document_uuid
    file_path = STORAGE_DIR / f"{doc_uuid}.json"
    file_path.write_text(json.dumps(doc.dict(), indent=2))

async def summarize_in_background(doc_uuid):
    doc = load_document(doc_uuid)

    response = await client.generate(
        model="gemma3:1b",
        prompt=f"Summarize the text from the page {doc.URL} in maximum 1500 characters!"
    )

    if response:
        doc.summary = response['response']
        doc.status = "SUCCESS"
    else:
        doc.summary = None
        doc.status = "FAILED"

    save_document(doc)

# API endpoints
@app.post("/documents", status_code=202, response_model=List[SummarizerDocument])
async def start_summarizer(payload: list[SummarizerInput], background_tasks: BackgroundTasks):
    docs_to_return = []
    for input in payload:
        if check_existing_document(input.name, input.URL):
            raise HTTPException(status_code=409, detail="Document with same name or URL already exists")
        doc = SummarizerDocument(
            document_uuid=str(uuid.uuid4()),
            status="PENDING",
            name=input.name,
            URL=input.URL,
            summary=None
        )
        save_document(doc)
        background_tasks.add_task(summarize_in_background, doc.document_uuid)
        docs_to_return.append(doc)
    return docs_to_return

@app.get("/documents/{doc_uuid}", response_model=SummarizerDocument)
async def summarize_process(doc_uuid: str):
    doc = load_document(doc_uuid)
    return doc
