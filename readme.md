### changing .env for pipeline:

- run `sem delete secret env`
- run `sem create secret env -f ./.env_semaphore:/home/semaphore/.env` from project directory

### changing .env for production:

- run `sem delete secret env_production`
- run `sem create secret env_production -f ./.env_production:/home/semaphore/.env_production` from project directory

### setting up virtualenv on server:
- `mkvirtualenv humorloos.pythonanywhere.com --python=/usr/bin/python3.9`
- `cd humorloos.pythonanywhere.com`
- `pip install -r requirements.txt`
- gdal does not work with setuptools>=58.0.0, so we need to downgrade it `pip install setuptools==57.5.0`
- install gdal from local sources
`pip install --global-option=build_ext --global-option="-I /usr/include/gdal" GDAL==$(gdal-config --version)`

### setting up local django backend (on Windows)
- Add following 2 lines to "C:\Windows\System32\drivers\etc\hosts":
  ```
    127.0.0.1     api.humorloos.pythonanywhere.com
    127.0.0.1     humorloos.pythonanywhere.com
  ```
- run `runsslserver`
- now django backend can be accessed at https://api.humorloos.pythonanywhere.com:8000
