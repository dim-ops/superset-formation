FROM apache/superset:5.0.0

ARG ORACLEDB_VERSION=3.3.0
ARG PYMSSQL_VERSION=2.3.7

WORKDIR /app

USER root

# Installation des dépendances système (SANS Firefox)
RUN apt-get update && apt-get install -y \
    libaio1 \
    wget \
    gnupg2 \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Installation de Google Chrome UNIQUEMENT
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Installation du ChromeDriver compatible
RUN CHROMEDRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE) \
    && wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver*

# Installation des packages Python
RUN uv pip install --no-cache-dir \
    oracledb==${ORACLEDB_VERSION} \
    pymssql==${PYMSSQL_VERSION} \
    gevent \
    psycopg2-binary \
    redis \
    Pillow \
    selenium \
    webdriver-manager

USER superset
