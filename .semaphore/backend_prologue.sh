#before checkout

# restore private repositories
cd ~ || exit
cache restore googleCalendarApp
cache restore GoogleApiHelper
# restore gdal
cache restore gdal_files
sudo cp -r /home/semaphore/gdal_files/usr /

cd ~/bouldern-app || exit

# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh

python manage.py makemigrations
python manage.py migrate
