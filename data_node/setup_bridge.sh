#!/bin/bash

OF_BRIDGE=ovs-br
OF_BRIDGE_PORT=6653
OVS_DB_PORT=6654

IOT_NIC_IP=10.27.151.127
IOT_NIC_BROADCAST=10.27.151.255

IOT_NIC=enp2s0f1
EXT_NIC=enp2s0f0

clear_bridge() {
    echo "Removing bridge in case it existed already."
    sudo ovs-vsctl del-br $OF_BRIDGE

    echo "Restarting bridged ifaces."
    sudo ifdown $EXT_NIC
    sudo ifup $EXT_NIC
    sudo ifdown $IOT_NIC
    sudo ifup $IOT_NIC
}

connect_interface() {
    local bridge_name="$1"
    local interface="$2"
    local port_num="$3"

    echo "Connecting NIC $interface"
    sudo ethtool -K $interface gro off

    # Add the given port_name as a port to the bridge, and assign it the given OpenFlow port number.
    sudo ovs-vsctl add-port $bridge_name $interface -- set interface $interface ofport_request=$port_num
    sudo ovs-ofctl mod-port $bridge_name $interface up

    # Remove the IP address from the NIC since it no longer makes sense.
    sudo ip addr flush dev $interface
}

setup_nic_bridge() {
    local bridge_name="$1"
    local nic1_name="$2"
    local nic2_name="$3"

    echo "Setting up NIC OVS bridge $bridge_name"
    sudo ovs-vsctl add-br $bridge_name

    # Connect to NIC to the OVS switch in port 1.
    connect_interface $bridge_name $nic1_name 1

    # Connect to NIC to the OVS switch in port 1.
    connect_interface $bridge_name $nic2_name 2

    echo "Setting up OF params"
    sudo ip link set $bridge_name up
    sudo ovs-vsctl set bridge $bridge_name protocols=OpenFlow13
    sudo ovs-vsctl set-controller $bridge_name ptcp:$OF_BRIDGE_PORT
    sudo ovs-vsctl set controller $bridge_name connection-mode=out-of-band

    # Configure OVS DB to listen to remote commands on given TCP port.
    sudo ovs-appctl -t ovsdb-server ovsdb-server/add-remote ptcp:$OVS_DB_PORT

    sudo ip addr add ${IOT_NIC_IP}/24 dev $bridge_name
    sudo ifconfig ovs-br broadcast ${IOT_NIC_BROADCAST}


    echo "Bridge setup complete"
 }

setup_passthrough_bridge_rules() {
    local bridge_name="$1"

    # Set rules to be able to process requests and responses to our own IP.
    sudo ovs-ofctl -O OpenFlow13 add-flow $bridge_name "priority=150,arp,nw_src=${IOT_NIC_IP},actions=normal"
    sudo ovs-ofctl -O OpenFlow13 add-flow $bridge_name "priority=150,arp,in_port=1,nw_dst=${IOT_NIC_IP},actions=normal"
    sudo ovs-ofctl -O OpenFlow13 add-flow $bridge_name "priority=150,ip,ip_src=${IOT_NIC_IP},actions=normal"
    sudo ovs-ofctl -O OpenFlow13 add-flow $bridge_name "priority=150,ip,in_port=1,ip_dst=${IOT_NIC_IP},actions=normal"

    # Set up default rules to connect bridges together.
    sudo ovs-ofctl -O OpenFlow13 add-flow $bridge_name "priority=50,in_port=1,actions=output:2"
    sudo ovs-ofctl -O OpenFlow13 add-flow $bridge_name "priority=50,in_port=2,actions=output:1"
    sudo ovs-ofctl -O OpenFlow13 add-flow $bridge_name "priority=0,actions=drop"

}

# Setup
echo "Beginning switches setup..."

clear_bridge
setup_nic_bridge $OF_BRIDGE $IOT_NIC $EXT_NIC
setup_passthrough_bridge_rules $OF_BRIDGE

echo "OVS switches ready"
