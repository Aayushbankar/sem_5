#!/bin/bash
# One-command replicate of the IOT local stack (no sudo, Fedora 43+).
# Usage: bash setup.sh
set -e
export PATH="$HOME/.local/bin:$PATH"
REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"   # sme_5/
STACK_DIR="$(cd "$(dirname "$0")" && pwd)"        # local-stack/
APPS="$HOME/apps/mosquitto"

echo "=== 1/5 arduino-cli ==="
if ! command -v arduino-cli >/dev/null; then
  curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh \
    | BINDIR=$HOME/.local/bin sh -s -- 0.35.3
fi
arduino-cli version

echo "=== 2/5 ESP32 core + libraries ==="
arduino-cli core update-index
arduino-cli core install esp32:esp32 || true
arduino-cli lib install "DHT sensor library" "Adafruit Unified Sensor" "PubSubClient" || true

echo "=== 3/5 mosquitto (user-local, no sudo) ==="
mkdir -p "$APPS/lib" /tmp/mosq-setup && cd /tmp/mosq-setup
dnf download mosquitto libwebsockets >/dev/null 2>&1 || true
rpm2cpio mosquitto-*.x86_64.rpm | cpio -idmv ./usr/bin/mosquitto >/dev/null 2>&1
rpm2cpio libwebsockets-*.x86_64.rpm | cpio -idmv "./usr/lib64/libwebsockets.so*" >/dev/null 2>&1
cp ./usr/bin/mosquitto "$APPS/"
cp ./usr/lib64/libwebsockets.so.21* "$APPS/lib/"

echo "=== 4/5 configs + dashboard ==="
cp "$STACK_DIR/mosquitto.conf" "$APPS/mosquitto.conf"
mkdir -p "$APPS/dash" && cp "$STACK_DIR/dash/mqtt-dash.html" "$APPS/dash/"
cp "$STACK_DIR/start-broker.sh" "$STACK_DIR/start-dashboard.sh" "$APPS/"
chmod +x "$APPS/start-broker.sh" "$APPS/start-dashboard.sh"

echo "=== 5/5 verify ==="
export LD_LIBRARY_PATH="$APPS/lib:$LD_LIBRARY_PATH"
timeout 8 "$APPS/mosquitto" -c "$APPS/mosquitto.conf" &
sleep 5
python3 -c "import socket; socket.create_connection(('127.0.0.1',1883),timeout=5); print('broker OK on 1883')"
pkill -x mosquitto || true

echo "DONE. Start with:"
echo "  bash $APPS/start-broker.sh"
echo "  bash $APPS/start-dashboard.sh   # then open http://localhost:8000/mqtt-dash.html"
