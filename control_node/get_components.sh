#!/bin/bash

# Include functions.
source ../build_functions.sh

# Ensure repos are initialized.
init_submodules

# Get updated repo info.
BRANCH=1.6.0
update_repo "kalki-db" $BRANCH
update_repo "kalki-umbox-controller" $BRANCH
update_repo "kalki-main-controller" $BRANCH
update_repo "kalki-device-controller" $BRANCH

