#!/usr/bin/env python3
"""
Script ultra-simple pour démarrer l'API
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Démarrage simple de l'API...")
    print("📡 Accessible sur: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("=" * 50)
    
    # Lancer directement l'API en important le module
    uvicorn.run(
        "api:app",  # Import string pour éviter les conflits
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 