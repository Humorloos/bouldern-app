### Windows build

install GDAL version `GDAL‑3.2.3‑cp39‑cp39‑win_amd64.whl` from https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal (source: https://gis.stackexchange.com/a/7617/195769)

### Updating requirements.txt:

run `pip list --format=freeze > requirements.txt` so that GDAL is included as version and not as direct reference (source: https://stackoverflow.com/questions/62885911/pip-freeze-creates-some-weird-path-instead-of-the-package-version)

### changing .env:
run `sem create secret env -f ./.env:/home/semaphore/.env` from project directory
