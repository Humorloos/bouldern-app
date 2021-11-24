# pull updated version of branch from repo
cd humorloos.pythonanywhere.com
git fetch --all
git reset --hard origin/$1

# compile vue files
cd frontend
npm ci
npm run build
cd ..

# perform django migration task
source ~/.env
source ~/.virtualenvs/humorloos.pythonanywhere.com/bin/activate
pip install -r requirements.txt --upgrade
# dataclasses leads to error with pandas (see https://github.com/huggingface/transformers/issues/8638)
pip uninstall dataclasses -y
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# restart web application
touch /var/www/humorloos_pythonanywhere_com_wsgi.py
