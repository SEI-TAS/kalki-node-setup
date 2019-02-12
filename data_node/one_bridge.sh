#!/bin/bash

OF_BRIDGE=ovs-br
OF_BRIDGE_PORT=6653
OVS_DB_PORT=6654

IOT_NIC=ens6
EXT_NIC=ens5

connect_interface() {
    local bridge_name="$1"
    local interface="$2"
    local port_num="$3"

    echo "Connecting NIC $interface"
    sudo ethtool -K $interface gro off

    # Add the given port_name as a port to the bridge, and assign it the given OpenFlow port number.
    sudo ovs-vsctl add-port $bridge_name $interface -- set interface $interface ofport_request=$port_num
    sudo ovs-ofctl mod-port $bridge_name $interface up
}

setup_nic_bridge() {
    local bridge_name="$1"
    local nic1_name="$2"
    local nic2_name="$3"

    echo "Setting up NIC OVS bridge $bridge_name"
    sudo ovs-vsctl add-br $bridge_name

    # Connect to NIC to the OVS switch in port 1.
    connect_interface $bridge_name $nic1_name 1
    sudo ip addr flush dev $nic1_name

    # Connect to NIC to the OVS switch in port 1.
    connect_interface $bridge_name $nic2_name 2
    sudo ip addr flush dev $nic2_name

    sudo ip link set $bridge_name up

    echo "Setting up OF version"
    sudo ovs-vsctl set bridge $bridge_name protocols=OpenFlow13
    sudo ovs-vsctl set-controller $bridge_name ptcp:$OF_BRIDGE_PORT
    sudo ovs-vsctl set controller $bridge_name connection-mode=out-of-band

    # Configure OVS DB to listen to remote commands on given TCP port.
    sudo ovs-appctl -t ovsdb-server ovsdb-server/add-remote ptcp:$OVS_DB_PORT

    echo "Bridge setup complete"
}

setup_passthrough_bridge_rules() {
    local bridge_name="$1"

    # Set up default rules to connect bridges together.
    sudo ovs-ofctl -O OpenFlow13 add-flow $bridge_name "in_port=1,priority=50,actions=output:2"
    sudo ovs-ofctl -O OpenFlow13 add-flow $bridge_name "in_port=2,priority=50,actions=output:1"
}

# Setup
echo "Beginning switches setup..."

setup_nic_bridge $OF_BRIDGE $IOT_NIC $EXT_NIC
setup_passthrough_bridge_rules $OF_BRIDGE

echo "OVS switches ready"
