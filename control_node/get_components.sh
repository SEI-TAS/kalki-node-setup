#!/bin/bash

# Include functions.
source ../build_functions.sh

# Ensure repos are initialized.
init_submodules

# Get updated repo info.
update_repo "kalki-db" dev
update_repo "kalki-umbox-controller" dev
update_repo "kalki-main-controller" dev
update_repo "kalki-device-controller" dev

