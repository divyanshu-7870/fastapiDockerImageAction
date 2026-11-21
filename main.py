import logging
import time
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

# --------------------------------------------------
# Structured Logging Setup (as per lecture unit 4)
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("notes-api")

app = FastAPI(title="Notes API")

# Simple in-memory list of notes
notes = [
    {"id": 1, "title": "First Note", "content": "Welcome to my Notes API"},
    {"id": 2, "title": "College Task", "content": "Complete Backend Unit 4 PBL"},
]


class Note(BaseModel):
    title: str
    content: str


# --------------------------------------------------
# Monitoring Middleware: Logs method, path, status, duration
# --------------------------------------------------
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


# --------------------------------------------------
# Endpoints
# --------------------------------------------------
@app.get("/")
def root():
    return {
        "application": "Notes API",
        "framework": "FastAPI",
        "status": "running",
        "sapid": "YOUR_SAP_ID",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/notes")
def get_all_notes():
    return notes


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.post("/notes")
def create_note(note: Note):
    new_id = len(notes) + 1 if notes else 1
    new_note = {"id": new_id, "title": note.title, "content": note.content}
    notes.append(new_note)
    return new_note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            deleted = notes.pop(i)
            return {"message": "Note deleted", "note": deleted}
    raise HTTPException(status_code=404, detail="Note not found")
