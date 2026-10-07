#!/bin/bash
# Start local mosquitto (detached, survives terminal close).
export LD_LIBRARY_PATH="$HOME/apps/mosquitto/lib:$LD_LIBRARY_PATH"
setsid "$HOME/apps/mosquitto/mosquitto" -c "$HOME/apps/mosquitto/mosquitto.conf" \
  > /tmp/mosquitto.log 2>&1 < /dev/null &
sleep 3
python3 -c "import socket; socket.create_connection(('127.0.0.1',1883),timeout=5); print('broker UP on 127.0.0.1:1883')"
