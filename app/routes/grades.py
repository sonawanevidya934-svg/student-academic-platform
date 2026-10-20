from flask import Blueprint, jsonify, request
from app.db import get_db, row_to_dict, rows_to_dicts
from app.services.grading_service import GRADE_SCALE, compute_gpa, grade_for_marks
grades_bp = Blueprint("grades", __name__)
SCALE_DOC = [{"grade": g, "min": lo, "max": hi, "points": p} for g, lo, hi, p in GRADE_SCALE]
def _rows(sid, sem=None):
    q = "SELECT e.*, c.title, c.credits FROM enrollments e JOIN courses c ON c.course_code=e.course_code WHERE e.student_id=?"
    args = [sid]
    if sem is not None: q += " AND e.semester=?"; args.append(sem)
    return rows_to_dicts(get_db().execute(q + " ORDER BY e.semester, e.course_code", args).fetchall())
@grades_bp.get("/api/grading-scale")
def grading_scale(): return jsonify(scale=SCALE_DOC), 200
@grades_bp.get("/api/students/<sid>/gpa")
def student_gpa(sid):
    if row_to_dict(get_db().execute("SELECT 1 FROM students WHERE student_id=?", (sid,)).fetchone()) is None: return jsonify(error="Student not found."), 404
    sem = request.args.get("semester")
    if sem is not None:
        try: sem = int(sem)
        except ValueError: return jsonify(error="Invalid semester filter."), 400
    rows = _rows(sid, sem)
    out = compute_gpa(rows); out["student_id"] = sid; out["semester"] = sem
    return jsonify(out), 200
@grades_bp.get("/api/students/<sid>/transcript")
def transcript(sid):
    s = row_to_dict(get_db().execute("SELECT * FROM students WHERE student_id=?", (sid,)).fetchone())
    if s is None: return jsonify(error="Student not found."), 404
    rows = _rows(sid)
    for r in rows:
        g, p = grade_for_marks(r.get("marks"))
        r["grade"] = g; r["grade_points"] = p
    out = compute_gpa(rows)
    return jsonify(student=s, records=rows, gpa=out["gpa"], total_credits=out["total_credits"], graded_credits=out["graded_credits"], scale=SCALE_DOC), 200

