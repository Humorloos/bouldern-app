. .semaphore/frontend_prologue.sh
cd ..
cd ~/bouldern-app/frontend || exit
# todo: check if moving npm ci here breaks pipeline,
# last time it did not work in frontend_prologue
# last time it worked just at the beginning of backend_prologue.sh
# restore npm
cache restore "$NPM_KEY"
npm ci
cd ..
. .semaphore/backend_prologue.sh
