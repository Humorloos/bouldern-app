checkout
# clone private repositories
. ./.semaphore/private_repos.sh
# install gdal
. ./.semaphore/install_gdal.sh
# install spatialite
. ./.semaphore/install_spatialite.sh
# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh
