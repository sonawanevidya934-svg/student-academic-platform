# Local Test Validation — Student Academic Platform

Date (UTC): 2026-10-19
Scope: Task 1 — validate Flask app + pytest suite locally.
No AWS, no terraform apply/destroy, no commits/pushes, no deletions.

## 1. Inspection (read from repo files)

- `requirements.txt`: Flask==3.0.3, pytest==8.0.2, gunicorn==22.0.0,
  flake8==7.0.0.
- `requirements-dev.txt`: pytest==8.0.2, pytest-cov==5.0.0,
  flake8==7.0.0.
- `pytest.ini`: `testpaths = tests`; addopts write
  `reports/junit.xml`, `reports/coverage.xml`, `reports/coverage_html`,
  plus terminal coverage.
- Flask factory `app/__init__.py`: `create_app`, blueprints
  health/students/courses/faculty/enrollments/grades, `/` running,
  404/405 handlers.
- `tests/conftest.py`: tmp-DB `app` + `client` fixtures; `student`
  (STU001) + `course` (CS101) fixtures posting 201.
- `tests/test_health.py`: `/`, `/health`, `/api/health` all 200.
- Jenkins JUnit: `Jenkinsfile` writes
  `reports/jenkins-test-results.xml` with `-o addopts=""`
  (bypasses pytest.ini addopts), published + archived via
  `junit`/`archiveArtifacts`. `reports/junit.xml` + coverage come
  only from local `pytest` runs via `pytest.ini`.

## 2. Virtual environment check

- `.venv/` EXISTS in project root (reused, not deleted/recreated).
- Earlier shell probe confirmed `.venv\Scripts\python.exe` present
  (`Test-Path` True) and system Python 3.14.7.
- Correct interpreter: `.venv\Scripts\python.exe`.
- No environment deletion or recreation performed.

## 3. Exact commands run (Windows PowerShell, project root)

```powershell
cd "c:\Users\Admin\OneDrive\Documents\project 1\Student-Academic-Platform"
Test-Path .\.venv\Scripts\python.exe
python --version
.\.venv\Scripts\python.exe -m pip show pytest Flask pytest-cov flake8
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -v
```

## 4. Test summary — VERIFIED from reports/pytest-run.log (2026-10-19)

- Evidence read directly from `reports/pytest-run.log` (UTF-16 log,
  decoded): `platform win32 -- Python 3.14.7, pytest-8.0.2`,
  `collected 21 items`, every test `PASSED`,
  `21 passed in 3.79s`, `TOTAL 381 stmts, 28 miss, 93%` coverage,
  JUnit written to `reports\junit.xml`, coverage XML/HTML written.
- `reports/pytest-exit-code.txt` contains `PYTEST_EXIT_CODE=0`.
- Matches your stated result (21 passed, 3.79s, 93%, exit 0).
  Recorded here because the log files themselves are the evidence —
  not because the shell returned output (it did not).
- No test files were modified, weakened, skipped, or removed.

## 5. Jenkins JUnit report status

- Path: `reports/jenkins-test-results.xml` (Jenkins only; local runs
  do not create it because of `-o addopts=""` override).
- Local pytest writes `reports/junit.xml` + `reports/coverage.xml`.
- Currency: UNKNOWN in this session (could not list timestamps via
  shell). Re-run pytest locally, then check timestamps before
  submission.

## 6. Docker validation (2026-10-19, VERIFIED via evidence files)

- Image: `student-academic-platform:v1.0.0` confirmed present earlier
  (197MB terminal echo). No rebuild performed.
- Container REUSED (no duplicate created): `docker-inspect.txt` shows
  `/student-academic-platform` = image
  `student-academic-platform:v1.0.0`, `ports={"5000/tcp":
  [{HostPort:"5000"}]}`, `health=healthy`, state Up 4 hours.
- Port 5000: occupied by this same container (`port-check.txt` shows
  listeners; inspect confirms the binding). No process stopped.
- Endpoints VERIFIED: `health-check.txt` = `{"status":"healthy"}`;
  `api-health-check.txt` =
  `{"service":"student-academic-platform","status":"healthy"}`.
- No images/containers/volumes deleted; unrelated containers
  (jenkins-server, minikube, student-academic-test/app, sap-test,
  my-running-app) untouched.

## 7. What to run manually (copy-paste, safe, local only)

```powershell
cd "c:\Users\Admin\OneDrive\Documents\project 1\Student-Academic-Platform"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -v
```

- pytest: VERIFIED (21 passed, 93%, exit 0 — see section 4).
- Docker: VERIFIED (reused healthy container, both endpoints 200 —
  see section 6). No manual container step needed.
