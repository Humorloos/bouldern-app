# install spatialite
cd ..
wget https://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0.tar.gz
tar xaf libspatialite-4.3.0.tar.gz
cd libspatialite-4.3.0
./configure
make
sudo make install
cd ../bouldern-app
