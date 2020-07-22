# Kalki Node Setup

This repository contains configurations and scripts useful to set up each node, or specific deployments. More specifically:

- control_node: has all scripts needed to setup and install all non-UI components of the Control Node as docker containers using docker compose.
- data_node: has all scripts needed to setup and install all non-UI components of the Data Node as docker containers using docker compose.
- deployments: has scripts needed to set up additional configurations in specific deployment instances.
- submodules: used by control_node and data_node scripts to download dependent repositories.

Kalki is an IoT platform for allowing untrusted IoT devices to connect to a network in a secure way, protecting both the IoT device and the network from malicious attackers.

Kalki comprises a total of 8 GitHub projects:
- kalki-node-setup (Kalki Main Repository, composes all non-UI components)
- kalki-controller (Kalki Main Controller)
- kalki-umbox-controller (Kalki Umbox Controller)
- kalki-device-controller (Kalki Device Controller)
- kalki-dashboard (Kalki Dashboard)
- kalki-db (Kalki Database Library)
- kalki-iot-interface (Kalki IoT Interface)
- kalki-umboxes (Kalki Umboxes, sample umboxes and umboxes components)
