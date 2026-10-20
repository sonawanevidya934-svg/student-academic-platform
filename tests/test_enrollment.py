def _mk(client, sid, code, cred=4, sem=2):
    client.post("/api/students", json={"student_id": sid, "name": "N", "email": sid.lower()+"@x.com", "department": "CS", "semester": sem})
    client.post("/api/courses", json={"course_code": code, "title": code, "credits": cred, "semester": sem})
def test_enroll_ok(client, student, course):
    r = client.post("/api/enrollments", json={"student_id": "STU001", "course_code": "CS101", "semester": 2})
    assert r.status_code == 201
    assert client.get("/api/students/STU001/enrollments").status_code == 200
def test_duplicate(client, student, course):
    p = {"student_id": "STU001", "course_code": "CS101", "semester": 2}
    assert client.post("/api/enrollments", json=p).status_code == 201
    assert client.post("/api/enrollments", json=p).status_code == 409
def test_credit_limit(client):
    _mk(client, "S90", "C1", 6); _mk(client, "S90X", "C2", 6); _mk(client, "S90Y", "C3", 6); _mk(client, "S90Z", "C4", 6)
    client.post("/api/students", json={"student_id": "S90", "name": "N", "email": "s90@x.com", "department": "CS", "semester": 2})
    for c in ("C1", "C2", "C3"):
        assert client.post("/api/enrollments", json={"student_id": "S90", "course_code": c, "semester": 2}).status_code == 201
    r = client.post("/api/enrollments", json={"student_id": "S90", "course_code": "C4", "semester": 2})
    assert r.status_code == 422
def test_missing_fk(client, student, course):
    assert client.post("/api/enrollments", json={"student_id": "GHOST", "course_code": "CS101", "semester": 2}).status_code == 404
    assert client.post("/api/enrollments", json={"student_id": "STU001", "course_code": "GHOST", "semester": 2}).status_code == 404
    assert client.post("/api/enrollments", json={}).status_code == 400
def test_unenroll(client, student, course):
    eid = client.post("/api/enrollments", json={"student_id": "STU001", "course_code": "CS101", "semester": 2}).get_json()["enrollment_id"]
    assert client.delete(f"/api/enrollments/{eid}").status_code == 200
    assert client.delete("/api/enrollments/99999").status_code == 404

