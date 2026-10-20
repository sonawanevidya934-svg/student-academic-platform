# Ansible setup for Student Academic Platform (Ubuntu 22.04, truthful status)

Status: configuration only. Nothing has been deployed to AWS and no playbook
run has been executed in this task. Validate locally with the commands below.

## Layout
- `ansible.cfg` - local defaults (inventory, roles path, no .retry files).
- `inventory.ini` - safe local inventory (`localhost ansible_connection=local`).
- `inventory.ini.example` - EC2 template with placeholders only (no real IPs).
- `playbook.yml` - modular play: system_setup -> docker_setup -> nginx_setup
  -> app_deploy, then strict health checks on `GET /api/health` (HTTP 200).
- `group_vars/app.yml` - all configurable values (ports, image, dirs, packages).
- `roles/system_setup/` - apt update + base packages on Ubuntu 22.04.
- `roles/docker_setup/` - installs `docker.io` + `python3-docker`, enables service.
- `roles/nginx_setup/` - Nginx reverse proxy 80 -> 127.0.0.1:5000, `nginx -t`, reload.
- `roles/app_deploy/` - builds image from local Dockerfile + `app/`, runs
  container on port 5000 with `unless-stopped` restart and Docker healthcheck.

## Design notes (from inspected files)
- Flask health: `app/routes/health.py` exposes `GET /api/health` (HTTP 200).
- Container port: `Dockerfile` runs gunicorn on `0.0.0.0:5000`, so the role
  builds that Dockerfile remotely at `/opt/sap/src` and maps `5000:5000`.
- No registry is assumed: default builds locally; set
  `app_image_pull_from_registry=true` only if you publish the image.
- Terraform SG already allows 22/80/5000 (`terraform/main.tf`).
- No passwords, keys, or AWS credentials are stored anywhere in `ansible/`.

## Prerequisites (local validation only)
- `pip install ansible`
- `ansible-galaxy collection install community.docker`

## Local validation (safe: no AWS, no deployment)
```powershell
cd "c:\Users\Admin\OneDrive\Documents\project 1\Student-Academic-Platform"
ansible-playbook ansible/playbook.yml --syntax-check
ansible-lint ansible/playbook.yml
ansible-playbook ansible/playbook.yml -i ansible/inventory.ini --check
ansible-inventory -i ansible/inventory.ini --list
python -m py_compile app/routes/health.py
```

## EC2 deployment (manual, NOT run here)
```powershell
cp ansible/inventory.ini.example ansible/inventory.ini
# Edit ansible/inventory.ini: replace <EC2_PUBLIC_IP_OR_DNS> with:
#   terraform -chdir=terraform output ec2_public_ip
# Replace <PATH_TO_YOUR_KEY_PEM> with your key path (never commit it).
ansible-playbook ansible/playbook.yml -i ansible/inventory.ini
# Then verify: curl http://<EC2_PUBLIC_IP>/api/health  (expect HTTP 200)
```

## Secrets
Never store SSH keys, passwords, or tokens in git. Use Ansible Vault or
environment variables for real deployments.
