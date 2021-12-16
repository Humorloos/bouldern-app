# Install gdal and spatialite
#if ! cache has_key usr_directory | grep -q "exists"; then
  echo "installing gdal"
  # install GDAL from ubuntugis/ppa
  # echo -ne '\n' | for automatically accepting with [ENTER]
  echo -ne '\n' | sudo add-apt-repository ppa:ubuntugis/ppa
  sudo apt-get update
  # -y for automatically answering with y
  sudo apt-get install -y libgdal-dev=2.4.2+dfsg-1~bionic0 gdal-bin=2.4.2+dfsg-1~bionic0
  export CPLUS_INCLUDE_PATH=/usr/include/gdal
  export C_INCLUDE_PATH=/usr/include/gdal
  echo "installing spatialite"
  # install spatialite
#  todo: check if spatialite is not already installed by previous command (Get:81 http://ppa.launchpad.net/ubuntugis/ppa/ubuntu bionic/main amd64 libspatialite-dev amd64 4.3.0a-5build1+bionic1 [1,370 kB])
#  cd ..
#  wget https://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0.tar.gz
#  tar xaf libspatialite-4.3.0.tar.gz
#  cd libspatialite-4.3.0 || exit
#  ./configure
#  make
#  sudo make install
#  cd ../bouldern-app || exit
  echo "caching /usr"
  cache store usr_directory /usr
#else
#  echo "/usr already in cache, skipping installation"
#fi
