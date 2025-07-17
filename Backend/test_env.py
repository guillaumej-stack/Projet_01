#!/usr/bin/env python3
"""
Script de test pour vérifier le chargement des variables d'environnement
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def test_env_loading():
    """Teste le chargement des variables d'environnement"""
    print("🔍 Test de chargement des variables d'environnement...")
    print(f"📂 Répertoire courant: {Path.cwd()}")
    
    # Vérifier si le fichier .env existe
    env_file = Path(".env")
    if env_file.exists():
        print(f"✅ Fichier .env trouvé: {env_file.absolute()}")
        print(f"📏 Taille du fichier: {env_file.stat().st_size} bytes")
    else:
        print("❌ Fichier .env non trouvé")
        return False
    
    # Charger les variables d'environnement
    load_dotenv(override=True)
    
    # Vérifier chaque variable
    variables = {
        'REDDIT_CLIENT_ID': 'Client ID Reddit',
        'REDDIT_CLIENT_SECRET': 'Client Secret Reddit', 
        'OPENAI_API_KEY': 'Clé API OpenAI'
    }
    
    print("\n📋 Vérification des variables:")
    all_good = True
    
    for var_name, description in variables.items():
        value = os.getenv(var_name)
        if value:
            # Masquer la valeur pour la sécurité
            masked_value = value[:6] + "..." + value[-4:] if len(value) > 10 else "***"
            print(f"✅ {var_name}: {masked_value} ({description})")
        else:
            print(f"❌ {var_name}: MANQUANTE ({description})")
            all_good = False
    
    return all_good

def show_env_file_content():
    """Affiche le contenu du fichier .env (masqué pour la sécurité)"""
    env_file = Path(".env")
    if env_file.exists():
        print(f"\n📄 Contenu du fichier .env:")
        with open(env_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        masked_value = value[:6] + "..." + value[-4:] if len(value) > 10 else "***"
                        print(f"  {i:2d}: {key}={masked_value}")
                    else:
                        print(f"  {i:2d}: {line} ⚠️  (Format incorrect)")
                else:
                    print(f"  {i:2d}: {line}")

if __name__ == "__main__":
    print("🧪 Test des variables d'environnement Reddit Analysis")
    print("=" * 50)
    
    # Tester le chargement
    success = test_env_loading()
    
    # Afficher le contenu du fichier
    show_env_file_content()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Toutes les variables sont correctement chargées!")
        print("✅ Vous pouvez lancer l'API avec: python start-backend.py")
    else:
        print("❌ Certaines variables manquent ou sont mal formatées")
        print("🔧 Vérifiez votre fichier .env et corrigez les problèmes") 