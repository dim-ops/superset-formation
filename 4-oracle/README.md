Pour déployer les BDDs dans Kubernetes

```bash
helm upgrade --install superset superset/superset -f values.yaml -n superset --create-namespace
```

Création des connexions manuellement

oracle+cx_oracle://admin:admindimops@database-1.c92oy2osmi5g.us-east-1.rds.amazonaws.com:1521/?service_name=ORCL

```SQL
SELECT DISTINCT owner
FROM all_tables
WHERE owner IN (USER, 'SYS', 'SYSTEM', 'HR', 'SCOTT')
ORDER BY owner;
```
