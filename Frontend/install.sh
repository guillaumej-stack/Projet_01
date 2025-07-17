#!/bin/bash

echo "🚀 Installation du Frontend Reddit Agents..."

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Veuillez l'installer depuis https://nodejs.org/"
    exit 1
fi

# Vérifier si npm est installé
if ! command -v npm &> /dev/null; then
    echo "❌ npm n'est pas installé. Veuillez l'installer."
    exit 1
fi

echo "✅ Node.js et npm détectés"

# Installer les dépendances
echo "📦 Installation des dépendances..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dépendances installées avec succès"
else
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi

# Créer le fichier .env.local s'il n'existe pas
if [ ! -f .env.local ]; then
    echo "🔧 Création du fichier .env.local..."
    cp env.example .env.local
    echo "✅ Fichier .env.local créé"
else
    echo "✅ Fichier .env.local existe déjà"
fi

echo ""
echo "🎉 Installation terminée !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Assurez-vous que votre backend Python est en cours d'exécution sur http://localhost:8000"
echo "2. Lancez le serveur de développement : npm run dev"
echo "3. Ouvrez http://localhost:3000 dans votre navigateur"
echo ""
echo "🔧 Commandes utiles :"
echo "  npm run dev      # Serveur de développement"
echo "  npm run build    # Build de production"
echo "  npm run start    # Serveur de production"
echo "  npm run lint     # Linting" 