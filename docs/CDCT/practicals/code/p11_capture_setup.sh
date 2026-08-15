#!/bin/bash
# p11_capture_setup.sh
# Run on the MININET HOST (outside Mininet) in FOUR separate terminals.
# Each terminal runs one tcpdump capturing a specific interface inside the Mininet namespaces.
# Interface names are as created by the topology script:
#   h1-eth0, r1-eth0, r1-eth1, h3-eth0
# Adjust if your Mininet version names them differently.

set -e

CAP_DIR=/tmp/mininet_captures
mkdir -p "$CAP_DIR"

echo "=========================================="
echo "Packet Capture Setup for P11 Demo"
echo "=========================================="
echo "Run EACH of the following commands in its OWN terminal."
echo "All captures write to $CAP_DIR/"
echo ""
echo "Terminal 1  (Client A - h1):"
echo "  sudo tcpdump -i h1-eth0 -w $CAP_DIR/h1_clientA.pcap -s 0 -U"
echo ""
echo "Terminal 2  (Router Ingress - r1-eth0):"
echo "  sudo tcpdump -i r1-eth0 -w $CAP_DIR/r1_ingress.pcap -s 0 -U"
echo ""
echo "Terminal 3  (Router Egress - r1-eth1):"
echo "  sudo tcpdump -i r1-eth1 -w $CAP_DIR/r1_egress.pcap -s 0 -U"
echo ""
echo "Terminal 4  (Server - h3):"
echo "  sudo tcpdump -i h3-eth0 -w $CAP_DIR/server.pcap -s 0 -U"
echo ""
echo "=========================================="
echo "After the demo, press Ctrl+C in each terminal to stop."
echo "PCAP files will be in $CAP_DIR/ ready for Wireshark."
echo "=========================================="

# If you want to start them all from one script (background), uncomment below:
# sudo tcpdump -i h1-eth0   -w $CAP_DIR/h1_clientA.pcap   -s 0 -U &
# sudo tcpdump -i r1-eth0   -w $CAP_DIR/r1_ingress.pcap   -s 0 -U &
# sudo tcpdump -i r1-eth1   -w $CAP_DIR/r1_egress.pcap    -s 0 -U &
# sudo tcpdump -i h3-eth0   -w $CAP_DIR/server.pcap       -s 0 -U &
# wait