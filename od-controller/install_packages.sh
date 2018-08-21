#!/bin/bash

update() {
    echo "Updating apt-get..."
    sudo apt-get -qq update
    echo "Update complete"
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

install_postgres() {
    echo "Installing postgresql..."
    sudo apt-get install postgresql postgresql-contrib
    echo "Postgresql installed"

    # TODO: configure pg_hba.conf to allow peer connections
}

# Install packages
echo "Beginning packages setup..."
update
install_python
install_libvirt
install_postgres
echo "Finished setting up packages"

# Also needed for network simple config:
# 1 - Disable Network Manager:
#  a- sudo systemctl stop NetworkManager.service
#  b- sudo systemctl disable NetworkManager.service
# 2 - Copy proper interfaces file to /etc/network/interfaces
# 3 - Reboot node
