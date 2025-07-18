from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Importer les agents
from reddit_agents import run_chat, clear_conversation_history, ROUTER_AGENT

# Configuration FastAPI
app = FastAPI(
    title="Reddit Analysis SaaS",
    description="API pour l'analyse de subreddits avec des agents IA - Version_00",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://votre-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== MODÈLES PYDANTIC =====

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    success: bool
    response: str
    session_id: str

class SubredditCheckRequest(BaseModel):
    subreddit_name: str

class AnalysisRequest(BaseModel):
    subreddit_name: str
    num_posts: int = 5
    comments_limit: int = 5
    sort_criteria: str = "top"
    time_filter: str = "month"

class ExportRequest(BaseModel):
    format_type: str = "pdf"
    subreddit: Optional[str] = None


# ===== ENDPOINTS PRINCIPAUX =====

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "Reddit Analysis SaaS API - Version_00",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "check_subreddit": "/check_subreddit",
            "analyze": "/analyze",
            "export": "/export",
            "clear_history": "/clear_history"
        }
    }

@app.get("/health")
async def health():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "agents": "loaded",
        "database": "supabase_connected"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal pour le chat avec RouterAgent
    """
    try:
        # Utiliser la fonction run_chat du système d'agents
        session_id = request.session_id or "default"
        result = await run_chat(request.message, session_id)
        
        return ChatResponse(
            success=result["success"],
            response=result.get("response", result.get("error", "Erreur inconnue")),
            session_id=result["session_id"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#=================== ENDPOINT SECONDAIRE ===================

@app.post("/check_subreddit")
async def check_subreddit_endpoint(request: SubredditCheckRequest):
    try:
        message = f"Vérifie si le subreddit {request.subreddit_name} existe"
        result = await run_chat(message, "check_subreddit")
        
        return {
            "success": result.get("success", False),
            "response": result.get("response", result.get("error", "Erreur inconnue")),
            "subreddit": request.subreddit_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_endpoint(request: AnalysisRequest):
    """
    Lance une analyse complète d'un subreddit
    """
    try:
        # Construire le message pour l'agent
        message = f"Analyse le subreddit r/{request.subreddit_name} avec {request.num_posts} posts, {request.comments_limit} commentaires par post, critère {request.sort_criteria}, période {request.time_filter}"
        
        result = await run_chat(message, f"analysis_{request.subreddit_name}")
        
        return {
            "success": result.get("success", False),
            "response": result.get("response", result.get("error", "Erreur inconnue")),
            "subreddit": request.subreddit_name,
            "parameters": {
                "num_posts": request.num_posts,
                "comments_limit": request.comments_limit,
                "sort_criteria": request.sort_criteria,
                "time_filter": request.time_filter
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export")
async def export_endpoint(request: ExportRequest):
    """
    Exporte les résultats d'analyse
    """
    try:
        # Construire le message pour l'agent
        message = f"Exporte les résultats au format {request.format_type}"
        if request.subreddit:
            message += f" pour le subreddit {request.subreddit}"
        
        result = await run_chat(message, "export_request")
        
        return {
            "success": result["success"],
            "response": result["response"],
            "format": request.format_type
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear_history")
async def clear_history_endpoint(session_id: str = "default"):
    """
    Efface l'historique de conversation
    """
    try:
        clear_conversation_history(session_id)
        return {
            "success": True,
            "message": f"Historique effacé pour la session {session_id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ===== LANCEMENT DE L'API =====

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Lancement de l'API Reddit Analysis SaaS")
    print("📊 Structure: Version_00.ipynb")
    print("🔗 Endpoints disponibles:")
    print("  - POST /chat (principal)")
    print("  - GET /health")
    print("  - POST /check_subreddit")
    print("  - POST /analyze")
    print("  - POST /export")
    print("  - DELETE /clear_history")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )