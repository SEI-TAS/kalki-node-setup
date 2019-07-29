#!/usr/bin/env bash
NETWORK_NAME=$1

sudo virsh net-destroy ${NETWORK_NAME}
sudo virsh net-undefine ${NETWORK_NAME}
sudo virsh net-define ${NETWORK_NAME}.xml
sudo virsh net-autostart ${NETWORK_NAME}
sudo virsh net-start ${NETWORK_NAME}
