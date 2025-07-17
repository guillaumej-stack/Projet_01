#!/usr/bin/env python3
"""
API FastAPI pour l'analyse Reddit
Expose les fonctions du notebook comme endpoints REST
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import json
import sqlite3
from typing import Dict, List, Any, Optional
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import praw
from openai import OpenAI
from agents import Agent, Runner, function_tool, trace, WebSearchTool

# Charger les variables d'environnement
load_dotenv(override=True)

# Configuration
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "RedditScraper/1.0"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialiser Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Créer les dossiers
Path("temp").mkdir(exist_ok=True)
Path("exports").mkdir(exist_ok=True)

# Initialiser FastAPI
app = FastAPI(
    title="Reddit Analysis API",
    description="API pour l'analyse de subreddits avec des agents IA",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic
class SubredditCheckRequest(BaseModel):
    subreddit_name: str = Field(..., description="Nom du subreddit à vérifier")

class AnalysisRequest(BaseModel):
    subreddit_name: str = Field(..., description="Nom du subreddit à analyser")
    num_posts: int = Field(default=10, ge=1, le=50, description="Nombre de posts à analyser")
    comments_limit: int = Field(default=10, ge=1, le=50, description="Nombre de commentaires par post")
    sort_criteria: str = Field(default="top", description="Critère de tri (top, new, hot, best, rising)")

class ChatRequest(BaseModel):
    message: str = Field(..., description="Message de l'utilisateur")

class ExportRequest(BaseModel):
    format_type: str = Field(default="pdf", description="Format d'export (pdf, json, csv)")

# Fonctions utilitaires (reprises du notebook)
def _init_solutions_database() -> Dict[str, Any]:
    """Initialise la base de données SQLite pour stocker les commentaires avec solutions"""
    try:
        conn = sqlite3.connect('solutions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id TEXT UNIQUE,
                post_id TEXT,
                author TEXT,
                solution_text TEXT,
                score INTEGER,
                pain_type TEXT,
                intensity INTEGER,
                subreddit TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "✅ Base de données initialisée avec succès"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@function_tool
def init_solutions_database() -> Dict[str, str]:
    """Version pour les agents - Initialise la base de données SQLite"""
    result = _init_solutions_database()
    return {
        "success": str(result["success"]),
        "message": result.get("message", ""),
        "error": result.get("error", "")
    }

def _check_subreddit_exists(subreddit_name: str) -> Dict[str, Any]:
    """Vérifie si un subreddit existe et est accessible"""
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Tenter d'accéder aux informations du subreddit
        title = subreddit.display_name
        subscribers = subreddit.subscribers
        description = subreddit.public_description
        
        return {
            "success": True,
            "exists": True,
            "subreddit": subreddit_name,
            "title": title,
            "subscribers": subscribers,
            "description": description[:200] + "..." if len(description) > 200 else description
        }
        
    except Exception as e:
        if "private" in str(e).lower():
            return {
                "success": False,
                "exists": True,
                "error": "Ce subreddit est privé",
                "subreddit": subreddit_name
            }
        elif "banned" in str(e).lower():
            return {
                "success": False,
                "exists": False,
                "error": "Ce subreddit est banni",
                "subreddit": subreddit_name
            }
        else:
            return {
                "success": False,
                "exists": False,
                "error": f"Subreddit '{subreddit_name}' non trouvé",
                "subreddit": subreddit_name
            }

@function_tool
def check_subreddit_exists(subreddit_name: str) -> Dict[str, Any]:
    """Version pour les agents - Vérifie si un subreddit existe et est accessible"""
    return _check_subreddit_exists(subreddit_name)

def _get_stored_solutions(subreddit: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
    """Récupère les solutions stockées en base"""
    try:
        conn = sqlite3.connect('solutions.db')
        cursor = conn.cursor()
        
        if subreddit:
            cursor.execute('''
                SELECT * FROM solutions 
                WHERE subreddit = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (subreddit, limit))
        else:
            cursor.execute('''
                SELECT * FROM solutions 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
        
        solutions = cursor.fetchall()
        conn.close()
        
        # Convertir en format JSON
        solutions_list = []
        for sol in solutions:
            solutions_list.append({
                "id": sol[0],
                "comment_id": sol[1],
                "post_id": sol[2],
                "author": sol[3],
                "solution_text": sol[4],
                "score": sol[5],
                "pain_type": sol[6],
                "intensity": sol[7],
                "subreddit": sol[8],
                "created_at": sol[9]
            })
        
        return {
            "success": True,
            "solutions": solutions_list,
            "count": len(solutions_list)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@function_tool
def get_stored_solutions(subreddit: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
    """Version pour les agents - Récupère les solutions stockées en base"""
    return _get_stored_solutions(subreddit, limit)

# Endpoints API
@app.get("/")
async def root():
    """Endpoint de santé"""
    return {
        "message": "Reddit Analysis API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/check_subreddit")
async def check_subreddit_endpoint(request: SubredditCheckRequest):
    """Vérifie si un subreddit existe et est accessible"""
    try:
        result = _check_subreddit_exists(request.subreddit_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze_subreddit")
async def analyze_subreddit_endpoint(request: AnalysisRequest):
    """Analyse un subreddit (endpoint simplifié - à connecter avec vos agents)"""
    try:
        # Vérifier d'abord si le subreddit existe
        check_result = _check_subreddit_exists(request.subreddit_name)
        if not check_result["success"]:
            raise HTTPException(status_code=404, detail=check_result["error"])
        
        # TODO: Intégrer ici votre logique d'agents du notebook
        # Pour l'instant, retourner un exemple de réponse
        return {
            "success": True,
            "message": "Analyse lancée avec succès",
            "data": {
                "subreddit": request.subreddit_name,
                "posts_to_analyze": request.num_posts,
                "comments_limit": request.comments_limit,
                "sort_criteria": request.sort_criteria,
                "status": "in_progress"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Endpoint de chat avec l'assistant"""
    try:
        # TODO: Intégrer ici votre RouterAgent du notebook
        # Pour l'instant, logique simplifiée
        
        message = request.message.lower()
        
        if "analyser" in message or "analyse" in message:
            # Extraire le nom du subreddit
            import re
            subreddit_match = re.search(r'r/([a-zA-Z0-9_]+)', message)
            if subreddit_match:
                subreddit_name = subreddit_match.group(1)
                
                # Vérifier le subreddit
                check_result = _check_subreddit_exists(subreddit_name)
                if check_result["success"]:
                    return {
                        "success": True,
                        "response": f"✅ Subreddit r/{subreddit_name} trouvé ! Je lance l'analyse...",
                        "analysis_results": {
                            "subreddit": subreddit_name,
                            "subscribers": check_result.get("subscribers", 0),
                            "status": "ready_for_analysis"
                        }
                    }
                else:
                    return {
                        "success": False,
                        "response": f"❌ {check_result['error']}"
                    }
            else:
                return {
                    "success": True,
                    "response": "Je peux analyser un subreddit ! Utilisez le format : 'analyser r/nom_du_subreddit'"
                }
        
        # Réponse générique
        return {
            "success": True,
            "response": "Je suis votre assistant d'analyse Reddit. Demandez-moi d'analyser un subreddit avec : 'analyser r/nom_du_subreddit'"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stored_solutions")
async def get_stored_solutions_endpoint(subreddit: Optional[str] = None, limit: int = 10):
    """Récupère les solutions stockées"""
    try:
        result = _get_stored_solutions(subreddit, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export_results")
async def export_results_endpoint(request: ExportRequest):
    """Export des résultats d'analyse"""
    try:
        # TODO: Intégrer ici votre logique d'export du notebook
        return {
            "success": True,
            "message": f"Export en format {request.format_type} préparé",
            "format": request.format_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialiser la base de données au démarrage
@app.on_event("startup")
async def startup_event():
    """Initialisation au démarrage"""
    try:
        init_result = _init_solutions_database()
        print(f"Base de données: {init_result['message']}")
    except Exception as e:
        print(f"Erreur d'initialisation: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 