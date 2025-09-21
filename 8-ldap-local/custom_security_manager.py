from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import AuthLDAPView
from flask_appbuilder.security.views import expose
from flask import g, redirect, flash
from flask_appbuilder.security.forms import LoginForm_db
from flask_login import login_user
from flask_appbuilder._compat import as_unicode

class AuthLocalAndLDAPView(AuthLDAPView): # Hérite de la classe LDAP standard
    @expose("/login/", methods=["GET", "POST"]) # Définit la route de connexion
    def login(self):
        # Vérification si l'utilisateur est déjà connecté
        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index) # Redirection vers l'accueil
         # Création du formulaire de connexion standard
        form = LoginForm_db()
        # Traitement du formulaire soumis (POST)
        if form.validate_on_submit():
            # ÉTAPE 1: Tentative d'authentification LDAP en priorité
            user = self.appbuilder.sm.auth_user_ldap(
                form.username.data, form.password.data
            )
            # ÉTAPE 2: Si LDAP échoue, essayer l'authentification locale (base de données)
            if not user:
                user = self.appbuilder.sm.auth_user_db(
                    form.username.data, form.password.data
                )
            # Si une des deux authentifications a réussi
            if user:
                login_user(user, remember=False) # Connexion de l'utilisateur (session temporaire)
                return redirect(self.appbuilder.get_url_for_index) # Redirection vers l'accueil
            else:
                flash(as_unicode(self.invalid_login_message), "warning") # error
                return redirect(self.appbuilder.get_url_for_login)
         # Affichage du formulaire de connexion (GET ou validation échouée)
        return self.render_template(
            self.login_template, title=self.title, form=form, appbuilder=self.appbuilder
        )


class CustomSecurityManager(SupersetSecurityManager): # Hérite du gestionnaire Superset
    authldapview = AuthLocalAndLDAPView # Remplace la vue LDAP par défaut par notre version hybride
    def __init__(self, appbuilder):
        # Initialisation du gestionnaire parent (conserve toutes les fonctionnalités existantes)
        super(CustomSecurityManager, self).__init__(appbuilder)
