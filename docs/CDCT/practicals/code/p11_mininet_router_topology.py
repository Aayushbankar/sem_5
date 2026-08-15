#!/usr/bin/env python3
"""
p11_mininet_router_topology.py

Two-switch, one-router topology for realistic multi-service traffic flow demo.

Topology:
  h1 (10.0.1.10) \
                  s1 (OVS) -- r1 (Linux router) -- s2 (OVS) -- h3 (10.0.2.10) [Server]
  h2 (10.0.1.11) /                                    |
                                                      Services: httpbin:80, dnsmasq:53, iperf3:5201

Router r1 has two interfaces:
  r1-eth0 -> 10.0.1.1/24 (connected to s1)
  r1-eth1 -> 10.0.2.1/24 (connected to s2)

Run: sudo python3 p11_mininet_router_topology.py
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, Controller
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info


class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable IPv4 forwarding
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class TwoSwitchRouterTopo(Topo):
    def build(self):
        # Switches
        s1 = self.addSwitch('s1', cls=OVSSwitch)
        s2 = self.addSwitch('s2', cls=OVSSwitch)

        # Router (Linux host with two interfaces)
        r1 = self.addNode('r1', cls=LinuxRouter, ip='10.0.1.1/24')

        # Hosts
        h1 = self.addHost('h1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1')
        h2 = self.addHost('h2', ip='10.0.1.11/24', defaultRoute='via 10.0.1.1')
        h3 = self.addHost('h3', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1')

        # Links: clients to access switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)

        # Link: access switch to router (first interface)
        self.addLink(s1, r1,
                     intfName1='s1-eth3',  # arbitrary, OVS names its own
                     params2={'ip': '10.0.1.1/24'})  # r1-eth0

        # Link: router second interface to aggregation switch
        self.addLink(r1, s2,
                     params1={'ip': '10.0.2.1/24'},  # r1-eth1
                     intfName2='s2-eth1')

        # Link: aggregation switch to server
        self.addLink(s2, h3)


def run():
    setLogLevel('info')
    topo = TwoSwitchRouterTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None, switch=OVSSwitch, autoSetMacs=True)

    # Add a default OpenFlow controller (reference controller)
    c0 = net.addController('c0', controller=Controller, protocol='tcp', port=6633)

    net.start()

    # Verify router interfaces have correct IPs (Mininet sets them via params)
    info('*** Router interfaces:\n')
    for intf in net['r1'].intfList():
        info(f'  {intf}: {net["r1"].cmd(f"ip addr show {intf}")}')

    # Print routing tables
    info('*** Routing tables:\n')
    for host in ['h1', 'h2', 'h3', 'r1']:
        info(f'{host}:\n{net[host].cmd("ip route show")}\n')

    info('*** Running pingAll to verify basic connectivity\n')
    net.pingAll()

    info('*** Starting Mininet CLI. Configure NAT on r1 manually:\n')
    info('    r1 iptables -t nat -A POSTROUTING -o r1-eth1 -j MASQUERADE\n')
    CLI(net)
    net.stop()


if __name__ == '__main__':
    run()