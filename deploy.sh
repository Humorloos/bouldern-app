# pull updated version of branch from repo
cd humorloos.pythonanywhere.com || exit
git fetch --all
git reset --hard origin/"$1"

# compile vue files
cd frontend || exit
echo "setting up npm"
source ~/nvm/nvm.sh
nvm use node
export NODE_OPTIONS=--openssl-legacy-provider
echo "installing node packages"
npm ci
echo "compiling vue files"
npm run build
cd ..

# perform django migration task
source ~/.env
source ~/.virtualenvs/humorloos.pythonanywhere.com/bin/activate
pip install -r requirements.txt --upgrade
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# restart web application
touch /var/www/humorloos_pythonanywhere_com_wsgi.py
