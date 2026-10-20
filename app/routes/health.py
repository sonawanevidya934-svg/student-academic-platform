from flask import Blueprint, jsonify
health_bp = Blueprint("health", __name__)
@health_bp.get("/health")
def health(): return jsonify(status="healthy"), 200
@health_bp.get("/api/health")
def api_health(): return jsonify(status="healthy", service="student-academic-platform"), 200

