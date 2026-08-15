#!/bin/bash
# p11_start_services.sh
# Run on the server host (h3) inside Mininet.
# Installs and starts httpbin (HTTP API), dnsmasq (DNS), and iperf3 (throughput).

set -e

echo "[*] Updating package list and installing dependencies..."
apt-get update -qq
apt-get install -y -qq dnsmasq iperf3 python3-pip >/dev/null

echo "[*] Installing gunicorn + httpbin via pip..."
pip3 install --quiet gunicorn httpbin

echo "[*] Starting httpbin on 0.0.0.0:80 ..."
gunicorn -b 0.0.0.0:80 httpbin:app --daemon --pid /tmp/gunicorn.pid

echo "[*] Starting dnsmasq on port 53 (resolves api.local -> 10.0.2.10) ..."
dnsmasq --port=53 --address=/api.local/10.0.2.10 --no-daemon --pid-file=/tmp/dnsmasq.pid &

echo "[*] Starting iperf3 server on port 5201 ..."
iperf3 -s -D --pidfile /tmp/iperf3.pid

echo "[*] Verifying listeners..."
netstat -tlnp | grep -E ':80|:53|:5201'

echo "[+] All services started."
echo "    httpbin  -> http://10.0.2.10/get   (and /uuid, /ip, etc.)"
echo "    dnsmasq  -> dig @10.0.2.10 api.local"
echo "    iperf3   -> iperf3 -c 10.0.2.10 -t 10"