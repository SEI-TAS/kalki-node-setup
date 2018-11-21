#!/bin/bash

OF_BRIDGE=ovs-br
OF_BRIDGE_PORT=6653
OVS_DB_PORT=6654

IOT_BRIDGE=ovs-iot
IOT_NIC=ens5

EXT_BRIDGE=ovs-ext
EXT_NIC=ens6

connect_interface() {
    local bridge_name="$1"
    local interface="$2"
    local port_num="$3"

    # Add the given port_name as a port to the bridge, and assign it the given OpenFlow port number.
    sudo ovs-vsctl add-port $bridge_name $interface -- set interface $interface ofport_request=$port_num
    sudo ovs-ofctl mod-port $bridge_name $interface up
}

connect_patch_port() {
    local bridge_name="$1"
    local patch_port_name="$2"
    local port_num="$3"

    sudo ovs-vsctl add-port $bridge_name $patch_port_name -- set interface $patch_port_name ofport_request=$port_num
    sudo ovs-vsctl set interface $patch_port_name type=patch
}

connect_patch_port_peers() {
    local peer1="$1"
    local peer2="$2"

    sudo ovs-vsctl set interface $peer1 options:peer=$peer2
    sudo ovs-vsctl set interface $peer2 options:peer=$peer1
}


setup_nic_bridge() {
    local bridge_name="$1"
    local nic_name="$2"
    local patch_port_name="$3"
    local patch_peer_name="$4"
    local of_bridge_name="$5"
    local of_patch_port_num="$6"

    echo "Setting up NIC OVS bridge $bridge_name"
    sudo ovs-vsctl add-br $bridge_name
    sudo ip link set $bridge_name up

    # Connect to NIC to the OVS switch in port 1.
    sudo ethtool -K $nic_name gro off
    connect_interface $bridge_name $nic_name 1

    # Set up patch port to main OVS switch in port 2.
    connect_patch_port $bridge_name $patch_port_name 2
    connect_patch_port $of_bridge_name $patch_peer_name $of_patch_port_num
    connect_patch_port_peers $patch_port_name $patch_peer_name

    echo "Bridge setup complete"
}

setup_ovs_bridge() {
    local bridge_name="$1"
    # Create and start up the OVS switch.
    echo "Setting up OpenFlow enabled OVS bridge..."
    sudo ovs-vsctl --may-exist add-br $bridge_name
    sudo ip link set $bridge_name up

    # Configure OVS switch to use OF1.3, listen in given port.
    sudo ovs-vsctl set bridge $bridge_name protocols=OpenFlow13
    sudo ovs-vsctl set-controller $bridge_name ptcp:$OF_BRIDGE_PORT
    sudo ovs-vsctl set controller $bridge_name connection-mode=out-of-band

    # Configure OVS DB to listen to remote commands on given TCP port.
    sudo ovs-appctl -t ovsdb-server ovsdb-server/add-remote pttp:$OVS_DB_PORT

    echo "Bridge setup complete"
}

# Setup
echo "Beginning switches setup..."

iot_to_of_patch="$IOT_BRIDGE-to-$OF_BRIDGE"
of_to_iot_patch="$OF_BRIDGE-to-$IOT_BRIDGE"
ext_to_of_patch="$EXT_BRIDGE-to-$OF_BRIDGE"
of_to_ext_patch="$OF_BRIDGE-to-$EXT_BRIDGE"

setup_ovs_bridge $OF_BRIDGE
setup_nic_bridge $IOT_BRIDGE $IOT_NIC $iot_to_of_patch $of_to_iot_patch $OF_BRIDGE 1
setup_nic_bridge $EXT_BRIDGE $EXT_NIC $ext_to_of_patch $of_to_ext_patch $OF_BRIDGE 2

echo "OVS switches ready"
