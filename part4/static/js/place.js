// Fonction pour obtenir un cookie par son nom
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Fonction pour extraire l'ID de la place depuis l'URL
function getPlaceIdFromURL() {
    // Récupérer l'ID depuis les paramètres de l'URL
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (placeId) {
        console.log("Place ID from URL parameters:", placeId);
        return placeId;
    }
    
    // Alternative: récupérer depuis le chemin /place/:id
    const pathParts = window.location.pathname.split('/');
    if (pathParts.includes('place')) {
        const index = pathParts.indexOf('place');
        if (index >= 0 && index < pathParts.length - 1) {
            const pathId = pathParts[index + 1];
            console.log("Place ID from URL path:", pathId);
            return pathId;
        }
    }
    
    console.log("No place ID found in URL");
    return null;
}

// Fonction pour déterminer la ville/région en fonction des coordonnées
function getLocationFromCoordinates(latitude, longitude) {
    // Définir les régions connues avec leurs coordonnées approximatives
    const locations = [
        { name: "Paris", lat: 48.8566, lon: 2.3522, radius: 50 },
        { name: "Londres", lat: 51.5074, lon: -0.1278, radius: 50 },
        { name: "New York", lat: 40.7128, lon: -74.0060, radius: 50 },
        { name: "Tokyo", lat: 35.6762, lon: 139.6503, radius: 50 },
        { name: "Lyon", lat: 45.7640, lon: 4.8357, radius: 30 },
        { name: "Marseille", lat: 43.2965, lon: 5.3698, radius: 30 },
        { name: "Toulouse", lat: 43.6047, lon: 1.4442, radius: 30 },
        { name: "Alpes", lat: 45.8992, lon: 6.9292, radius: 100 }
    ];
    
    // Calculer les distances et trouver la région la plus proche
    let closestLocation = null;
    let minDistance = Number.MAX_VALUE;
    
    for (const location of locations) {
        const distance = calculateDistance(
            location.lat, location.lon,
            parseFloat(latitude), parseFloat(longitude)
        );
        
        if (distance < location.radius && distance < minDistance) {
            minDistance = distance;
            closestLocation = location;
        }
    }
    
    return closestLocation ? closestLocation.name : "Autre région";
}

// Fonction pour calculer la distance entre deux points en km (formule de Haversine)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Rayon de la Terre en km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Fonction pour récupérer les détails d'une place
async function fetchPlaceDetails() {
    // Récupérer l'ID de la place
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        document.getElementById('place-details').innerHTML = 
            '<p class="error">No place ID provided</p>';
        return;
    }
    
    const token = getCookie('token');
    console.log("Fetching place data with ID:", placeId);
    
    try {
        // Récupérer toutes les places
        const response = await fetch('http://localhost:5001/api/v1/places/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : ''
            }
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        const places = await response.json();
        console.log(`Received ${places.length} places from API`);
        
        // Trouver la place par son ID
        const place = places.find(p => p.id === placeId);
        
        if (!place) {
            throw new Error(`Place with ID ${placeId} not found`);
        }
        
        console.log("Found place:", place);
        
        // Afficher les détails
        renderPlaceDetails(place);
        
        // Configurer le bouton d'ajout de review
        setupAddReviewButton(placeId);
        
    } catch (error) {
        console.error('Error fetching place:', error);
        document.getElementById('place-details').innerHTML = 
            `<p class="error">Error: ${error.message}</p>`;
    }
}

// Fonction pour afficher les détails d'une place
function renderPlaceDetails(place) {
    // Déterminer le nom de l'image à utiliser basé sur le titre de la place
    let imageName = 'placeholder.jpg';
    const title = place.title ? place.title.toLowerCase() : '';
    
    if (title.includes('admin')) {
        imageName = 'places/maison_admin.jpg';
    } else if (title.includes('économique') || title.includes('economique')) {
        imageName = 'places/appartement_economique.jpg';
    } else if (title.includes('confortable')) {
        imageName = 'places/maison_confortable.jpg';
    } else if (title.includes('luxe')) {
        imageName = 'places/villa_luxe.jpg';
    } else if (title.includes('studio') || title.includes('centre-ville')) {
        imageName = 'places/studio_centre_ville.jpg';
    } else if (title.includes('chalet') || title.includes('montagne')) {
        imageName = 'places/chalet_montagne.jpg';
    }
    
    // Déterminer la ville/région
    const locationName = getLocationFromCoordinates(place.latitude || 0, place.longitude || 0);
    
    // Préparation du HTML pour les informations
    const placeInfo = `
        <div class="place-detail-image">
            <img src="/static/images/${imageName}" onerror="this.src='/static/images/placeholder.jpg'" alt="${place.title || 'Logement'}" />
        </div>
        <h1>${place.title || 'Unnamed Place'}</h1>
        <p class="price">€${place.price || '0'} per night</p>
        <p class="description">${place.description || 'No description available'}</p>
        
        <div class="details">
            <p><strong>Région:</strong> ${locationName}</p>
            <p><strong>Coordonnées:</strong> ${place.latitude || '0'}, ${place.longitude || '0'}</p>
            <p><strong>Propriétaire:</strong> ${place.owner ? 
                `${place.owner.first_name || ''} ${place.owner.last_name || ''}`.trim() || 'Unknown' 
                : 'Unknown'}</p>
        </div>

        <div class="amenities">
            <h2>Amenities</h2>
            <ul>
                ${Array.isArray(place.amenities) && place.amenities.length > 0 ? 
                    place.amenities.map(amenity => 
                        `<li>${amenity.name || 'Unnamed amenity'}</li>`
                    ).join('') 
                    : '<li>No amenities listed</li>'
                }
            </ul>
        </div>
    `;

    // Préparation du HTML pour les reviews
    const reviewsHTML = `
        <h2>Reviews</h2>
        <div id="reviews-list">
            ${Array.isArray(place.reviews) && place.reviews.length > 0 ? 
                place.reviews.map(review => {
                    // Essayer de parser le texte comme JSON pour extraire les évaluations détaillées
                    let reviewComment = review.text || 'No review text';
                    let detailedRatings = null;
                    
                    try {
                        const reviewData = JSON.parse(review.text);
                        if (reviewData.comment) {
                            reviewComment = reviewData.comment;
                        }
                        if (reviewData.detailed_ratings) {
                            detailedRatings = reviewData.detailed_ratings;
                        }
                    } catch (e) {
                        // Ce n'est pas un JSON valide, utiliser le texte tel quel
                        console.log('Review text is not valid JSON:', review.text);
                    }
                    
                    // Générer le HTML pour les évaluations détaillées si disponibles
                    let detailedRatingsHTML = '';
                    if (detailedRatings) {
                        detailedRatingsHTML = `
                            <div class="detailed-ratings-display">
                                <div class="rating-item">
                                    <span class="rating-label">Propreté:</span>
                                    <span class="rating-stars">${'★'.repeat(detailedRatings.cleanliness)}${'☆'.repeat(5 - detailedRatings.cleanliness)}</span>
                                </div>
                                <div class="rating-item">
                                    <span class="rating-label">Emplacement:</span>
                                    <span class="rating-stars">${'★'.repeat(detailedRatings.location)}${'☆'.repeat(5 - detailedRatings.location)}</span>
                                </div>
                                <div class="rating-item">
                                    <span class="rating-label">Rapport qualité/prix:</span>
                                    <span class="rating-stars">${'★'.repeat(detailedRatings.value)}${'☆'.repeat(5 - detailedRatings.value)}</span>
                                </div>
                                <div class="rating-item">
                                    <span class="rating-label">Précision:</span>
                                    <span class="rating-stars">${'★'.repeat(detailedRatings.accuracy)}${'☆'.repeat(5 - detailedRatings.accuracy)}</span>
                                </div>
                            </div>
                        `;
                    }
                    
                    return `
                        <div class="review-card">
                            <div class="review-rating">
                                ${'★'.repeat(review.rating || 0)}${'☆'.repeat(5 - (review.rating || 0))}
                                <span class="rating-text">Note globale</span>
                            </div>
                            ${detailedRatingsHTML}
                            <p class="review-text">${reviewComment}</p>
                            <p class="review-user">By: ${review.user ? 
                                `${review.user.first_name || ''} ${review.user.last_name || ''}`.trim() || 'Anonymous' 
                                : 'Anonymous'}</p>
                            <p class="review-date">${review.created_at ? 
                                new Date(review.created_at).toLocaleDateString() 
                                : 'Unknown date'}</p>
                        </div>
                    `;
                }).join('') 
                : '<p>No reviews yet</p>'
            }
        </div>
        <a href="/templates/add_review.html?id=${place.id}" class="details-button" id="add-review-button">Add Review</a>
    `;

    // Mise à jour du DOM
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        placeDetails.innerHTML = `
            <div class="place-info">${placeInfo}</div>
            <div class="reviews">${reviewsHTML}</div>
        `;
    } else {
        console.error('Element #place-details not found');
    }
}

// Fonction pour configurer le bouton d'ajout de review
function setupAddReviewButton(placeId) {
    const addReviewButton = document.getElementById('add-review-button');
    if (addReviewButton && placeId) {
        addReviewButton.href = `/templates/add_review.html?id=${placeId}`;
        
        // Vérifier si l'utilisateur est connecté
        const token = getCookie('token');
        if (!token) {
            // Cacher le bouton si non connecté
            addReviewButton.style.display = 'none';
        }
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    console.log("Page loaded, fetching place details");
    fetchPlaceDetails();
}); 