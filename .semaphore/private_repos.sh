# Install private repository dependencies
cd ..
# Correct permissions since they are too open by default:
chmod 0600 ~/.ssh/id_rsa_semaphoreci
# Add the key to the ssh agent:
ssh-add ~/.ssh/id_rsa_semaphoreci
# clone repos
git clone git@github.com:Humorloos/GoogleApiHelper.git
git clone git@github.com:Humorloos/googleCalendarApp.git
cd bouldern-app
