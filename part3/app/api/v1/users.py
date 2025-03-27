from flask_restx import Resource, Namespace, fields
from app.api.v1.models import user_model
from app.api import api
from app.api.v1.facades import user_facade as facade
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required

api = Namespace('users', description='User related operations')
api.models[user_model.name] = user_model

@api.route('/<user_id>')
@api.param('user_id', 'Identifiant de l\'utilisateur')
class UserResource(Resource):
    """
    Ressource utilisateur individuelle.
    Permet de récupérer, mettre à jour ou supprimer un utilisateur spécifique.
    """
    @api.doc('get_user')
    @api.marshal_with(user_model)
    @api.response(200, 'Succès', user_model)
    @api.response(404, 'Utilisateur non trouvé')
    def get(self, user_id):
        """
        Récupère les informations d'un utilisateur par son ID.
        
        Args:
            user_id (str): Identifiant de l'utilisateur
            
        Returns:
            dict: Informations de l'utilisateur
            
        Raises:
            404: Si l'utilisateur n'existe pas
        """
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"Utilisateur avec l'id {user_id} non trouvé")
        return user.to_dict()
    
    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'Utilisateur mis à jour avec succès', user_model)
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(403, 'Permission refusée')
    @jwt_required()
    def put(self, user_id):
        """
        Met à jour les informations d'un utilisateur.
        Nécessite d'être connecté comme l'utilisateur concerné ou comme administrateur.
        L'email et le mot de passe ne peuvent être modifiés que par les administrateurs.
        
        Args:
            user_id (str): Identifiant de l'utilisateur à mettre à jour
            
        Returns:
            dict: Informations de l'utilisateur mises à jour
            
        Raises:
            404: Si l'utilisateur n'existe pas
            400: Si les données fournies sont invalides
            403: Si l'utilisateur connecté n'a pas les permissions nécessaires
        """
        # Vérification des permissions
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Vérifier si l'utilisateur est admin ou s'il modifie son propre profil
        if not is_admin and current_user_id != user_id:
            api.abort(403, "Unauthorized action")
        
        # Vérifier les restrictions sur l'email et le mot de passe
        update_data = api.payload.copy()
        
        # Si ce n'est pas un admin et qu'il essaie de modifier l'email ou le mot de passe
        if not is_admin and ('email' in update_data or 'password' in update_data):
            api.abort(400, "You cannot modify email or password")
            
        try:
            user = facade.update_user(user_id, update_data)
            if not user:
                api.abort(404, f"Utilisateur avec l'id {user_id} non trouvé")
            return user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))