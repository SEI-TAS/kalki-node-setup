#!/bin/bash

update() {
    echo "Updating apt-get..."
    sudo apt-get -qq update
    echo "Update complete"
}

install_java() {
    echo "Installing Java OpenJDK..."
    sudo apt-get -yqq install openjdk-8-jdk
    echo "Java OpenJDK Install Complete"
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
install_java
install_docker
echo "Finished setting up packages"
