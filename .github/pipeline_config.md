### pipeline secrets:
#### .env for pipeline:
- run `sem delete secret env`
- run `sem create secret env -f ./.env:/root/.env` from directory .semaphore/secrets

#### .env for production:
- run `sem delete secret env_production`
- run `sem create secret env_production -f ./.env_production:/root/.env_production` from directory .semaphore/secrets

#### github ssh key for private repos:
- run `sem delete secret private-repo`
- run `sem create secret private-repo -f ./.ssh/id_rsa_semaphoreci:/root/.ssh/id_rsa_semaphoreci` from directory .semaphore/secrets

#### pythonanywhere ssh key:
- run `sem delete secret pythonanywhere-credentials`
- run `sem create secret pythonanywhere-credentials -f ./.ssh/id_rsa_pa:/root/.ssh/id_rsa_pa` from directory .semaphore/secrets

#### github ssh key for release pushes:
- run `sem delete secret github-push-key`
- run `sem create secret github-push-key -f ./.ssh/id_rsa_semaphoreci_push:/root/.ssh/id_rsa_semaphoreci_push` from directory .semaphore/secrets

#### google play publisher service account key:
- run `sem delete secret gpp-key`
- run `sem create secret gpp-key -f ./gpp-key.json:/root/gpp-key.json` from directory .semaphore/secrets

#### android release keystore:
- run `sem delete secret release-keystore`
- run `sem create secret release-keystore -f ./release-keystore.jks:/root/release-keystore.jks` from directory .semaphore/secrets
