# Student Academic Platform
Flask + SQLite academic records (students, faculty, courses, enrollments, GPA/transcript) with DevOps: pytest, Docker, Jenkins, K8s, Terraform, Ansible.

## Quickstart
pip install -r requirements.txt
python run.py
# health: http://127.0.0.1:5000/health and /api/health

## Tests
pip install -r requirements-dev.txt
pytest -v
# JUnit: reports/junit.xml, coverage: reports/coverage.xml + html

## Docker
docker build -t student-academic-platform:v1.0.0 .
docker run -p 5000:5000 student-academic-platform:v1.0.0

## Kubernetes (minikube)
kubectl apply -f k8s/
kubectl get pods,svc -l app=student-academic-platform
# Service NodePort 30090 -> 5000, 3 replicas, probes on /api/health

## Jenkins
Pipeline from SCM using ./Jenkinsfile: checkout, env check, venv install, flake8 (non-blocking), pytest+junit, conditional docker build. See reports/DEVOPS_WORKFLOW.md.

## Terraform / Ansible (safe, no cloud spend)
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
ansible-playbook ansible/playbook.yml --syntax-check
Never run terraform apply/destroy without approval. See reports/ for audit, technical, checklist, troubleshooting.
