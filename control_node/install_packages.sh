#!/bin/bash

update() {
    echo "Updating apt-get..."
    sudo apt-get -qq update
    echo "Update complete"
}

install_docker() {
    echo "Installing Docker.."
    sudo apt-get -yqq install docker.io docker-compose
    sudo usermod -a -G docker $USER
    echo "Docker Install Complete"
}

# Install packages
echo "Beginning packages setup..."
update
install_docker
echo "Finished setting up packages"
