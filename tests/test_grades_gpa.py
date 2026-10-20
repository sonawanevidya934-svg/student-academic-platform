from app.services.grading_service import compute_gpa, grade_for_marks, validate_marks
def test_scale():
    assert grade_for_marks(95) == ("O", 10)
    assert grade_for_marks(85) == ("A+", 9)
    assert grade_for_marks(75) == ("A", 8)
    assert grade_for_marks(65) == ("B+", 7)
    assert grade_for_marks(55) == ("B", 6)
    assert grade_for_marks(45) == ("C", 5)
    assert grade_for_marks(20) == ("F", 0)
    assert validate_marks(101) != [] and validate_marks(-1) != [] and validate_marks("x") != []
def test_gpa_math():
    rows = [{"credits": 4, "marks": 95}, {"credits": 4, "marks": 75}]
    assert compute_gpa(rows)["gpa"] == 9.0
    assert compute_gpa([{"credits": 3, "marks": None}])["gpa"] is None
def test_marks_api(client, student, course):
    eid = client.post("/api/enrollments", json={"student_id": "STU001", "course_code": "CS101", "semester": 2}).get_json()["enrollment_id"]
    assert client.put(f"/api/enrollments/{eid}/marks", json={"marks": 92}).status_code == 200
    assert client.put(f"/api/enrollments/{eid}/marks", json={"marks": 150}).status_code == 400
    assert client.put("/api/enrollments/99999/marks", json={"marks": 80}).status_code == 404
    g = client.get("/api/students/STU001/gpa").get_json()
    assert g["gpa"] == 10.0 and g["graded_credits"] == 4
    t = client.get("/api/students/STU001/transcript").get_json()
    assert t["records"][0]["grade"] == "O" and t["gpa"] == 10.0
    assert client.get("/api/grading-scale").status_code == 200
def test_gpa_missing(client):
    assert client.get("/api/students/NOPE/gpa").status_code == 404
    assert client.get("/api/students/NOPE/transcript").status_code == 404

