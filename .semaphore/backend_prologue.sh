# restore private repositories
cd ~ || exit
cache restore googleCalendarApp
cache restore GoogleApiHelper
# restore gdal
cache restore gdal_files
sudo cp -r /home/semaphore/gdal_files/usr /

cd "$PROJECT_DIR" || exit

# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh

python3 manage.py makemigrations
python3 manage.py migrate
