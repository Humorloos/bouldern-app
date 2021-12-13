# restore private repositories
cache restore googleCalendarApp
cache restore GoogleApiHelper
checkout
# install gdal
. ./.semaphore/install_gdal.sh
# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh
