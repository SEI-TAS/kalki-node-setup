# Node-Setup - Data Node

## Prerequisites
- Git is needed to get this repo and to be able to pull the dependent repos.
- Docker and Docker-Compose 1.16.0+ are needed to run the different components.

Note that Docker and Docker-Compose can be installed in Debian/Ubuntu with `bash install_packages,sh`. If installing in a different distribution, you may to install these components some other way.

## Configuration
Each dependent repo has its own configuration. For the Data Node, there are two components that need specific configurations ovs-docker-server and kalki-iot-interface. More specifically, ovs-docker-server needs to have the 3 NICs of the Data Node properly configured, as well as the contorl plane network and IP of the control node. The kalki-iot-interface needs to be configured to have the proper Control Node IP address. See details of their config files in the corresponding repos (kalki-umbox-controller/ovs-docker-server and kalki-iot-interface).

Once you have a proper configuration for the components, create a folder in the `deployments` folder in the root of this repo for your deployment, and inside a subfolder call `data_node`. Inside this, create sub-folders for each dependent repo that has a configuration with that repo's name. Inside put the configuration files that are needed, using the same folder structure from their respective repos.

## Building
To download dependent repos (this needs to be executed every time there is a change to the dependent repos):

`bash get_components.sh`

NOTE: If building on a Raspberry Pi or another ARM32 platform, you'll have to run this script before attempting to build the components to get the custom gradle images needed for this platform:

`bash ../deployments/pi/create_gradle_image.sh`

To build all dependent components:

`bash build_all.sh <deployment>`

Where <deployment> refers to a set of configurations for the specific deployment being built. This has to match a subfolder inside the `deployments` folder in the root of this repo. See the Configuration section for more information about the contents of this folder.

Note that this will create a "dist" folder. The data_node folder, along with this dist subfolder, can be moved to a deployment installation, and contains all that is needed to run the components, except for the docker images, which need to be exported as well.

## Running
To run all components in a unified docker-compose instance, execute this either from this repo folder, or from a generated distribution folder:

`bash run_all.sh`

If you Ctrl+C, docker-compose will continue running the components. To see the logs again:

`bash compose_logs.sh`

To stop the docker-compose instance:

`bash stop_all.sh`

