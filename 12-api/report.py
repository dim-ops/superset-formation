#!/usr/bin/env python3
"""
Script pour déclencher l'exécution d'un rapport Superset via API
"""

import requests
from bs4 import BeautifulSoup
import json

class SupersetReportTrigger:
    def __init__(self, host='51.68.16.250:30088', username='admin', password='admin'):
        self.host = host
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.authenticated = False

    def authenticate(self):
        """
        Authentifie la session avec Superset
        """
        try:
            print(f"🔐 Authentification sur {self.host}...")
            
            # Récupération du formulaire de login
            login_form = self.session.get(f"http://{self.host}/login/")
            
            # Extraction du token CSRF
            soup = BeautifulSoup(login_form.text, 'html.parser')
            csrf_token = soup.find('input', {'id': 'csrf_token'})['value']
            
            # Authentification
            data = {
                'username': self.username,
                'password': self.password,
                'csrf_token': csrf_token
            }
            
            auth_response = self.session.post(f'http://{self.host}/login/', data=data)
            
            if auth_response.status_code == 200:
                self.authenticated = True
                print("✅ Authentification réussie")
                return True
            else:
                print(f"❌ Erreur d'authentification: {auth_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de l'authentification: {e}")
            return False

    def list_reports(self):
        """
        Liste tous les rapports disponibles
        """
        if not self.authenticated:
            if not self.authenticate():
                return None

        try:
            url = f'http://{self.host}/api/v1/report/'
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                reports = data['result']
                
                print(f"\n📧 {data['count']} rapports trouvés:")
                print("=" * 80)
                
                for report in reports:
                    active_status = "🟢 Actif" if report['active'] else "🔴 Inactif"
                    last_state = report.get('last_state', 'N/A')
                    state_icon = {'Success': '✅', 'Error': '❌', 'Working': '🔄'}.get(last_state, '❓')
                    
                    print(f"ID: {report['id']} | {report['name']}")
                    print(f"   UUID: {report['uuid']}")
                    print(f"   Statut: {active_status} | État: {state_icon} {last_state}")
                    print(f"   Type: {report['type']}")
                    
                    if report.get('crontab'):
                        print(f"   Planning: {report['crontab']}")
                    
                    print("-" * 80)
                
                return reports
            else:
                print(f"❌ Erreur lors de la récupération: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return None

    def trigger_report(self, report_id):
        """
        Déclenche l'exécution d'un rapport spécifique
        """
        if not self.authenticated:
            if not self.authenticate():
                return False

        try:
            url = f'http://{self.host}/api/v1/report/{report_id}/execute'
            
            print(f"🚀 Déclenchement du rapport ID: {report_id}")
            print(f"URL: {url}")
            
            response = self.session.post(url)
            
            print(f"📡 Code de réponse: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Rapport déclenché avec succès!")
                try:
                    result = response.json()
                    print(f"📄 Réponse: {json.dumps(result, indent=2)}")
                except:
                    print(f"📄 Réponse: {response.text}")
                return True
                
            elif response.status_code == 202:
                print("✅ Rapport mis en queue avec succès!")
                return True
                
            else:
                print(f"❌ Erreur lors du déclenchement: {response.status_code}")
                print(f"📄 Réponse: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False

    def get_report_status(self, report_id):
        """
        Récupère le statut d'un rapport spécifique
        """
        if not self.authenticated:
            if not self.authenticate():
                return None

        try:
            url = f'http://{self.host}/api/v1/report/{report_id}'
            response = self.session.get(url)
            
            if response.status_code == 200:
                report = response.json()['result']
                
                print(f"\n📊 Statut du rapport: {report['name']}")
                print("=" * 50)
                print(f"ID: {report['id']}")
                print(f"UUID: {report['uuid']}")
                print(f"Actif: {'🟢 Oui' if report['active'] else '🔴 Non'}")
                print(f"Dernier état: {report.get('last_state', 'N/A')}")
                print(f"Dernière exécution: {report.get('last_eval_dttm', 'N/A')}")
                
                if report.get('last_error_message'):
                    print(f"Dernière erreur: {report['last_error_message']}")
                
                return report
            else:
                print(f"❌ Erreur: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return None

def main():
    """
    Fonction principale avec menu interactif
    """
    print("🎯 SUPERSET REPORT TRIGGER")
    print("Déclenchement de rapports via API\n")
    
    # Créer l'instance
    trigger = SupersetReportTrigger()
    
    while True:
        print("\n" + "=" * 50)
        print("📋 MENU:")
        print("1. Lister tous les rapports")
        print("2. Déclencher un rapport par ID")
        print("3. Déclencher un rapport par UUID")
        print("4. Voir le statut d'un rapport")
        print("5. Quitter")
        
        choice = input("\nVotre choix (1-5): ").strip()
        
        if choice == '1':
            trigger.list_reports()
            
        elif choice == '2':
            report_id = input("Entrez l'ID du rapport: ").strip()
            if report_id.isdigit():
                trigger.trigger_report(int(report_id))
            else:
                print("❌ ID invalide")
                
        elif choice == '3':
            report_uuid = input("Entrez l'UUID du rapport: ").strip()
            trigger.trigger_report(report_uuid)
            
        elif choice == '4':
            report_id = input("Entrez l'ID du rapport: ").strip()
            if report_id.isdigit():
                trigger.get_report_status(int(report_id))
            else:
                print("❌ ID invalide")
                
        elif choice == '5':
            print("👋 Au revoir!")
            break
            
        else:
            print("❌ Choix invalide")

# Utilisation directe
def quick_trigger(report_id):
    """
    Fonction pour déclencher rapidement un rapport
    """
    trigger = SupersetReportTrigger()
    return trigger.trigger_report(report_id)

if __name__ == "__main__":
    main()
