import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "running"


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_get_notes():
    res = client.get("/notes")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_create_note():
    data = {"title": "Lab Exam", "content": "Revise Docker commands"}
    res = client.post("/notes", json=data)
    assert res.status_code == 200
    assert res.json()["title"] == "Lab Exam"


def test_get_single_note():
    res = client.get("/notes/1")
    assert res.status_code == 200
    assert res.json()["id"] == 1


def test_delete_note():
    res = client.delete("/notes/1")
    assert res.status_code == 200
    assert res.json()["message"] == "Note deleted"


if __name__ == "__main__":
    test_root()
    test_health()
    test_get_notes()
    test_create_note()
    test_get_single_note()
    test_delete_note()
    print("All tests passed successfully!")
