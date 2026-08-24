#!/bin/bash
set -euo pipefail

MQTT_USER="vision"
MQTT_PASS_FILE="/etc/mosquitto/passwd"

echo "=== Vision Platform Local — Setup MQTT (Mosquitto) ==="

# Install packages
echo ""
echo "--- Installing mosquitto ---"
sudo apt-get update -qq
sudo apt-get install -y mosquitto mosquitto-clients

# Broker config
echo ""
echo "--- Writing broker config ---"
sudo tee /etc/mosquitto/conf.d/geofissura.conf > /dev/null << EOF
listener 1883
allow_anonymous false
password_file ${MQTT_PASS_FILE}
EOF

# Broker user + app user credentials
if sudo test -f "${MQTT_PASS_FILE}"; then
    echo ""
    echo "--- Password file already exists, keeping existing users ---"
else
    echo ""
    echo "--- Creating broker internal user ---"
    sudo mosquitto_passwd -c -b "${MQTT_PASS_FILE}" "${MQTT_USER}" "$(openssl rand -hex 16)"
fi

if id "${USER_NAME}" &>/dev/null && sudo grep -q "^${USER_NAME}:" <(sudo cat "${MQTT_PASS_FILE}" 2>/dev/null); then
    echo "App user '${USER_NAME}' already in password file"
else
    read -r -p "Senha MQTT para o usuário '${USER_NAME}': " APP_MQTT_PASS
    sudo mosquitto_passwd -b "${MQTT_PASS_FILE}" "${USER_NAME}" "${APP_MQTT_PASS}"
fi

# Restart broker
echo ""
echo "--- Restarting mosquitto ---"
sudo systemctl enable --now mosquitto
sudo systemctl restart mosquitto
sleep 2

# Smoke test
echo ""
echo "--- Smoke test (pub/sub localhost) ---"
mosquitto_sub -h localhost -p 1883 -u "${USER_NAME}" -P "${APP_MQTT_PASS}" \
    -t 'geofissura/test' -C 1 -W 5 &
SUB_PID=$!
sleep 1
mosquitto_pub -h localhost -p 1883 -u "${USER_NAME}" -P "${APP_MQTT_PASS}" \
    -t 'geofissura/test' -m '{"ok": true}'
wait ${SUB_PID} && echo "Smoke test OK" || echo "WARNING: smoke test failed"

echo ""
echo "=== Setup MQTT complete ==="
echo "Broker: localhost:1883 (autenticação obrigatória)"
echo "Configure no dashboard: mqtt_broker_host, mqtt_broker_port,"
echo "mqtt_username=${USER_NAME}, mqtt_password=<senha>, mqtt_enabled=true"
