FROM registry.semaphoreci.com/android:30-node

RUN apt-get update \
    && apt-get install -y \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libsqlite3-mod-spatialite \
    spatialite-bin \
    python3-pip \
    && pip install gdal
