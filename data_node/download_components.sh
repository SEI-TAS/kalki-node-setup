#!/bin/bash

GIT_USER=$1

get_and_update_repo() {
  local repo_name="$1"
  local git_user="$2"

  if [ ! -d "${repo_name}" ]; then
    git clone https:/${git_user}@github.com/SEI-TAS/${repo_name}.git
  fi

  (cd ${repo_name} && git checkout dev && git pull)
}

(mkdir -p ../../kalki-repos/dn && \
 cd ../../kalki-repos/dn && \
 get_and_update_repo "kalki-iot-interface" ${GIT_USER} && \
 get_and_update_repo "kalki-umbox-controller" ${GIT_USER} )
