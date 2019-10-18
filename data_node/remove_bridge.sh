#!/usr/bin/env bash

IOT_NIC=enp2s0f0
EXT_NIC=enp2s0f1

sudo ovs-vsctl del-br ovs-br
sudo ovs-vsctl del-br ovs-iot
sudo ovs-vsctl del-br ovs-ext

sudo ifdown $EXT_NIC
sudo ifup $EXT_NIC
sudo ifdown $IOT_NIC
sudo ifup $IOT_NIC

cd hertz
bash kalki_network.sh