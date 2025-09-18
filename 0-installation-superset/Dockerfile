FROM apache/superset:5.0.0

USER root

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# shttps://superset.apache.org/docs/configuration/configuring-superset/#setting-up-a-production-metadata-database
RUN pip install --no-cache-dir psycopg2-binary

USER superset
