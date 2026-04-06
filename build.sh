#!/usr/bin/env bash
# ==============================================================================
# SCRIPT DE BUILD POUR RENDER
# ==============================================================================

set -o errexit
set -o pipefail

echo "🚀 Début du build..."

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate --no-input

# Charger les données initiales si nécessaire
if [ -f "load_initial_data.py" ]; then
    echo "📊 Chargement des données initiales..."
    python load_initial_data.py
fi

echo "✅ Build terminé avec succès!"
