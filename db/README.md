Pour déployer les BDDs dans Kubernetes

```bash
kubectl apply -f oracle-values.yaml
kubectl apply -f sql-server-values.yaml
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install postgresql bitnami/postgresql -f postgresql-values.yml -n default
```
