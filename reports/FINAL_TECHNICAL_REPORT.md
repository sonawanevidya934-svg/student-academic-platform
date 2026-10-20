# FINAL TECHNICAL REPORT — Student Academic Platform

Date (UTC): 2026-10-19
GitHub: https://github.com/Pushkar726/student-academic-platform
Scope: submission report. Existing docs (`reports/TECHNICAL_REPORT.md`,
`docs/FINAL_PROJECT_REVIEW.md`, `reports/FINAL_SUBMISSION_CHECKLIST.md`,
`reports/local_test_validation.md`) are preserved and referenced, not
duplicated. No AWS deployment performed; nothing below claims otherwise.

## 1. Project title and objective

Student Academic Platform — a Flask + SQLite academic records system
with a college DevOps mini-project pipeline: tested, containerized,
CI-built, orchestrated, and provisioned-as-code (configuration only).

## 2. Problem statement and proposed solution

Manual academic record handling is error-prone. The solution is a small
REST service (students, faculty, courses, enrollments, marks,
GPA/transcript) plus a reproducible DevOps path: local pytest, Docker
image, Jenkins pipeline, Kubernetes manifests, Terraform VPC design,
and modular Ansible deployment — each verifiable independently.

## 3. Technology stack

- App: Python 3.14, Flask 3.0.3, gunicorn 22.0.0, SQLite (FK ON).
- Quality: pytest 8.0.2, pytest-cov 5.0.0, flake8 7.0.0.
- DevOps: Docker (python:3.14-slim), Jenkins declarative pipeline,
  Kubernetes (Deployment + NodePort Service), Terraform >= 1.5 with
  AWS provider ~> 5.0, Ansible (Ubuntu 22.04 roles).

## 4. System architecture and component relationships

Client -> Flask factory (`create_app`) -> blueprints
(health/students/courses/faculty/enrollments/grades) -> services
(validators, enrollment, grading, student) -> `db.py` (sqlite3)
-> `schema.sql`. Entrypoints: `run.py` (dev `127.0.0.1:5000`),
`wsgi.py` (`wsgi:app`, gunicorn 2 workers in Docker).
Deployment layers: Docker image `student-academic-platform:v1.0.0`
(port 5000) -> K8s 3-replica Deployment + NodePort 30090 Service
-> Terraform VPC/subnet/IGW/SG/EC2/S3 design -> Ansible roles
(system -> docker -> nginx 80->5000 -> app container).

## 5. Flask application and health endpoints

`app/routes/health.py`: `GET /` (project running), `GET /health`
(`{"status":"healthy"}`, 200), `GET /api/health`
(`{"status":"healthy","service":"student-academic-platform"}`, 200).
Domain routes: students/faculty/courses CRUD, enrollments
(validate/FK/duplicate 409/credit-limit 422), marks, grading scale,
GPA/transcript. Tests use tmp-DB fixtures (`tests/conftest.py`).

## 6. Docker configuration and validation status

`Dockerfile`: `python:3.14-slim`, `SAP_DATABASE=/app/data/app.db`,
non-root `appuser`, `EXPOSE 5000`, `HEALTHCHECK /api/health`,
`CMD gunicorn 0.0.0.0:5000 wsgi:app`. Status: CONFIGURATION REVIEWED
(source read); build/run/health output PENDING (no observable Docker
output in this session; nothing claimed).

## 7. Jenkins CI pipeline and available evidence

`Jenkinsfile` stages: Checkout SCM -> Verify Environment
(java/git/python/docker) -> Install Dependencies (`.venv-ci`,
requirements + dev) -> Lint non-blocking (flake8, max-line 120) ->
Run Automated Tests (pytest, `reports/jenkins-test-results.xml`,
junit + archive always) -> Docker Build conditional on daemon.
Post: success/failure/always messages, 10-build rotation. Status:
CONFIGURATION REVIEWED; green-build + junit evidence PENDING.

## 8. Kubernetes deployment, service, replicas, self-healing

`k8s/deployment.yaml`: 3 replicas, image
`student-academic-platform:v1.0.0`, `IfNotPresent`, port 5000,
readiness + liveness probes on `/api/health:5000`. `k8s/service.yaml`:
NodePort, 5000->30090, selector `app` match. Note: no
`resources.requests/limits` (acceptable for mini-project; add if
faculty requires). Status: CONFIGURATION REVIEWED; `kubectl get`,
curl, delete-pod self-heal evidence PENDING (cluster untouched here).

## 9. Terraform infrastructure configuration (NOT DEPLOYED)

Defines (not provisions): provider `var.aws_region` (default
`ap-south-1`); VPC `10.0.0.0/16` + DNS; subnet `10.0.1.0/24`; IGW +
route table + `0.0.0.0/0` + association; SG 22/80/`var.app_port`
(5000); EC2 `var.instance_type` (t3.micro), Canonical Ubuntu 22.04
AMI data source, 20 GiB gp3; S3 prefix + versioning + AES256.
Outputs: `vpc_id`, `subnet_id`, `security_group_id`,
`s3_bucket_name`, `ec2_public_ip`, `ec2_public_dns`. No apply/destroy
run; no AWS resources created. See `docs/FINAL_PROJECT_REVIEW.md`.

## 10. Modular Ansible roles and deployment workflow (NOT EXECUTED)

`ansible/playbook.yml` (`become: true`): `system_setup` (apt +
packages) -> `docker_setup` (docker.io, service enabled/started) ->
`nginx_setup` (site 80 -> 127.0.0.1:5000, `nginx -t`, reload handler)
-> `app_deploy` (copies Dockerfile + `app/`, builds
`student-academic-platform:v1.0.0` locally, runs `5000:5000`
`unless-stopped` + healthcheck) -> strict `wait_for` + two HTTP-200
`GET /api/health` checks (direct + via Nginx). Variables in
`group_vars/app.yml`; `inventory.ini.example` placeholders only.
Playbook never executed here; EC2 run requires a real Ubuntu target.

## 11. GitHub repository URL

https://github.com/Pushkar726/student-academic-platform

## 12. Testing and validation results (honest status)

- Suite: VERIFIED — `reports/pytest-run.log` shows `collected 21
  items`, all PASSED, `21 passed in 3.79s`, TOTAL coverage 93%
  (381 stmts, 28 miss); `reports/pytest-exit-code.txt` = 0.
  `pytest.ini` writes `reports/junit.xml` + coverage; Jenkins writes
  `reports/jenkins-test-results.xml` (Jenkins evidence still PENDING).
- Docker: VERIFIED — image `student-academic-platform:v1.0.0`
  present; container `/student-academic-platform` reused (Up 4h,
  `health=healthy`, 5000:5000); `GET /health` =
  `{"status":"healthy"}`, `GET /api/health` =
  `{"service":"student-academic-platform","status":"healthy"}`
  (evidence: `reports/docker-inspect.txt`, `health-check.txt`,
  `api-health-check.txt`).
- Terraform/Ansible live outputs: Terraform VERIFIED — `tf-fmt.txt`
  empty (fmt clean), `tf-init.txt` "successfully initialized" (aws
  v5.100.0), `tf-validate.txt` "Success! The configuration is valid."
  Ansible VERIFIED — WSL has `/usr/bin/ansible-playbook`;
  `ansible-syntax.txt` returns `playbook: ansible/playbook.yml`
  (syntax-check passed). AWS NOT DEPLOYED; live playbook not run.

## 13. Security considerations

- No credentials, keys, or tokens in repo (verified by search);
  Ansible uses placeholders + Vault guidance.
- DISCLOSED RISK: SG SSH 22 defaults to `0.0.0.0/0`
  (`allowed_http_cidr`). Restrict with
  `-var allowed_http_cidr=<YOUR_IP>/32` (ideally separate SSH/HTTP
  CIDRs) before any real apply. Egress open (standard for app server).
- Docker runs non-root; S3 encrypted + versioned; Nginx proxies 80.

## 14. Limitations and future improvements

- Evidence gap: all runtime proofs pending (shell blind this session).
- K8s lacks `resources` limits; add requests/limits if required.
- Jenkinsfile targets Linux agents (`python3`/`.venv-ci`); Windows
  local runs use `.venv\Scripts\python.exe`.
- Future: split SSH/HTTP CIDRs, remote-state backend, registry push,
  TLS on Nginx, rollout/secret management docs.

## 15. Screenshot/evidence checklist (all PENDING)

- [ ] pytest `X passed` + `reports/junit.xml` timestamp.
- [ ] `/health` + `/api/health` JSON (200).
- [ ] `docker images` + `docker ps sap-review` + logs tail.
- [ ] Jenkins green build + stages + junit trend.
- [ ] `kubectl get pods` (3 Running) + svc + NodePort curl +
  delete-pod self-heal + `rollout status`.
- [ ] `terraform fmt -check -diff` + `validate` output.
- [ ] `ansible-playbook --syntax-check` + `--check` output.

## 16. Conclusion

The application, container, pipeline, orchestration, and
infrastructure-as-code configurations are complete, consistent
(port 5000, image v1.0.0, NodePort 30090, `/api/health`), and
reviewed. Cloud resources have NOT been provisioned and runtime
evidence is PENDING. Correct submission wording: "Terraform and
Ansible configurations are complete; AWS infrastructure has not been
deployed."
