# Install private repository dependencies
cd ..
# Correct permissions since they are too open by default:
chmod 0600 ~/.ssh/id_rsa_semaphoreci
# Add the key to the ssh agent:
ssh-add ~/.ssh/id_rsa_semaphoreci
# clone repos
git clone git@github.com:Humorloos/GoogleApiHelper.git
cache store GoogleApiHelper ~/GoogleApiHelper
git clone git@github.com:Humorloos/googleCalendarApp.git
cache store googleCalendarApp ~/googleCalendarApp
cd bouldern-app || exit
