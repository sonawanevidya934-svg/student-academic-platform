import sqlite3
from flask import Blueprint, jsonify, request
from app.db import get_db, row_to_dict, rows_to_dicts
from app.services.validators import validate_student_payload
students_bp = Blueprint("students", __name__)
@students_bp.post("/api/students")
def create_student():
    d = request.get_json(silent=True) or {}
    errs = validate_student_payload(d)
    if errs: return jsonify(error="Validation failed.", details=errs), 400
    db = get_db()
    try:
        db.execute("INSERT INTO students (student_id,name,email,department,semester) VALUES (?,?,?,?,?)", (d["student_id"].strip(), d["name"].strip(), d["email"].strip(), d["department"].strip(), int(d["semester"])))
        db.commit()
    except sqlite3.IntegrityError: return jsonify(error="Student ID or email already exists."), 409
    return jsonify(db.execute("SELECT * FROM students WHERE student_id=?", (d["student_id"].strip(),)).fetchone() and row_to_dict(db.execute("SELECT * FROM students WHERE student_id=?", (d["student_id"].strip(),)).fetchone())), 201
@students_bp.get("/api/students")
def list_students(): return jsonify(rows_to_dicts(get_db().execute("SELECT * FROM students ORDER BY student_id").fetchall())), 200
@students_bp.get("/api/students/<sid>")
def get_student(sid):
    r = row_to_dict(get_db().execute("SELECT * FROM students WHERE student_id=?", (sid,)).fetchone())
    return (jsonify(r), 200) if r else (jsonify(error="Student not found."), 404)
@students_bp.put("/api/students/<sid>")
def update_student(sid):
    d = request.get_json(silent=True) or {}; d["student_id"] = sid
    errs = validate_student_payload(d)
    if errs: return jsonify(error="Validation failed.", details=errs), 400
    db = get_db()
    if db.execute("SELECT 1 FROM students WHERE student_id=?", (sid,)).fetchone() is None: return jsonify(error="Student not found."), 404
    try:
        db.execute("UPDATE students SET name=?,email=?,department=?,semester=? WHERE student_id=?", (d["name"].strip(), d["email"].strip(), d["department"].strip(), int(d["semester"]), sid))
        db.commit()
    except sqlite3.IntegrityError: return jsonify(error="Email already exists."), 409
    return jsonify(row_to_dict(db.execute("SELECT * FROM students WHERE student_id=?", (sid,)).fetchone())), 200
@students_bp.delete("/api/students/<sid>")
def delete_student(sid):
    db = get_db()
    if db.execute("SELECT 1 FROM students WHERE student_id=?", (sid,)).fetchone() is None: return jsonify(error="Student not found."), 404
    db.execute("DELETE FROM students WHERE student_id=?", (sid,)); db.commit()
    return jsonify(message="Student deleted."), 200

