import re
EMAIL_RE = "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"
def _req(v): return v is not None and str(v).strip() != ""
def _email(v): return bool(re.match(EMAIL_RE, str(v or "")))
def validate_student_payload(d):
    e = []
    if not _req(d.get("student_id")): e.append("Student ID is required.")
    if not _req(d.get("name")): e.append("Student name is required.")
    if not _email(d.get("email")): e.append("A valid email address is required.")
    if not _req(d.get("department")): e.append("Department is required.")
    try:
        s = int(d.get("semester"))
        if not 1 <= s <= 8: e.append("Semester must be between 1 and 8.")
    except (TypeError, ValueError): e.append("Semester must be between 1 and 8.")
    return e
def validate_course_payload(d):
    e = []
    if not _req(d.get("course_code")): e.append("Course code is required.")
    if not _req(d.get("title")): e.append("Course title is required.")
    try:
        c = int(d.get("credits"))
        if not 1 <= c <= 6: e.append("Credits must be between 1 and 6.")
    except (TypeError, ValueError): e.append("Credits must be between 1 and 6.")
    try:
        s = int(d.get("semester"))
        if not 1 <= s <= 8: e.append("Semester must be between 1 and 8.")
    except (TypeError, ValueError): e.append("Semester must be between 1 and 8.")
    return e
def validate_faculty_payload(d):
    e = []
    if not _req(d.get("faculty_id")): e.append("Faculty ID is required.")
    if not _req(d.get("name")): e.append("Faculty name is required.")
    if not _email(d.get("email")): e.append("A valid email address is required.")
    if not _req(d.get("department")): e.append("Department is required.")
    return e
def validate_enrollment_payload(d):
    e = []
    if not _req(d.get("student_id")): e.append("student_id is required.")
    if not _req(d.get("course_code")): e.append("course_code is required.")
    try:
        s = int(d.get("semester"))
        if not 1 <= s <= 8: e.append("Semester must be between 1 and 8.")
    except (TypeError, ValueError): e.append("Semester must be between 1 and 8.")
    return e

