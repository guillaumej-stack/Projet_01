#!/usr/bin/env python3
"""
Test simple pour vérifier la connexion à l'API
"""
import requests
import json

BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def test_connection():
    """Test de connexion basique"""
    print("🔍 Test de connexion à l'API...")
    
    try:
        # Test du endpoint health
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Connexion réussie !")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        data = {"subreddit_name": "python"}
        response2 = requests.post(f"{BASE_URL}/check_subreddit", json=data, headers=HEADERS, timeout=10)
        print(f"Status: {response2.status_code}")
        print(f"Response: {response2.json()}")
        return response2.status_code == 200
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API")
        print("💡 Vérifiez que l'API est démarrée avec: uv run start_server.py")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    test_connection() 