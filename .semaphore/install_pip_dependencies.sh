# At this point, the cache contains the downloaded packages ...
cache restore
# ... so pip does the installation much faster.
pip install -r requirements.txt --cache-dir .pip_cache
