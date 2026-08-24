#!/bin/bash
set -euo pipefail

# Setup Mosquitto para o Vision Platform Local.
# Uso interativo:  sudo bash deploy/setup-mqtt.sh
# Uso automático:  MQTT_APP_USER=vision MQTT_APP_PASS=senha sudo -E bash deploy/setup-mqtt.sh

MQTT_APP_USER="${MQTT_APP_USER:-vision}"
MQTT_PASS_FILE="/etc/mosquitto/passwd"
MQTT_CONF="/etc/mosquitto/conf.d/geofissura.conf"

echo "=== Vision Platform Local — Setup MQTT (Mosquitto) ==="

if [[ $EUID -ne 0 ]]; then
    echo "ERRO: execute com sudo." >&2
    exit 1
fi

echo ""
echo "--- Instalando mosquitto ---"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq || true
apt-get install -y -qq mosquitto mosquitto-clients > /dev/null

echo ""
echo "--- Configurando broker (${MQTT_CONF}) ---"
mkdir -p /etc/mosquitto/conf.d
cat > "${MQTT_CONF}" << EOF
listener 1883
allow_anonymous false
password_file ${MQTT_PASS_FILE}
EOF

echo ""
echo "--- Usuarios do broker ---"
if [[ ! -f "${MQTT_PASS_FILE}" ]]; then
    mosquitto_passwd -c -b "${MQTT_PASS_FILE}" broker-internal "$(openssl rand -hex 16)"
fi

if grep -q "^${MQTT_APP_USER}:" "${MQTT_PASS_FILE}"; then
    echo "Usuario '${MQTT_APP_USER}' ja existe — atualizando senha"
fi

APP_MQTT_PASS="${MQTT_APP_PASS:-}"
if [[ -z "${APP_MQTT_PASS}" ]]; then
    read -r -s -p "Senha MQTT para o usuario '${MQTT_APP_USER}': " APP_MQTT_PASS
    echo ""
fi
mosquitto_passwd -b "${MQTT_PASS_FILE}" "${MQTT_APP_USER}" "${APP_MQTT_PASS}"
chown root:mosquitto "${MQTT_PASS_FILE}"
chmod 640 "${MQTT_PASS_FILE}"

echo ""
echo "--- Reiniciando mosquitto ---"
systemctl enable --now mosquitto > /dev/null 2>&1
systemctl restart mosquitto
sleep 2

echo ""
echo "--- Smoke test (pub/sub localhost) ---"
mosquitto_sub -h localhost -p 1883 -u "${MQTT_APP_USER}" -P "${APP_MQTT_PASS}" \
    -t 'geofissura/test' -C 1 -W 5 > /tmp/mqtt_smoke.txt &
SUB_PID=$!
sleep 1
mosquitto_pub -h localhost -p 1883 -u "${MQTT_APP_USER}" -P "${APP_MQTT_PASS}" \
    -t 'geofissura/test' -m '{"ok": true}'
wait ${SUB_PID} && echo "Smoke test OK -> $(cat /tmp/mqtt_smoke.txt)" || echo "WARNING: smoke test falhou"
rm -f /tmp/mqtt_smoke.txt

echo ""
echo "=== Setup MQTT completo ==="
echo "Broker: localhost:1883 (autenticacao obrigatoria)"
echo "Configure no dashboard ou via API:"
echo "  mqtt_broker_host=localhost, mqtt_broker_port=1883,"
echo "  mqtt_username=${MQTT_APP_USER}, mqtt_password=<senha>, mqtt_enabled=true"
