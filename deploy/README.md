# SmartAir VPS Deploy

This folder contains a minimal bootstrap to deploy SmartAir API on a clean Ubuntu/Debian VPS.

Contents:
- `vps_bootstrap.sh` — installs Python, sets up a venv, systemd service for Uvicorn, and Nginx reverse-proxy (HTTP). Includes IPv6 listen and removes the default site.

## Prerequisites
- VPS reachable via SSH (default root@<VPS_IP>, port 22)
- DNS A/AAAA records for:
  - api.smartair.space -> VPS IP (IPv4 and optionally IPv6)
  - images.smartair.space -> VPS IP
- Local tools: ssh, scp, tar available on your Windows machine.

## Local deploy (from Windows)
Use the helper script we provide at `C:\Users\...\.smartair\scripts\deploy_vps.ps1` (created separately) which will:
1) Pack `app/` and `requirements.txt` into a tarball
2) Upload it to `/tmp/smartair_deploy.tgz`
3) Upload `vps_bootstrap.sh` to `/tmp/vps_bootstrap.sh`
4) SSH into the VPS and run `sudo bash /tmp/vps_bootstrap.sh <api_domain> <images_domain>`

## After bootstrap
- Issue SSL certs once DNS is pointing to the VPS:
  ```bash
  sudo apt-get install -y certbot python3-certbot-nginx
  sudo certbot --nginx -d api.smartair.space -d images.smartair.space --redirect --hsts --staple-ocsp -m admin@smartair.space --agree-tos -n
  ```
- Verify:
  - http(s)://api.smartair.space/health
  - http(s)://images.smartair.space/health.txt

## Notes
- Systemd service: `systemctl status smartair.service`
- Nginx config lives at `/etc/nginx/sites-available/smartair_api.conf`
- App root: `/opt/smartair` (venv under `/opt/smartair/venv`)
- To redeploy code only, re-upload and restart service: `systemctl restart smartair.service`
