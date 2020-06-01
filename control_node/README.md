# Node-Setup - Control Node

## Prerequisites
- Git is needed to get this repo and to be able to pull the dependent repos.
- Docker and Docker-Compose 1.16.0+ are needed to run the different components.

Note that Docker and Docker-Compose can be installed in Debian/Ubuntu with `bash install_packages,sh`. If installing in a different distribution, you may to install these components some other way.

## Configuration
Each dependent repo has its own configuration. However, using the default configuration for all Control Node components should be enough for most deployments.

## Building
To download dependent repos (this needs to be executed every time there is a change to the dependent repos):

`bash get_components.sh`

NOTE: If building on a Raspberry Pi or another ARM32 platform, you'll have to run this script before attempting to build the components to get the custom gradle images needed for this platform:

`bash ../deployments/pi/create_gradle_image.sh`

To build all dependent components:

`bash build_all.sh`

## Deployment
If running from the same computer where the build was generated, no deployment is needed.

It is possible to create a distribution tar.gz that can be copied to a deployment installation, and contains all that is needed to run the components. To generate such a file and deploy it in another computer, follow these steps. Note that this assumes that `gz` is available on the build computer, and `tar` is available on the deployment computer.

1. Execute `bash export.sh`
1. Copy the `control_node_dist.tar.gz` file and the file `import.sh` to the deployment computer
1. Ensure that Docker is installed in the deployment computer
1. Install the deployment executing `bash import.sh`

## Running
To run all components in a unified docker-compose instance, execute this script from the folder it is in:

`bash run_all.sh`

If you Ctrl+C, docker-compose will continue running the components. To see the logs again:

`bash compose_logs.sh`

To stop the docker-compose instance:

`bash stop_all.sh`

