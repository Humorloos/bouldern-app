#before checkout

# restore private repositories
cd ~ || exit
cache restore googleCalendarApp
cache restore GoogleApiHelper
sudo -E cache restore usr_directory

cd ~/bouldern-app || exit

# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh

python manage.py makemigrations
python manage.py migrate