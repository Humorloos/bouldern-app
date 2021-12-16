# restore private repositories
cache restore googleCalendarApp
cache restore GoogleApiHelper
sudo -E cache restore usr_directory
# restore gdal
cache restore gdal_files
sudo cp -r /home/semaphore/gdal_files/usr /

checkout
# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh
