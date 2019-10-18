#!/usr/bin/env bash
sudo cp sei_daemon.json /etc/docker/daemon.json

sudo cp http-proxy.conf /etc/systemd/system/docker.service.d/
sudo systemctl daemon-reload
sudo systemctl restart docker

cp config.json ~/.docker/

