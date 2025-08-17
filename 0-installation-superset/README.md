Pour déployer superset veuillez executer les commandes suivantes:


```bash
│ superset-init-db A Default SECRET_KEY was detected, please use superset_config.py to override it.                                         │
│ superset-init-db Use a strong complex alphanumeric string and use a tool to help you generate                                             │
│ superset-init-db a sufficiently random sequence, ex: openssl rand -base64 42                                                              │
│ superset-init-db For more info, see: https://superset.apache.org/docs/configuration/configuring-superset#specifying-a-secret_key
```

```bash
helm repo add superset https://apache.github.io/superset
helm repo update
helm upgrade --install superset superset/superset -f superset-values.yaml -n superset --create-namespace
```
