#!/usr/bin/env python3
"""
Module d'initialisation de l'application HolbertonBnB.
Ce fichier configure l'application Flask, ses extensions et les routes API.
Il définit également les gestionnaires d'erreurs personnalisés.
"""

from flask import Flask, jsonify, render_template_string
from flask_restx import Api  # Extension pour créer des API RESTful avec documentation Swagger
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from config import DevelopmentConfig, config  # Configurations pour différents environnements
from app.extensions import bcrypt, jwt, db, cors  # Extensions Flask importées depuis extensions.py
import os

def create_app(config_class=DevelopmentConfig):
    """
    Fonction factory qui crée une instance de l'application Flask.
    
    Args:
        config_class: La classe de configuration à utiliser (par défaut: DevelopmentConfig)
    
    Returns:
        Flask: Instance configurée de l'application Flask
    """
    # Création de l'instance Flask
    app = Flask(__name__)
    
    # Chargement de la configuration appropriée depuis l'objet config_class
    app.config.from_object(config_class)
    
    # Initialisation des extensions
    bcrypt.init_app(app)  # Pour le hachage des mots de passe
    jwt.init_app(app)     # Pour l'authentification JWT
    db.init_app(app)      # SQLAlchemy pour l'ORM
    
    # Configuration CORS pour autoriser les requêtes du frontend
    cors.init_app(app, origins=["http://localhost:8000", "http://127.0.0.1:8000"], 
                 supports_credentials=True, 
                 allow_headers=["Content-Type", "Authorization"],
                 methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Création de l'API avec Swagger UI accessible à /api/v1/
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Enregistrement des espaces de noms (namespaces) de l'API
    # Chaque namespace correspond à une ressource REST distincte
    api.add_namespace(auth_ns, path='/api/v1/auth')       # Pour l'authentification
    api.add_namespace(users_ns, path='/api/v1/users')     # Pour la gestion des utilisateurs
    api.add_namespace(amenities_ns, path='/api/v1/amenities')  # Pour les commodités
    api.add_namespace(places_ns, path='/api/v1/places')   # Pour les logements
    api.add_namespace(reviews_ns, path='/api/v1/reviews') # Pour les avis

    # Gestionnaire d'erreur personnalisé pour les erreurs 404 (page non trouvée)
    @app.errorhandler(404)
    def page_not_found(e):
        """
        Gestionnaire pour les erreurs 404 - Page non trouvée.
        Affiche une page HTML personnalisée avec des canards animés.
        
        Args:
            e: L'exception qui a été levée
            
        Returns:
            tuple: HTML à afficher et code de statut 404
        """
        # Page HTML avec CSS et JavaScript intégrés pour une expérience ludique
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>HBnB API - Not Found</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f5f5f5;
                    overflow: hidden;
                    position: relative;
                }
                .container {
                    text-align: center;
                    padding: 40px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    z-index: 10;
                }
                h1 {
                    color: #e74c3c;
                    margin-bottom: 20px;
                }
                p {
                    color: #333;
                    margin-bottom: 20px;
                    line-height: 1.6;
                }
                a {
                    display: inline-block;
                    color: white;
                    background-color: #3498db;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background-color 0.3s;
                }
                a:hover {
                    background-color: #2980b9;
                }
                
                /* Styles pour les canards */
                .duck {
                    position: absolute;
                    font-size: 40px;
                    animation: dance 3s infinite alternate;
                    z-index: 1;
                    cursor: pointer;
                }
                
                @keyframes dance {
                    0% { transform: translateY(0) rotate(0deg); }
                    25% { transform: translateY(-20px) rotate(10deg); }
                    50% { transform: translateY(0) rotate(-10deg); }
                    75% { transform: translateY(-10px) rotate(5deg); }
                    100% { transform: translateY(0) rotate(0deg); }
                }
                
                .quack {
                    position: absolute;
                    color: #e67e22;
                    font-weight: bold;
                    font-size: 24px;
                    opacity: 0;
                    animation: fadeOut 2s forwards;
                    z-index: 5;
                }
                
                @keyframes fadeOut {
                    0% { opacity: 0; transform: scale(0.5); }
                    10% { opacity: 1; transform: scale(1); }
                    80% { opacity: 1; transform: scale(1.1) translateY(-20px); }
                    100% { opacity: 0; transform: scale(1) translateY(-40px); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Page Not Found</h1>
                <p>The page you are looking for does not exist. This is an API server, not a website.</p>
                <p>Please visit the API documentation to learn how to use the API.</p>
                <a href="/api/v1/">Go to API Documentation</a>
            </div>
            
            <script>
                // Création de 5 canards dansants
                for (let i = 0; i < 5; i++) {
                    createDuck();
                }
                
                // Fonction pour créer un canard à une position aléatoire
                function createDuck() {
                    const duck = document.createElement('div');
                    duck.className = 'duck';
                    duck.innerHTML = '🦆';
                    duck.style.left = Math.random() * 100 + '%';
                    duck.style.top = Math.random() * 100 + '%';
                    duck.style.animationDelay = Math.random() * 2 + 's';
                    document.body.appendChild(duck);
                    
                    // Faire "coincoin" aléatoirement
                    setInterval(() => {
                        if (Math.random() > 0.7) {
                            quack(duck);
                        }
                    }, 3000);
                    
                    // Faire "coincoin" lors d'un clic sur le canard
                    duck.addEventListener('click', () => {
                        quack(duck);
                    });
                }
                
                // Fonction pour faire "coincoin"
                function quack(duck) {
                    const quackElem = document.createElement('div');
                    quackElem.className = 'quack';
                    quackElem.innerHTML = 'COIN!';
                    quackElem.style.left = duck.style.left;
                    quackElem.style.top = duck.style.top;
                    document.body.appendChild(quackElem);
                    
                    // Supprimer l'élément après l'animation
                    setTimeout(() => {
                        quackElem.remove();
                    }, 2000);
                }
            </script>
        </body>
        </html>
        '''
        return render_template_string(html), 404
    
    # Route racine qui redirige vers la documentation de l'API
    @app.route('/')
    def index():
        """
        Route racine de l'application qui redirige vers la documentation de l'API.
        Utilise une redirection HTML avec meta refresh pour une meilleure compatibilité.
        
        Returns:
            str: HTML de redirection
        """
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>HBnB API</title>
            <meta http-equiv="refresh" content="0;url=/api/v1/" />
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <p>Redirecting to API documentation...</p>
            <p>If you are not redirected automatically, <a href="/api/v1/">click here</a>.</p>
        </body>
        </html>
        ''')

    return app 