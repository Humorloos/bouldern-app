### local django backend
- run `python manage.py runsslserver localhost:8000` in project root

### webpack development server
- run `npx vite` in frontend directory

### chrome https configuration:
- in case of error `NET::ERR_CERT_AUTHORITY_INVALID` in chrome, visit `chrome://flags/#allow-insecure-localhost` and set "Allow invalid certificates for resources loaded from localhost" to Enabled

### debugging android with devtools:
- visit chrome://inspect/#devices and devtools by clicking inspect for the device

### locally publishing android release via cli
- set environment variables `RELEASE_KEY_ALIAS`, `RELEASE_KEYSTORE_PASSWORD`, and `RELEASE_KEY_PASSWORD` from .env 
- copy keystore and gpp-key from secrets dir to `frontend/android/app`
- execute `gradle.bat publishReleaseBundle --track <alpha|internal>` in terminal from android dir
