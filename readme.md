### changing .env for pipeline:

run `sem delete secret env`
run `sem create secret env -f ./.env_semaphore:/home/semaphore/.env` from project directory

### changing .env for production:

run `sem delete secret env_production`
run `sem create secret env_production -f ./.env_production:/home/semaphore/.env_production` from project directory
