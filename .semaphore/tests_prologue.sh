# Install private repository dependencies
# Correct permissions since they are too open by default:
chmod 0600 ~/.ssh/id_rsa_semaphoreci
# Add the key to the ssh agent:
ssh-add ~/.ssh/id_rsa_semaphoreci
# clone repos
git clone git@github.com:Humorloos/GoogleApiHelper.git
git clone git@github.com:Humorloos/googleCalendarApp.git
# install GDAL from ubuntugis/ppa
# echo -ne '\n' | for automatically accepting with [ENTER]
echo -ne '\n' | sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
# -y for automatically answering with y
sudo apt-get install -y libgdal-dev gdal-bin
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
# install spatialite
wget https://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0.tar.gz
tar xaf libspatialite-4.3.0.tar.gz
cd libspatialite-4.3.0
./configure
make
sudo make install
cd ..
checkout
# At this point, the cache contains the downloaded packages ...
cache restore
sem-version python 3.9
# ... so pip does the installation much faster.
pip install -r requirements.txt --cache-dir .pip_cache
# setuptools >= 58.0.0 currently (2021-11-14) don't work with gdal, so we need to downgrade to 57.5.0
pip install setuptools==57.5.0
# install gdal from local sources
pip3 install --global-option=build_ext --global-option="-I /usr/include/gdal" GDAL==`gdal-config --version`
cache store