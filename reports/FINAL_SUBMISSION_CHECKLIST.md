# FINAL SUBMISSION CHECKLIST — Student Academic Platform (2026-10-19 UTC)

Status labels: VERIFIED (observable evidence) | CONFIGURATION REVIEWED
(source read only) | PENDING EXECUTION (safe command identified, not run
here) | NOT DEPLOYED (no AWS resources) | BLOCKED (needs user action).

## 1. Required deliverables (verified 2026-10-19)

- Flask app + tests: VERIFIED (21 passed in 3.79s, 93%, exit 0 —
  `reports/pytest-run.log`, `reports/pytest-exit-code.txt`).
- Dockerized app: VERIFIED (image present; healthy container reused;
  `/health` + `/api/health` healthy).
- Jenkins pipeline: CONFIGURATION REVIEWED (6 stages, junit archive;
  green build MISSING/PENDING — no screenshot folder found).
- Kubernetes manifests: CONFIGURATION REVIEWED (3 replicas, probes,
  NodePort 30090; cluster evidence MISSING/PENDING).
- Terraform: VERIFIED (fmt clean, init ok, validate success)
  | NOT DEPLOYED (no apply/destroy; SSH 0.0.0.0/0 disclosed).
- Ansible: VERIFIED (WSL syntax-check passed) | NOT DEPLOYED
  (live playbook not executed).
- README + GitHub: CONFIGURATION REVIEWED (README present; status
  observable, push pending approval).
- Final technical report: CONFIGURATION REVIEWED
  (`reports/TECHNICAL_REPORT.md` exists; this checklist + review are
  the submission companions).

## 2. Files and folders to submit

- `app/`, `tests/`, `run.py`, `wsgi.py`, `requirements.txt`,
  `requirements-dev.txt`, `pytest.ini`
- `Dockerfile`, `.dockerignore`, `Jenkinsfile`, `k8s/`
- `terraform/` (main, variables, outputs, README)
- `ansible/` (cfg, inventories, playbook, group_vars, 4 roles,
  template, handler, README)
- `README.md`, `docs/FINAL_PROJECT_REVIEW.md`,
  `reports/FINAL_SUBMISSION_CHECKLIST.md` (this file),
  `reports/local_test_validation.md`, `reports/TECHNICAL_REPORT.md`
- Do NOT submit: `.venv/`, `.venv-ci/`, `*.log`, `reports/junit.xml`,
  `reports/coverage.xml`, `reports/jenkins-test-results.xml`,
  `reports/coverage_html/`, `.coverage`, `*.db`, `instance/`
  (all covered by `.gitignore`).

## 3. Screenshots/evidence required

- [ ] pytest terminal: `X passed` + `reports/junit.xml` timestamp.
- [ ] `GET /health` + `GET /api/health` JSON (200).
- [ ] `docker images` + `docker ps --filter name=sap-review` + logs.
- [ ] Jenkins build page: green stages + junit trend.
- [ ] `kubectl get pods` (3 Running) + svc + NodePort curl +
  delete-one-pod self-heal + `rollout status`.
- [ ] `terraform fmt -check -diff` + `validate` output.
- [ ] `ansible-playbook --syntax-check` + `--check` output.

## 4. Safe validation commands (PowerShell, project root)

```powershell
cd "c:\Users\Admin\OneDrive\Documents\project 1\Student-Academic-Platform"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
(.\.venv\Scripts\python.exe -m pytest -v; "PYTEST_EXIT_CODE=$LASTEXITCODE") *>&1 | Tee-Object reports\pytest-run.log
docker build -t student-academic-platform:v1.0.0 .
docker run -d --name sap-review -p 5000:5000 -v sap-data:/app/data student-academic-platform:v1.0.0
Invoke-RestMethod http://127.0.0.1:5000/api/health | ConvertTo-Json
minikube start; kubectl apply -f k8s/
kubectl get pods,svc -l app=student-academic-platform
terraform -chdir=terraform fmt -check -diff
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
ansible-playbook ansible/playbook.yml --syntax-check
ansible-playbook ansible/playbook.yml -i ansible/inventory.ini --check
git status --short --branch
```

NEVER: `terraform apply/destroy/plan`, live playbook run,
commit/push/reset/clean without approval.

## 5. Verification status per component

| Component | Status | Evidence |
|---|---|---|
| Flask tests | VERIFIED | `reports/pytest-run.log`: 21 passed, 3.79s, 93%; exit 0 |
| Docker | VERIFIED | Healthy container reused; both endpoints healthy |
| Jenkins | CONFIGURATION REVIEWED | Stages/junit paths read; screenshot MISSING |
| K8s | CONFIGURATION REVIEWED | Manifests read; screenshots MISSING |
| Terraform | VERIFIED + NOT DEPLOYED | fmt/init/validate evidence files; no apply |
| Ansible | VERIFIED + NOT DEPLOYED | WSL syntax-check passed; live run not done |
| GitHub | STATUS OBSERVABLE | Tree listed; push pending approval |

Nothing is VERIFIED by execution in this session (no observable
command output). Do not label execution items VERIFIED until logs
exist.

## 6. Remaining blockers

1. Shell tool returns exit-1 with no captured output — all live
   validation must be run by you in real PowerShell.
2. Test results UNVERIFIED — run the pytest log command first.
3. Docker daemon/images UNVERIFIED — run `docker version/info/images`.
4. Git status/branch UNVERIFIED — run `git status --short --branch`.
5. K8s/Jenkins evidence missing — minikube + Jenkins manual steps.
6. SSH `0.0.0.0/0` default — disclose + restrict before any apply.

## 7. GitHub update steps (manual, with approval only)

1. `git status --short --branch` + `git diff --stat` (review).
2. `git add` only: source, configs, docs, checklists (never
   `.venv/`, logs, reports XML, coverage, db files).
3. `git commit -m "..."` + `git push` only after your approval.

## 8. Final report requirements

- Keep `reports/TECHNICAL_REPORT.md` (architecture/modules/testing).
- Keep `docs/FINAL_PROJECT_REVIEW.md` (senior review + findings).
- Keep `reports/local_test_validation.md` (update only with verified
  pytest log output).
- This checklist is the submission tracker — update statuses to
  VERIFIED only with pasted log/screenshot evidence.
- Wording: "Terraform and Ansible configurations are complete;
  cloud resources have NOT been provisioned."
