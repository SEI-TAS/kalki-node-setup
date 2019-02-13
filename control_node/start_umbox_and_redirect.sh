#!/usr/bin/env bash

DATA_NODE_IP=192.168.58.102
UMBOX_IMAGE_NAME=umbox-sniffer
IOT_DEVICE_DB_ID=1
IOT_DEVICE_IP=192.168.56.103

UMBOX_OVS_PORT="$(python umbox.py -c start -s $DATA_NODE_IP -d $IOT_DEVICE_DB_ID -i $UMBOX_IMAGE_NAME)"
echo "${UMBOX_OVS_PORT}"
python ovs.py -c add_rule -s $DATA_NODE_IP -d $IOT_DEVICE_IP -o $UMBOX_OVS_PORT
