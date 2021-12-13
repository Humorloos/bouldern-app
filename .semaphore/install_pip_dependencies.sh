# At this point, the cache contains the downloaded packages ...
cache restore
sem-version python 3.9
# ... so pip does the installation much faster.
pip install -r requirements.txt --cache-dir .pip_cache
# setuptools >= 58.0.0 currently (2021-11-14) don't work with gdal, so we need to downgrade to 57.5.0
# todo: define this in requirements.txt
pip install setuptools==57.5.0
# install gdal from local sources
# todo: check if pip3 is really necessary and if we can cache this too
pip3 install --global-option=build_ext --global-option="-I /usr/include/gdal" GDAL=="$(gdal-config --version)"
