#!/usr/bin/env bash
sudo cp googledns_daemon.json /etc/docker/daemon.json

sudo rm /etc/systemd/system/docker.service.d/http-proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker

rm -f ~/.docker/config.json

