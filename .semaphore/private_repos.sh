# Install private repository dependencies
GoogleApiHelper_cached=$(cache has_key GoogleApiHelper)
googleCalendarApp_cached=$(cache has_key googleCalendarApp)

if [[ $GoogleApiHelper_cached == *"exists"* ]] && [[ $googleCalendarApp_cached == *"exists"* ]]; then
  echo "Private repositories already in cache, skipping installation"
else
  # Correct permissions since they are too open by default:
  chmod 0600 ~/.ssh/id_rsa_semaphoreci
  # Add the key to the ssh agent:
  ssh-add ~/.ssh/id_rsa_semaphoreci
  cd ..
  # clone repos if necessary
  if [[ $GoogleApiHelper_cached == *"doesn't"* ]]; then
    echo "Installing and caching private repository GoogleApiHelper"
    git clone git@github.com:Humorloos/GoogleApiHelper.git
    cache store GoogleApiHelper ~/GoogleApiHelper
  fi
  if [[ $googleCalendarApp_cached == *"doesn't"* ]]; then
    echo "Installing and caching private repository googleCalendarApp"
    git clone git@github.com:Humorloos/googleCalendarApp.git
    cache store googleCalendarApp ~/googleCalendarApp
  fi
  cd "$PROJECT_DIR" || exit
fi
