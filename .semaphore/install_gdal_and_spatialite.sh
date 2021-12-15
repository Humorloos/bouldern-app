# Install gdal and spatialite
if ! cache has_key usr_directory | grep -q "exists"; then
  echo "installing gdal"
  # install GDAL from ubuntugis/ppa
  # echo -ne '\n' | for automatically accepting with [ENTER]
  echo -ne '\n' | sudo add-apt-repository ppa:ubuntugis/ppa
  sudo apt-get update
  # -y for automatically answering with y
  sudo apt-get install -y libgdal-dev gdal-bin
  export CPLUS_INCLUDE_PATH=/usr/include/gdal
  export C_INCLUDE_PATH=/usr/include/gdal
  echo "installing spatialite"
  # install spatialite
  cd ..
  wget https://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0.tar.gz
  tar xaf libspatialite-4.3.0.tar.gz
  cd libspatialite-4.3.0 || exit
  ./configure
  make
  sudo make install
  cd "$PROJECT_DIR" || exit
  echo "caching /usr"
  cache store usr_directory /usr
else
  echo "/usr already in cache, skipping installation"
fi
