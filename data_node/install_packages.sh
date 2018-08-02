#!/bin/bash

update() {
    echo "Updating apt-get..."
    sudo apt-get -qq update
    echo "Update complete"
}

install_qemu() {
    echo "Installing Qemu and Libvirt Daemon..."
    sudo apt-get -yqq install qemu-system-x86_64 libvirt-bin
    echo "Python Install Complete"
}

install_ovs() {
    echo "Installing OVS..."
    sudo apt-get -yqq install openvswitch-common openvswitch-switch openvswitch-dbg ethtool
    sudo systemctl start openvswitch-switch
    sudo systemctl enable openvswitch-switch
    echo "OVS Install Complete"
}


# Install packages
echo "Beginning packages setup..."
update
install_ovs
echo "Finished setting up packages"
