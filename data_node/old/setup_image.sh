#!/bin/bash

FOLDER=$1
NAME=$2

setup_image() {
    sudo docker build $FOLDER -t $NAME
}

# Setup
echo "Beginning image setup..."
setup_image
echo "Image ready"
