from app.models.student import Student
from app.services.student_service import validate_student


def test_valid_student():
    student = Student(
        student_id="STU001",
        name="Pushkar",
        email="pushkar@example.com",
        department="AIDS",
        semester=2,
    )

    assert validate_student(student) == []
