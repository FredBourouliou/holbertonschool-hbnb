#!/bin/bash

# Script pour télécharger des images de logements et les renommer selon les IDs des places
# Ce script télécharge des images de maisons/appartements depuis Unsplash

# Créer le répertoire des images si nécessaire
mkdir -p static/images/places

# Télécharger des images de qualité pour les logements
echo "Téléchargement des images de logements..."

# Images d'Unsplash (libres de droits)
IMAGES=(
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800"
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800"
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"
    "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800"
    "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800"
    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800"
)

# Liste des noms de logements (pour pouvoir les identifier même sans l'ID)
PLACE_NAMES=(
    "maison_admin"
    "appartement_economique"
    "maison_confortable"
    "villa_luxe"
    "studio_centre_ville"
    "chalet_montagne"
)

# Télécharger une image par défaut (placeholder)
echo "Téléchargement de l'image placeholder..."
curl -s "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800" -o static/images/placeholder.jpg

# Télécharger les images et les renommer
echo "Téléchargement des images pour les logements..."
for i in "${!IMAGES[@]}"; do
    echo "Téléchargement de l'image ${i}..."
    curl -s "${IMAGES[$i]}" -o "static/images/places/${PLACE_NAMES[$i]}.jpg"
    echo "Image ${PLACE_NAMES[$i]}.jpg téléchargée."
done

echo "Téléchargement des images terminé!"
echo "Les images sont disponibles dans static/images/places/" 