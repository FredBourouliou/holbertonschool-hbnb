#!/usr/bin/env python3
"""
Script pour ajouter une place de test à la base de données.
Ce script est utile pour tester le fonctionnement du filtrage par prix.
"""

from app import create_app
from app.models.place import Place
from app.models.user import User
from app.extensions import db
from config import DevelopmentConfig

# Création de l'application avec la configuration de développement
app = create_app(DevelopmentConfig)

with app.app_context():
    # Vérifier s'il y a déjà des places dans la base de données
    existing_places = Place.query.all()
    if existing_places:
        print(f"La base de données contient déjà {len(existing_places)} places.")
        for place in existing_places:
            print(f"- ID: {place.id}, Titre: {place.title}, Prix: ${place.price}")
    else:
        print("Aucune place trouvée dans la base de données.")
    
    # Trouver un utilisateur pour être propriétaire
    user = User.query.first()
    
    if not user:
        print("Aucun utilisateur trouvé. Création d'un utilisateur de test...")
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="testpassword"
        )
        db.session.add(user)
        db.session.commit()
        print(f"Utilisateur créé avec ID: {user.id}")
    
    # Créer trois places avec des prix différents pour tester le filtrage
    place1 = Place(
        title="Appartement économique",
        description="Petit appartement abordable, parfait pour un court séjour.",
        price=45,
        latitude=48.8566,
        longitude=2.3522,
        owner_id=user.id
    )
    
    place2 = Place(
        title="Maison confortable",
        description="Maison spacieuse avec toutes les commodités pour un séjour en famille.",
        price=85,
        latitude=51.5074,
        longitude=-0.1278,
        owner_id=user.id
    )
    
    place3 = Place(
        title="Villa de luxe",
        description="Magnifique villa avec piscine et vue panoramique.",
        price=250,
        latitude=40.7128,
        longitude=-74.0060,
        owner_id=user.id
    )
    
    # Ajouter les places à la base de données
    db.session.add(place1)
    db.session.add(place2)
    db.session.add(place3)
    db.session.commit()
    
    print(f"Places créées avec succès :")
    print(f"- ID: {place1.id}, Titre: {place1.title}, Prix: ${place1.price}")
    print(f"- ID: {place2.id}, Titre: {place2.title}, Prix: ${place2.price}")
    print(f"- ID: {place3.id}, Titre: {place3.title}, Prix: ${place3.price}")
    
    print("Redémarrez le serveur backend (part3) pour que les changements prennent effet.") 