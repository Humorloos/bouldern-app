if [[ $(git log -1 --pretty=%B) == "chore(release): "* ]]; then
  echo "Skipping deployment to pythonanywhere due to release commit"
else
  chmod 0600 ~/.ssh/id_rsa_pa
  ssh-keyscan -H ssh.pythonanywhere.com >> ~/.ssh/known_hosts
  ssh-add ~/.ssh/id_rsa_pa
  cd ~ || exit
  sftp "${SSH_USER}"@ssh.pythonanywhere.com <<< $'put bouldern-app/deploy.sh deploy.sh\n put .env_production .env'
  # shellcheck disable=SC2029
  ssh "${SSH_USER}"@ssh.pythonanywhere.com bash deploy.sh "${SEMAPHORE_GIT_PR_BRANCH-master}"
fi
