#!/bin/bash

rm -r components
mkdir -p components
cd components

wget https://github.com/SEI-TAS/kalki-iot-interface/archive/master.zip
unzip master.zip

wget https://github.com/SEI-TAS/kalki-umbox-controller/archive/master.zip
unzip master.zip

rm master.zip
