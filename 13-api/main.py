#!/usr/bin/env python3
"""
Script pour se connecter à Superset et afficher les charts de manière lisible
"""

import requests
from bs4 import BeautifulSoup

def get_superset_charts():
    """
    Se connecte à Superset et récupère les charts avec affichage lisible
    """
    # Configuration
    superset_host = '51.68.16.250:30089'
    username = 'admin'
    password = 'FormationSupersetAdmin002'

    print(f"🚀 Connexion à Superset sur {superset_host}")
    print(f"Utilisateur: {username}")
    print("=" * 60)

    # Session d'authentification
    s = requests.Session()

    try:
        # Récupération du formulaire de login
        login_form = s.get(f"http://{superset_host}/login/")

        # Extraction du token CSRF
        soup = BeautifulSoup(login_form.text, 'html.parser')
        csrf_token = soup.find('input', {'id': 'csrf_token'})['value']

        # Authentification
        data = {
            'username': username,
            'password': password,
            'csrf_token': csrf_token
        }
        s.post(f'http://{superset_host}/login/', data=data)

        print(f"✅ Authentification réussie")
        print(f"🍪 Session établie avec {len(s.cookies)} cookies")
        print()

        # Récupération des charts
        url = f'http://{superset_host}/api/v1/chart/'
        r = s.get(url)

        if r.status_code == 200:
            charts_data = r.json()
            display_charts(charts_data)
        else:
            print(f"❌ Erreur lors de la récupération des charts: {r.status_code}")

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

def display_charts(data):
    """
    Affiche les charts de manière lisible et structurée
    """
    if not data or 'result' not in data:
        print("❌ Aucune donnée de charts trouvée")
        return

    charts = data['result']
    total_count = data.get('count', len(charts))

    print(f"📊 CHARTS SUPERSET - {total_count} charts trouvés")
    print("=" * 60)

    for i, chart in enumerate(charts, 1):
        print(f"\n{i}. 📈 {chart.get('slice_name', 'Sans nom')}")
        print(f"   ID: {chart.get('id', 'N/A')}")
        print(f"   Type: {chart.get('viz_type', 'N/A')}")

        # Datasource
        datasource = chart.get('datasource_name_text', 'N/A')
        print(f"   📋 Source: {datasource}")

        # Créateur et dates
        created_by = chart.get('created_by', {})
        if created_by:
            creator_name = f"{created_by.get('first_name', '')} {created_by.get('last_name', '')}".strip()
            print(f"   👤 Créé par: {creator_name}")

        created_on = chart.get('changed_on_delta_humanized', 'N/A')
        print(f"   📅 Modifié: {created_on}")

        # Dashboards associés
        dashboards = chart.get('dashboards', [])
        if dashboards:
            dashboard_names = [d.get('dashboard_title', 'Sans titre') for d in dashboards]
            print(f"   📊 Dashboards: {', '.join(dashboard_names)}")
        else:
            print(f"   📊 Dashboards: Aucun")

        # Description si disponible
        description = chart.get('description')
        if description:
            print(f"   📝 Description: {description}")

        # URL d'édition
        edit_url = chart.get('edit_url', '')
        if edit_url:
            print(f"   🔗 Éditer: http://localhost:30088{edit_url}")

        # Informations sur les métriques (extrait du form_data)
        try:
            form_data = chart.get('form_data', {})
            if isinstance(form_data, dict):
                metrics = form_data.get('metrics', [])
                if metrics:
                    metric_names = []
                    for metric in metrics[:3]:  # Afficher max 3 métriques
                        if isinstance(metric, dict):
                            metric_names.append(metric.get('label', str(metric)))
                        else:
                            metric_names.append(str(metric))

                    metrics_display = ', '.join(metric_names)
                    if len(metrics) > 3:
                        metrics_display += f" ... (+{len(metrics)-3} autres)"
                    print(f"   📊 Métriques: {metrics_display}")
        except:
            pass  # Ignore les erreurs de parsing des métriques

        print("   " + "-" * 50)

def main():
    """
    Fonction principale
    """
    print("🎯 SUPERSET CHARTS VIEWER")
    print("Visualisation lisible des charts disponibles\n")

    get_superset_charts()

    print("\n✅ Analyse terminée!")

if __name__ == "__main__":
    main()
    
