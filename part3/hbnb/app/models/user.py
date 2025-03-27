#!/usr/bin/env python3
"""
Modèle User pour l'application HolbertonBnB.
Ce module définit la classe User qui représente les utilisateurs dans la base de données.
Intègre les fonctionnalités pour la gestion sécurisée des mots de passe et la validation des données.
"""

import re
from app.models.base import BaseModel
from app.extensions import bcrypt, db

class User(BaseModel):
    """
    Modèle représentant un utilisateur dans l'application HolbertonBnB.
    
    Hérite de BaseModel qui fournit id, created_at, updated_at et les méthodes communes.
    Gère le stockage sécurisé du mot de passe et les relations avec d'autres modèles.
    """
    __tablename__ = 'users'  # Nom de la table dans la base de données
    
    # Attributs spécifiques aux utilisateurs
    first_name = db.Column(db.String(50), nullable=False)    # Prénom (obligatoire)
    last_name = db.Column(db.String(50), nullable=False)     # Nom de famille (obligatoire)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email unique (obligatoire)
    _password_hash = db.Column(db.String(128), nullable=True)  # Hachage du mot de passe (caché)
    is_admin = db.Column(db.Boolean, default=False)  # Indicateur si l'utilisateur est administrateur
    
    # Relations avec d'autres tables (ORM)
    # Relation One-to-Many : un utilisateur peut avoir plusieurs logements
    places = db.relationship('Place', backref='owner_rel', lazy='dynamic', 
                            cascade='all, delete-orphan')  # Supprime les logements si l'utilisateur est supprimé
    
    # Relation One-to-Many : un utilisateur peut rédiger plusieurs avis
    reviews = db.relationship('Review', backref='user_rel', lazy='dynamic', 
                             cascade='all, delete-orphan')  # Supprime les avis si l'utilisateur est supprimé
    
    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        """
        Initialise un nouvel utilisateur avec validation des données.
        
        Args:
            first_name (str): Prénom de l'utilisateur
            last_name (str): Nom de famille de l'utilisateur
            email (str): Adresse email unique
            password (str, optional): Mot de passe (sera haché)
            is_admin (bool, optional): Si l'utilisateur est administrateur
            **kwargs: Attributs supplémentaires pour la classe parente
            
        Raises:
            ValueError: Si les informations fournies ne sont pas valides
        """
        # Validation des données avant de les passer au constructeur parent
        self.validate_name(first_name, "first_name")
        self.validate_name(last_name, "last_name")
        self.validate_email(email)
        
        # Appel au constructeur de la classe parente (BaseModel)
        super().__init__(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_admin=is_admin,
            **kwargs
        )
        
        # Hash du mot de passe s'il est fourni
        if password:
            self.set_password(password)

    @property
    def password(self):
        """
        Propriété password qui empêche la lecture directe du mot de passe.
        
        Raises:
            AttributeError: Toujours levée pour empêcher l'accès au mot de passe
        """
        raise AttributeError('Le mot de passe n\'est pas un attribut lisible')
        
    def hash_password(self, password):
        """
        Hache et stocke le mot de passe de l'utilisateur.
        
        Args:
            password (str): Mot de passe en texte brut à hacher
            
        Raises:
            ValueError: Si le mot de passe est invalide ou trop court
        """
        if not password or not isinstance(password, str):
            raise ValueError("Le mot de passe est requis et doit être une chaîne de caractères")
        if len(password) < 8:
            raise ValueError("Le mot de passe doit comporter au moins 8 caractères")
        # Génère un hash bcrypt du mot de passe
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Alias de hash_password pour maintenir la compatibilité avec le code existant
    def set_password(self, password):
        """
        Alias de hash_password pour maintenir la compatibilité avec le code existant.
        
        Args:
            password (str): Mot de passe en texte brut à hacher
        """
        return self.hash_password(password)
        
    def verify_password(self, password):
        """
        Vérifie si le mot de passe fourni correspond au hash stocké.
        
        Args:
            password (str): Mot de passe à vérifier
            
        Returns:
            bool: True si le mot de passe correspond, False sinon
        """
        if not self._password_hash:
            return False
        # Compare le hash stocké avec un hash du mot de passe fourni
        return bcrypt.check_password_hash(self._password_hash, password)
    
    # Alias de verify_password pour maintenir la compatibilité avec le code existant
    def check_password(self, password):
        """
        Alias de verify_password pour maintenir la compatibilité avec le code existant.
        
        Args:
            password (str): Mot de passe à vérifier
            
        Returns:
            bool: True si le mot de passe correspond, False sinon
        """
        return self.verify_password(password)

    @staticmethod
    def validate_name(name, field):
        """
        Valide les champs de nom (prénom, nom de famille).
        
        Args:
            name (str): Valeur à valider
            field (str): Nom du champ pour les messages d'erreur
            
        Raises:
            ValueError: Si le nom n'est pas valide
        """
        if not name or not isinstance(name, str):
            raise ValueError(f"{field} est requis et doit être une chaîne de caractères")
        if len(name) > 50:
            raise ValueError(f"{field} ne doit pas dépasser 50 caractères")

    @staticmethod
    def validate_email(email):
        """
        Valide le format de l'adresse email avec une expression régulière.
        
        Args:
            email (str): Email à valider
            
        Raises:
            ValueError: Si l'email n'est pas valide
        """
        if not email or not isinstance(email, str):
            raise ValueError("L'email est requis et doit être une chaîne de caractères")
        
        # Expression régulière pour valider le format d'email
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValueError("Format d'email invalide")

    def add_place(self, place):
        """
        Ajoute un logement à la liste des logements de l'utilisateur.
        
        Args:
            place (Place): Instance de Place à ajouter
        """
        self.places.append(place)

    def update(self, data):
        """
        Met à jour les attributs de l'utilisateur avec validation.
        
        Args:
            data (dict): Dictionnaire des attributs à mettre à jour
            
        Raises:
            ValueError: Si les données fournies ne sont pas valides
        """
        # Validation des attributs mis à jour
        if 'first_name' in data:
            self.validate_name(data['first_name'], "first_name")
        if 'last_name' in data:
            self.validate_name(data['last_name'], "last_name")
        if 'email' in data:
            self.validate_email(data['email'])
        if 'password' in data:
            # Définit le nouveau mot de passe haché
            self.set_password(data['password'])
            # Supprime le mot de passe du dictionnaire pour éviter qu'il soit stocké en clair
            data = {k: v for k, v in data.items() if k != 'password'}
        
        # Appel à la méthode de la classe parente pour la mise à jour
        super().update(data)
        
    def to_dict(self):
        """
        Convertit l'utilisateur en dictionnaire sans le mot de passe haché.
        
        Returns:
            dict: Représentation dictionnaire de l'utilisateur sans informations sensibles
        """
        user_dict = super().to_dict()
        # S'assure que le hash du mot de passe n'est pas inclus
        if '_password_hash' in user_dict:
            del user_dict['_password_hash']
        return user_dict
