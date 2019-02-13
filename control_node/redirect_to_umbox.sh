#!/usr/bin/env bash
# $1: IP address of data node.
# $2: IP address of device to redirect traffic from.
# $3: OVS port to redirect traffic to.
# $4: OVS port the outside world is reachable through.
# $5: OVS port the device is reachable through.
python ovs.py -c add_rule -s $1 -di $2 -i $4 -o $3 -p 100
python ovs.py -c add_rule -s $1 -si $2 -i $5 -o $3 -p 100
python ovs.py -c add_rule -s $1 -di $2 -i $3 -o $5 -p 110
python ovs.py -c add_rule -s $1 -si $2 -i $3 -o $4 -p 110
