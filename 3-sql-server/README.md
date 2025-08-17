Pour déployer les BDDs dans Kubernetes

```bash
kubectl apply -f sql-server-values.yaml -n default
docker build -t superset-custom:4.0.0 .
helm upgrade --install superset superset/superset -f values.yaml -n superset --create-namespace
```

Création des connexions manuellement

URI: `mssql+pymssql://sa:XXXXXXXXXX@sqlserver-service.default.svc.cluster.local:1433`
