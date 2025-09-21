#!/bin/bash
# generate-superset-test-metrics.sh

echo "Génération de métriques Superset de test vers StatSD"

# Générer différents types de métriques Superset
kubectl run superset-metrics-generator --rm -i --tty --image=python:3.9-slim --restart=Never -- /bin/bash -c "
pip install statsd > /dev/null 2>&1
python3 -c \"
import statsd
import random
import time

# Client StatSD
stats = statsd.StatsClient('statsd-exporter-prometheus-statsd-exporter.monitoring.svc.cluster.local', 9125, prefix='superset')

print('Génération de métriques Superset...')

# Métriques de dashboard
for i in range(5):
    stats.incr('dashboard.loads')
    stats.incr(f'dashboard.{100 + i}.views')
    stats.timing('dashboard.load_time', random.randint(100, 500))

# Métriques de requêtes
for i in range(10):
    query_type = random.choice(['sql', 'chart', 'explore'])
    stats.incr(f'query.{query_type}.total')
    stats.timing(f'query.{query_type}.execution_time', random.randint(50, 2000))
    
    if random.random() > 0.9:  # 10% d'erreurs
        stats.incr(f'query.{query_type}.errors')
    else:
        stats.incr(f'query.{query_type}.success')

# Métriques utilisateurs
stats.gauge('users.active', random.randint(5, 25))
stats.incr('users.login.total')

# Métriques de cache
stats.incr('cache.hits')
stats.incr('cache.misses')

# Métriques de performance
stats.timing('response.time', random.randint(100, 800))
stats.gauge('memory.usage', random.randint(60, 90))

print('Métriques Superset générées avec succès!')
\"
"
