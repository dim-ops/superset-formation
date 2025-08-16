Pour déployer superset veuillez executer les commandes suivantes:

```bash
helm repo add superset https://apache.github.io/superset
helm repo update
helm upgrade --install superset superset/superset -f superset-values.yaml -n superset --create-namespace
```


Docker:

```
docker build -t superset-custom:3.0.0
```
