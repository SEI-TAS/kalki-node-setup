#!/usr/bin/env bash
sudo iptables -A FORWARD -o enp0s31f6 -i enp2s0f0 -s 10.27.153.0/24 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -t nat -F POSTROUTING
sudo iptables -t nat -A POSTROUTING -o enp0s31f6 -j MASQUERADE