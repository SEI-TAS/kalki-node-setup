#!/usr/bin/env bash

chmod ugo+x setup_bridge.sh
cp setup_ovs.service /etc/systemd/system/
systemctl enable setup_ovs
systemctl start setup_ovs
