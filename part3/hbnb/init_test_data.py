#!/usr/bin/env python3
"""
Script d'initialisation de données de test pour l'application HolbertonBnB.
Ce script ajoute des utilisateurs et des places pour tester le fonctionnement du filtrage par prix.
"""

from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.extensions import db

def init_test_data(app):
    """
    Initialise des données de test dans la base de données.
    
    Args:
        app: L'instance de l'application Flask
    """
    with app.app_context():
        # Récupérer l'utilisateur admin existant ou en créer un si nécessaire
        admin_user = User.query.filter_by(email='admin@hbnb.com').first()
        if not admin_user:
            admin_user = User(
                first_name="Admin",
                last_name="User",
                email="admin@hbnb.com",
                password="adminpassword",
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Utilisateur administrateur créé avec succès.")
        
        # Créer un utilisateur standard conformément à initial_data.sql
        regular_user = User.query.filter_by(email='user@hbnb.com').first()
        if not regular_user:
            regular_user = User(
                first_name="Regular",
                last_name="User",
                email="user@hbnb.com",
                password="userpassword"
            )
            db.session.add(regular_user)
            db.session.commit()
            print("Utilisateur standard créé avec succès.")
        
        # Créer un logement appartenant à l'administrateur (pour que l'utilisateur standard puisse laisser une review)
        admin_place = Place.query.filter_by(title="Maison de l'administrateur").first()
        if not admin_place:
            admin_place = Place(
                title="Maison de l'administrateur",
                description="Une belle maison pour tester les reviews. Ce logement appartient à l'administrateur et peut être noté par l'utilisateur standard.",
                price=150,
                latitude=43.6047,
                longitude=1.4442,  # Coordonnées de Toulouse
                owner_id=admin_user.id
            )
            db.session.add(admin_place)
            db.session.commit()
            print("Logement de l'administrateur créé avec succès.")
        
        # Créer quelques places avec différents prix
        # Ces places appartiennent à l'utilisateur standard
        places = [
            Place(
                title="Appartement économique",
                description="Petit appartement abordable, parfait pour un court séjour.",
                price=45,
                latitude=48.8566,
                longitude=2.3522,
                owner_id=regular_user.id
            ),
            Place(
                title="Maison confortable",
                description="Maison spacieuse avec toutes les commodités pour un séjour en famille.",
                price=85,
                latitude=51.5074,
                longitude=-0.1278,
                owner_id=regular_user.id
            ),
            Place(
                title="Villa de luxe",
                description="Magnifique villa avec piscine et vue panoramique.",
                price=250,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=regular_user.id
            ),
            Place(
                title="Studio en centre-ville",
                description="Petit studio idéalement situé en plein cœur de la ville.",
                price=60,
                latitude=45.7640,
                longitude=4.8357,
                owner_id=regular_user.id
            ),
            Place(
                title="Chalet à la montagne",
                description="Chalet chaleureux avec vue imprenable sur les montagnes.",
                price=120,
                latitude=46.5197,
                longitude=6.6323,
                owner_id=regular_user.id
            )
        ]
        
        # Vérifier si les places existent déjà avant de les ajouter
        existing_titles = [p.title for p in Place.query.filter_by(owner_id=regular_user.id).all()]
        places_to_add = [p for p in places if p.title not in existing_titles]
        
        for place in places_to_add:
            db.session.add(place)
        
        db.session.commit()
        print(f"{len(places_to_add)} places de test ont été ajoutées à la base de données.") 