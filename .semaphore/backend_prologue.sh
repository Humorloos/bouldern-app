# restore private repositories
cd frontend || exit
# todo: check if moving npm ci here breaks pipeline,
# last time it did not work in frontend_prologue
#  last time it worked just before installing pip dependencies
npm ci
cd ..
cd ~ || exit
cache restore googleCalendarApp
cache restore GoogleApiHelper
sudo -E cache restore usr_directory

cd ~/bouldern-app || exit

# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh

python manage.py makemigrations
python manage.py migrate
