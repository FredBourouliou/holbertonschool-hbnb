// Constants
const API_URL = 'http://localhost:5001/api/v1';

$(document).ready(function() {
    // Éléments du DOM
    const $errorMessage = $('#error-message');
    const $successMessage = $('#success-message');
    const $reviewForm = $('#review-form');
    const $backLink = $('#back-to-place');

    // Récupérer l'ID de la place depuis l'URL
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id');

    if (!placeId) {
        window.location.href = '/templates/index.html';
        return;
    }

    // Mettre à jour les liens et champs
    $backLink.attr('href', `/templates/place.html?id=${placeId}`);
    $('#place-id').val(placeId);

    // Vérifier l'authentification
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/templates/login.html?redirect=' + encodeURIComponent(window.location.href);
        return;
    }

    // Décoder le token pour obtenir les informations utilisateur
    const decodedToken = parseJwt(token);
    if (!decodedToken) {
        showError('Erreur d\'authentification. Veuillez vous reconnecter.');
        return;
    }

    // Utiliser l'identifiant de l'utilisateur directement depuis le token
    const userId = decodedToken.sub; // L'identité de l'utilisateur est stockée dans le claim 'sub'

    console.log('Utilisateur authentifié avec ID:', userId);

    // Vérifier si l'utilisateur est propriétaire du logement en utilisant XMLHttpRequest pour éviter les problèmes CORS
    const placeCheckXhr = new XMLHttpRequest();
    placeCheckXhr.open('GET', `${API_URL}/places/${placeId}`, true);
    placeCheckXhr.setRequestHeader('Authorization', `Bearer ${token}`);
    
    placeCheckXhr.onload = function() {
        if (this.status >= 200 && this.status < 300) {
            const place = JSON.parse(this.responseText);
            
            if (place.owner && place.owner.id === userId) {
                showError('Vous ne pouvez pas noter votre propre logement.');
                $reviewForm.hide();
            } else {
                // Afficher le formulaire
                $reviewForm.show();
            }
        } else {
            console.error('Erreur lors de la récupération des informations du logement:', this.status);
            showError('Erreur lors de la récupération des informations du logement. Veuillez réessayer.');
        }
    };
    
    placeCheckXhr.onerror = function() {
        console.error('Erreur réseau lors de la vérification du logement');
        showError('Erreur de connexion au serveur. Veuillez vérifier votre connexion et réessayer.');
    };
    
    placeCheckXhr.send();

    // Gestion de la soumission du formulaire
    $reviewForm.on('submit', function(event) {
        event.preventDefault();
        
        const reviewText = $('#review-text').val();
        const rating = parseInt($('#rating').val());
        
        if (!reviewText || !rating) {
            showError('Veuillez remplir tous les champs obligatoires.');
            return;
        }
        
        // Récupérer les notes détaillées
        const detailedRatings = {
            cleanliness: parseInt($('#cleanliness').val()),
            location: parseInt($('#location').val()),
            value: parseInt($('#value').val()),
            accuracy: parseInt($('#accuracy').val())
        };
        
        // Calculer la moyenne des notes détaillées pour suggestion
        const avgDetailedRating = Math.round(
            (detailedRatings.cleanliness + 
             detailedRatings.location + 
             detailedRatings.value + 
             detailedRatings.accuracy) / 4
        );
        
        // Si l'utilisateur n'a pas explicitement choisi une note globale,
        // suggérer la moyenne des notes détaillées
        if (!$('#rating').val() && avgDetailedRating) {
            if (confirm(`Suggestion: D'après vos évaluations détaillées, la note globale pourrait être ${avgDetailedRating}/5. Voulez-vous utiliser cette note?`)) {
                $('#rating').val(avgDetailedRating);
                rating = avgDetailedRating;
            } else {
                showError('Veuillez sélectionner une note globale.');
                return;
            }
        }
        
        // Ajouter les notes détaillées au texte de la review au format JSON
        // Cela permet de conserver la structure de la base de données tout en ajoutant nos données
        const fullReviewText = JSON.stringify({
            comment: reviewText,
            detailed_ratings: detailedRatings
        });
        
        // Données de l'avis incluant place_id et user_id
        const reviewData = {
            text: fullReviewText,
            rating: rating,
            place_id: placeId,
            user_id: userId
        };
        
        console.log('Submitting review data:', reviewData);
        
        // Utiliser XMLHttpRequest au lieu de $.ajax pour éviter les problèmes CORS
        const xhr = new XMLHttpRequest();
        xhr.open('POST', `${API_URL}/reviews/`, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Authorization', `Bearer ${token}`);
        xhr.withCredentials = true;
        
        xhr.onload = function() {
            if (this.status >= 200 && this.status < 300) {
                console.log('Review submitted successfully');
                // Afficher le message de succès
                $successMessage.show();
                $reviewForm[0].reset();
                
                // Rediriger après un délai
                setTimeout(function() {
                    window.location.href = `/templates/place.html?id=${placeId}`;
                }, 2000);
            } else {
                console.error('Error submitting review:', this.status, this.statusText);
                console.error('Response text (if any):', this.responseText || 'No response text');
                
                let errorMsg = 'Échec de la soumission de l\'avis.';
                
                if (this.responseText) {
                    try {
                        const errorData = JSON.parse(this.responseText);
                        errorMsg = errorData.message || errorData.error || errorMsg;
                    } catch (e) {
                        // Pas de JSON valide dans la réponse
                    }
                }
                
                showError(errorMsg);
            }
        };
        
        xhr.onerror = function() {
            console.error('Network error during review submission');
            showError('Erreur de connexion au serveur. Veuillez vérifier votre connexion et réessayer.');
        };
        
        // Ajouter un gestionnaire de timeout pour détecter les problèmes de délai d'attente
        xhr.timeout = 10000; // 10 secondes
        xhr.ontimeout = function() {
            console.error('Timeout during review submission');
            showError('La connexion au serveur a expiré. Veuillez réessayer ultérieurement.');
        };
        
        // Envoyer les données au format JSON
        xhr.send(JSON.stringify(reviewData));
    });

    // Fonctions utilitaires
    function showError(message) {
        $errorMessage.text(message).show();
    }
});

// Fonction pour obtenir un cookie par son nom
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Fonction pour décoder un token JWT
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        console.error('Erreur lors du décodage du token JWT:', e);
        return null;
    }
} 