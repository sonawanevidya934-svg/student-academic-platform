# Audit part 2 — changes, gaps, resume

## 2. Baseline (user-provided, not re-run; shell blocked)
- Claimed: 21 passed, image v1.0.0 on :5000 healthy, /health healthy, jenkins on :8080.
- Code inspection supports it. No app code changed this session.

## 3. Changed this session (safe, reversible, uncommitted)
1. Created .gitignore (venv, pytest, coverage, db, instance, env, tfstate, retry).
2. Jenkinsfile: checkout scm, env verify + docker version, dev reqs, flake8 non-blocking, junit+archive, conditional docker build, timestamps/rotation.
3. terraform/ main+variables+outputs+README: zero-resource validate-only, vars for region/type/port/CIDR, no creds.
4. ansible/ inventory+playbook+README: docker deploy + health check, local-safe.
5. Docs: audit + technical + workflow + checklist + troubleshooting + root README.

## 4. Gaps / TO-VERIFY tomorrow (~20 min)
- pytest -v (expect 21 passed) + screenshot + reports/junit.xml.
- Invoke-RestMethod /health and /api/health + screenshot.
- docker images/ps/logs; rebuild only if Dockerfile/app changed (they did not).
- Jenkins localhost:8080 Pipeline from SCM, Build Now, screenshot stages+junit.
- minikube: kubectl apply -f k8s/, get pods,svc, NodePort 30090 curl, delete-one-pod self-heal.
- terraform fmt -check, init -backend=false, validate (never apply/destroy).
- ansible playbook --syntax-check + --check dry run.
- git status/diff review; commit/push only with approval.

## 5. Resume commands (PowerShell, project root)
git status --short
.\.venv\Scripts\Activate.ps1
pytest -v
Invoke-RestMethod http://localhost:5000/health | ConvertTo-Json
Invoke-RestMethod http://localhost:5000/api/health | ConvertTo-Json
docker ps --filter name=student
kubectl get pods,svc -l app=student-academic-platform
terraform -chdir=terraform fmt -check
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
ansible-playbook ansible/playbook.yml --syntax-check
