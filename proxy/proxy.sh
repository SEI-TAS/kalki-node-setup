#!/usr/bin/env bash
PROXY="http://proxy.sei.cmu.edu:8080"

export http_proxy=${PROXY}
export https_proxy=${PROXY}
export HTTP_PROXY=${PROXY} 
export HTTPS_PROXY=${PROXY}

sudo cp 01proxy /etc/apt/apt.conf.d/

cd docker
bash docker_setup.sh

cd ..
cd gradle
bash gradle_setup.sh
