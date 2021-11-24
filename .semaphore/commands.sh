# Correct permissions since they are too open by default:
chmod 0600 ~/.ssh/id_rsa_semaphoreci
# Add the key to the ssh agent:
ssh-add ~/.ssh/id_rsa_semaphoreci
git clone git@github.com:Humorloos/GoogleApiHelper.git
git clone git@github.com:Humorloos/googleCalendarApp.git
# At this point, the cache contains the downloaded packages ...
cache restore
sem-version python 3.9
# ... so pip does the installation much faster.
pip install -r requirements.txt --cache-dir .pip_cache
# setuptools >= 58.0.0 currently (2021-11-14) don't work with gdal, so we need to downgrade to 57.5.0
pip install setuptools==57.5.0
# install GDAL from ubuntugis/ppa
# echo -ne '\n' | for automatically accepting with [ENTER]
echo -ne '\n' | sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
# -y for automatically answering with y
sudo apt-get install -y libgdal-dev gdal-bin
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
# install gdal from local sources
pip3 install --global-option=build_ext --global-option="-I /usr/include/gdal" GDAL==`gdal-config --version`
