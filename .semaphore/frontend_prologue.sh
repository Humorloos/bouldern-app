checkout


# after checkout ---
nvm use
node --version
npm --version
cd frontend || exit
# restore node_modules
cache restore node_modules
# see https://community.atlassian.com/t5/Bitbucket-questions/Module-not-found-Error-Can-t-resolve-cypress-file-upload-in-opt/qaq-p/1184319
npm update
npm install
