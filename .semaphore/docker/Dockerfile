FROM registry.semaphoreci.com/android:30-node

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    #  gdal (adapted from https://github.com/wooyek/docker-geodjango/blob/master/Dockerfile)
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libsqlite3-mod-spatialite \
    spatialite-bin \
    # pip
    python3-pip \
    # cypress dependencies (see https://github.com/cypress-io/cypress-docker-images/blob/master/base/16.3.0/Dockerfile)
    libgtk2.0-0 \
    libgtk-3-0 \
    libnotify-dev \
    libgconf-2-4 \
    libgbm-dev \
    libnss3 \
    libxss1 \
    libasound2 \
    libxtst6 \
    xauth \
    xvfb \
    # install text editors
    vim-tiny \
    nano \
    # install emoji font
    fonts-noto-color-emoji \
    # install Chinese fonts
    # this list was copied from https://github.com/jim3ma/docker-leanote
    fonts-arphic-bkai00mp \
    fonts-arphic-bsmi00lp \
    fonts-arphic-gbsn00lp \
    fonts-arphic-gkai00mp \
    fonts-arphic-ukai \
    fonts-arphic-uming \
    ttf-wqy-zenhei \
    ttf-wqy-microhei \
    xfonts-wqy \
# Chrome dependencies
    fonts-liberation \
    xdg-utils \
    # clean up
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && pip install gdal \
    && ln -s /usr/bin/python3 /usr/bin/python


# install Chrome browser
ENV CHROME_VERSION 95.0.4638.69
RUN wget -O /usr/src/google-chrome-stable_current_amd64.deb "http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb" && \
  dpkg -i /usr/src/google-chrome-stable_current_amd64.deb ; \
  apt-get install -f -y && \
  rm -f /usr/src/google-chrome-stable_current_amd64.deb

# "fake" dbus address to prevent errors
# https://github.com/SeleniumHQ/docker-selenium/issues/87
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null
