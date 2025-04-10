#!/usr/bin/env python3
"""
Configuration de l'application HolbertonBnB.
Ce module définit les configurations pour différents environnements
(développement, test, production), en utilisant un modèle basé sur des classes.
"""

import os
from datetime import timedelta

# Chemin absolu du répertoire de base
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Classe de configuration de base.
    Contient les paramètres communs à tous les environnements.
    Les autres configurations héritent de cette classe.
    """
    # Clé secrète pour Flask (sessions, cookies, etc.)
    # Utilise la variable d'environnement SECRET_KEY si elle existe, sinon utilise une valeur par défaut
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    
    # Configuration JWT (JSON Web Token)
    # Pour l'authentification des utilisateurs
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
    # Les tokens expirent après 1 heure
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Configuration SQLAlchemy (ORM)
    # Désactivation du suivi des modifications pour améliorer les performances
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # URI de la base de données par défaut (SQLite)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASEDIR, "hbnb_dev.db")}')

class DevelopmentConfig(Config):
    """
    Configuration pour l'environnement de développement.
    Active le mode debug et utilise une base de données SQLite spécifique au développement.
    """
    DEBUG = True
    # Base de données SQLite pour le développement dans le répertoire courant
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASEDIR, "hbnb_dev.db")}')

class TestingConfig(Config):
    """
    Configuration pour l'environnement de test.
    Utilise une base de données en mémoire pour des tests plus rapides.
    """
    TESTING = True
    # Base de données SQLite en mémoire - disparaît après les tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """
    Configuration pour l'environnement de production.
    Utilise une base de données MySQL pour de meilleures performances et fiabilité.
    """
    # Base de données MySQL pour la production
    # Les identifiants réels devraient être définis via des variables d'environnement
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://username:password@localhost/hbnb_prod')

# Dictionnaire qui mappe les noms d'environnement à leurs classes de configuration
# Utilisé par la fonction create_app() pour sélectionner la configuration appropriée
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # Configuration par défaut si aucun environnement n'est spécifié
} 