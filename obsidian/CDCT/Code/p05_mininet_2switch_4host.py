#!/usr/bin/env python3
"""
P05 - Mininet Virtual SDN Lab: 2 switches, 4 hosts, ping test.

Topology:
            h1 ---- s1 ---- s2 ---- h4
            h2 ----/        \---- h3

Run with Mininet installed (lab VM):
    sudo python3 p05_mininet_2switch_4host.py

Requirements: Mininet (http://mininet.org) - install into an Ubuntu VM:
    sudo apt update && sudo apt install -y mininet
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel


class TwoSwitchFourHostTopo(Topo):
    """Two switches (s1, s2) linked together; two hosts per switch."""

    def build(self):
        # Two OpenFlow switches
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")

        # Four hosts
        h1 = self.addHost("h1", ip="10.0.0.1/24")
        h2 = self.addHost("h2", ip="10.0.0.2/24")
        h3 = self.addHost("h3", ip="10.0.0.3/24")
        h4 = self.addHost("h4", ip="10.0.0.4/24")

        # Links: hosts to their switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)

        # Inter-switch link (the SDN "fabric" between the two switches)
        self.addLink(s1, s2)


def run():
    setLogLevel("info")
    topo = TwoSwitchFourHostTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.addController("c0")
    net.start()

    print(">>> Node list:")
    print("    switches:", net.switches)
    print("    hosts   :", net.hosts)

    print("\n>>> Ping test: every host pings every other host (full mesh)")
    print(net.pingAll())

    print("\n>>> Connectivity check from h1")
    print(net["h1"].cmd("ping -c 3 10.0.0.4"))

    # Interactive CLI so you can run extra commands, e.g.  s1 ifconfig, h2 ping
    CLI(net)
    net.stop()


if __name__ == "__main__":
    run()
