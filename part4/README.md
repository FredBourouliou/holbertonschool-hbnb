# Partie 4 - Client Web Simple

Dans cette phase, nous nous concentrons sur le développement front-end de l'application en utilisant HTML5, CSS3 et JavaScript ES6. L'objectif est de concevoir et d'implémenter une interface utilisateur interactive qui se connecte aux services back-end développés dans les parties précédentes du projet.

## Objectifs

- Développer une interface conviviale suivant les spécifications de conception fournies
- Implémenter des fonctionnalités côté client pour interagir avec l'API back-end
- Assurer une gestion sécurisée et efficace des données avec JavaScript
- Appliquer les pratiques modernes de développement web pour créer une application dynamique

## Compétences acquises

- Comprendre et appliquer HTML5, CSS3 et JavaScript ES6 dans un projet réel
- Apprendre à interagir avec les services back-end en utilisant AJAX/Fetch API
- Implémenter des mécanismes d'authentification et gérer les sessions utilisateur
- Utiliser les scripts côté client pour améliorer l'expérience utilisateur sans rechargement de page

## Structure du projet

- **`/static`** : Ressources statiques de l'application
  - **`/css`** : Feuilles de style CSS
  - **`/js`** : Scripts JavaScript
  - **`/images`** : Images et ressources graphiques
    - **`/places`** : Images des logements

- **`/templates`** : Fichiers HTML pour les différentes pages
  - `index.html` : Page d'accueil avec la liste des logements
  - `login.html` : Page de connexion utilisateur
  - `place.html` : Page de détail d'un logement
  - `add_review.html` : Formulaire d'ajout d'avis

- **Scripts utilitaires**
  - `server.py` : Serveur HTTP simple pour le développement
  - `download_assets.sh` : Script pour télécharger le logo et l'icône
  - `download_place_images.sh` : Script pour télécharger les images des logements

## Démarrage rapide

1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

2. Télécharger les ressources graphiques (si nécessaire) :
   ```bash
   bash download_assets.sh
   bash download_place_images.sh
   ```

3. Démarrer le serveur de développement :
   ```bash
   python server.py
   ```

4. Accéder à l'application à l'adresse : http://localhost:8000

## Pages principales

1. **Page d'accueil** : Affiche la liste des logements disponibles avec filtre par prix et recherche
2. **Page de détail** : Montre les informations complètes sur un logement et les avis
3. **Page de connexion** : Permet à l'utilisateur de s'authentifier
4. **Page d'ajout d'avis** : Formulaire pour ajouter un commentaire sur un logement

## Améliorations récentes de l'interface

Les améliorations suivantes ont été implémentées pour améliorer l'expérience utilisateur :

1. **Éléments de design moderne**
   - Schéma de couleurs amélioré avec une couleur principale #FF5A5F (inspirée d'AirBnB)
   - Typographie améliorée avec 'Helvetica Neue' comme police principale
   - Ajout d'ombres et d'effets au survol pour créer de la profondeur et de l'interactivité
   - Rayon de bordure et rembourrage cohérents sur tous les éléments de l'interface

2. **Section Hero**
   - Ajout d'une section hero avec un arrière-plan en dégradé
   - Appel à l'action clair et proposition de valeur
   - Fonctionnalité de recherche intégrée directement dans la section hero

3. **Éléments interactifs**
   - Design de bouton amélioré avec un style cohérent
   - Navigation améliorée avec des effets de soulignement subtils
   - États de survol animés pour les cartes et les boutons

4. **Localisation**
   - Interface traduite en français pour une meilleure expérience utilisateur
   - Terminologie cohérente dans toute l'application

5. **Fonctionnalité spéciale**
   - Ajout d'une annonce thématique pour "La maison des feuilles de l'administrateur"
   - Description personnalisée et image faisant référence au roman de Mark Z. Danielewski
   - Transformation dynamique du contenu grâce à JavaScript

## Remarques techniques

- L'application utilise uniquement des requêtes GET pour récupérer les données
- La persistance des sessions est gérée par des cookies stockant le token JWT
- L'application est conçue pour fonctionner avec l'API développée dans la partie 3
- Le serveur intégré est destiné uniquement au développement et ne doit pas être utilisé en production

## Identifiants de test

⚠️ **AVERTISSEMENT DE SÉCURITÉ** ⚠️  
_Les identifiants ci-dessous sont fournis uniquement à des fins éducatives. L'exposition des informations d'identification dans un fichier README n'est pas une bonne pratique en situation réelle et présente un risque de sécurité important. Ces identifiants ne devraient être utilisés que dans un environnement de développement local isolé._

L'application dispose de deux comptes utilisateur pour tester les différentes fonctionnalités :

1. **Utilisateur administrateur**
   - Email : `admin@hbnb.com`
   - Mot de passe : `adminpassword`
   - Rôle : Propriétaire de "La maison des feuilles de l'administrateur"
   - Droits : Accès complet à l'application, mais ne peut pas évaluer son propre logement

2. **Utilisateur standard**
   - Email : `user@hbnb.com`
   - Mot de passe : `userpassword`
   - Rôle : Propriétaire de plusieurs logements (appartement économique, villa de luxe, etc.)
   - Droits : Peut consulter, réserver et évaluer les logements qui ne lui appartiennent pas

Ces comptes permettent de tester les différentes fonctionnalités de l'application selon le niveau d'accès :
- La connexion/déconnexion
- L'affichage différencié des boutons d'ajout d'avis (visibles uniquement pour les logements n'appartenant pas à l'utilisateur connecté)

