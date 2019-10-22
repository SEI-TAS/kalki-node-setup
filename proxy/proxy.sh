#!/usr/bin/env bash

source env/env_proxy.sh

sudo cp env/env_proxy.sh /etc/profile.d/env_proxy.sh

sudo rm /etc/apt/apt.conf.d/01noproxy
sudo cp apt/01proxy /etc/apt/apt.conf.d/

cd docker
bash docker_proxy.sh

cd ..
cd gradle
bash gradle_proxy.sh
