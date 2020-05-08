#!/bin/bash

get_and_update_repo() {
  local repo_name="$1"

  if [ ! -d "${repo_name}" ]; then
    git clone git@github.com:SEI-TAS/${repo_name}.git
    git checkout dev
  fi

  git pull

}

mkdir -p repos
cd repos

get_and_update_repo "kalki-iot-interface"
get_and_update_repo "kalki-umbox-controller"

cd ..
