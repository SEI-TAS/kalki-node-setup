#!/bin/bash

update_repo() {
  local repo_name="$1"
  local branch="$2"
  (cd ${repo_name} && git checkout ${branch} && git pull)
}

(git submodule update --init && \
 cd ../submodules && \
 update_repo "kalki-iot-interface" dev && \
 update_repo "kalki-umbox-controller" dev )
