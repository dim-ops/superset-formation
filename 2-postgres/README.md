Pour déployer les BDDs dans Kubernetes

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install postgresql bitnami/postgresql -f postgresql-values.yml -n default
```

Création des connexions manuellement

```SQL
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'attributes'
AND table_schema = 'information_schema';
```
