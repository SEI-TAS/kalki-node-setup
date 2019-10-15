#!/usr/bin/env bash
sudo cp http-proxy.conf /etc/systemd/system/docker.service.d/
sudo systemctl daemon-reload
sudo systemctl restart docker

cp config.json ~/.docker/
