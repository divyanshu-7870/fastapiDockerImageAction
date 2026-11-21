import logging
import time
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("notes-api")

app = FastAPI(
    title="Notes Management API",
    description="Backend API with CRUD, structured logging, health checks, and CI/CD readiness.",
    version="1.0.0",
)

# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------
class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    content: str = Field(..., min_length=1)
    tags: Optional[List[str]] = Field(default_factory=list)


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    content: Optional[str] = Field(None, min_length=1)
    tags: Optional[List[str]] = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: str
    updated_at: str


# ---------------------------------------------------------
# In-Memory Database & State
# ---------------------------------------------------------
notes_db: dict[int, dict] = {}
id_counter = 1


def reset_db_for_testing():
    """Helper to reset database state during testing."""
    global notes_db, id_counter
    notes_db = {}
    id_counter = 1


# ---------------------------------------------------------
# Structured Request Logging Middleware
# ---------------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    try:
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
    except Exception:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.exception(
            "method=%s path=%s status=500 duration_ms=%.2f",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise


# ---------------------------------------------------------
# Core Endpoints
# ---------------------------------------------------------
@app.get("/", tags=["Info"])
def root():
    return {
        "application": "Notes Management API",
        "framework": "FastAPI",
        "status": "running",
        "version": "1.0.0",
        "sapid": "YOUR_SAP_ID",
    }


@app.get("/health", tags=["Monitoring"])
def health():
    return {"status": "healthy"}


@app.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_note(payload: NoteCreate):
    global id_counter
    now = datetime.now(timezone.utc).isoformat()
    note = {
        "id": id_counter,
        "title": payload.title,
        "content": payload.content,
        "tags": payload.tags or [],
        "created_at": now,
        "updated_at": now,
    }
    notes_db[id_counter] = note
    id_counter += 1
    return note


@app.get("/notes", response_model=List[NoteResponse], tags=["Notes"])
def list_notes(tag: Optional[str] = None):
    all_notes = list(notes_db.values())
    if tag:
        return [note for note in all_notes if tag.lower() in [t.lower() for t in note["tags"]]]
    return all_notes


@app.get("/notes/{note_id}", response_model=NoteResponse, tags=["Notes"])
def get_note(note_id: int):
    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found",
        )
    return notes_db[note_id]


@app.put("/notes/{note_id}", response_model=NoteResponse, tags=["Notes"])
def update_note(note_id: int, payload: NoteUpdate):
    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found",
        )
    note = notes_db[note_id]
    if payload.title is not None:
        note["title"] = payload.title
    if payload.content is not None:
        note["content"] = payload.content
    if payload.tags is not None:
        note["tags"] = payload.tags
    note["updated_at"] = datetime.now(timezone.utc).isoformat()
    return note


@app.delete("/notes/{note_id}", status_code=status.HTTP_200_OK, tags=["Notes"])
def delete_note(note_id: int):
    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found",
        )
    deleted = notes_db.pop(note_id)
    return {"message": "Note deleted successfully", "deleted_note_id": deleted["id"]}
