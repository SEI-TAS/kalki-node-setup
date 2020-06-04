#!/usr/bin/env bash

source env/no_env_proxy.sh

sudo rm /etc/profile.d/env_proxy.sh

sudo rm /etc/apt/apt.conf.d/01proxy
sudo cp apt/01noproxy /etc/apt/apt.conf.d/

cd docker
bash docker_noproxy.sh

cd ..
cd gradle
bash gradle_noproxy.sh

