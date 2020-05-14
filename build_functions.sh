#!/usr/bin/env bash

DIST_FOLDER="$PWD/dist"
BASE_PATH=../submodules

# Inits git submodules.
init_submodules() {
  git submodule update --init
}

# Gets newest changes for repo.
update_repo() {
  local repo_name="$1"
  local branch="$2"
  (cd ${BASE_PATH}/${repo_name} && git checkout ${branch} && git pull)
}

# Builds images for a lib, build env.
build_image_lib() {
  local component_folder="$1"

  # Create images.
  (cd ${BASE_PATH}/${component_folder} && bash build_dev_container.sh )
}

# Builds images and dist folders for components.
build_and_dist() {
  local component="$1"
  local component_folder="$2"

  # Create images.
  echo "---> Building component: $component"
  (cd ${BASE_PATH}/${component_folder} && bash build_container.sh )

  # Copy docker-compose configs.
  mkdir -p dist/${component}
  cp ${BASE_PATH}/${component_folder}/docker-compose.yml ${DIST_FOLDER}/${component}/

  # Execute dist scripts for specific component.
  if [ -f ${BASE_PATH}/${component_folder}/create_dist.sh ]; then
    echo "Executing dist script."
    (cd ${BASE_PATH}/${component_folder}/ && \
     bash create_dist.sh "${DIST_FOLDER}/${component}")
  fi
}
