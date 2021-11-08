lower_ssh_user=$(echo ${SSH_USER} | tr A-Z a-z)
lower_ssh_user=$(echo Humorloos | tr A-Z a-z)
# pull updated version of branch from repo
cd ${lower_ssh_user}.pythonanywhere.com
echo ${lower_ssh_user}.pythonanywhere.com
git fetch --all
echo origin/$SEMAPHORE_GIT_BRANCH
git reset --hard origin/$SEMAPHORE_GIT_BRANCH

# perform django migration task
workon ${lower_ssh_user}.pythonanywhere.com
python manage.py migrate

# restart web application
touch /var/www/${lower_ssh_user}_pythonanywhere_com_wsgi.py
echo /var/www/${lower_ssh_user}_pythonanywhere_com_wsgi.py