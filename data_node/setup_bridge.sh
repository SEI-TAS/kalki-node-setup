#!/bin/bash

BRIDGE_NAME=br0
IF_ONE=enp0s3
IF_TWO=enp0s8
OD_IP=192.168.58.3

connect_interface() {
    local interface="$1"
    local port_num="$2"

    sudo ethtool -K $interface gro off

    # Add the given interface as a port to the bridge, and assign it the given OpenFlow port number.
    sudo ovs-vsctl --may-exist add-port $BRIDGE_NAME $interface -- set Interface $interface ofport_request=$port_num
    sudo ovs-ofctl mod-port $BRIDGE_NAME $interface up
}

setup_bridge() {
    echo "Setting up basic bridge..."
    sudo ovs-vsctl --may-exist add-br $BRIDGE_NAME
    sudo ip link set $BRIDGE_NAME up

    connect_interface $IF_ONE 1
    connect_interface $IF_TWO 2

    sudo ovs-vsctl set bridge $BRIDGE_NAME protocols=OpenFlow13
    sudo ovs-vsctl set-controller $BRIDGE_NAME tcp:$OD_IP:6633
    sudo ovs-vsctl set controller $BRIDGE_NAME connection-mode=out-of-band

    echo "Bridge setup complete"
}

# Setup
echo "Beginning dataplane setup..."
setup_bridge
echo "Dataplane ready"
