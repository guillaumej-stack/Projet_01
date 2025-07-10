#!/usr/bin/env python3
"""
Script de debug pour identifier les problèmes Jupyter/Kernel
"""
import sys
import os
import subprocess
import json
from pathlib import Path

def debug_jupyter_setup():
    print("=== DEBUG JUPYTER SETUP ===\n")
    
    # 1. Python info
    print("1. PYTHON INFO:")
    print(f"   Executable: {sys.executable}")
    print(f"   Version: {sys.version}")
    print(f"   Virtual env: {hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)}")
    print()
    
    # 2. Jupyter info
    print("2. JUPYTER INFO:")
    try:
        result = subprocess.run([sys.executable, "-m", "jupyter", "--version"], 
                              capture_output=True, text=True)
        print(f"   Jupyter version: {result.stdout.strip()}")
    except Exception as e:
        print(f"   ❌ Jupyter not installed: {e}")
    
    # 3. Kernels disponibles
    print("\n3. KERNELS DISPONIBLES:")
    try:
        result = subprocess.run([sys.executable, "-m", "jupyter", "kernelspec", "list"], 
                              capture_output=True, text=True)
        print(f"   {result.stdout}")
    except Exception as e:
        print(f"   ❌ Erreur kernelspec: {e}")
    
    # 4. Packages installés
    print("4. PACKAGES CLÉS:")
    packages = ['jupyter', 'ipykernel', 'notebook', 'ipython']
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"   ✅ {pkg}")
        except ImportError:
            print(f"   ❌ {pkg} manquant")
    
    # 5. Chemins Jupyter
    print("\n5. CHEMINS JUPYTER:")
    try:
        result = subprocess.run([sys.executable, "-m", "jupyter", "--paths"], 
                              capture_output=True, text=True)
        print(f"   {result.stdout}")
    except Exception as e:
        print(f"   ❌ Erreur paths: {e}")
    
    # 6. Test de création de kernel
    print("6. TEST CRÉATION KERNEL:")
    try:
        result = subprocess.run([
            sys.executable, "-m", "ipykernel", "install", "--user", 
            "--name=test-kernel", "--display-name=Test Kernel"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Kernel créé avec succès")
        else:
            print(f"   ❌ Erreur création kernel: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Exception création kernel: {e}")

if __name__ == "__main__":
    debug_jupyter_setup()