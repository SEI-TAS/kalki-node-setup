# Node-Setup - Data Node

## Prerequisites
- Git is needed to get this repo and to be able to pull the dependent repos.
- Java 8 is needed to compile the dependent repos.
- Docker and Docker-Compose are needed to run the different components.

Note that Java 8, Docker and Docker-Compose can be installed in Debian/Ubuntu with `bash install_packages,sh`. If installing in a different distribution, you may to install these components some other way.

## Configuration
See the configuration details for each dependent repo.

## Usage
To download dependent repos (this needs to be executed every time there is a change to the dependent repos):

`bash download_components.sh <git_username>`

To build all dependent components:

`bash build_all.sh`

To run all components in an unified docker-compose instance:

`bash run_all.sh`

If you Ctrl+C, docker-compose will continue running the components. To see the logs again:

`bash compose_logs.sh`

To stop the docker-compose instance:

`bash stop_all.sh`

