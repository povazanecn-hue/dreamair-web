# SmartAir

Minimal FastAPI backend with deployment scripts and tests.

## Run locally (Windows)

- Install deps: `python -m pip install -r requirements.txt`
- Start API: `python -m uvicorn app.main:app --reload --port 8000`
- Run tests: `python -m pytest -q`

## VS Code helpers

- Tasks: "Tests: Pytest (C:)" and "API: Start (uvicorn, C:)"
- Debug: "API: Debug (uvicorn, C:)" launch config

## Deployment (VPS)

- See `deploy/README.md` and `deploy/vps_bootstrap.sh`
- Nginx proxies `api.smartair.space`; static files under `/var/www/smartair` for `images.smartair.space`

## Notes

- Config uses env-first, with `config.json` as fallback (expands ${VARS})
- Line endings: `.gitattributes` enforces LF for shell scripts
