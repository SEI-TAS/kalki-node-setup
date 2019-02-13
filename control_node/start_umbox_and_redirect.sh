#!/usr/bin/env bash

DATA_NODE_IP=192.168.58.102
UMBOX_IMAGE_NAME=umbox-sniffer
IOT_DEVICE_DB_ID=1
IOT_DEVICE_IP=192.168.56.103

IOT_DEVICE_OVS_PORT=1
EXT_OVS_PORT=2

UMBOX_OVS_PORT="$(python umbox.py -c start -s $DATA_NODE_IP -d $IOT_DEVICE_DB_ID -i $UMBOX_IMAGE_NAME)"
echo "${UMBOX_OVS_PORT}"
bash redirect_to_umbox.sh $DATA_NODE_IP $IOT_DEVICE_IP $UMBOX_OVS_PORT $IOT_DEVICE_OVS_PORT $EXT_OVS_PORT
