#!/usr/bin/env python3
"""
API pour la gestion des avis (reviews) dans l'application HolbertonBnB.
Ce module définit les endpoints REST pour créer, lire, mettre à jour et supprimer
des avis sur les logements, ainsi que pour lister les avis par logement.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request

# Création du namespace pour les avis
api = Namespace('reviews', description='Opérations liées aux avis')

# Définition du modèle utilisateur pour les réponses imbriquées
user_model = api.model('ReviewUser', {
    'id': fields.String(description='Identifiant de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de famille de l\'utilisateur'),
    'email': fields.String(description='Adresse email')
})

# Définition du modèle logement pour les réponses imbriquées
place_model = api.model('ReviewPlace', {
    'id': fields.String(description='Identifiant du logement'),
    'title': fields.String(description='Titre du logement')
})

# Définition du modèle avis pour la validation des entrées et la documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Texte de l\'avis'),
    'rating': fields.Integer(required=True, description='Note (1-5)', min=1, max=5),
    'place_id': fields.String(required=True, description='Identifiant du logement concerné'),
    'user_id': fields.String(required=True, description='Identifiant de l\'utilisateur qui donne l\'avis')
})

# Définition du modèle de réponse avis
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Identifiant unique de l\'avis'),
    'text': fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note attribuée (1-5)'),
    'place': fields.Nested(place_model, description='Informations sur le logement'),
    'user': fields.Nested(user_model, description='Informations sur l\'utilisateur'),
    'created_at': fields.String(description='Date de création de l\'avis'),
    'updated_at': fields.String(description='Date de dernière mise à jour')
})

@api.route('/')
class ReviewList(Resource):
    """
    Collection d'avis.
    Permet de créer de nouveaux avis et de lister tous les avis.
    """
    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.response(201, 'Avis créé avec succès', review_response_model)
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(401, 'Non authentifié')
    @api.response(403, 'Action non autorisée')
    @api.response(404, 'Utilisateur ou logement non trouvé')
    @api.marshal_with(review_response_model, code=201)
    @jwt_required()
    def post(self):
        """
        Crée un nouvel avis sur un logement.
        
        L'utilisateur doit être authentifié.
        L'utilisateur ne peut créer des avis que pour lui-même (sauf admin).
        L'utilisateur ne peut pas noter son propre logement (sauf admin).
        L'utilisateur ne peut pas noter deux fois le même logement (sauf admin).
        
        Returns:
            dict: Informations de l'avis créé
            
        Raises:
            400: Si les données fournies sont invalides
            401: Si l'utilisateur n'est pas authentifié
            403: Si l'utilisateur n'a pas les droits nécessaires
            404: Si l'utilisateur ou le logement n'existe pas
        """
        review_data = api.payload
        
        # Récupérer les paramètres d'URL s'ils sont présents
        place_id_url = request.args.get('place_id')
        user_id_url = request.args.get('user_id')
        
        # Si les paramètres sont fournis dans l'URL, les utiliser
        if place_id_url and 'place_id' not in review_data:
            review_data['place_id'] = place_id_url
        if user_id_url and 'user_id' not in review_data:
            review_data['user_id'] = user_id_url
        
        # Récupérer l'identité de l'utilisateur et ses droits
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Si user_id n'est pas spécifié, utiliser l'utilisateur courant
        if 'user_id' not in review_data:
            review_data['user_id'] = current_user_id
        
        # Si ce n'est pas un admin et essaie de créer un avis pour quelqu'un d'autre
        if not is_admin and review_data.get('user_id') != current_user_id:
            api.abort(403, 'Unauthorized action')
            
        try:
            # Vérifier que l'utilisateur ne note pas son propre logement (sauf admin)
            place = facade.get_place(review_data.get('place_id'))
            if not place:
                api.abort(404, 'Logement non trouvé')
                
            # Si ce n'est pas un admin et c'est son propre logement
            if not is_admin and place.owner_id == current_user_id:
                api.abort(400, 'You cannot review your own place')
                
            # Vérifier que l'utilisateur n'a pas déjà noté ce logement (sauf admin)
            # Si c'est un admin qui crée au nom de quelqu'un d'autre, vérifier pour cet utilisateur
            user_id_to_check = review_data.get('user_id')
            existing_review = facade.review_repo.get_by_place_and_user(review_data.get('place_id'), user_id_to_check)
            
            if not is_admin and existing_review:
                api.abort(400, 'You have already reviewed this place')
                
            review = facade.create_review(review_data)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(404, str(e))
    
    @api.doc('list_reviews')
    @api.response(200, 'Liste des avis récupérée avec succès')
    @api.marshal_list_with(review_response_model)
    def get(self):
        """
        Récupère la liste de tous les avis.
        
        Returns:
            list: Liste des avis enregistrés
        """
        return facade.get_all_reviews()

@api.route('/<review_id>')
@api.param('review_id', 'Identifiant de l\'avis')
class ReviewResource(Resource):
    """
    Ressource avis individuelle.
    Permet de récupérer, mettre à jour ou supprimer un avis spécifique.
    """
    @api.doc('get_review')
    @api.response(200, 'Détails de l\'avis récupérés avec succès', review_response_model)
    @api.response(404, 'Avis non trouvé')
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """
        Récupère les informations d'un avis par son ID.
        
        Args:
            review_id (str): Identifiant de l'avis
            
        Returns:
            dict: Informations de l'avis
            
        Raises:
            404: Si l'avis n'existe pas
        """
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Avis avec l'id {review_id} non trouvé")
        return review
    
    @api.doc('update_review')
    @api.expect(review_model)
    @api.response(200, 'Avis mis à jour avec succès', review_response_model)
    @api.response(401, 'Non authentifié')
    @api.response(403, 'Action non autorisée')
    @api.response(404, 'Avis non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.marshal_with(review_response_model)
    @jwt_required()
    def put(self, review_id):
        """
        Met à jour les informations d'un avis.
        
        L'utilisateur doit être authentifié.
        L'utilisateur ne peut modifier que ses propres avis, sauf les administrateurs
        qui peuvent modifier n'importe quel avis.
        
        Args:
            review_id (str): Identifiant de l'avis à mettre à jour
            
        Returns:
            dict: Informations de l'avis mises à jour
            
        Raises:
            400: Si les données fournies sont invalides
            401: Si l'utilisateur n'est pas authentifié
            403: Si l'utilisateur n'a pas les droits nécessaires
            404: Si l'avis n'existe pas
        """
        # Récupérer l'avis existant
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Avis avec l'id {review_id} non trouvé")
        
        # Vérifier que l'utilisateur a le droit de modifier cet avis
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Les administrateurs peuvent modifier n'importe quel avis
        # Si l'utilisateur n'est pas admin et n'est pas l'auteur de l'avis
        if not is_admin and review.user_id != current_user_id:
            api.abort(403, 'Unauthorized action')
        
        try:
            review = facade.update_review(review_id, api.payload)
            if not review:
                api.abort(404, f"Avis avec l'id {review_id} non trouvé")
            return review
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(404, str(e))
    
    @api.doc('delete_review')
    @api.response(200, 'Avis supprimé avec succès')
    @api.response(401, 'Non authentifié')
    @api.response(403, 'Action non autorisée')
    @api.response(404, 'Avis non trouvé')
    @jwt_required()
    def delete(self, review_id):
        """
        Supprime un avis.
        
        L'utilisateur doit être authentifié.
        L'utilisateur ne peut supprimer que ses propres avis, sauf les administrateurs
        qui peuvent supprimer n'importe quel avis.
        
        Args:
            review_id (str): Identifiant de l'avis à supprimer
            
        Returns:
            dict: Message de confirmation
            
        Raises:
            401: Si l'utilisateur n'est pas authentifié
            403: Si l'utilisateur n'a pas les droits nécessaires
            404: Si l'avis n'existe pas
        """
        # Récupérer l'avis existant
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Avis avec l'id {review_id} non trouvé")
            
        # Vérifier que l'utilisateur a le droit de supprimer cet avis
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Les administrateurs peuvent supprimer n'importe quel avis
        # Si l'utilisateur n'est pas admin et n'est pas l'auteur de l'avis
        if not is_admin and review.user_id != current_user_id:
            api.abort(403, 'Unauthorized action')
        
        success = facade.delete_review(review_id)
        if not success:
            api.abort(404, f"Avis avec l'id {review_id} non trouvé")
            
        return {"message": "Avis supprimé avec succès"}

@api.route('/places/<place_id>/reviews')
@api.param('place_id', 'Identifiant du logement')
class PlaceReviewList(Resource):
    """
    Collection d'avis pour un logement spécifique.
    Permet de lister tous les avis pour un logement donné.
    """
    @api.doc('get_place_reviews')
    @api.response(200, 'Liste des avis pour le logement récupérée avec succès')
    @api.response(404, 'Logement non trouvé')
    @api.marshal_list_with(review_response_model)
    def get(self, place_id):
        """
        Récupère la liste des avis pour un logement spécifique.
        
        Args:
            place_id (str): Identifiant du logement
            
        Returns:
            list: Liste des avis pour ce logement
            
        Raises:
            404: Si le logement n'existe pas
        """
        # Vérifier d'abord si le logement existe
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Logement avec l'id {place_id} non trouvé")
            
        return facade.get_reviews_by_place(place_id)
