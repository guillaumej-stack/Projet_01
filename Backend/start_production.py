#!/usr/bin/env python3
"""
Script de démarrage pour la production (Railway)
"""
import os
import uvicorn
from core.api import app

if __name__ == "__main__":
    # Configuration pour la production
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print("🚀 Démarrage du serveur API en production...")
    print(f"📡 Host: {host}")
    print(f"📡 Port: {port}")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    ) 