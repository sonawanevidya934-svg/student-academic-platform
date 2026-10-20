# TROUBLESHOOTING — actual issues this session

## 1. run_commands shell captured no output (exit 1)
Symptom: git/echo commands showed terminal text but tool returned success:false.
Impact: could not live re-run pytest/docker/kubectl via agent.
Workaround: used read_files + search_codebase for full inspection; file creation via editor still works.
Fix tomorrow: run the Resume commands in a real PowerShell terminal (see audit part 2). No repo damage.

## 2. Missing .gitignore / README / terraform / ansible / reports md
Symptom: reads returned ENOENT.
Fix: created minimal safe versions (gitignore, tf validate-only, ansible local-safe, 5 docs + root README). Uncommitted; review with git diff before commit.

## 3. Reports artifacts dirty (coverage.xml, junit.xml, .coverage)
Symptom: earlier git status showed M reports/* + ?? .coverage.
Fix: .gitignore now excludes them. Run `git checkout -- reports/coverage.xml reports/junit.xml` if you want a clean tree, or keep fresh run outputs. Remove .coverage with `del .coverage` (Windows) — safe.

## 4. Jenkins Docker may be unavailable
Symptom risk: docker build fails on agent without daemon.
Fix: Jenkinsfile now guards with `docker info` check and skips gracefully; pipeline still green via tests.

## 5. App preserves working code
No app/*.py modified. If tests fail tomorrow, check: venv active, SAP_DATABASE path writable, port 5000 free, instance/ write perms.
