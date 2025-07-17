#!/usr/bin/env python3
"""
Script de lancement pour l'API FastAPI
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

def check_requirements():
    """Vérifier que les dépendances sont installées"""
    try:
        import fastapi
        import uvicorn
        import praw
        import openai
        print("✅ Dépendances OK")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("Installez les dépendances avec: pip install -r requirements.txt")
        return False

def check_env_vars():
    """Vérifier les variables d'environnement"""
    required_vars = [
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'OPENAI_API_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Variables d'environnement manquantes: {', '.join(missing)}")
        print("Créez un fichier .env avec ces variables")
        return False
    
    print("✅ Variables d'environnement OK")
    return True

def main():
    """Fonction principale"""
    print("🚀 Démarrage de l'API Reddit Analysis...")
    
    # Vérifier les prérequis
    if not check_requirements():
        sys.exit(1)
    
    if not check_env_vars():
        sys.exit(1)
    
    # Démarrer l'API
    print("🌐 Démarrage du serveur FastAPI sur http://localhost:8000")
    print("📖 Documentation disponible sur http://localhost:8000/docs")
    print("Appuyez sur Ctrl+C pour arrêter")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur")

if __name__ == "__main__":
    main() 