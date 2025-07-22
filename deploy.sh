#!/bin/bash

echo "🚀 Script de déploiement - Projet Reddit"
echo "========================================"

# Vérifier que git est configuré
if ! git config --get user.name > /dev/null 2>&1; then
    echo "❌ Git n'est pas configuré. Veuillez configurer votre nom et email Git."
    exit 1
fi

# Vérifier les modifications
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Modifications détectées. Commit en cours..."
    git add .
    git commit -m "🔧 Préparation pour déploiement Vercel/Railway"
fi

# Pousser vers GitHub
echo "📤 Push vers GitHub..."
git push origin main

echo "✅ Déploiement préparé !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Allez sur Railway.app et déployez le backend"
echo "2. Allez sur Vercel.com et déployez le frontend"
echo "3. Configurez les variables d'environnement"
echo ""
echo "📖 Consultez DEPLOYMENT_GUIDE.md pour les instructions détaillées" 