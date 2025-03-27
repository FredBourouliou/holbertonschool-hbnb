#!/usr/bin/env python3
"""
Script simplifié d'initialisation de l'utilisateur administrateur.
"""

import os
import sys
import sqlite3
import hashlib
import datetime

def create_admin():
    """
    Crée un utilisateur administrateur en utilisant SQLite directement.
    Utilise des variables d'environnement pour les informations d'identification.
    """
    # Récupérer les valeurs depuis les variables d'environnement avec des valeurs par défaut
    admin_first_name = os.environ.get('ADMIN_FIRST_NAME', 'Admin')
    admin_last_name = os.environ.get('ADMIN_LAST_NAME', 'User')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@hbnb.com')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'adminpassword')
    
    # Créer un hachage simple du mot de passe
    # Note: Dans une application réelle, utilisez bcrypt ou un autre algorithme sécurisé
    hashed_password = hashlib.sha256(admin_password.encode()).hexdigest()
    
    # Timestamp actuel pour created_at et updated_at (en utilisant UTC)
    # Utilisation de la méthode recommandée qui ne déclenche pas d'avertissement de dépréciation
    try:
        # datetime.UTC est disponible dans les versions récentes de Python (3.11+)
        now = datetime.datetime.now(datetime.UTC).isoformat()
    except AttributeError:
        # Pour les versions plus anciennes, on continue d'utiliser utcnow mais on évite l'avertissement
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            now = datetime.datetime.utcnow().isoformat()
    
    # Se connecter à la base de données SQLite
    db_path = 'instance/hbnb_dev.db'
    
    # Créer le répertoire instance s'il n'existe pas
    os.makedirs('instance', exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Vérifier si la table users existe, sinon la créer
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        _password_hash TEXT,
        is_admin BOOLEAN DEFAULT FALSE,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')
    
    # Vérifier si l'utilisateur existe déjà
    cursor.execute('SELECT id FROM users WHERE email = ?', (admin_email,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        print(f"L'utilisateur administrateur avec l'email {admin_email} existe déjà.")
        conn.close()
        return
    
    # Ajouter l'utilisateur administrateur
    cursor.execute('''
    INSERT INTO users (first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (admin_first_name, admin_last_name, admin_email, hashed_password, True, now, now))
    
    # Récupérer l'ID généré
    admin_id = cursor.lastrowid
    
    # Valider les changements et fermer la connexion
    conn.commit()
    conn.close()
    
    print("Utilisateur administrateur créé avec succès.")
    print(f"ID Admin: {admin_id}")
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