# DEVOPS_WORKFLOW — Student Academic Platform

## Git/GitHub
Remote origin https://github.com/Pushkar726/student-academic-platform.git, branch main. Feature branches exist for each unit. Rule: inspect, small diffs, never force-push, commit/push only with approval. .gitignore excludes venv/pytest/coverage/db/instance/env/tfstate.

## CI/CD + Jenkins
Jenkinsfile stages: Checkout scm -> Verify env (java/git/python/docker) -> venv install (requirements + dev) -> flake8 non-blocking -> pytest with junit reports/jenkins-test-results.xml + archive -> conditional docker build (skips if no daemon). Manual: localhost:8080 -> New Pipeline from SCM -> repo URL + Jenkinsfile path -> Build Now -> check junit trend.

## Docker
python:3.14-slim, SAP_DATABASE=/app/data, non-root appuser, EXPOSE 5000, HEALTHCHECK /api/health, CMD gunicorn wsgi:app. Image student-academic-platform:v1.0.0. Rebuild only on Dockerfile/app change. Verify: docker ps, logs, Invoke-RestMethod /api/health.

## Kubernetes
deployment.yaml: 3 replicas, IfNotPresent, port 5000, readiness/liveness /api/health. service.yaml: NodePort 5000:30090 selector app match. Deploy: minikube start; kubectl apply -f k8s/; kubectl get pods,svc; curl NodePort; kubectl delete pod <one> proves self-healing; kubectl rollout status.

## Terraform
terraform/ DEFINES full infra (VPC, subnet, IGW, SG, EC2, S3) but nothing
is provisioned: validate-only workflow. Vars: region ap-south-1, t3.micro, port 5000. Validate: fmt -check, init -backend=false, validate. Never apply/destroy (cost + rules).

## Ansible
ansible/playbook.yml ensures data dir, runs container with healthcheck, checks /api/health. Inventory local by default. Checks: --syntax-check, --check dry run. Secrets via Vault only.
