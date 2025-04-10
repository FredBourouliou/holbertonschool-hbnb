#!/usr/bin/env python3
"""
Script de démarrage de l'application HolbertonBnB.
Ce fichier est le point d'entrée principal de l'application.
Il initialise l'application Flask et la base de données.
"""

from app import create_app
from app.db_init import init_db
from config import TestingConfig
from init_test_data import init_test_data
import os

# Création de l'instance de l'application Flask en mode test
# Utiliser le mode test qui utilise une base de données en mémoire pour éviter les problèmes de permissions
app = create_app(TestingConfig)

# Activer le mode debug pour afficher les erreurs détaillées
app.debug = True

# Initialisation de la base de données
# Le contexte d'application est nécessaire pour accéder aux configurations Flask
with app.app_context():
    # La fonction init_db crée les tables si elles n'existent pas
    # et ajoute un utilisateur admin et des commodités par défaut
    init_db(app)
    
    # Ajouter des données de test
    init_test_data(app)
    print("Base de données initialisée avec des données de test.")

# Vérification si ce fichier est exécuté directement (et non importé)
if __name__ == '__main__':
    # Démarrage du serveur Flask sur le port 5001
    # Différent du port par défaut 5000 pour éviter les conflits
    app.run(host='127.0.0.1', port=5001, debug=True) 