#!/bin/bash

# Include functions.
source ../build_functions.sh

# Ensure repos are initialized.
init_submodules

# Get updated repo info.
update_repo "kalki-iot-interface" dev
update_repo "kalki-umbox-controller" dev
