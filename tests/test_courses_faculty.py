def test_course_crud(client):
    c = {"course_code": "MA101", "title": "Maths", "credits": 3, "semester": 1}
    assert client.post("/api/courses", json=c).status_code == 201
    assert client.get("/api/courses/MA101").status_code == 200
    c["title"] = "Maths II"
    assert client.put("/api/courses/MA101", json=c).status_code == 200
    assert client.post("/api/courses", json=c).status_code == 409
    bad = dict(c); bad["credits"] = 9
    assert client.put("/api/courses/MA101", json=bad).status_code == 400
    assert client.delete("/api/courses/MA101").status_code == 200
def test_course_invalid(client):
    assert client.post("/api/courses", json={}).status_code == 400
    assert client.post("/api/courses", json={"course_code": "X", "title": "T", "credits": 0, "semester": 1}).status_code == 400
    assert client.get("/api/courses/NOPE").status_code == 404
def test_faculty_crud(client):
    f = {"faculty_id": "F01", "name": "Dr A", "email": "a@uni.edu", "department": "CS"}
    assert client.post("/api/faculty", json=f).status_code == 201
    assert client.get("/api/faculty/F01").status_code == 200
    f["name"] = "Dr B"
    assert client.put("/api/faculty/F01", json=f).status_code == 200
    assert client.post("/api/faculty", json=f).status_code == 409
    bad = dict(f); bad["email"] = "bad"
    assert client.put("/api/faculty/F01", json=bad).status_code == 400
    assert client.delete("/api/faculty/F01").status_code == 200
    assert client.get("/api/faculty/F01").status_code == 404
def test_course_faculty_link(client):
    f = {"faculty_id": "F09", "name": "Dr Z", "email": "z@uni.edu", "department": "CS"}
    assert client.post("/api/faculty", json=f).status_code == 201
    c = {"course_code": "PH101", "title": "Phy", "credits": 4, "semester": 1, "faculty_id": "F09"}
    assert client.post("/api/courses", json=c).status_code == 201
    c2 = {"course_code": "PH102", "title": "Phy2", "credits": 4, "semester": 1, "faculty_id": "GHOST"}
    assert client.post("/api/courses", json=c2).status_code == 404

