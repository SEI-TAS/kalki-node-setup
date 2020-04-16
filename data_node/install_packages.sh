#!/bin/bash

update() {
    echo "Updating apt-get..."
    sudo apt-get -qq update
    echo "Update complete"
}

install_ovs() {
    echo "Installing OVS..."
    sudo apt-get -yqq install openvswitch-common openvswitch-switch openvswitch-dbg ethtool
    sudo systemctl start openvswitch-switch
    sudo systemctl enable openvswitch-switch
    echo "OVS Install Complete"
}

install_docker() {
    echo "Installing Docker.."
    sudo apt-get -yqq install docker.io
    sudo usermod -a -G docker $USER
    echo "Docker Install Complete"
}

install_dhcp_server() {
   echo "Installing DHCP server..."
   sudo apt install isc-dhcp-server
   echo "DHCP server installed"
}

# Install packages
echo "Beginning packages setup..."
update
install_ovs
install_docker
install_dhcp_server
echo "Finished setting up packages"

# To enable nested VMs, if needed: http://www.server-world.info/en/note?os=Ubuntu_16.04&p=kvm&f=8
