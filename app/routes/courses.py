import sqlite3
from flask import Blueprint, jsonify, request
from app.db import get_db, row_to_dict, rows_to_dicts
from app.services.validators import validate_course_payload
courses_bp = Blueprint("courses", __name__)
@courses_bp.post("/api/courses")
def create_course():
    d = request.get_json(silent=True) or {}
    errs = validate_course_payload(d)
    if errs: return jsonify(error="Validation failed.", details=errs), 400
    if d.get("faculty_id"):
        if get_db().execute("SELECT 1 FROM faculty WHERE faculty_id=?", (d["faculty_id"],)).fetchone() is None: return jsonify(error="Faculty not found."), 404
    db = get_db()
    try:
        db.execute("INSERT INTO courses (course_code,title,credits,semester,faculty_id) VALUES (?,?,?,?,?)", (d["course_code"].strip(), d["title"].strip(), int(d["credits"]), int(d["semester"]), d.get("faculty_id")))
        db.commit()
    except sqlite3.IntegrityError: return jsonify(error="Course code already exists."), 409
    return jsonify(row_to_dict(db.execute("SELECT * FROM courses WHERE course_code=?", (d["course_code"].strip(),)).fetchone())), 201
@courses_bp.get("/api/courses")
def list_courses(): return jsonify(rows_to_dicts(get_db().execute("SELECT * FROM courses ORDER BY course_code").fetchall())), 200
@courses_bp.get("/api/courses/<code>")
def get_course(code):
    r = row_to_dict(get_db().execute("SELECT * FROM courses WHERE course_code=?", (code,)).fetchone())
    return (jsonify(r), 200) if r else (jsonify(error="Course not found."), 404)
@courses_bp.put("/api/courses/<code>")
def update_course(code):
    d = request.get_json(silent=True) or {}; d["course_code"] = code
    errs = validate_course_payload(d)
    if errs: return jsonify(error="Validation failed.", details=errs), 400
    db = get_db()
    if db.execute("SELECT 1 FROM courses WHERE course_code=?", (code,)).fetchone() is None: return jsonify(error="Course not found."), 404
    if d.get("faculty_id") and db.execute("SELECT 1 FROM faculty WHERE faculty_id=?", (d["faculty_id"],)).fetchone() is None: return jsonify(error="Faculty not found."), 404
    db.execute("UPDATE courses SET title=?,credits=?,semester=?,faculty_id=? WHERE course_code=?", (d["title"].strip(), int(d["credits"]), int(d["semester"]), d.get("faculty_id"), code))
    db.commit()
    return jsonify(row_to_dict(db.execute("SELECT * FROM courses WHERE course_code=?", (code,)).fetchone())), 200
@courses_bp.delete("/api/courses/<code>")
def delete_course(code):
    db = get_db()
    if db.execute("SELECT 1 FROM courses WHERE course_code=?", (code,)).fetchone() is None: return jsonify(error="Course not found."), 404
    db.execute("DELETE FROM courses WHERE course_code=?", (code,)); db.commit()
    return jsonify(message="Course deleted."), 200

