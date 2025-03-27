#!/usr/bin/env python3
"""
Module d'initialisation de la base de données HolbertonBnB.
Ce script crée les tables nécessaires et ajoute des données initiales
comme un utilisateur administrateur et des commodités de base.
"""

from app.extensions import db  # SQLAlchemy pour ORM
from app.models.user import User  # Modèle User pour créer l'administrateur
from app.models.place import Place  # Modèle des logements
from app.models.review import Review  # Modèle des avis
from app.models.amenity import Amenity  # Modèle des commodités
from app import create_app  # Factory function pour créer l'application
from config import DevelopmentConfig
import os

def init_db(app=None):
    """
    Initialise la base de données avec les tables et les données de base.
    
    Cette fonction:
    1. Crée toutes les tables basées sur les modèles
    2. Crée un utilisateur admin s'il n'existe pas
    3. Ajoute des commodités communes si elles n'existent pas
    
    Args:
        app (Flask, optional): Instance de l'application Flask. 
            Si None, une instance est créée en mode développement.
    """
    # Crée une instance d'application si aucune n'est fournie
    if app is None:
        app = create_app(DevelopmentConfig)
    
    # Le contexte d'application est nécessaire pour les opérations de base de données
    with app.app_context():
        # Crée toutes les tables définies dans les modèles
        # Ne fait rien si les tables existent déjà
        db.create_all()
        
        # Vérifie si un utilisateur admin existe déjà
        admin = User.query.filter_by(email='admin@hbnb.com').first()
        if not admin:
            # Crée un utilisateur administrateur par défaut
            # Note: En production, il faudrait utiliser un mot de passe plus sécurisé
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@hbnb.com',
                password='adminpassword',  # Sera automatiquement haché par le modèle
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Utilisateur administrateur créé avec succès.")
        
        # Liste des commodités communes à ajouter à la base de données
        # Cela permet aux utilisateurs de les sélectionner lors de la création d'un logement
        amenities = [
            'WiFi', 'Kitchen', 'Washer', 'Dryer', 'Air Conditioning',
            'Heating', 'Dedicated Workspace', 'TV', 'Hair Dryer',
            'Iron', 'Pool', 'Hot Tub', 'Free Parking', 'EV Charger',
            'Crib', 'Gym', 'BBQ Grill', 'Breakfast', 'Indoor Fireplace',
            'Smoking Allowed', 'Beachfront', 'Waterfront', 'Ski-in/Ski-out'
        ]
        
        # Ajoute chaque commodité si elle n'existe pas déjà
        for amenity_name in amenities:
            if not Amenity.query.filter_by(name=amenity_name).first():
                amenity = Amenity(name=amenity_name)
                db.session.add(amenity)
        
        # Enregistre toutes les commodités ajoutées
        db.session.commit()
        print("Base de données initialisée avec succès.")

# Permet d'exécuter ce script directement pour initialiser la base de données
if __name__ == '__main__':
    init_db() 