
if cache has_key googleCalendarApp | grep -q "exists"; then
  echo "Installing spatialite"
  cd ..
  wget https://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0.tar.gz
  tar xaf libspatialite-4.3.0.tar.gz
  cd libspatialite-4.3.0 || exit
  ./configure
  make
  sudo make install
  cd ../bouldern-app || exit
  cache store spatialite /usr/local/lib/mod_spatialite.so
else
  echo "Spatialite already in cache, skipping installation"
  sudo -E cache restore spatialite
fi