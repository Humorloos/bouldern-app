checkout

nvm use
cd frontend || exit
# restore npm
cache restore "$NPM_KEY"
npm ci
