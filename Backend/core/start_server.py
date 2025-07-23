#!/usr/bin/env python3
"""
Script de démarrage simple pour l'API Reddit Analysis SaaS
"""
import uvicorn
from .api import app

if __name__ == "__main__":
    print("🚀 Démarrage du serveur API...")
    print("📡 Accessible sur: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="127.0.0.1",  # localhost spécifiquement
        port=8000,
        reload=True,
        log_level="info"
    ) 