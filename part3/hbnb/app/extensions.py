#!/usr/bin/env python3
"""
Extensions Flask utilisées par l'application HolbertonBnB.
Ce module initialise les extensions Flask de manière centralisée pour éviter
les dépendances circulaires et permettre leur réutilisation dans différents modules.
"""

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Extension pour le hachage des mots de passe
# Utilise l'algorithme bcrypt, considéré comme sécurisé pour le stockage des mots de passe
bcrypt = Bcrypt()

# Extension pour gérer l'authentification par tokens JWT (JSON Web Tokens)
# Permet de créer, valider et rafraîchir les tokens d'authentification
jwt = JWTManager()

# ORM (Object-Relational Mapping) pour interagir avec la base de données
# Permet de définir des modèles Python qui sont mappés aux tables de la base de données
db = SQLAlchemy()

# Configuration CORS pour permettre les requêtes depuis le frontend (port 8000)
cors = CORS(supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:8000", "http://127.0.0.1:8000"], "allow_headers": ["Content-Type", "Authorization"], "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}}) 