# restore private repositories
cache restore googleCalendarApp,GoogleApiHelper
checkout
#. ./.semaphore/private_repos.sh
# install gdal
. ./.semaphore/install_gdal.sh
# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh
