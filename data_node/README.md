# Node-Setup - Data Node

## Prerequisites
- Git is needed to get this repo and to be able to pull the dependent repos.
- Docker and Docker-Compose 1.16.0+ are needed to run the different components.

Note that Docker and Docker-Compose can be installed in Debian/Ubuntu with `bash install_packages,sh`. If installing in a different distribution, you may to install these components some other way.

## Configuration
Each dependent repo has its own configuration. For the Data Node, there are two components that need specific configurations ovs-docker-server and kalki-iot-interface. More specifically, ovs-docker-server needs to have the 3 NICs of the Data Node properly configured, as well as the contorl plane network and IP of the control node. The kalki-iot-interface needs to be configured to have the proper Control Node IP address. See details of their config files in the corresponding repos (kalki-umbox-controller/ovs-docker-server and kalki-iot-interface).

Once you have a proper configuration for the components, create a folder in the `deployments` folder in the root of this repo for your deployment, and inside a subfolder call `data_node`. Inside this, create sub-folders for each dependent repo that has a configuration with that repo's name. Inside put the configuration files that are needed, using the same folder structure from their respective repos.

## Building
NOTE: If building on a Raspberry Pi or another ARM32 platform, you'll have to run this script before attempting to build the components to get the custom gradle images needed for this platform (this only needs to be done once per machine):

`bash ../platforms/pi/create_gradle_image.sh`

To download dependent repos (this needs to be executed every time there is a change to the dependent repos)

`bash get_components.sh`

Note that this assumes you have SSH Github access configured in the computer you are running this on.

To build all dependent components:

`bash build_all.sh <deployment>`

Where <deployment> refers to a set of configurations for the specific deployment being built. This has to match a subfolder inside the `deployments` folder in the root of this repo. See the Configuration section for more information about the contents of this folder.

## Deployment
If running from the same computer where the build was generated, no deployment is needed.

It is possible to create a distribution tar.gz that can be copied to a deployment installation, and contains all that is needed to run the components. To generate such a file and deploy it in another computer, follow these steps. Note that this assumes that `gz` is available on the build computer, and `tar` is available on the deployment computer.

1. Execute `bash export.sh`
1. Copy the `data_node_dist.tar.gz` file and the file `import.sh` to the deployment computer
1. Ensure that Docker is installed in the deployment computer
1. Install the deployment executing `bash import.sh`

## Running
To run all components in a unified docker-compose instance, execute this script from the folder it is in:

`bash run_all.sh`

If you Ctrl+C, docker-compose will continue running the components. To see the logs again:

`bash compose_logs.sh`

To stop the docker-compose instance:

`bash stop_all.sh`

