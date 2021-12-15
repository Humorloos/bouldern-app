# restore private repositories
cd ~ || exit
cache restore googleCalendarApp
cache restore GoogleApiHelper
sudo -E cache restore usr_directory

cd "$PROJECT_DIR" || exit

# install pip dependencies
. ./.semaphore/install_pip_dependencies.sh

python manage.py makemigrations
python manage.py migrate
# todo: cache cypress binary like in https://github.com/cypress-io/cypress-example-kitchensink/blob/master/basic/.semaphore.yml
