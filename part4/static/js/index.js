document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://localhost:5001/api/v1';
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    const locationSearch = document.getElementById('location-search');
    const searchButton = document.getElementById('search-button');
    
    let places = []; // Stockage des places pour le filtrage
    let placesOriginal = []; // Copie des places originales pour la réinitialisation des filtres

    // Fonction pour récupérer les places depuis l'API
    async function fetchPlaces() {
        try {
            const token = getCookie('token');
            const headers = {
                'Content-Type': 'application/json'
            };
            
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
                console.log('Using token for authorization');
            } else {
                console.log('No token found, proceeding without authentication');
            }
            
            console.log('Fetching places from:', `${API_URL}/places/`);
            const response = await fetch(`${API_URL}/places/`, {
                headers: headers
            });

            console.log('Response status:', response.status);
            
            if (response.ok) {
                places = await response.json();
                placesOriginal = [...places]; // Faire une copie
                console.log('Places loaded:', places.length);
                displayPlaces(places);
                initSearchListeners(); // Initialiser les écouteurs pour la recherche
            } else {
                console.error('Failed to fetch places:', response.status, response.statusText);
                placesList.innerHTML = '<p class="error">Failed to load places. Please try again later.</p>';
            }
        } catch (error) {
            console.error('Error fetching places:', error);
            placesList.innerHTML = '<p class="error">Error connecting to server. Please try again later.</p>';
        }
    }

    // Fonction pour obtenir un cookie par son nom
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
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

    // Fonction pour afficher les places
    function displayPlaces(placesToShow) {
        placesList.innerHTML = ''; // Nettoyer la liste existante

        if (placesToShow.length === 0) {
            placesList.innerHTML = '<p class="no-results">No places found matching your criteria.</p>';
            return;
        }

        placesToShow.forEach(place => {
            // Utiliser price_by_night s'il existe, sinon utiliser price
            const priceValue = place.price_by_night !== undefined ? place.price_by_night : place.price;
            
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
            
            const placeCard = document.createElement('div');
            placeCard.className = 'place-card';
            placeCard.innerHTML = `
                <div class="place-image">
                    <img src="/static/images/${imageName}" onerror="this.src='/static/images/placeholder.jpg'" alt="${place.title || 'Logement'}" />
                </div>
                <h3>${place.name || place.title}</h3>
                <div class="place-info">
                    <p class="place-location"><i class="location-icon"></i> ${locationName}</p>
                    <p class="place-price">€${priceValue} par nuit</p>
                </div>
                <p>${place.description ? place.description.substring(0, 150) + '...' : 'No description available'}</p>
                <a href="/templates/place.html?id=${place.id}" class="details-button">View Details</a>
            `;
            placesList.appendChild(placeCard);
        });
    }

    // Initialiser les écouteurs pour la recherche
    function initSearchListeners() {
        // Gestionnaire pour le bouton de recherche
        searchButton.addEventListener('click', performSearch);
        
        // Gestionnaire pour la recherche avec la touche Entrée
        locationSearch.addEventListener('keyup', (event) => {
            if (event.key === 'Enter') {
                performSearch();
            }
        });
    }

    // Fonction pour effectuer la recherche par localisation
    function performSearch() {
        const searchTerm = locationSearch.value.trim().toLowerCase();
        
        if (!searchTerm) {
            // Si la recherche est vide, revenir à toutes les places
            places = [...placesOriginal];
            filterByCurrentPrice();
            return;
        }
        
        // Recherche simple par correspondance de texte
        const locationFilteredPlaces = placesOriginal.filter(place => {
            const description = place.description ? place.description.toLowerCase() : '';
            const title = place.title ? place.title.toLowerCase() : '';
            
            // Rechercher dans différents champs liés à la localisation
            return (
                description.includes(searchTerm) || 
                title.includes(searchTerm) ||
                searchByCoordinates(place, searchTerm)
            );
        });
        
        places = locationFilteredPlaces;
        filterByCurrentPrice();
        
        console.log(`Found ${places.length} places matching "${searchTerm}"`);
    }
    
    // Fonction pour chercher par proximité des coordonnées
    // Ceci est une simulation simplifiée - un vrai système utiliserait une API de géocodage
    function searchByCoordinates(place, searchTerm) {
        // Liste des villes/régions et leurs coordonnées approximatives
        const locations = {
            'paris': { lat: 48.8566, lon: 2.3522 },
            'londres': { lat: 51.5074, lon: -0.1278 },
            'london': { lat: 51.5074, lon: -0.1278 },
            'newyork': { lat: 40.7128, lon: -74.0060 },
            'new york': { lat: 40.7128, lon: -74.0060 },
            'tokyo': { lat: 35.6762, lon: 139.6503 },
            'lyon': { lat: 45.7640, lon: 4.8357 },
            'marseille': { lat: 43.2965, lon: 5.3698 },
            'toulouse': { lat: 43.6047, lon: 1.4442 },
            'alpes': { lat: 45.8992, lon: 6.9292 },
            'montagne': { lat: 45.8992, lon: 6.9292 }
        };
        
        // Vérifier si le terme de recherche correspond à une ville/région connue
        for (const [location, coords] of Object.entries(locations)) {
            if (searchTerm.includes(location)) {
                // Si oui, vérifier si les coordonnées de la place sont proches
                if (place.latitude && place.longitude) {
                    const distance = calculateDistance(
                        coords.lat, coords.lon,
                        parseFloat(place.latitude), parseFloat(place.longitude)
                    );
                    // Considérer comme "proche" si moins de 100km (valeur arbitraire)
                    return distance < 100;
                }
            }
        }
        
        return false;
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

    // Gestionnaire de filtre par prix
    priceFilter.addEventListener('change', (event) => {
        filterByCurrentPrice();
    });
    
    // Fonction pour filtrer par le prix actuellement sélectionné
    function filterByCurrentPrice() {
        const maxPrice = priceFilter.value;
        console.log('Filter by price:', maxPrice);
        
        if (maxPrice === 'all') {
            displayPlaces(places);
        } else {
            // Vérifier que chaque place a une propriété price_by_night ou price et qu'elle est un nombre
            const filteredPlaces = places.filter(place => {
                // Utiliser price_by_night s'il existe, sinon utiliser price
                const priceValue = place.price_by_night !== undefined ? place.price_by_night : place.price;
                const price = Number(priceValue);
                const maxPriceValue = Number(maxPrice);
                
                // Vérifier si les valeurs sont valides
                if (isNaN(price) || isNaN(maxPriceValue)) {
                    console.error('Invalid price value:', priceValue, maxPrice);
                    return false;
                }
                
                return price <= maxPriceValue;
            });
            
            console.log('Filtered places:', filteredPlaces.length);
            displayPlaces(filteredPlaces);
        }
    }

    // Charger les places sans vérification d'authentification
    fetchPlaces();
}); 