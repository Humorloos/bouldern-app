# restore private repositories
cache restore googleCalendarApp
cache restore GoogleApiHelper
sudo -E cache restore usr_directory

checkout
# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh