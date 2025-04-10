#!/usr/bin/env python3
"""
Script pour réinitialiser la base de données et ajouter les données de test.
Ce script supprime la base de données existante, la recrée avec les tables nécessaires
et ajoute les données de test, y compris l'utilisateur standard conforme à initial_data.sql.
"""

import os
import sys
from app import create_app
from app.db_init import init_db
from init_test_data import init_test_data

def main():
    """Fonction principale qui réinitialise la base de données et ajoute les données de test."""
    # Supprimer la base de données existante si elle existe
    db_path = os.path.join('instance', 'hbnb_dev.db')
    if os.path.exists(db_path):
        print(f"Suppression de la base de données existante : {db_path}")
        os.remove(db_path)
    
    # Créer l'application Flask
    app = create_app()
    
    # Initialiser la base de données et ajouter les données de test
    with app.app_context():
        print("Initialisation de la base de données...")
        init_db(app)
        print("Ajout des données de test...")
        init_test_data(app)
    
    print("Base de données réinitialisée avec succès!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 