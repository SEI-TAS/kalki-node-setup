#!/usr/bin/env bash

IOT_NIC=enp2s0f1
EXT_NIC=enp2s0f0

IOT_NIC_IP=10.27.151.127
EXT_NIC_IP=10.27.152.6

IOT_NIC_BROADCAST=10.27.151.255
EXT_NIC_BROADCAST=10.27.152.255

sudo ovs-vsctl del-br ovs-br

sudo ifdown $EXT_NIC
sudo ifup $EXT_NIC
sudo ifdown $IOT_NIC
sudo ifup $IOT_NIC

sudo ip addr add ${IOT_NIC_IP}/24 dev $IOT_NIC
sudo ip addr add ${EXT_NIC_IP}/24 dev $EXT_NIC

sudo ifconfig $IOT_NIC broadcast ${IOT_NIC_BROADCAST}
sudo ifconfig $EXT_NIC broadcast ${EXT_NIC_BROADCAST}
