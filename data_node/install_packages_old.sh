#!/bin/bash

update() {
    echo "Updating apt-get..."
    sudo apt-get -qq update
    echo "Update complete"
}

install_docker() {
    echo "Installing Docker..."
    sudo apt-get -yqq install docker-compose
    sudo apt-get -yqq install apt-transport-https ca-certificates curl software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    sudo apt-get -qq update
    sudo apt-get -yqq install docker-ce

    sudo systemctl start docker
    sudo systemctl enable docker
    echo "Docker Install Complete"
}

install_qemu() {
    echo "Installing Qemu..."
    sudo apt-get -yqq install qemu-system-x86_64 libvirt-dev
    echo "Python Install Complete"
}

install_python_packages() {
    echo "Installing Python..."
    sudo apt-get -yqq install python python-ipaddress python-subprocess32 python-pip
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
#install_docker
install_ovs
install_python_packages
echo "Finished setting up packages"
