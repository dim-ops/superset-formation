#!/bin/bash
# validate-metrics-vm.sh

VM_URL="http://51.68.16.250:30428"

echo "Validation des métriques dans VictoriaMetrics"

echo -e "\n1. Test de connectivité VictoriaMetrics"
curl -s "$VM_URL/api/v1/query?query=up" | jq '.status'

echo -e "\n2. Recherche des métriques Superset"
echo "Métriques trouvées :"
curl -s "$VM_URL/api/v1/label/__name__/values" | jq -r '.data[] | select(startswith("superset"))'

echo -e "\n3. Détail des métriques de dashboard"
curl -s "$VM_URL/api/v1/query?query=superset_dashboard_loads" | jq '.data.result[]'

echo -e "\n4. Métriques de requêtes par type"
curl -s "$VM_URL/api/v1/query?query={__name__=~\"superset_query.*total\"}" | jq '.data.result[] | {metric: .__name__, value: .value[1]}'

echo -e "\n5. Utilisateurs actifs"
curl -s "$VM_URL/api/v1/query?query=superset_users_active" | jq '.data.result[]'

echo -e "\n6. Taux d'erreur des requêtes"
curl -s "$VM_URL/api/v1/query?query=rate(superset_query_sql_errors[5m])" | jq '.data.result[]'
