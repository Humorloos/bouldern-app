checkout


# after checkout ---
nvm use
node --version
npm --version
cd frontend || exit
# restore node_modules
cache restore node_modules
npm update
npm install
