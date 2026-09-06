#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/not-troll-game"
DATA_DIR="/var/lib/not-troll-game"
REPO_URL="https://github.com/moteroamigable3000-code/not-troll-game.git"
SERVICE_FILE="/etc/systemd/system/not-troll-game.service"
NGINX_FILE="/etc/nginx/sites-available/not-troll-game"

if [ "$(id -u)" -ne 0 ]; then
  echo "Run this script as root."
  exit 1
fi

apt-get update
apt-get install -y git python3 python3-venv nginx

mkdir -p "$DATA_DIR"

if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" fetch origin main
  git -C "$APP_DIR" checkout main
  git -C "$APP_DIR" pull --ff-only origin main
else
  rm -rf "$APP_DIR"
  git clone --branch main "$REPO_URL" "$APP_DIR"
fi

python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/pip" install --upgrade pip
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Not A Troll Game
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR/backend
Environment=FRONTEND_DIR=$APP_DIR
Environment=DATABASE_PATH=$DATA_DIR/scores.db
ExecStart=$APP_DIR/.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable not-troll-game
systemctl restart not-troll-game

cat > "$NGINX_FILE" <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    client_max_body_size 10m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

rm -f /etc/nginx/sites-enabled/default
ln -sf "$NGINX_FILE" /etc/nginx/sites-enabled/not-troll-game
nginx -t
systemctl reload nginx

echo
echo "Deployed successfully."
echo "Open: http://2.25.174.40/"
echo "Health: http://2.25.174.40/health"
