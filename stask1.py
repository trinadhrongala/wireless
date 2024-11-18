#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

def topology():
    "Create a network for Task 1 with updated coordinates."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    # Adding access points with specified positions
    ap1 = net.addAccessPoint('ap1', ssid="AP1-SSID", mode="g", channel="1", position='10,35,0', range=35)
    ap2 = net.addAccessPoint('ap2', ssid="AP2-SSID", mode="g", channel="6", position='50,35,0', range=35)
    ap3 = net.addAccessPoint('ap3', ssid="AP3-SSID", mode="g", channel="11", position='90,35,0', range=35)
    ap4 = net.addAccessPoint('ap4', ssid="AP4-SSID", mode="g", channel="1", position='125,0,0', range=50)
    ap5 = net.addAccessPoint('ap5', ssid="AP5-SSID", mode="g", channel="6", position='160,0,0', range=50)

    # Adding stations with initial positions
    sta1 = net.addStation('sta1', ip='192.168.0.1/24', position='5,30,0')  # Starts near AP1
    sta2 = net.addStation('sta2', ip='192.168.0.2/24', position='45,30,0')  # Starts near AP2
    sta3 = net.addStation('sta3', ip='192.168.0.3/24', position='150,-50,0')  # Starts near AP5 on the bottom

    # Adding controller
    c1 = net.addController('c1')
    
    # Configuring propagation model
    net.setPropagationModel(model="logDistance", exp=5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    # Plot the graph with extended range to include negative Y-axis
    net.plotGraph(max_x=200, min_x=0, max_y=100, min_y=-100)

    # Define linear topology by adding links between APs
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)
    net.addLink(ap3, ap4)
    net.addLink(ap4, ap5)

    # Mobility setup for stations
    net.startMobility(time=0)
    # STA1 movement from AP1 to the center
    net.mobility(sta1, 'start', time=10, position='5,30,0')
    net.mobility(sta1, 'stop', time=20, position='45,30,0', min_v=1, max_v=5)

    # STA2 movement from AP2 to the right but avoiding the dead spot
    net.mobility(sta2, 'start', time=30, position='45,30,0')
    net.mobility(sta2, 'stop', time=60, position='100,0,0', min_v=5, max_v=10)

    # STA3 movement along the bottom, avoiding the dead spot
    net.mobility(sta3, 'start', time=25, position='150,-50,0')
    net.mobility(sta3, 'stop', time=60, position='100,-50,0', min_v=2, max_v=7)
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
    topology()
