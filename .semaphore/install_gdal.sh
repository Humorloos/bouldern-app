# install GDAL from ubuntugis/ppa
# echo -ne '\n' | for automatically accepting with [ENTER]
echo -ne '\n' | sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
# -y for automatically answering with y
sudo apt-get install -y libgdal-dev gdal-bin
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
