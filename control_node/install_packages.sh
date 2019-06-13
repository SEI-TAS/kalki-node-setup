#!/bin/bash

update() {
    echo "Updating apt-get..."
    sudo apt-get -qq update
    echo "Update complete"
}

install_git() {
    echo "Installing Git..."
    sudo apt-get -yqq install git
    echo "Git Install Complete"
}


install_python() {
    echo "Installing Python..."
    sudo apt-get -yqq install python python-pip
    echo "Python Install Complete"
}

install_libvirt() {
    echo "Installing Libvirt..."
    sudo apt-get -yqq install libvirt-dev
    sudo pip install libvirt-python
    echo "Libvirt Install Complete"
}

install_ovs_tools() {
    echo "Installing OVS tools..."
    sudo apt-get -yqq install openvswitch-common openvswitch-switch
    echo "OVS Install Complete"
}

install_java() {
    echo "Installing Java OpenJDK..."
    sudo apt-get -yqq install openjdk-8-jdk
    echo "Java OpenJDK Install Complete"
}

install_docker() {
    echo "Installing Docker.."
    sudo apt-get -yqq install docker.io
    sudo usermod -a -G docker $USER
    echo "Docker Install Complete"
}

install_postgres() {
    echo "Installing postgresql..."
    sudo apt-get install postgresql postgresql-contrib
    echo "Postgresql installed"

    # TODO: configure pg_hba.conf to allow peer connections
}

# Install packages
echo "Beginning packages setup..."
update
install_git
install_java
install_docker
#install_python
#install_libvirt
#install_ovs_tools
#install_postgres
echo "Finished setting up packages"

# Also needed for network simple config:
# 1 - Disable Network Manager:
#  a- sudo systemctl stop NetworkManager.service
#  b- sudo systemctl disable NetworkManager.service
# 2 - Copy proper interfaces file to /etc/network/interfaces
# 3 - Reboot node
