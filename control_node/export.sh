#!/usr/bin/env bash

EXPORT_FOLDER=export

source ../run_functions.sh

rm -r ${EXPORT_FOLDER}
mkdir -p ${EXPORT_FOLDER}

cp run_functions.sh ${EXPORT_FOLDER}/
cp run_all.sh ${EXPORT_FOLDER}/
cp stop_all.sh ${EXPORT_FOLDER}/
cp compose_logs.sh ${EXPORT_FOLDER}/
cp install_packages.sh ${EXPORT_FOLDER}/
cp README.md ${EXPORT_FOLDER}/

cp -R ./dist cp ${EXPORT_FOLDER}/dist

export_image "kalki-db"
export_image "kalki-umbox-controller"
export_image "kalki-main-controller"
export_image "kalki-device-controller"
