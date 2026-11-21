"""
automationTesting.py
Automated test suite for Notes Management FastAPI application.
Tests all routes, status codes, input validations, and error handling.
Can be executed directly (`python automationTesting.py`) or with pytest (`pytest automationTesting.py`).
"""

import sys
from fastapi.testclient import TestClient
from main import app, reset_db_for_testing

client = TestClient(app)


def setup_function():
    """Reset the database before each test execution."""
    reset_db_for_testing()


# =====================================================================
# Route Test Cases
# =====================================================================

def test_root_endpoint():
    """Verify GET / returns application info and running status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["application"] == "Notes Management API"
    assert data["framework"] == "FastAPI"
    assert data["status"] == "running"
    assert "sapid" in data


def test_health_check_endpoint():
    """Verify GET /health returns 200 with healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_create_note_success():
    """Verify POST /notes successfully creates a new note."""
    payload = {
        "title": "Study Docker & Kubernetes",
        "content": "Prepare containers, compose files, and ingress.",
        "tags": ["devops", "docker"],
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert data["tags"] == payload["tags"]
    assert "created_at" in data
    assert "updated_at" in data


def test_create_note_validation_failure():
    """Verify POST /notes returns 422 Unprocessable Entity when title is missing."""
    invalid_payload = {"content": "Content without title"}
    response = client.post("/notes", json=invalid_payload)
    assert response.status_code == 422


def test_list_notes_empty_and_populated():
    """Verify GET /notes lists all available notes."""
    # Initially empty
    empty_res = client.get("/notes")
    assert empty_res.status_code == 200
    assert empty_res.json() == []

    # Insert two notes
    client.post("/notes", json={"title": "Note 1", "content": "Content 1", "tags": ["personal"]})
    client.post("/notes", json={"title": "Note 2", "content": "Content 2", "tags": ["work"]})

    res = client.get("/notes")
    assert res.status_code == 200
    notes = res.json()
    assert len(notes) == 2
    assert notes[0]["title"] == "Note 1"
    assert notes[1]["title"] == "Note 2"


def test_list_notes_tag_filter():
    """Verify GET /notes?tag=... properly filters notes."""
    client.post("/notes", json={"title": "Work Note", "content": "Work details", "tags": ["work"]})
    client.post("/notes", json={"title": "Home Note", "content": "Home chores", "tags": ["home"]})

    response = client.get("/notes?tag=work")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Work Note"


def test_get_note_by_id_success():
    """Verify GET /notes/{note_id} returns the specific note."""
    create_res = client.post("/notes", json={"title": "Target Note", "content": "Find me", "tags": ["target"]})
    note_id = create_res.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["title"] == "Target Note"


def test_get_note_by_id_not_found():
    """Verify GET /notes/{note_id} returns 404 for non-existent note."""
    response = client.get("/notes/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_note_success():
    """Verify PUT /notes/{note_id} updates specified fields."""
    create_res = client.post("/notes", json={"title": "Draft", "content": "Initial", "tags": ["draft"]})
    note_id = create_res.json()["id"]

    update_payload = {"title": "Finalized Title", "content": "Updated content"}
    response = client.put(f"/notes/{note_id}", json=update_payload)
    assert response.status_code == 200
    updated_note = response.json()
    assert updated_note["title"] == "Finalized Title"
    assert updated_note["content"] == "Updated content"
    assert updated_note["tags"] == ["draft"]  # Untouched


def test_update_note_not_found():
    """Verify PUT /notes/{note_id} returns 404 for non-existent note."""
    response = client.put("/notes/99999", json={"title": "Update non-existent"})
    assert response.status_code == 404


def test_delete_note_success():
    """Verify DELETE /notes/{note_id} removes the note."""
    create_res = client.post("/notes", json={"title": "To Delete", "content": "Will be removed"})
    note_id = create_res.json()["id"]

    del_res = client.delete(f"/notes/{note_id}")
    assert del_res.status_code == 200
    assert del_res.json()["deleted_note_id"] == note_id

    # Verify it is no longer retrievable
    get_res = client.get(f"/notes/{note_id}")
    assert get_res.status_code == 404


def test_delete_note_not_found():
    """Verify DELETE /notes/{note_id} returns 404 for non-existent note."""
    response = client.delete("/notes/99999")
    assert response.status_code == 404


# =====================================================================
# CLI Standalone Execution Runner
# =====================================================================
if __name__ == "__main__":
    tests = [
        test_root_endpoint,
        test_health_check_endpoint,
        test_create_note_success,
        test_create_note_validation_failure,
        test_list_notes_empty_and_populated,
        test_list_notes_tag_filter,
        test_get_note_by_id_success,
        test_get_note_by_id_not_found,
        test_update_note_success,
        test_update_note_not_found,
        test_delete_note_success,
        test_delete_note_not_found,
    ]

    print("=" * 65)
    print("🚀 Running Notes API Automation Route Testing Suite")
    print("=" * 65)

    passed = 0
    failed = 0

    for test in tests:
        setup_function()
        try:
            test()
            print(f" [PASS] {test.__name__}")
            passed += 1
        except Exception as e:
            print(f" [FAIL] {test.__name__}: {e}")
            failed += 1

    print("-" * 65)
    print(f"Test Summary: Total={len(tests)}, Passed={passed}, Failed={failed}")
    print("=" * 65)

    if failed > 0:
        sys.exit(1)
    else:
        print(" All automated tests passed successfully!")
        sys.exit(0)
