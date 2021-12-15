. .semaphore/frontend_prologue.sh
npm ci
cd ..
. .semaphore/backend_prologue.sh
# todo: check if moving npm ci here (beginning of jobs) breaks pipeline, if not, move into end of e2e_prologue and further until pipeline breaks
