#!/usr/bin/env bash

EXPORT_FOLDER=control_node_dist

source ../run_functions.sh

echo "Recreating folder..."
rm -r ${EXPORT_FOLDER}
mkdir -p ${EXPORT_FOLDER}

echo "Copying scripts..."
cp run_functions.sh ${EXPORT_FOLDER}/
cp run_all.sh ${EXPORT_FOLDER}/
cp stop_all.sh ${EXPORT_FOLDER}/
cp compose_logs.sh ${EXPORT_FOLDER}/
cp install_packages.sh ${EXPORT_FOLDER}/
cp README.md ${EXPORT_FOLDER}/

echo "Copying distribution (docker compose files and component scripts)..."
cp -R ./dist ${EXPORT_FOLDER}/

echo "Exporting docker images..."
export_image "kalki-postgres"
export_image "kalki-umbox-controller"
export_image "kalki-main-controller"
export_image "kalki-device-controller"

echo "Creating compressed output file..."
tar-zcvf control_node_dist.tar.gz ./${EXPORT_FOLDER}

#echo "Deleting temporary folder"
#rm -r ${EXPORT_FOLDER}

echo "Finished"
