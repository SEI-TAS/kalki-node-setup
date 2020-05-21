# Node-Setup - Control Node

## Prerequisites
- Git is needed to get this repo and to be able to pull the dependent repos.
- Docker and Docker-Compose 1.16.0+ are needed to run the different components.

Note that Docker and Docker-Compose can be installed in Debian/Ubuntu with `bash install_packages,sh`. If installing in a different distribution, you may to install these components some other way.

## Configuration
See the configuration details for each dependent repo.

## Usage
To download dependent repos (this needs to be executed every time there is a change to the dependent repos):

`bash get_components.sh`

To build all dependent components:

`bash build_all.sh`

Note that this will create a "dist" folder. The control_node folder, along with this dist subfolder, can be moved to a deployment installation, and contains all that is needed to run the components, except for the docker images, which need to be exported as well.

To run all components in a unified docker-compose instance:

`bash run_all.sh`

If you Ctrl+C, docker-compose will continue running the components. To see the logs again:

`bash compose_logs.sh`

To stop the docker-compose instance:

`bash stop_all.sh`

