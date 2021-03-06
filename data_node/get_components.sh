#!/bin/bash

# Include functions.
source ../build_functions.sh

# Ensure repos are initialized.
init_submodules

# Get updated repo info.
BRANCH=dev
update_repo "kalki-db" $BRANCH
update_repo "kalki-iot-interface" $BRANCH
update_repo "kalki-umbox-controller" $BRANCH
