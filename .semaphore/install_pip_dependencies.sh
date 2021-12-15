# At this point, the cache contains the downloaded packages ...
cache restore
sem-version python 3.9
# ... so pip does the installation much faster.
pip install -r requirements.txt --cache-dir .pip_cache
# install gdal from local sources
pip install --global-option=build_ext --global-option="-I /usr/include/gdal" GDAL=="$(gdal-config --version)"
#todo: set cypress priority over eslint in pipeline
