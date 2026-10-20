import sqlite3
from flask import Blueprint, current_app, jsonify, request
from app.db import get_db, row_to_dict, rows_to_dicts
from app.services.validators import validate_enrollment_payload
from app.services.enrollment_service import check_enrollment_rules
from app.services.grading_service import validate_marks
enrollments_bp = Blueprint("enrollments", __name__)
@enrollments_bp.post("/api/enrollments")
def create_enrollment():
    d = request.get_json(silent=True) or {}
    errs = validate_enrollment_payload(d)
    if errs: return jsonify(error="Validation failed.", details=errs), 400
    sid = str(d["student_id"]).strip(); code = str(d["course_code"]).strip(); sem = int(d["semester"])
    st, msg = check_enrollment_rules(sid, code, sem, current_app.config.get("MAX_CREDITS_PER_SEMESTER", 18))
    if st: return jsonify(error=msg), st
    db = get_db()
    try:
        cur = db.execute("INSERT INTO enrollments (student_id,course_code,semester) VALUES (?,?,?)", (sid, code, sem))
        db.commit(); eid = cur.lastrowid
    except sqlite3.IntegrityError: return jsonify(error="Student is already enrolled in this course for the semester."), 409
    return jsonify(row_to_dict(db.execute("SELECT * FROM enrollments WHERE enrollment_id=?", (eid,)).fetchone())), 201
@enrollments_bp.get("/api/students/<sid>/enrollments")
def list_student_enrollments(sid):
    q = "SELECT e.*, c.title, c.credits FROM enrollments e JOIN courses c ON c.course_code=e.course_code WHERE e.student_id=?"
    args = [sid]
    sem = request.args.get("semester")
    if sem is not None:
        try: sem = int(sem)
        except ValueError: return jsonify(error="Invalid semester filter."), 400
        q += " AND e.semester=?"; args.append(sem)
    return jsonify(rows_to_dicts(get_db().execute(q + " ORDER BY e.semester, e.course_code", args).fetchall())), 200
@enrollments_bp.delete("/api/enrollments/<int:eid>")
def delete_enrollment(eid):
    db = get_db()
    if db.execute("SELECT 1 FROM enrollments WHERE enrollment_id=?", (eid,)).fetchone() is None: return jsonify(error="Enrollment not found."), 404
    db.execute("DELETE FROM enrollments WHERE enrollment_id=?", (eid,)); db.commit()
    return jsonify(message="Enrollment deleted."), 200
@enrollments_bp.put("/api/enrollments/<int:eid>/marks")
def record_marks(eid):
    d = request.get_json(silent=True) or {}
    if "marks" not in d: return jsonify(error="marks is required."), 400
    errs = validate_marks(d["marks"])
    if errs: return jsonify(error="Validation failed.", details=errs), 400
    db = get_db()
    if db.execute("SELECT 1 FROM enrollments WHERE enrollment_id=?", (eid,)).fetchone() is None: return jsonify(error="Enrollment not found."), 404
    db.execute("UPDATE enrollments SET marks=? WHERE enrollment_id=?", (float(d["marks"]), eid)); db.commit()
    return jsonify(row_to_dict(db.execute("SELECT * FROM enrollments WHERE enrollment_id=?", (eid,)).fetchone())), 200

