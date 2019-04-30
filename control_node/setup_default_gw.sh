#!/usr/bin/env bash
sudo route delete default gw 192.168.57.1 ens5
sudo route add default gw 192.168.122.1 ens3
