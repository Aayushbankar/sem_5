#!/bin/bash
# Serve the local MQTT web dashboard, then print its URL.
setsid python3 -m http.server 8000 --directory "$HOME/apps/mosquitto/dash" \
  > /tmp/mqtt-dash-http.log 2>&1 < /dev/null &
sleep 2
echo "dashboard: http://localhost:8000/mqtt-dash.html"
