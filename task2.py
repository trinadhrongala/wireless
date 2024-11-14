#!/usr/bin/python
import sys
#from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

def topology(plot):
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    
    # Task 1: Add 5 access points with specified configurations
    ap1 = net.addAccessPoint('ap1', ssid="AP1-SSID", mode="g", channel="1", position='10,20,0', range=35)
    ap2 = net.addAccessPoint('ap2', ssid="AP2-SSID", mode="g", channel="6", position='30,20,0', range=35)
    ap3 = net.addAccessPoint('ap3', ssid="AP3-SSID", mode="g", channel="11", position='50,20,0', range=35)
    ap4 = net.addAccessPoint('ap4', ssid="AP4-SSID", mode="g", channel="1", position='70,20,0', range=50)
    ap5 = net.addAccessPoint('ap5', ssid="AP5-SSID", mode="g", channel="6", position='90,20,0', range=50)

    # Adding 3 Stations with specific IP addresses and initial positions
    sta1 = net.addStation('sta1', ip='192.168.0.1/24', position='5,10,0')
    sta2 = net.addStation('sta2', ip='192.168.0.2/24', position='5,30,0')
    sta3 = net.addStation('sta3', ip='192.168.0.3/24', position='5,50,0')

    c1 = net.addController('c1')
    
    net.setPropagationModel(model="logDistance", exp=5)
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    # Plotting the network graph
    if plot:
        net.plotGraph(max_x=100, max_y=100)

    info("*** Creating mobility scenario\n")
    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=10, position='5,10,0')
    net.mobility(sta1, 'stop', time=20, position='100,10,0')

    net.mobility(sta2, 'start', time=30, position='5,30,0')
    net.mobility(sta2, 'stop', time=60, position='100,30,0')

    net.mobility(sta3, 'start', time=25, position='100,50,0')
    net.mobility(sta3, 'stop', time=60, position='5,50,0')

    net.stopMobility(time=70)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])
    ap5.start([c1])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    plot = True # Set to True to enable graph plotting
    topology(plot)



