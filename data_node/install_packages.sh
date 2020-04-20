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

# Install packages
echo "Beginning packages setup..."
update
install_ovs
install_docker
echo "Finished setting up packages"
