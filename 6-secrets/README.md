![schema](./schema.png)

Processus de récupération sécurisée des secrets :
1. Stockage centralisé - Les credentials des bases de données sont stockés de manière chiffrée dans HashiCorp Vault sous des chemins comme secret/superset/db/*
2. Authentification et récupération - L'opérateur Secret Sync (utilisant Vault Agent) s'authentifie auprès de Vault et récupère les secrets de manière sécurisée
3. Synchronisation automatique - Les secrets sont automatiquement synchronisés et créés comme des objets Kubernetes Secrets (ex: superset-db-secret)
4. Montage sécurisé - Superset monte ces secrets comme des fichiers dans son pod, évitant toute exposition dans les values Helm
5. Connexion à la base - Superset utilise les credentials montés pour se connecter de manière sécurisée aux bases de données
Avantages clés :

Sécurité renforcée : Aucun secret n'est jamais exposé en clair dans les configurations
Rotation automatique : Vault peut faire tourner les secrets automatiquement
Audit complet : Traçabilité de tous les accès aux secrets
Gestion centralisée : Politiques d'accès unifiées via Vault

Cette approche élimine complètement le risque d'exposition des secrets dans les values Helm tout en maintenant une gestion automatisée et sécurisée des credentials.

Le code présent dans ce répertoire est une esquisse, il n'a pas été testé réellement, mais la vérité est proche.
