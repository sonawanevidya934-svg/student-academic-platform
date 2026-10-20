# SUBMISSION_CHECKLIST — Student Academic Platform (2026-10-18)

## Done (in repo, needs tomorrow screenshots)
- [x] Flask app + SQLite schema + validators/grading/enrollment logic.
- [x] 21 tests present (count verified by search; re-run TO-VERIFY).
- [x] requirements.txt + dev, pytest.ini (junit+coverage).
- [x] Dockerfile + .dockerignore (image v1.0.0 claimed; re-verify docker ps).
- [x] Jenkinsfile upgraded (checkout/env/venv/flake8/pytest-junit/docker-conditional).
- [x] k8s deployment (3 replicas, probes) + service (NodePort 30090) consistent.
- [x] terraform validate-only + ansible playbook (syntax-check TO-VERIFY).
- [x] Docs: audit, technical, workflow, checklist, troubleshooting, README.
- [x] .gitignore created.

## Evidence still needed (manual, do not fabricate)
- [ ] pytest -v terminal screenshot showing 21 passed + reports/junit.xml timestamp.
- [ ] curl /health + /api/health JSON screenshot.
- [ ] docker images + docker ps screenshot; container logs tail.
- [ ] Jenkins build # screenshot (green stages + junit).
- [ ] kubectl get pods (3 Running) + svc + NodePort curl + delete-pod self-heal log.
- [ ] terraform validate + ansible --syntax-check output screenshot/text.
- [ ] git status/diff review; commit message draft; push only with approval.

## Manual actions tomorrow (order, ~25 min)
1. pytest -v. 2. health curls. 3. docker ps/logs. 4. Jenkins build. 5. minikube deploy. 6. tf/ansible checks. 7. git review.
