#!/usr/bin/env bash

sudo ovs-vsctl del-br ovs-br
sudo ovs-vsctl del-br ovs-iot
sudo ovs-vsctl del-br ovs-ext

sudo ifdown ens5
sudo ifup ens5
sudo ifdown ens6
sudo ifup ens6
