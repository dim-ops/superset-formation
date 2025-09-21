FROM apache/superset:4.0.0

ARG ORACLEDB_VERSION=3.3.0
ARG PYMSSQL_VERSION=2.3.7
ARG PYTHON_LDAP_VERSION=3.4.4
ARG REDIS_VERSION=4.5.4
ARG GEVENT_VERSION=25.9.1
ARG PSYCOPG2_VERSION=2.9.10
ARG STATSD_VERSION=4.0.1

USER root

RUN apt-get update && apt-get install -y \
    wget \
    zip \
    unzip \
    gnupg2 \
    libaio1 \
    libldap2-dev \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_140.0.7339.185-1_amd64.deb && \
    dpkg -i google-chrome-stable_140.0.7339.185-1_amd64.deb || apt-get install -fy && \
    rm google-chrome-stable_140.0.7339.185-1_amd64.deb

# Installation de ChromeDriver version compatible (140)
RUN CHROMEDRIVER_VERSION="140.0.7339.185" && \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip -j chromedriver-linux64.zip -d /usr/bin && \
    chmod 755 /usr/bin/chromedriver && \
    rm -f chromedriver-linux64.zip

# Installation des packages Python
RUN pip install --no-cache-dir \
    oracledb==${ORACLEDB_VERSION} \
    pymssql==${PYMSSQL_VERSION} \
    python-ldap==${PYTHON_LDAP_VERSION} \
    gevent==${GEVENT_VERSION} \
    psycopg2-binary==${PSYCOPG2_VERSION} \
    redis==${REDIS_VERSION} \
    statsd==${STATSD_VERSION}

WORKDIR /app
COPY custom_security_manager.py .
RUN touch __init__.py
# for loading custom security manager
ENV PYTHONPATH="${PYTHONPATH}:/app"

USER superset
