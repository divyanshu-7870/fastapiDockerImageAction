import sys
import os

# Add project root and src to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_create_note():
    payload = {"title": "Lab Exam", "content": "Revise Docker commands"}
    response = client.post("/notes", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Lab Exam"


def test_get_single_note():
    response = client.get("/notes/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_delete_note():
    response = client.delete("/notes/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Note deleted"


if __name__ == "__main__":
    test_root()
    test_health()
    test_get_notes()
    test_create_note()
    test_get_single_note()
    test_delete_note()
    print("All automated tests passed successfully!")
