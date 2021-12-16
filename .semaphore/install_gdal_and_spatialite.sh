# Install gdal and spatialite
if ! cache has_key gdal_files | grep -q "exists"; then
  # install GDAL from ubuntugis/ppa
  echo "installing gdal"
  # echo -ne '\n' | for automatically accepting with [ENTER]
  echo -ne '\n' | sudo add-apt-repository ppa:ubuntugis/ppa
  sudo apt-get update
  # -y for automatically answering with y
  sudo apt-get install -y libgdal-dev=2.4.2+dfsg-1~bionic0 gdal-bin=2.4.2+dfsg-1~bionic0

  # install spatialite, this requires installing gdal first
  echo "installing spatialite"
  cd ..
  wget https://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0.tar.gz
  tar xaf libspatialite-4.3.0.tar.gz
  cd libspatialite-4.3.0 || exit
  ./configure
  make
  sudo make install
  cd "$PROJECT_DIR" || exit

  # copy all files in gdal_files to gdal_paths folder for caching
  while read -r p; do
    mkdir --parents "$(dirname ~/gdal_files"$p")"
    cp -r "$p" ~/gdal_files"$p"
  done < /home/semaphore/bouldern-app/.semaphore/gdal_paths
  # cache collected files
  cache store gdal_files /home/semaphore/gdal_files
else
  echo "gdal_files already in cache, skipping installation"
fi
