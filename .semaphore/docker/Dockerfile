FROM registry.semaphoreci.com/android:30-node

RUN apt-get update \
    && apt-get install -y \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libsqlite3-mod-spatialite \
    spatialite-bin \
    python3-pip \
    # cypress dependencies
    libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 \
    libxss1 libasound2 libxtst6 xauth xvfb \
    && pip install gdal
