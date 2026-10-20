# PROJECT_AUDIT — Student Academic Platform (2026-10-18 UTC)
Branch: main. Remote: https://github.com/Pushkar726/student-academic-platform.git
Method: direct file reads. Shell tool returned exit-1 without capture, so live
re-verification is marked TO-VERIFY with copy-paste commands in section 5.

## 1. Exists (verified by read)
- Flask factory app/__init__.py: create_app + blueprints health/students/courses/faculty/enrollments/grades.
- Config app/config.py: SAP_DATABASE env, default instance/app.db, MAX_CREDITS=18.
- DB app/db.py + app/schema.sql: sqlite, FK ON, tables students/faculty/courses/enrollments.
- Routes app/routes/*.py: CRUD + enroll credit-limit/duplicate + marks + GPA/transcript + health.
- Services: validators, grading_service (O..F), enrollment_service, student_service.
- Entrypoints run.py (127.0.0.1:5000) and wsgi.py (gunicorn target).
- requirements.txt (Flask 3.0.3, pytest 8.0.2, gunicorn 22.0.0, flake8 7.0.0).
- requirements-dev.txt (pytest-cov 5.0.0).
- Tests: conftest + 6 files, 21 def test_ found (matches claimed 21 passed).
- Dockerfile (py3.14-slim, appuser, HEALTHCHECK /api/health, gunicorn wsgi:app).
- Jenkinsfile (improved this session, see audit part 2).
- k8s/deployment.yaml (replicas 3, image v1.0.0, port 5000, probes /api/health).
- k8s/service.yaml (NodePort 5000->30090, selector match). Consistent.
- reports/ dir with prior junit/coverage artifacts.
- Missing at start: .gitignore, README.md, terraform/*, ansible/*, reports/*.md. Created now.
