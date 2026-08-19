#!/bin/bash
set -euo pipefail

# ── Colors ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
err()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"
STATE_FILE="$SCRIPT_DIR/.setup_state"

# ── Read .env safely ──
read_env() {
    grep -E "^${1}=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d'=' -f2-
}

# ── First run: ask everything ──
if [ ! -f "$STATE_FILE" ]; then
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  GeoFissura Vision Platform — Setup${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo ""

    # ── Database ──
    echo -e "${YELLOW}── Banco de Dados ──${NC}"
    read -p "  Usuário PostgreSQL [vision]: " DB_USER; DB_USER="${DB_USER:-vision}"
    read -s -p "  Senha PostgreSQL [dqgh3ffrdg]: " DB_PASS; echo ""; DB_PASS="${DB_PASS:-dqgh3ffrdg}"
    read -p "  Nome do banco [vision_local]: " DB_NAME; DB_NAME="${DB_NAME:-vision_local}"
    read -p "  Host do banco [localhost]: " DB_HOST; DB_HOST="${DB_HOST:-localhost}"
    read -p "  Porta do banco [5432]: " DB_PORT; DB_PORT="${DB_PORT:-5432}"
    DB_URL="postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

    # ── Sudo user ──
    echo ""
    echo -e "${YELLOW}── Usuário do Sistema ──${NC}"
    read -p "  Usuário sudo [geofissura]: " SUDO_USER; SUDO_USER="${SUDO_USER:-geofissura}"
    read -s -p "  Senha sudo [Estoicismo&70x7]: " SUDO_PASS; echo ""; SUDO_PASS="${SUDO_PASS:-Estoicismo&70x7}"

    # ── Local ──
    echo ""
    echo -e "${YELLOW}── Local ──${NC}"
    read -p "  Local ID [LOCAL-001]: " LOCAL_ID; LOCAL_ID="${LOCAL_ID:-LOCAL-001}"
    read -p "  Local Name [Central Orange Pi 001]: " LOCAL_NAME; LOCAL_NAME="${LOCAL_NAME:-Central Orange Pi 001}"

    # ── Camera ──
    echo ""
    echo -e "${YELLOW}── Câmera ──${NC}"
    read -p "  Camera ID [GeoFissura_CAM_000001]: " CAM_ID; CAM_ID="${CAM_ID:-GeoFissura_CAM_000001}"
    read -p "  Camera Name [VIPC-1230-B-G2 geofissura]: " CAM_NAME; CAM_NAME="${CAM_NAME:-VIPC-1230-B-G2 geofissura}"
    read -p "  Hostname câmera [geofissuracam01]: " CAM_HOST; CAM_HOST="${CAM_HOST:-geofissuracam01}"
    read -p "  Usuário câmera [admin]: " CAM_USER; CAM_USER="${CAM_USER:-admin}"
    read -s -p "  Senha câmera [{Alohomor4}]: " CAM_PASS; echo ""; CAM_PASS="${CAM_PASS:-{Alohomor4}}"
    CAM_RTSP="rtsp://${CAM_USER}:${CAM_PASS}@${CAM_HOST}:554/cam/realmonitor?channel=1&subtype=0"

    # ── Central ──
    echo ""
    echo -e "${YELLOW}── Central ──${NC}"
    read -p "  Central API URL [http://192.168.1.20:8081]: " CENTRAL_URL; CENTRAL_URL="${CENTRAL_URL:-http://192.168.1.20:8081}"
    read -p "  Central API Token [change-me]: " CENTRAL_TOKEN; CENTRAL_TOKEN="${CENTRAL_TOKEN:-change-me}"

    # ── Dashboard ──
    echo ""
    echo -e "${YELLOW}── Dashboard ──${NC}"
    read -p "  Usuário admin [admin]: " ADMIN_USER; ADMIN_USER="${ADMIN_USER:-admin}"
    read -s -p "  Senha admin [admin]: " ADMIN_PASS; echo ""; ADMIN_PASS="${ADMIN_PASS:-admin}"

    # ── Generate secrets ──
    JWT_SECRET=$(head -c 32 /dev/urandom | base64 | tr -d '/+=' | head -c 32)
    API_TOKEN=$(head -c 16 /dev/urandom | base64 | tr -d '/+=' | head -c 16)

    # ── Write .env ──
    info "Gerando .env..."
    cat > "$ENV_FILE" <<EOF
LOCAL_ID=${LOCAL_ID}
LOCAL_NAME=${LOCAL_NAME}
TIMEZONE=America/Sao_Paulo

CAMERA_ID=${CAM_ID}
CAMERA_NAME=${CAM_NAME}
CAMERA_HOSTNAME=${CAM_HOST}
CAMERA_USERNAME=${CAM_USER}
CAMERA_PASSWORD=${CAM_PASS}
CAMERA_AUTO_DISCOVER=true
CAMERA_STREAM_TYPE=main
CAMERA_CHANNEL=1
CAMERA_RTSP_URL=${CAM_RTSP}
CAMERA_RTSP_TRANSPORT=tcp
CAMERA_CONNECT_TIMEOUT_MS=10000
CAMERA_RECONNECT_INTERVAL_MS=5000
CAMERA_CAPTURE_INTERVAL_MS=60000
CAMERA_CAPTURE_WIDTH=1920
CAMERA_CAPTURE_HEIGHT=1080
CAMERA_CAPTURE_JPEG_QUALITY=90

LOCAL_DATA_DIR=/var/lib/vision-platform-local
LOCAL_EVIDENCE_DIR=/var/lib/vision-platform-local/evidence
LOCAL_DB_URL=${DB_URL}
LOCAL_API_HOST=0.0.0.0
LOCAL_API_PORT=8080
LOCAL_API_TOKEN=${API_TOKEN}

CENTRAL_API_BASE_URL=${CENTRAL_URL}
CENTRAL_API_TOKEN=${CENTRAL_TOKEN}
CENTRAL_DELIVERY_INTERVAL_MS=60000

JWT_SECRET_KEY=${JWT_SECRET}
ADMIN_USERNAME=${ADMIN_USER}
ADMIN_PASSWORD=${ADMIN_PASS}
EOF
    ok ".env criado"

    # ── Save state (for subsequent runs) ──
    cat > "$STATE_FILE" <<EOF
SUDO_USER=${SUDO_USER}
SUDO_PASS=${SUDO_PASS}
EOF
    chmod 600 "$STATE_FILE"
    ok "Configuração salva"
else
    info "Setup já feito. Lendo configurações..."
fi

# ── Read sudo credentials from state ──
SUDO_USER=$(grep SUDO_USER "$STATE_FILE" | cut -d'=' -f2-)
SUDO_PASS=$(grep SUDO_PASS "$STATE_FILE" | cut -d'=' -f2-)

# ── Read DB credentials from .env ──
LOCAL_DB_URL_VAL=$(read_env LOCAL_DB_URL)
DB_USER_VAL=$(echo "$LOCAL_DB_URL_VAL" | sed -n 's|.*://\([^:]*\):.*|\1|p')
DB_PASS_VAL=$(echo "$LOCAL_DB_URL_VAL" | sed -n 's|.*://[^:]*:\([^@]*\)@.*|\1|p')
DB_NAME_VAL=$(echo "$LOCAL_DB_URL_VAL" | sed -n 's|.*/\([^?]*\).*|\1|p')

# ── Install system dependencies ──
info "Instalando dependências do sistema..."
echo "${SUDO_PASS}" | sudo -S -k bash -c "apt-get update -qq && apt-get install -y -qq python3 python3-pip python3-venv libpq-dev postgresql postgresql-contrib > /dev/null 2>&1"
ok "Dependências do sistema instaladas"

# ── Create PostgreSQL user and database ──
info "Configurando PostgreSQL..."
echo "${SUDO_PASS}" | sudo -S -k bash -c "
    sudo -u postgres psql -tc \"SELECT 1 FROM pg_roles WHERE rolname='${DB_USER_VAL}'\" 2>/dev/null | grep -q 1 || \
        sudo -u postgres psql -c \"CREATE USER ${DB_USER_VAL} WITH PASSWORD '${DB_PASS_VAL}';\" 2>/dev/null

    sudo -u postgres psql -tc \"SELECT 1 FROM pg_database WHERE datname='${DB_NAME_VAL}'\" 2>/dev/null | grep -q 1 || \
        sudo -u postgres psql -c \"CREATE DATABASE ${DB_NAME_VAL} OWNER ${DB_USER_VAL};\" 2>/dev/null

    sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME_VAL} TO ${DB_USER_VAL};\" 2>/dev/null
"
ok "PostgreSQL configurado"

# ── Create venv and install dependencies ──
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    info "Criando virtualenv..."
    python3 -m venv "$SCRIPT_DIR/venv"
fi

info "Instalando dependências Python..."
"$SCRIPT_DIR/venv/bin/pip" install -q --upgrade pip 2>/dev/null
"$SCRIPT_DIR/venv/bin/pip" install -q -e "$SCRIPT_DIR" 2>/dev/null
ok "Dependências Python instaladas"

# ── Create data directories ──
info "Criando diretórios de dados..."
echo "${SUDO_PASS}" | sudo -S -k mkdir -p /var/lib/vision-platform-local/evidence 2>/dev/null
echo "${SUDO_PASS}" | sudo -S -k chown -R "${SUDO_USER}:${SUDO_USER}" /var/lib/vision-platform-local 2>/dev/null
ok "Diretórios criados"

# ── Run migrations ──
info "Rodando migrations..."
cd "$SCRIPT_DIR"
"$SCRIPT_DIR/venv/bin/alembic" upgrade head 2>/dev/null
ok "Migrations aplicadas"

# ── Create systemd service ──
info "Instalando serviço systemd..."
cat > /tmp/vision-platform-local.service <<EOF
[Unit]
Description=Vision Platform Local - Capture Service
After=network-online.target postgresql.service
Wants=network-online.target

[Service]
Type=simple
user=${SUDO_USER}
group=${SUDO_USER}
WorkingDirectory=${SCRIPT_DIR}
EnvironmentFile=${SCRIPT_DIR}/.env
ExecStart=${SCRIPT_DIR}/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=vision-platform-local

[Install]
WantedBy=multi-user.target
EOF

echo "${SUDO_PASS}" | sudo -S -k cp /tmp/vision-platform-local.service /etc/systemd/system/ 2>/dev/null
echo "${SUDO_PASS}" | sudo -S -k systemctl daemon-reload 2>/dev/null
echo "${SUDO_PASS}" | sudo -S -k systemctl enable vision-platform-local 2>/dev/null
ok "Serviço systemd instalado"

# ── Start service ──
info "Iniciando serviço..."
echo "${SUDO_PASS}" | sudo -S -k systemctl restart vision-platform-local 2>/dev/null
sleep 2

if echo "${SUDO_PASS}" | sudo -S -k systemctl is-active --quiet vision-platform-local 2>/dev/null; then
    ok "Serviço rodando!"
else
    warn "Serviço pode ter iniciado com erro. Verifique:"
    warn "  sudo journalctl -u vision-platform-local -n 20"
fi

# ── Summary ──
IP_ADDR=$(hostname -I | awk '{print $1}')
ADMIN_USER_VAL=$(read_env ADMIN_USERNAME)
ADMIN_PASS_VAL=$(read_env ADMIN_PASSWORD)
API_TOKEN_VAL=$(read_env LOCAL_API_TOKEN)

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Setup completo!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo "  Dashboard:  http://${IP_ADDR}:8080/dashboard"
echo "  Login:      ${ADMIN_USER_VAL} / ${ADMIN_PASS_VAL}"
echo "  API Token:  ${API_TOKEN_VAL}"
echo ""
echo "  Comandos úteis:"
echo "    sudo systemctl status vision-platform-local"
echo "    sudo journalctl -u vision-platform-local -f"
echo "    sudo systemctl restart vision-platform-local"
echo ""
