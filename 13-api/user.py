#!/usr/bin/env python3
"""
Script pour créer un utilisateur via l'API Superset 6.0.0
"""

import requests
from bs4 import BeautifulSoup
import json

class SupersetUserManager:
    def __init__(self, host='51.68.16.250:30089', admin_username='admin', admin_password='FormationSupersetAdmin002'):
        self.superset_host = host
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.session = requests.Session()
        self.authenticated = False
        
    def authenticate(self):
        """
        Authentifie l'administrateur pour pouvoir utiliser l'API
        """
        print(f"🚀 Connexion à Superset sur {self.superset_host}")
        print(f"Utilisateur admin: {self.admin_username}")
        print("=" * 60)

        try:
            # Récupération du formulaire de login
            login_form = self.session.get(f"http://{self.superset_host}/login/")

            # Extraction du token CSRF
            soup = BeautifulSoup(login_form.text, 'html.parser')
            csrf_token = soup.find('input', {'id': 'csrf_token'})['value']

            # Authentification (comme dans le script qui fonctionne)
            data = {
                'username': self.admin_username,
                'password': self.admin_password,
                'csrf_token': csrf_token
            }
            self.session.post(f'http://{self.superset_host}/login/', data=data)

            print(f"✅ Authentification réussie")
            print(f"🍪 Session établie avec {len(self.session.cookies)} cookies")
            print()

            # Marquer comme authentifié
            self.authenticated = True
            return True

        except Exception as e:
            print(f"❌ Erreur d'authentification: {str(e)}")
            return False

    def get_available_roles(self):
        """
        Récupère la liste des rôles disponibles
        """
        if not self.authenticated:
            print("❌ Authentification requise")
            return []

        try:
            response = self.session.get(f'http://{self.superset_host}/api/v1/security/roles/')
            response.raise_for_status()
            
            roles_data = response.json()
            roles = roles_data.get('result', [])
            
            print("📋 Rôles disponibles:")
            for role in roles:
                print(f"   - {role['name']} (ID: {role['id']})")
            print()
            
            return roles
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des rôles: {str(e)}")
            return []

    def create_user(self, username, first_name, last_name, email, password, role_ids=None, active=True):
        """
        Crée un nouvel utilisateur (compatible Superset 6.0.0)
        
        Args:
            username: nom d'utilisateur (unique)
            first_name: prénom
            last_name: nom de famille
            email: adresse email (unique)
            password: mot de passe
            role_ids: liste des IDs des rôles à assigner (par défaut: rôle Gamma)
            active: utilisateur actif (True/False)
        """
        if not self.authenticated:
            print("❌ Authentification requise")
            return False

        print(f"👤 Création de l'utilisateur: {username}")
        print(f"📧 Email: {email}")
        print(f"🏷️  Nom complet: {first_name} {last_name}")

        # Si aucun rôle spécifié, utiliser le rôle Gamma par défaut
        if role_ids is None:
            roles = self.get_available_roles()
            gamma_role = next((role for role in roles if role['name'] == 'Gamma'), None)
            if gamma_role:
                role_ids = [gamma_role['id']]
                print(f"🎭 Rôle assigné par défaut: Gamma (ID: {gamma_role['id']})")
            else:
                print("⚠️  Aucun rôle Gamma trouvé, création sans rôle")
                role_ids = []

        # Données de l'utilisateur - Format pour Superset 6.0.0
        user_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,  # Pas de conf_password dans v6.0.0
            "roles": role_ids,
            "active": active
        }

        try:
            # Création de l'utilisateur via l'API
            response = self.session.post(
                f'http://{self.superset_host}/api/v1/security/users/',
                json=user_data,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 201:
                created_user = response.json()
                print("✅ Utilisateur créé avec succès!")
                print(f"   ID: {created_user.get('id', 'N/A')}")
                print(f"   Username: {created_user.get('username', 'N/A')}")
                print(f"   Email: {created_user.get('email', 'N/A')}")
                return True
            else:
                print(f"❌ Erreur lors de la création: {response.status_code}")
                try:
                    error_data = response.json()
                    if 'message' in error_data:
                        print(f"   Message: {error_data['message']}")
                    if 'errors' in error_data:
                        for field, errors in error_data['errors'].items():
                            print(f"   {field}: {', '.join(errors)}")
                except:
                    print(f"   Réponse: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Erreur lors de la création: {str(e)}")
            return False

    def list_users(self, limit=20):
        """
        Liste les utilisateurs existants
        """
        if not self.authenticated:
            print("❌ Authentification requise")
            return []

        try:
            response = self.session.get(f'http://{self.superset_host}/api/v1/security/users/?q=(page_size:{limit})')
            response.raise_for_status()
            
            users_data = response.json()
            users = users_data.get('result', [])
            
            print(f"👥 Utilisateurs existants ({len(users)}):")
            print("=" * 60)
            
            for user in users:
                roles = [role['name'] for role in user.get('roles', [])]
                status = "🟢 Actif" if user.get('active') else "🔴 Inactif"
                
                print(f"   {user.get('username', 'N/A')} - {user.get('email', 'N/A')}")
                print(f"   Nom: {user.get('first_name', '')} {user.get('last_name', '')}")
                print(f"   Rôles: {', '.join(roles) if roles else 'Aucun'}")
                print(f"   Statut: {status}")
                print("   " + "-" * 50)
            
            return users
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des utilisateurs: {str(e)}")
            return []

    def update_user_password(self, user_id, new_password):
        """
        Met à jour le mot de passe d'un utilisateur existant
        (Fonctionnalité supplémentaire pour Superset 6.0.0)
        """
        if not self.authenticated:
            print("❌ Authentification requise")
            return False

        try:
            response = self.session.put(
                f'http://{self.superset_host}/api/v1/security/users/{user_id}',
                json={"password": new_password},
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print("✅ Mot de passe mis à jour avec succès!")
                return True
            else:
                print(f"❌ Erreur lors de la mise à jour: {response.status_code}")
                print(f"   Réponse: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour: {str(e)}")
            return False

def main():
    """
    Fonction principale avec exemple d'utilisation
    """
    print("🎯 SUPERSET USER MANAGER v6.0.0")
    print("Création et gestion d'utilisateurs via l'API\n")

    # Initialisation du gestionnaire
    user_manager = SupersetUserManager()
    
    # Authentification
    if not user_manager.authenticate():
        return

    # Afficher les rôles disponibles
    user_manager.get_available_roles()
    
    # Exemple de création d'utilisateur
    print("📝 Exemple de création d'utilisateur:")
    print("=" * 60)
    
    # Vous pouvez personnaliser ces valeurs
    example_user = {
        'username': 'john_doe',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'SecurePassword123!'
    }
    
    print(f"Voulez-vous créer l'utilisateur exemple '{example_user['username']}' ? (y/n)")
    
    # Pour automatiser, décommentez la ligne suivante et commentez l'input
    # response = 'y'  # Création automatique
    response = input().lower()
    
    if response in ['y', 'yes', 'oui']:
        success = user_manager.create_user(**example_user)
        if success:
            print(f"\n🎉 Utilisateur créé! Vous pouvez maintenant vous connecter avec:")
            print(f"   Username: {example_user['username']}")
            print(f"   Password: {example_user['password']}")
    
    # Lister les utilisateurs existants
    print(f"\n📋 Liste des utilisateurs:")
    user_manager.list_users()
    
    print("\n✅ Script terminé!")

# Fonction utilitaire pour créer un utilisateur rapidement
def create_quick_user(username, email, password, first_name="", last_name=""):
    """
    Fonction utilitaire pour créer rapidement un utilisateur
    """
    user_manager = SupersetUserManager()
    
    if user_manager.authenticate():
        return user_manager.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
    return False

if __name__ == "__main__":
    main()
