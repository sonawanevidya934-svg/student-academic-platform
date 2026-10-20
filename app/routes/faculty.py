import sqlite3
from flask import Blueprint, jsonify, request
from app.db import get_db, row_to_dict, rows_to_dicts
from app.services.validators import validate_faculty_payload
faculty_bp = Blueprint("faculty", __name__)
@faculty_bp.post("/api/faculty")
def create_faculty():
    d = request.get_json(silent=True) or {}
    errs = validate_faculty_payload(d)
    if errs: return jsonify(error="Validation failed.", details=errs), 400
    db = get_db()
    try:
        db.execute("INSERT INTO faculty (faculty_id,name,email,department) VALUES (?,?,?,?)", (d["faculty_id"].strip(), d["name"].strip(), d["email"].strip(), d["department"].strip()))
        db.commit()
    except sqlite3.IntegrityError: return jsonify(error="Faculty ID or email already exists."), 409
    return jsonify(row_to_dict(db.execute("SELECT * FROM faculty WHERE faculty_id=?", (d["faculty_id"].strip(),)).fetchone())), 201
@faculty_bp.get("/api/faculty")
def list_faculty(): return jsonify(rows_to_dicts(get_db().execute("SELECT * FROM faculty ORDER BY faculty_id").fetchall())), 200
@faculty_bp.get("/api/faculty/<fid>")
def get_faculty(fid):
    r = row_to_dict(get_db().execute("SELECT * FROM faculty WHERE faculty_id=?", (fid,)).fetchone())
    return (jsonify(r), 200) if r else (jsonify(error="Faculty not found."), 404)
@faculty_bp.put("/api/faculty/<fid>")
def update_faculty(fid):
    d = request.get_json(silent=True) or {}; d["faculty_id"] = fid
    errs = validate_faculty_payload(d)
    if errs: return jsonify(error="Validation failed.", details=errs), 400
    db = get_db()
    if db.execute("SELECT 1 FROM faculty WHERE faculty_id=?", (fid,)).fetchone() is None: return jsonify(error="Faculty not found."), 404
    try:
        db.execute("UPDATE faculty SET name=?,email=?,department=? WHERE faculty_id=?", (d["name"].strip(), d["email"].strip(), d["department"].strip(), fid))
        db.commit()
    except sqlite3.IntegrityError: return jsonify(error="Email already exists."), 409
    return jsonify(row_to_dict(db.execute("SELECT * FROM faculty WHERE faculty_id=?", (fid,)).fetchone())), 200
@faculty_bp.delete("/api/faculty/<fid>")
def delete_faculty(fid):
    db = get_db()
    if db.execute("SELECT 1 FROM faculty WHERE faculty_id=?", (fid,)).fetchone() is None: return jsonify(error="Faculty not found."), 404
    db.execute("DELETE FROM faculty WHERE faculty_id=?", (fid,)); db.commit()
    return jsonify(message="Faculty deleted."), 200

