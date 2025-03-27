#!/usr/bin/env python3
"""
Script d'initialisation de l'utilisateur administrateur pour l'application HolbertonBnB.
Ce script crée un utilisateur avec des droits d'administrateur si celui-ci n'existe pas déjà.
À utiliser lors de la première configuration de l'application.
"""

import os
import sys

def create_admin():
    """
    Crée un utilisateur administrateur pour l'application HolbertonBnB.
    
    Cette fonction:
    1. Vérifie si un administrateur existe déjà (avec l'email défini par ADMIN_EMAIL)
    2. Si non, crée un nouvel utilisateur avec les droits d'administration
    3. Affiche les informations de connexion pour l'administrateur
    
    Utilise les variables d'environnement suivantes:
    - ADMIN_FIRST_NAME: Prénom de l'administrateur (par défaut: 'Admin')
    - ADMIN_LAST_NAME: Nom de l'administrateur (par défaut: 'User')
    - ADMIN_EMAIL: Email de l'administrateur (par défaut: 'admin@hbnb.com')
    - ADMIN_PASSWORD: Mot de passe de l'administrateur (par défaut: 'adminpassword')
    
    Note: En production, assurez-vous de définir ces variables d'environnement
    avec des valeurs sécurisées, notamment pour ADMIN_PASSWORD.
    """
    # S'assurer que le répertoire parent est dans le chemin Python
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Importer après avoir ajouté le chemin pour éviter les problèmes d'importation
    from hbnb.app import create_app
    from hbnb.app.extensions import db
    from hbnb.app.models.user import User
    from hbnb.config import DevelopmentConfig
    
    # Récupérer les valeurs depuis les variables d'environnement avec des valeurs par défaut
    admin_first_name = os.environ.get('ADMIN_FIRST_NAME', 'Admin')
    admin_last_name = os.environ.get('ADMIN_LAST_NAME', 'User')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@hbnb.com')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'adminpassword')
    
    # Création d'une instance de l'application en mode développement
    app = create_app(DevelopmentConfig)
    
    with app.app_context():
        # Vérifie si l'utilisateur admin existe déjà
        admin = User.query.filter_by(email=admin_email).first()
        if admin:
            print(f"L'utilisateur administrateur avec l'email {admin_email} existe déjà.")
            return
        
        # Création de l'utilisateur administrateur
        admin = User(
            first_name=admin_first_name,
            last_name=admin_last_name,
            email=admin_email,
            password=admin_password,  # Sera automatiquement haché par le modèle
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Utilisateur administrateur créé avec succès.")
        print(f"ID Admin: {admin.id}")
        print(f"Email Admin: {admin_email}")
        
        # Message d'avertissement si le mot de passe par défaut est utilisé
        if admin_password == 'adminpassword':
            print("AVERTISSEMENT: Vous utilisez le mot de passe par défaut.")
            print("Pour des raisons de sécurité, définissez la variable d'environnement ADMIN_PASSWORD.")
        
        # Affiche le mot de passe ou indique qu'il est défini par variable d'environnement
        password_display = '<défini par variable d\'environnement>' if admin_password != 'adminpassword' else admin_password
        print(f"Mot de passe Admin: {password_display}")

if __name__ == '__main__':
    create_admin() 