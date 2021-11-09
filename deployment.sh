# pull updated version of branch from repo
cd humorloos.pythonanywhere.com
git fetch --all
git reset --hard origin/$1

# perform django migration task
source ~/.env
source ~/.virtualenvs/humorloos.pythonanywhere.com/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput

# restart web application
touch /var/www/humorloos_pythonanywhere_com_wsgi.py
