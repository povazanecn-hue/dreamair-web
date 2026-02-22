# SmartAir – AI Agent Guide (concise)

Use this as a practical map to build, test, and deploy SmartAir quickly.

## Big picture
- Backend: FastAPI in `app/` exporting `app.main:app`. Routes include `/` and `/health`.
- Config: `config.json` with env placeholders (e.g., `gemini_api_key: "${GEMINI_API_KEY}", server_port: 5000, debug_mode, cors_origins`). Prefer environment variables; config is a fallback.
- Deploy: `systemd` runs Uvicorn on `127.0.0.1:8000`; Nginx proxies `api.smartair.space` and serves static files for `images.smartair.space` from `/var/www/smartair`.

## Key files
- `app/main.py` – FastAPI routes and app wiring (`app.main:app`).
- `config.json` – runtime settings with `${VAR}` expansion.
- `deploy/vps_bootstrap.sh` – idempotent VPS setup (venv, systemd, Nginx, health check for images).
- `deploy/README.md` – step-by-step VPS deploy + SSL issuance.
- Root Windows helpers: `deploy_smartair.ps1`, `upgrade_frontend_windows.ps1`, `smartair_deployment.py` (package + upload + bootstrap).
- `tests/` – pytest tests (FastAPI `TestClient`). If empty, add a simple `test_health.py`.

## Local development
- Python 3.11+ recommended. Install deps via `pip install -r requirements.txt` (or `fastapi uvicorn[standard] pytest` if missing).
- Run API: `uvicorn app.main:app --reload --port 8000`. Note: CLI args/host override `config.json` values locally.

## Testing
- Use `pytest` with `from fastapi.testclient import TestClient` against `app.main.app`.
- Minimal check: `GET /health` returns 200 and `{"status": "ok"}`.

## Deployment (VPS)
- DNS: point `api.smartair.space` and `images.smartair.space` to the VPS.
- Bootstrap: upload `app/` + `requirements.txt` under `/tmp/smartair_deploy` and run `sudo bash /tmp/vps_bootstrap.sh <api_domain> <images_domain>`.
- Service: `systemctl status|restart smartair.service`. Nginx site: `/etc/nginx/sites-available/smartair_api.conf`.
- SSL (after DNS): install Certbot, then `certbot --nginx -d <api> -d <images> --redirect --hsts --staple-ocsp -m admin@smartair.space --agree-tos -n`.

## Conventions and gotchas
- Secrets via env only; `config.json` expands `${VAR}`. UTF‑8 throughout.
- Uvicorn binds loopback; Nginx is the public edge (IPv4 + IPv6).
- Port changes: update BOTH systemd `ExecStart` (Uvicorn args) and Nginx `proxy_pass`.
- Static assets: `/var/www/smartair` (bootstrap creates `health.txt`).
- Mirror each new endpoint with a simple pytest in `tests/`.

## Agent tips
- Add endpoints in `app/main.py`, add a pytest in `tests/`, and extend `config.json` only when config is truly runtime‑tunable (read env first).
- Keep `deploy/vps_bootstrap.sh` idempotent; reflect any path/port changes in both systemd and Nginx blocks.

Questions for maintainers
- Confirm required Python version and dependency pins (`requirements.txt`).
- Confirm final domains if different from defaults.

## Cross-AI repo governance (MENUMAT context)
- Canonical repository name for the MENUMAT project context is `MENUMAT-MENUMAESTRO-AKTUAL`.
- Before making changes, read `.ai-context/current-sprint.md` and verify latest Lovable push.
- Use branch + PR workflow; do not assume direct pushes to `main` are allowed.
- Merge is allowed only after explicit owner approval.

- Read `.ai-context/cloud-knowledge.md` before large refactors to avoid blocking Lovable workflows.
- Keep changes compatible with Lovable-generated structure unless owner approved otherwise.
