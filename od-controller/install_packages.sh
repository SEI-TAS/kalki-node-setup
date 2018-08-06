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

}

# Install packages
echo "Beginning packages setup..."
update
install_python
install_libvirt
install_postgres
echo "Finished setting up packages"
