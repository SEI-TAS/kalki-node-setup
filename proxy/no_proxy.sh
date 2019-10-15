#!/usr/bin/env bash

export http_proxy=''
export https_proxy=''
export HTTP_PROXY=''
export HTTPS_PROXY=''

sudo rm /etc/apt/apt.conf.d/01proxy

cd docker
bash docker_removal.sh

cd ..
cd gradle
bash gradle_removal.sh

