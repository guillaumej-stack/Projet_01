#!/usr/bin/env python3
"""
Script de test pour l'API Reddit Analysis SaaS
"""
import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def test_health():
    """Test de l'endpoint health"""
    print("🔍 Test de l'endpoint /health")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_check_subreddit():
    """Test de l'endpoint check_subreddit"""
    print("\n🔍 Test de l'endpoint /check_subreddit")
    try:
        # Test avec un subreddit existant
        data = {"subreddit_name": "python"}
        response = requests.post(f"{BASE_URL}/check_subreddit", json=data, headers=HEADERS, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_chat_simple():
    """Test de l'endpoint chat avec un message simple"""
    print("\n🔍 Test de l'endpoint /chat - Message simple")
    try:
        data = {
            "message": "Bonjour, peux-tu me présenter tes fonctionnalités ?",
            "session_id": "test_session_123"
        }
        response = requests.post(f"{BASE_URL}/chat", json=data, headers=HEADERS, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success', False)}")
            print(f"Response: {result.get('response', 'No response')[:200]}...")
            return True
        else:
            print(f"Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_analyze():
    """Test de l'endpoint analyze"""
    print("\n🔍 Test de l'endpoint /analyze")
    try:
        data = {
            "subreddit_name": "python",
            "num_posts": 5,
            "comments_limit": 5,
            "sort_criteria": "top",
            "time_filter": "month"
        }
        response = requests.post(f"{BASE_URL}/analyze", json=data, headers=HEADERS, timeout=60)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success', False)}")
            print(f"Message: {result.get('message', 'No message')}")
            return True
        else:
            print(f"Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_clear_history():
    """Test de l'endpoint clear_history"""
    print("\n🔍 Test de l'endpoint /clear_history")
    try:
        data = {"session_id": "test_session_123"}
        response = requests.delete(f"{BASE_URL}/clear_history", json=data, headers=HEADERS, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def run_all_tests():
    """Exécuter tous les tests"""
    print("🧪 DÉMARRAGE DES TESTS DE L'API")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Check Subreddit", test_check_subreddit),
        ("Chat Simple", test_chat_simple),
        ("Analyze", test_analyze),
        ("Clear History", test_clear_history),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 Test: {name}")
        print("-" * 30)
        success = test_func()
        results.append((name, success))
        time.sleep(2)  # Pause entre les tests
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DES TESTS")
    print("=" * 50)
    
    for name, success in results:
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"{name}: {status}")
    
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    print(f"\n🎯 Score: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        print("🎉 TOUS LES TESTS SONT PASSÉS ! L'API fonctionne correctement.")
    else:
        print(f"⚠️  {total_count - success_count} test(s) ont échoué.")

if __name__ == "__main__":
    run_all_tests() 