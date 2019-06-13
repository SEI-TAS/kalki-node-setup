#!/usr/bin/env bash
sudo route delete default gw 192.168.58.1 ens4
sudo route add default gw 192.168.122.1 ens3
