#!/bin/bash
set -euo pipefail

SERVICE_NAME="vision-local"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="${PROJECT_DIR}/venv"
USER_NAME="$(whoami)"

echo "=== Vision Platform Local — Setup ==="
echo "Project: ${PROJECT_DIR}"
echo "Venv:    ${VENV_DIR}"
echo "User:    ${USER_NAME}"

# Check venv exists
if [ ! -f "${VENV_DIR}/bin/activate" ]; then
    echo "ERROR: venv not found at ${VENV_DIR}"
    echo "Run: python3 -m venv venv && source venv/bin/activate && pip install -e ."
    exit 1
fi

# Run migrations
echo ""
echo "--- Running Alembic migrations ---"
"${VENV_DIR}/bin/alembic" upgrade head

# Create systemd service
echo ""
echo "--- Creating systemd service ---"
sudo tee "${SERVICE_FILE}" > /dev/null << EOF
[Unit]
Description=Vision Platform Local
After=network.target postgresql.service

[Service]
Type=simple
User=${USER_NAME}
WorkingDirectory=${PROJECT_DIR}
ExecStart=${VENV_DIR}/bin/uvicorn src.main:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=10
Environment=PATH=${VENV_DIR}/bin:/usr/local/bin:/usr/bin

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now "${SERVICE_NAME}"

echo ""
echo "--- Status ---"
sudo systemctl status "${SERVICE_NAME}" --no-pager

echo ""
echo "=== Setup complete ==="
echo "Logs:  sudo journalctl -u ${SERVICE_NAME} -f"
echo "API:   http://$(hostname -I | awk '{print $1}'):8080/health"
