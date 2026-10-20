# TECHNICAL_REPORT — Student Academic Platform

## 1. Overview
Flask + SQLite academic records system: students, faculty, courses, enrollments
(credit-limit 18/semester), marks, GPA/transcript, health endpoints. DevOps:
Git/GitHub, pytest+junit/coverage, Docker (non-root, healthcheck), Jenkins
pipeline, K8s 3-replica NodePort 30090, Terraform validate-only, Ansible deploy.

## 2. Architecture
Client -> Flask factory (create_app) -> Blueprints (health/students/courses/
faculty/enrollments/grades) -> Services (validators, enrollment, grading,
student) -> db.py (sqlite3, FK ON) -> schema.sql. Entrypoints: run.py (dev),
wsgi.py (gunicorn wsgi:app, 2 workers in Docker).

## 3. Setup
Python 3.14, pip install -r requirements.txt (-dev for cov/flake8).
Run: python run.py (http://127.0.0.1:5000). Health: / , /health, /api/health.
Docker: docker build -t student-academic-platform:v1.0.0 . ; docker run -p
5000:5000 -v sap-data:/app/data student-academic-platform:v1.0.0.
K8s: kubectl apply -f k8s/ ; service NodePort 30090.

## 4. Modules and DB
- students.py: POST/GET/LIST/PUT/DELETE /api/students, 400/404/409 handling.
- courses.py: CRUD /api/courses + optional faculty_id FK check.
- faculty.py: CRUD /api/faculty.
- enrollments.py: POST /api/enrollments (validate, FK, duplicate 409, credit 422), list per student, DELETE, PUT marks.
- grades.py: /api/grading-scale, /api/students/<id>/gpa[?semester], /transcript.
- Schema: students PK student_id; faculty PK; courses PK + faculty FK SET NULL; enrollments auto-id + UNIQUE(sid,code,sem) + marks 0..100.

## 5. Testing
21 tests: health 3, students_api 4, courses_faculty 4, enrollment 5, grades 4, student model 1. Fixtures: tmp DB per test. pytest.ini -> reports/junit.xml + coverage xml/html/term. JUnit published in Jenkins.
