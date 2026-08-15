#!/bin/bash
# p11_client_tests.sh
# Run on client hosts (h1 and h2) inside Mininet.
# Performs DNS lookup, HTTP requests, and iperf3 throughput test.

set -e

SERVER=10.0.2.10
DNS=10.0.2.10
HOSTNAME=$(hostname)

echo "=== Client $HOSTNAME starting tests ==="

echo "[1] DNS query for api.local via $DNS"
dig @$DNS api.local +short

echo "[2] HTTP GET /get (User A style)"
curl -v --max-time 10 http://api.local/get

if [ "$HOSTNAME" = "h2" ]; then
    echo "[3] HTTP GET /uuid (User B style)"
    curl -v --max-time 10 http://api.local/uuid

    echo "[4] iperf3 throughput test (10 seconds)..."
    iperf3 -c $SERVER -t 10
fi

echo "=== Client $HOSTNAME tests completed ==="