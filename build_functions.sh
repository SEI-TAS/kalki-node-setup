#!/usr/bin/env bash

DIST_FOLDER="$PWD/dist"
BASE_PATH=../submodules

# Inits git submodules.
init_submodules() {
  git submodule update --init
}

# Copies deployment configs to dist folder.
copy_deployment_configs() {
  local deployment="$1"
  local node_name="$2"

  # Check if we got the deployment.
  if [ -z $deployment ]; then
    echo "Deployment name for configuration needs to be passed as an argument."
    exit 1
  fi

  # Check if the given deployment exists.
  local deployment_path="../deployments/$deployment"
  if [ ! -d $deployment_path ]; then
    echo "Given deployment not found: $deployment_path"
    exit 1
  fi

  echo "Copying configurations for deployment:"
  cp -r -v $deployment_path/$node_name/* ${BASE_PATH}/
}

# Gets newest changes for repo.
update_repo() {
  local repo_name="$1"
  local branch="$2"
  (cd ${BASE_PATH}/${repo_name} && git checkout -- . && git checkout ${branch} && git pull)
}

# Builds images for a lib, build env.
build_image_lib() {
  local component_folder="$1"

  # Create images.
  (cd ${BASE_PATH}/${component_folder} && bash build_dev_container.sh )
}

# Builds images and dist folders for component.
build_and_dist() {
  local component="$1"
  local component_folder="$2"

  if [ -z $component_folder ]; then
    component_folder=$component
  fi

  # Create images.
  echo ":::: Building component: $component"
  (cd ${BASE_PATH}/${component_folder} && bash build_container.sh )

  # Copy docker-compose configs.
  mkdir -p ${DIST_FOLDER}/${component}
  cp ${BASE_PATH}/${component_folder}/docker-compose.yml ${DIST_FOLDER}/${component}/

  # Execute dist scripts for specific component.
  if [ -f ${BASE_PATH}/${component_folder}/create_dist.sh ]; then
    echo "Executing dist script."
    (cd ${BASE_PATH}/${component_folder}/ && \
     bash create_dist.sh "${DIST_FOLDER}/${component}")
  fi
}
