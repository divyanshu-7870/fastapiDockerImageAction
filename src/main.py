import logging
import time
from fastapi import FastAPI, HTTPException, Request
import uvicorn

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("notes-api")

PORT = 8000
app = FastAPI(title="Notes API")

# In-memory storage for notes
notes = [
    {"id": 1, "title": "Unit 4 Assignment", "content": "Finish FastAPI and Docker setup"},
    {"id": 2, "title": "Revision", "content": "Revise backend theory topics"},
]


# Middleware to log requests and duration
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


@app.get("/")
async def read_root():
    return {"message": "Notes API is running", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/notes")
async def get_all_notes():
    return notes


@app.get("/notes/{note_id}")
async def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.post("/notes")
async def create_note(note: dict):
    new_id = len(notes) + 1 if notes else 1
    new_note = {
        "id": new_id,
        "title": note.get("title", ""),
        "content": note.get("content", ""),
    }
    notes.append(new_note)
    return new_note


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            deleted = notes.pop(i)
            return {"message": "Note deleted", "note": deleted}
    raise HTTPException(status_code=404, detail="Note not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
