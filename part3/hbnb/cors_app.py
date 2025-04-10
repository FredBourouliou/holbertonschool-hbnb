#!/usr/bin/env python3
"""
Module pour ajouter la configuration CORS à l'application HolbertonBnB.
Ce fichier enveloppe l'application Flask avec CORS correctement configuré.
"""

from app import create_app
from flask_cors import CORS

# Création de l'instance de l'application
app = create_app()

# Configuration CORS explicite et permissive
# Cette configuration remplace celle définie dans app/__init__.py
CORS(app, 
     resources={r"/*": {"origins": "*"}}, 
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type", "Authorization"],
     send_wildcard=True)

if __name__ == '__main__':
    # Démarrage du serveur Flask sur le port 5001
    app.run(host='0.0.0.0', port=5001, debug=True) 