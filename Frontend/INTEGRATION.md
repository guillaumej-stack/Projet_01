# Guide d'Intégration Backend-Frontend

Ce guide explique comment connecter le frontend Next.js à votre backend Python avec les agents Reddit.

## 🔗 Architecture de Communication

```
Frontend (Next.js) ←→ Backend (Python + Agents)
     Port 3000           Port 8000
```

## 📋 Prérequis

1. **Backend Python** en cours d'exécution sur `http://localhost:8000`
2. **Frontend Next.js** installé et configuré
3. **Variables d'environnement** correctement définies

## 🚀 Étapes d'Intégration

### 1. Démarrer le Backend Python

```bash
cd Backend
# Assurez-vous que votre serveur Python est en cours d'exécution
# Par exemple avec FastAPI ou Gradio
```

### 2. Démarrer le Frontend

```bash
cd Frontend
npm run dev
```

### 3. Tester la Connexion

Ouvrez `http://localhost:3000` et testez l'interface.

## 🔧 Configuration Backend

### Endpoints Requis

Votre backend Python doit exposer ces endpoints :

#### 1. Vérification de Subreddit
```python
@app.post("/check_subreddit")
async def check_subreddit(request: dict):
    subreddit_name = request.get("subreddit_name")
    # Utiliser votre fonction check_subreddit_exists
    result = check_subreddit_exists(subreddit_name)
    return result
```

#### 2. Analyse de Subreddit
```python
@app.post("/analyze_subreddit")
async def analyze_subreddit(request: dict):
    # Utiliser votre système d'agents
    # RouterAgent → WorkflowManager → Agents spécialisés
    result = await run_analysis(request)
    return result
```

#### 3. Export des Résultats
```python
@app.post("/export_results")
async def export_results(request: dict):
    format_type = request.get("format", "pdf")
    # Utiliser vos fonctions d'export
    result = export_final_report(analysis_data, recommendations_data, format_type)
    return result
```

#### 4. Solutions Stockées
```python
@app.get("/stored_solutions")
async def get_stored_solutions(subreddit: str = None):
    # Utiliser votre fonction get_stored_solutions
    result = get_stored_solutions(subreddit)
    return result
```

## 🔄 Intégration avec vos Agents

### Modification du Frontend

Dans `Frontend/app/page.tsx`, remplacez la fonction `simulateBackendResponse` par :

```typescript
const handleSendMessage = async (content: string) => {
  if (!content.trim() || isProcessing) return

  addMessage({ role: 'user', content })
  setIsProcessing(true)
  setTyping(true)

  try {
    // Appel réel à votre backend
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: content })
    })
    
    const data = await response.json()
    
    if (data.success) {
      addMessage({ role: 'assistant', content: data.response })
      
      // Si c'est une analyse, traiter les résultats
      if (data.analysis_results) {
        setAnalysisResults(data.analysis_results)
      }
    } else {
      addMessage({ 
        role: 'assistant', 
        content: `❌ Erreur: ${data.error}` 
      })
    }
    
  } catch (error) {
    console.error('Erreur:', error)
    addMessage({ 
      role: 'assistant', 
      content: '❌ Erreur de connexion au serveur' 
    })
  } finally {
    setIsProcessing(false)
    setTyping(false)
  }
}
```

### Endpoint Chat dans le Backend

Ajoutez cet endpoint à votre backend Python :

```python
@app.post("/chat")
async def chat_endpoint(request: dict):
    message = request.get("message", "")
    
    # Utiliser votre RouterAgent
    context = f"Humain: {message}\nAssistant: "
    result = await Runner.run(agent_0, context)
    
    return {
        "success": True,
        "response": result.final_output,
        "analysis_results": None  # Si applicable
    }
```

## 📊 Gestion des Données

### Format des Données

Le frontend s'attend à recevoir les données dans ce format :

```typescript
interface AnalysisResponse {
  success: boolean
  data?: {
    subreddit: string
    posts_analyzed: number
    total_comments_analyzed: number
    top_3_pains: Array<{
      pain_type: string
      score: number
      summary: string
    }>
    solutions_found: Array<{
      comment_id: string
      author: string
      solution_text: string
      score: number
    }>
    overall_summary: string
  }
  error?: string
}
```

### Mapping des Données

Assurez-vous que votre backend retourne les données dans le bon format :

```python
def format_analysis_results(analysis_data):
    """Formate les résultats pour le frontend"""
    return {
        "success": True,
        "data": {
            "subreddit": analysis_data.get("subreddit"),
            "posts_analyzed": analysis_data.get("posts_analyzed", 0),
            "total_comments_analyzed": analysis_data.get("total_comments_analyzed", 0),
            "top_3_pains": analysis_data.get("top_3_pains", []),
            "solutions_found": analysis_data.get("solutions_found", []),
            "overall_summary": analysis_data.get("overall_summary", "")
        }
    }
```

## 🔒 Gestion des Erreurs

### Côté Frontend

```typescript
// Dans lib/api.ts
const handleApiError = (error: any) => {
  if (error.response?.status === 404) {
    return "Service non trouvé"
  }
  if (error.response?.status === 500) {
    return "Erreur interne du serveur"
  }
  if (error.code === 'ECONNREFUSED') {
    return "Impossible de se connecter au serveur"
  }
  return "Erreur inconnue"
}
```

### Côté Backend

```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {
        "success": False,
        "error": str(exc),
        "timestamp": datetime.now().isoformat()
    }
```

## 🚀 Déploiement

### Variables d'Environnement Production

```env
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://votre-backend.com

# Backend
CORS_ORIGINS=https://votre-frontend.com
```

### CORS Configuration

Dans votre backend Python :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://votre-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Tests

### Test de Connexion

```bash
# Test du backend
curl -X POST http://localhost:8000/check_subreddit \
  -H "Content-Type: application/json" \
  -d '{"subreddit_name": "programming"}'

# Test du frontend
curl http://localhost:3000
```

### Test d'Intégration

1. Ouvrez le frontend
2. Tapez "analyser r/programming"
3. Vérifiez que l'analyse se lance
4. Vérifiez que les résultats s'affichent

## 🔧 Dépannage

### Problèmes Courants

1. **CORS Error** : Vérifiez la configuration CORS du backend
2. **Connection Refused** : Vérifiez que le backend est en cours d'exécution
3. **Data Format Error** : Vérifiez le format des données retournées
4. **Timeout** : Augmentez les timeouts si nécessaire

### Logs de Débogage

```typescript
// Frontend - Activer les logs
console.log('API Response:', response)
```

```python
# Backend - Activer les logs
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

En cas de problème :

1. Vérifiez les logs du backend et du frontend
2. Testez les endpoints individuellement
3. Vérifiez la configuration CORS
4. Assurez-vous que les formats de données correspondent 