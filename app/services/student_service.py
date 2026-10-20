import re
from app.models.student import Student


def validate_student(student: Student) -> list[str]:
    errors = []

    if not student.student_id.strip():
        errors.append("Student ID is required.")

    if not student.name.strip():
        errors.append("Student name is required.")

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", student.email):
        errors.append("A valid email address is required.")

    if not student.department.strip():
        errors.append("Department is required.")

    if not 1 <= student.semester <= 8:
        errors.append("Semester must be between 1 and 8.")

    return errors
