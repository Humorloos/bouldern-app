. .semaphore/frontend_prologue.sh
cd ..
. .semaphore/backend_prologue.sh
cd frontend || exit
npm ci
cd ..
# todo: check if moving npm ci here (beginning of jobs) breaks pipeline, if not, move into end of e2e_prologue and further until pipeline breaks
