#!/bin/bash

update() {
    echo "Updating apt-get..."
    sudo apt-get -qq update
    echo "Update complete"
}

# Note that for the libvirt-bin daemon to actually listen to incoming connections, the following config changes are needed:
# - /etc/libvirt/libvirtd.conf: uncomment the line #listen_tcp = 1
# - /etc/libvirt/libvirtd.conf: uncomment the line #listen_tls = 0
# - /etc/libvirt/libvirtd.conf: uncomment the line and change to #auth_tcp = "none"
# - /etc/default/libvirt-bin or /etc/default/libvirtd: set libvirtd_opts to "--listen" , and uncomment.
install_qemu() {
    echo "Installing Qemu and Libvirt Daemon..."
    sudo apt-get -yqq install qemu-system libvirt-bin
    echo "Qemu and Libvirt Install Complete"
}

install_python() {
    echo "Installing Python..."
    sudo apt-get -yqq install python python-pip
    sudo python -m pip install pipenv
    echo "Python Install Complete"
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
install_qemu
install_ovs
install_python
echo "Finished setting up packages"

# To enable nested VMs, if needed: http://www.server-world.info/en/note?os=Ubuntu_16.04&p=kvm&f=8
