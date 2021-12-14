. .semaphore/frontend_prologue.sh
cd ..
. .semaphore/backend_prologue.sh

python manage.py runserver &
cd frontend || exit
npm run serve &
