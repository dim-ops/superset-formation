#!/usr/bin/env python3
"""
Script simple pour créer un rôle via l'API Superset 6.0.0
"""

import requests
from bs4 import BeautifulSoup

def create_superset_role():
    # Configuration
    SUPERSET_HOST = '51.68.16.250:30089'
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'FormationSupersetAdmin002'
    
    session = requests.Session()
    
    print("🚀 Connexion à Superset...")
    
    # 1. Récupération du token CSRF
    login_form = session.get(f"http://{SUPERSET_HOST}/login/")
    soup = BeautifulSoup(login_form.text, 'html.parser')
    csrf_token = soup.find('input', {'id': 'csrf_token'})['value']
    
    # 2. Authentification
    login_data = {
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD,
        'csrf_token': csrf_token
    }
    session.post(f'http://{SUPERSET_HOST}/login/', data=login_data)
    print("✅ Connecté!")
    
    # 3. Récupération de quelques permissions (exemple)
    print("📋 Récupération des permissions...")
    permissions_response = session.get(f'http://{SUPERSET_HOST}/api/v1/security/permissions/')
    permissions = permissions_response.json()['result']
    
    # Debug: voir la structure des permissions
    if permissions:
        print(f"   Structure d'une permission: {list(permissions[0].keys())}")
    
    # Exemple: prendre les permissions de lecture sur Dashboard et Chart
    # Adaptation selon la vraie structure de l'API
    dashboard_read = None
    chart_read = None
    
    for p in permissions:
        perm_name = p.get('name', '')  # ou p.get('permission', '') selon l'API
        resource_name = p.get('resource', '')  # ou autre champ
        
        if 'can_read' in perm_name and 'Dashboard' in resource_name:
            dashboard_read = p
        elif 'can_read' in perm_name and 'Chart' in resource_name:
            chart_read = p
    
    permission_ids = []
    if dashboard_read:
        permission_ids.append(dashboard_read['id'])
        print(f"   📊 Dashboard lecture: {dashboard_read['id']}")
    if chart_read:
        permission_ids.append(chart_read['id'])
        print(f"   📈 Chart lecture: {chart_read['id']}")
    
    # Si aucune permission trouvée, prendre les 2 premières comme exemple
    if not permission_ids and permissions:
        permission_ids = [permissions[0]['id'], permissions[1]['id']]
        print(f"   🔧 Utilisation des 2 premières permissions comme exemple: {permission_ids}")
    
    # 4. Création du rôle
    role_name = "SimpleViewer"
    print(f"\n🎭 Création du rôle '{role_name}'...")
    
    # Pour Superset 6.0.0, essayons différents formats
    role_data = {
        "name": role_name
        # Pas de permissions dans la création initiale pour v6.0.0
    }
    
    response = session.post(
        f'http://{SUPERSET_HOST}/api/v1/security/roles/',
        json=role_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 201:
        created_role = response.json()
        print("✅ Rôle créé avec succès!")
        print(f"   ID: {created_role.get('id', 'N/A')}")
        print(f"   Nom: {role_name}")  # Utiliser le nom qu'on a donné

        print(f"\n🎯 Rôle '{role_name}' créé avec l'ID {created_role.get('id')}")
        print("📝 Note: Les permissions doivent être ajoutées manuellement via l'interface web")
        print("   ou avec l'API Flask-AppBuilder de Superset")

    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"   Réponse: {response.text}")

if __name__ == "__main__":
    create_superset_role()
