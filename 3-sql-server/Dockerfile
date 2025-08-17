FROM apache/superset:4.0.0

USER root

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    libaio1 \
    && rm -rf /var/lib/apt/lists/*

# Installation des drivers comme indiqué dans la doc Superset
RUN pip install --no-cache-dir pymssql

USER superset
