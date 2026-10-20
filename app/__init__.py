from flask import Flask, jsonify
from app.config import Config
from app.db import close_db, init_db
from app.routes import courses_bp, enrollments_bp, faculty_bp, grades_bp, health_bp, students_bp
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config: app.config.update(test_config)
    init_db(app)
    app.teardown_appcontext(close_db)
    @app.route("/")
    def home(): return {"project": "Student Academic Platform", "status": "running", "message": "Welcome to the Student Academic Platform"}
    for bp in (health_bp, students_bp, courses_bp, faculty_bp, enrollments_bp, grades_bp): app.register_blueprint(bp)
    @app.errorhandler(404)
    def nf(_e): return jsonify(error="Not found."), 404
    @app.errorhandler(405)
    def mm(_e): return jsonify(error="Method not allowed."), 405
    return app

