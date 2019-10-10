#!/usr/bin/env bash
sudo ip route add default via 10.27.153.3
echo "nameserver 10.64.28.100" | sudo tee /etc/resolv.conf.d/tail
sudo resolvconf -u
