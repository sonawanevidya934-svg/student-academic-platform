from app.db import get_db
from app.services.validators import validate_enrollment_payload
DUPLICATE_MSG = "Student is already enrolled in this course for the semester."
CREDIT_MSG = "Enrollment would exceed the maximum of 18 credits for the semester."
def current_semester_credits(sid, sem):
    db = get_db()
    r = db.execute("SELECT COALESCE(SUM(c.credits),0) AS t FROM enrollments e JOIN courses c ON c.course_code=e.course_code WHERE e.student_id=? AND e.semester=?", (sid, sem)).fetchone()
    return int(r["t"] or 0)
def check_enrollment_rules(sid, code, sem, maxc=18):
    db = get_db()
    if db.execute("SELECT 1 FROM students WHERE student_id=?", (sid,)).fetchone() is None: return (404, "Student not found.")
    crs = db.execute("SELECT * FROM courses WHERE course_code=?", (code,)).fetchone()
    if crs is None: return (404, "Course not found.")
    if db.execute("SELECT 1 FROM enrollments WHERE student_id=? AND course_code=? AND semester=?", (sid, code, sem)).fetchone() is not None: return (409, DUPLICATE_MSG)
    if current_semester_credits(sid, sem) + int(crs["credits"]) > maxc: return (422, CREDIT_MSG)
    return (None, None)

