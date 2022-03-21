# pull updated version of branch from repo
cd humorloos.pythonanywhere.com || exit

# fetch repository
git fetch --all
git reset --hard origin/"$1"

# compile vue files
echo "setting up npm"
source ~/nvm/nvm.sh
nvm use node
export NODE_OPTIONS=--openssl-legacy-provider
cd frontend || exit
echo "installing node packages"
npm ci
echo "compiling vue files"
npx vite build
cd ..

# make database backup
sqlite3 db.sqlite ".backup db.backup.sqlite"

# perform django migration task
source ~/.env
source ~/.virtualenvs/humorloos.pythonanywhere.com/bin/activate
pip install -r requirements.txt --upgrade
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# restart web application
touch /var/www/humorloos_pythonanywhere_com_wsgi.py
