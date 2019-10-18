#!/usr/bin/env bash

export http_proxy=''
export https_proxy=''
export HTTP_PROXY=''
export HTTPS_PROXY=''

sudo rm /etc/apt/apt.conf.d/01proxy
sudo cp 01noproxy /etc/apt/apt.conf.d/

cd docker
bash docker_noproxy.sh

cd ..
cd gradle
bash gradle_noproxy.sh

