import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app import create_app
@pytest.fixture()
def app(tmp_path):
    a = create_app({"DATABASE": str(tmp_path / "test.db"), "TESTING": True})
    yield a
@pytest.fixture()
def client(app): return app.test_client()
@pytest.fixture()
def student(client):
    s = {"student_id": "STU001", "name": "Pushkar", "email": "pushkar@example.com", "department": "AIDS", "semester": 2}
    assert client.post("/api/students", json=s).status_code == 201
    return s
@pytest.fixture()
def course(client):
    c = {"course_code": "CS101", "title": "Intro to CS", "credits": 4, "semester": 2}
    assert client.post("/api/courses", json=c).status_code == 201
    return c

