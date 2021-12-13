# restore private repositories
cache restore googleCalendarApp
cache restore GoogleApiHelper
checkout
# install gdal
. ./.semaphore/install_gdal.sh
# install spatialite
. ./.semaphore/install_spatialite.sh
# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh
