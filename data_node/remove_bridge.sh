#!/usr/bin/env bash

IOT_NIC=ens6
EXT_NIC=ens5

sudo ovs-vsctl del-br ovs-br
sudo ovs-vsctl del-br ovs-iot
sudo ovs-vsctl del-br ovs-ext

sudo ifdown $EXT_NIC
sudo ifup $EXT_NIC
sudo ifdown $IOT_NIC
sudo ifup $IOT_NIC
