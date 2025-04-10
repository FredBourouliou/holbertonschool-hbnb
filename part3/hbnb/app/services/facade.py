#!/usr/bin/env python3
"""
Module de façade pour l'application HolbertonBnB.
Implémente le pattern Façade pour centraliser l'accès aux différentes fonctionnalités
et simplifier l'interface entre les contrôleurs API et la couche de persistance.
"""

from app.persistence.repository import InMemoryRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from flask_jwt_extended import create_access_token
from datetime import datetime
from app.extensions import db

class HBnBFacade:
    """
    Façade qui centralise l'accès à toutes les fonctionnalités de l'application.
    
    Cette classe suit le pattern de conception Façade (Facade) qui:
    - Fournit une interface unifiée pour un ensemble d'interfaces du système
    - Masque la complexité du système aux contrôleurs API
    - Facilite les tests unitaires en permettant de mocker la façade
    """
    
    def __init__(self):
        """
        Initialise la façade avec les repositories nécessaires.
        
        Chaque repository est responsable de la persistance d'un type d'entité:
        - UserRepository: gestion des utilisateurs
        - PlaceRepository: gestion des logements
        - ReviewRepository: gestion des avis
        - AmenityRepository: gestion des commodités
        """
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def authenticate_user(self, email, password):
        """
        Authentifie un utilisateur et retourne un token JWT.
        
        Cette fonction:
        1. Récupère l'utilisateur par son email
        2. Vérifie que le mot de passe fourni correspond
        3. Génère un token JWT avec les claims appropriés (dont le rôle admin)
        
        Args:
            email (str): L'adresse email de l'utilisateur
            password (str): Le mot de passe en clair à vérifier
            
        Returns:
            str: Token JWT si l'authentification réussit
            None: Si l'utilisateur n'existe pas ou si le mot de passe est incorrect
        """
        # Récupération de l'utilisateur par email
        user = self.get_user_by_email(email)
        
        # Vérification de l'existence de l'utilisateur et du mot de passe
        if not user or not user.check_password(password):
            return None
        
        # Création des claims supplémentaires pour le token JWT
        # is_admin sera utilisé pour l'autorisation basée sur les rôles
        additional_claims = {
            'is_admin': user.is_admin
        }
        
        # Génération du token JWT avec l'identité de l'utilisateur
        # identity est utilisé pour identifier l'utilisateur à partir du token
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        
        return access_token

    # Méthodes liées aux utilisateurs
    def create_user(self, user_data):
        """
        Crée un nouvel utilisateur.
        
        Args:
            user_data (dict): Données de l'utilisateur à créer
            
        Returns:
            User: L'utilisateur créé
            
        Raises:
            ValueError: Si les données sont invalides
        """
        try:
            return self.user_repo.create_user(user_data)
        except ValueError as e:
            raise e

    def get_user(self, user_id):
        """
        Récupère un utilisateur par son ID.
        
        Args:
            user_id (str): ID de l'utilisateur à récupérer
            
        Returns:
            User: L'utilisateur correspondant à l'ID ou None s'il n'existe pas
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son email.
        
        Args:
            email (str): Adresse email de l'utilisateur
            
        Returns:
            User: L'utilisateur correspondant à l'email ou None s'il n'existe pas
        """
        return self.user_repo.get_by_email(email)

    def get_all_users(self):
        """
        Récupère tous les utilisateurs enregistrés.
        
        Returns:
            list: Liste de tous les utilisateurs
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Met à jour les informations d'un utilisateur.
        
        Args:
            user_id (str): ID de l'utilisateur à mettre à jour
            user_data (dict): Nouvelles données de l'utilisateur
            
        Returns:
            User: L'utilisateur mis à jour
            
        Raises:
            ValueError: Si l'utilisateur n'existe pas ou si les données sont invalides
        """
        try:
            return self.user_repo.update_user(user_id, user_data)
        except ValueError as e:
            raise e

    # Méthodes liées aux logements
    def create_place(self, place_data):
        """
        Crée un nouveau logement.
        
        Cette méthode:
        1. Vérifie que le propriétaire existe
        2. Vérifie que les équipements existent (si fournis)
        3. Crée le logement
        4. Associe les équipements au logement
        
        Args:
            place_data (dict): Données du logement à créer
            
        Returns:
            Place: Le logement créé
            
        Raises:
            ValueError: Si le propriétaire n'existe pas, si un équipement n'existe pas,
                       ou si les données sont invalides
        """
        try:
            # Récupère le propriétaire
            owner_id = place_data.get('owner_id')
            owner = self.get_user(owner_id)
            if not owner:
                raise ValueError('Propriétaire non trouvé')
            
            # Gère les équipements s'ils sont fournis
            amenities = []
            if 'amenity_ids' in place_data:
                amenity_ids = place_data.pop('amenity_ids')
                for amenity_id in amenity_ids:
                    amenity = self.get_amenity(amenity_id)
                    if not amenity:
                        raise ValueError(f'Équipement avec ID {amenity_id} non trouvé')
                    amenities.append(amenity)
            
            # Crée le logement
            # Note : on ne modifie pas owner_id car c'est ce que le modèle attend directement
            # Créer une copie des données pour éviter de modifier le dictionnaire original
            place_creation_data = place_data.copy()
            place_creation_data['owner'] = owner  # Ajouter l'objet owner pour le constructeur de Place
            place = self.place_repo.create_place(place_creation_data)
            
            # Ajoute les équipements au logement
            for amenity in amenities:
                place.add_amenity(amenity)
            
            db.session.commit()
            return place
        except ValueError as e:
            raise e
        except Exception as e:
            # Ajouter un log d'erreur plus détaillé pour les autres exceptions
            db.session.rollback()
            raise ValueError(f"Erreur lors de la création du logement: {str(e)}")

    def get_place(self, place_id):
        """
        Récupère un logement par son ID.
        
        Args:
            place_id (str): ID du logement à récupérer
            
        Returns:
            Place: Le logement correspondant à l'ID ou None s'il n'existe pas
        """
        return self.place_repo.get(place_id)

    def get_places_by_owner(self, owner_id):
        """
        Récupère tous les logements appartenant à un utilisateur spécifique.
        
        Args:
            owner_id (str): ID du propriétaire des logements
            
        Returns:
            list: Liste des logements appartenant à cet utilisateur
        """
        return self.place_repo.get_by_owner(owner_id)

    def get_all_places(self):
        """
        Récupère tous les logements enregistrés.
        
        Returns:
            list: Liste de tous les logements
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Met à jour les informations d'un logement.
        
        Cette méthode gère également la mise à jour des équipements associés
        au logement si des IDs d'équipements sont fournis.
        
        Args:
            place_id (str): ID du logement à mettre à jour
            place_data (dict): Nouvelles données du logement
            
        Returns:
            Place: Le logement mis à jour
            
        Raises:
            ValueError: Si le logement n'existe pas, si un équipement n'existe pas,
                       ou si les données sont invalides
        """
        try:
            # Gère les équipements s'ils sont fournis
            if 'amenity_ids' in place_data:
                amenity_ids = place_data.pop('amenity_ids')
                amenities = []
                for amenity_id in amenity_ids:
                    amenity = self.get_amenity(amenity_id)
                    if not amenity:
                        raise ValueError(f'Équipement avec ID {amenity_id} non trouvé')
                    amenities.append(amenity)
                place_data['amenities'] = amenities
            
            return self.place_repo.update_place(place_id, place_data)
        except ValueError as e:
            raise e
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """
        Ajoute un équipement à un logement.
        
        Args:
            place_id (str): ID du logement
            amenity_id (str): ID de l'équipement à ajouter
            
        Returns:
            Place: Le logement mis à jour
            
        Raises:
            ValueError: Si le logement ou l'équipement n'existe pas
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Logement non trouvé')
            
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError('Équipement non trouvé')
            
        return self.place_repo.add_amenity_to_place(place_id, amenity)
    
    def remove_amenity_from_place(self, place_id, amenity_id):
        """
        Supprime un équipement d'un logement.
        
        Args:
            place_id (str): ID du logement
            amenity_id (str): ID de l'équipement à supprimer
            
        Returns:
            Place: Le logement mis à jour
            
        Raises:
            ValueError: Si le logement ou l'équipement n'existe pas
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Logement non trouvé')
            
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError('Équipement non trouvé')
            
        return self.place_repo.remove_amenity_from_place(place_id, amenity)

    # Méthodes liées aux avis
    def create_review(self, review_data):
        """
        Crée un nouvel avis pour un logement.
        
        Cette méthode effectue plusieurs vérifications:
        1. Le logement doit exister
        2. L'utilisateur doit exister
        3. L'utilisateur ne peut pas noter son propre logement
        4. L'utilisateur ne peut pas noter deux fois le même logement
        
        Args:
            review_data (dict): Données de l'avis à créer
            
        Returns:
            Review: L'avis créé
            
        Raises:
            ValueError: Si le logement ou l'utilisateur n'existe pas,
                       si l'utilisateur est le propriétaire, ou s'il a déjà noté ce logement
        """
        try:
            # Récupère le logement
            place_id = review_data.get('place_id')
            place = self.get_place(place_id)
            if not place:
                raise ValueError('Logement non trouvé')
                
            # Récupère l'utilisateur
            user_id = review_data.get('user_id')
            user = self.get_user(user_id)
            if not user:
                raise ValueError('Utilisateur non trouvé')
                
            # Vérifie que l'utilisateur n'est pas le propriétaire du logement
            if place.owner_id == user_id:
                raise ValueError('Le propriétaire ne peut pas noter son propre logement')
                
            # Vérifie que l'utilisateur n'a pas déjà noté ce logement
            existing_review = self.review_repo.get_by_place_and_user(place_id, user_id)
            if existing_review:
                raise ValueError('L\'utilisateur a déjà noté ce logement')
                
            # Crée une copie des données pour éviter de modifier l'original
            review_data_copy = review_data.copy()
            
            # Supprimer place_id et user_id du dictionnaire pour éviter les arguments en double
            if 'place_id' in review_data_copy:
                del review_data_copy['place_id']
            if 'user_id' in review_data_copy:
                del review_data_copy['user_id']
            
            # Ajouter place et user au dictionnaire
            review_data_copy['place'] = place
            review_data_copy['user'] = user
            
            # Crée l'avis avec les données modifiées
            return self.review_repo.create_review(review_data_copy)
        except ValueError as e:
            raise e

    def get_review(self, review_id):
        """
        Récupère un avis par son ID.
        
        Args:
            review_id (str): ID de l'avis à récupérer
            
        Returns:
            Review: L'avis correspondant à l'ID ou None s'il n'existe pas
        """
        return self.review_repo.get(review_id)

    def get_reviews_by_place(self, place_id):
        """
        Récupère tous les avis pour un logement spécifique.
        
        Args:
            place_id (str): ID du logement
            
        Returns:
            list: Liste des avis pour ce logement
            
        Raises:
            ValueError: Si le logement n'existe pas
        """
        return self.review_repo.get_by_place(place_id)

    def get_reviews_by_user(self, user_id):
        """
        Récupère tous les avis rédigés par un utilisateur spécifique.
        
        Args:
            user_id (str): ID de l'utilisateur
            
        Returns:
            list: Liste des avis rédigés par cet utilisateur
        """
        return self.review_repo.get_by_user(user_id)

    def get_all_reviews(self):
        """
        Récupère tous les avis enregistrés.
        
        Returns:
            list: Liste de tous les avis
        """
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """
        Met à jour les informations d'un avis.
        
        Args:
            review_id (str): ID de l'avis à mettre à jour
            review_data (dict): Nouvelles données de l'avis
            
        Returns:
            Review: L'avis mis à jour
            
        Raises:
            ValueError: Si l'avis n'existe pas ou si les données sont invalides
        """
        try:
            return self.review_repo.update_review(review_id, review_data)
        except ValueError as e:
            raise e

    # Méthodes liées aux équipements
    def create_amenity(self, amenity_data):
        """
        Crée un nouvel équipement.
        
        Args:
            amenity_data (dict): Données de l'équipement à créer
            
        Returns:
            Amenity: L'équipement créé
            
        Raises:
            ValueError: Si les données sont invalides ou si un équipement avec 
                       le même nom existe déjà
        """
        try:
            return self.amenity_repo.create_amenity(amenity_data)
        except ValueError as e:
            raise e

    def get_amenity(self, amenity_id):
        """
        Récupère un équipement par son ID.
        
        Args:
            amenity_id (str): ID de l'équipement à récupérer
            
        Returns:
            Amenity: L'équipement correspondant à l'ID ou None s'il n'existe pas
        """
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """
        Récupère un équipement par son nom.
        
        Args:
            name (str): Nom de l'équipement
            
        Returns:
            Amenity: L'équipement correspondant au nom ou None s'il n'existe pas
        """
        return self.amenity_repo.get_by_name(name)

    def get_all_amenities(self):
        """
        Récupère tous les équipements enregistrés.
        
        Returns:
            list: Liste de tous les équipements
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Met à jour les informations d'un équipement.
        
        Args:
            amenity_id (str): ID de l'équipement à mettre à jour
            amenity_data (dict): Nouvelles données de l'équipement
            
        Returns:
            Amenity: L'équipement mis à jour
            
        Raises:
            ValueError: Si l'équipement n'existe pas, si les données sont invalides,
                       ou si le nouveau nom est déjà utilisé par un autre équipement
        """
        try:
            return self.amenity_repo.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            raise e
    
    def get_places_by_amenity(self, amenity_id):
        """
        Récupère tous les logements qui possèdent un équipement spécifique.
        
        Args:
            amenity_id (str): ID de l'équipement
            
        Returns:
            list: Liste des logements avec cet équipement
            
        Raises:
            ValueError: Si l'équipement n'existe pas
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError('Équipement non trouvé')
        
        return amenity.places.all() 