#nvm use
ls
ls "$PROJECT_DIR"
cd "$FRONTEND_DIR" || exit
cache restore "$NPM_KEY"
cache restore "$CYPRESS_KEY"
npm ci
