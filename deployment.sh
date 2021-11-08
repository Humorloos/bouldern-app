# pull updated version of branch from repo
cd ${SSH_USER}.pythonanywhere.com
git fetch --all
git reset --hard origin/$SEMAPHORE_GIT_BRANCH

# perform django migration task
workon ${SSH_USER}.pythonanywhere.com
python manage.py migrate

# restart web application
touch /user/Humorloos/files/var/www/${SSH_USER}_pythonanywhere_com_wsgi.py