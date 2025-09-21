FROM apache/superset:4.0.0

ARG ORACLEDB_VERSION=3.3.0
ARG PYMSSQL_VERSION=2.3.7
ARG PYTHON_LDAP_VERSION=3.4.4

USER root

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    libldap2-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des drivers avec versions spécifiées
RUN pip install --no-cache-dir \
    oracledb==${ORACLEDB_VERSION} \
    pymssql==${PYMSSQL_VERSION} \
    python-ldap==${PYTHON_LDAP_VERSION}

USER superset
