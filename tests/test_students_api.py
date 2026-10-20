def _s(n="STU100"): return {"student_id": n, "name": "A", "email": n.lower()+"@x.com", "department": "AIDS", "semester": 2}
def test_crud(client):
    assert client.post("/api/students", json=_s()).status_code == 201
    assert client.get("/api/students/STU100").status_code == 200
    u = _s(); u["name"] = "B"
    assert client.put("/api/students/STU100", json=u).status_code == 200
    assert client.get("/api/students").status_code == 200
    assert client.delete("/api/students/STU100").status_code == 200
    assert client.get("/api/students/STU100").status_code == 404
def test_invalid(client):
    bad = _s(); bad["email"] = "nope"
    assert client.post("/api/students", json=bad).status_code == 400
    bad2 = _s("STU101"); bad2["semester"] = 9
    assert client.post("/api/students", json=bad2).status_code == 400
    assert client.post("/api/students", json={}).status_code == 400
def test_duplicate(client):
    assert client.post("/api/students", json=_s("STU102")).status_code == 201
    assert client.post("/api/students", json=_s("STU102")).status_code == 409
    other = _s("STU103"); other["email"] = "stu102@x.com"
    assert client.post("/api/students", json=other).status_code == 409
def test_missing_404(client):
    assert client.get("/api/students/NOPE").status_code == 404
    assert client.delete("/api/students/NOPE").status_code == 404

