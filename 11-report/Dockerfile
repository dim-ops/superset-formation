FROM apache/superset:5.0.0

ARG ORACLEDB_VERSION=3.3.0
ARG PYMSSQL_VERSION=2.3.7

WORKDIR /app

USER root

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    libaio1 \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

ENV GECKODRIVER_VERSION=0.29.0
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz && \
    tar -x geckodriver -zf geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz -O > /usr/bin/geckodriver && \
    chmod 755 /usr/bin/geckodriver && \
    rm geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz

# Installation des packages Python dans le virtual environment de Superset
RUN uv pip install --no-cache-dir \
    oracledb==${ORACLEDB_VERSION} \
    pymssql==${PYMSSQL_VERSION} \
    gevent \
    psycopg2-binary \
    redis

USER superset
