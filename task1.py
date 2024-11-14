#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

def topology():
    "Create a network for Task 1."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    
    # Adding 5 access points with increased range for better connectivity
    ap1 = net.addAccessPoint('ap1', ssid="AP1-SSID", mode="g", channel="1", position='10,20,0', range=40)
    ap2 = net.addAccessPoint('ap2', ssid="AP2-SSID", mode="g", channel="6", position='30,20,0', range=40)
    ap3 = net.addAccessPoint('ap3', ssid="AP3-SSID", mode="g", channel="11", position='50,20,0', range=40)
    ap4 = net.addAccessPoint('ap4', ssid="AP4-SSID", mode="g", channel="1", position='70,20,0', range=50)
    ap5 = net.addAccessPoint('ap5', ssid="AP5-SSID", mode="g", channel="6", position='90,20,0', range=50)

    # Adding 3 Stations with specific IP addresses and initial positions
    sta1 = net.addStation('sta1', ip='192.168.0.1/24', position='5,10,0')
    sta2 = net.addStation('sta2', ip='192.168.0.2/24', position='5,30,0')
    sta3 = net.addStation('sta3', ip='192.168.0.3/24', position='5,50,0')

    # Adding controller
    c1 = net.addController('c1')
    
    # Configuring propagation model
    net.setPropagationModel(model="logDistance", exp=5)
    
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    # Mobility scenario for stations, with adjusted stop positions for better AP association
    info("*** Creating mobility scenario\n")
    net.startMobility(time=0)

    # Moving stations to be within range of their respective APs
    net.mobility(sta1, 'start', time=10, position='5,10,0')
    net.mobility(sta1, 'stop', time=20, position='15,20,0')  # Near ap1

    net.mobility(sta2, 'start', time=30, position='5,30,0')
    net.mobility(sta2, 'stop', time=60, position='35,20,0')  # Near ap2

    net.mobility(sta3, 'start', time=25, position='5,50,0')
    net.mobility(sta3, 'stop', time=60, position='75,20,0')  # Near ap4

    net.stopMobility(time=70)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])
    ap5.start([c1])

    # Run connectivity tests to verify AP associations
    info("*** Testing connectivity\n")
    net.pingAll()  # Test connectivity between all nodes

    # Additional ping tests between stations
    sta1.cmd('ping -c 3 192.168.0.2')  # Ping from sta1 to sta2
    sta2.cmd('ping -c 3 192.168.0.3')  # Ping from sta2 to sta3
    sta3.cmd('ping -c 3 192.168.0.1')  # Ping from sta3 to sta1

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
