# 🚀 Guide de Lancement - Reddit Analysis App

## 📋 Vue d'ensemble

Votre application est maintenant prête ! Voici comment la lancer :

```
Backend (FastAPI)  ←→  Frontend (Next.js)
   Port 8000              Port 3000
```

## 🔧 Prérequis

### 1. Variables d'environnement

Créez un fichier `.env` dans le dossier `Backend/` :

```bash
# Backend/.env
REDDIT_CLIENT_ID=votre_client_id
REDDIT_CLIENT_SECRET=votre_client_secret
OPENAI_API_KEY=votre_openai_key
```

### 2. Dépendances Python

```bash
cd Backend
pip install -r requirements.txt
```

### 3. Dépendances Node.js

```bash
cd Frontend
npm install
```

## 🚀 Lancement

### Option 1 : Lancement automatique (Recommandé)

#### Terminal 1 - Backend
```bash
cd Backend
python start-backend.py
```

#### Terminal 2 - Frontend
```bash
cd Frontend
npm run dev
```

### Option 2 : Lancement manuel

#### Terminal 1 - Backend
```bash
cd Backend
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 - Frontend
```bash
cd Frontend
npm run dev
```

## 🌐 Accès à l'application

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## 📱 Utilisation

1. Ouvrez http://localhost:3000
2. Tapez : `analyser r/programming` (ou n'importe quel subreddit)
3. L'application va :
   - Vérifier que le subreddit existe
   - Lancer l'analyse (actuellement basique)
   - Afficher les résultats

## 🔍 Test rapide

Pour tester la connexion :

```bash
# Tester l'API
curl http://localhost:8000/

# Tester la vérification d'un subreddit
curl -X POST http://localhost:8000/check_subreddit \
  -H "Content-Type: application/json" \
  -d '{"subreddit_name": "programming"}'
```

## 🔧 Prochaines étapes

### 1. Intégrer vos Agents du notebook

Dans `Backend/api.py`, remplacez les TODO par votre logique d'agents :

```python
# TODO dans analyze_subreddit_endpoint
# Intégrer ici votre logique d'agents du notebook

# TODO dans chat_endpoint  
# Intégrer ici votre RouterAgent du notebook
```

### 2. Copier les fonctions du notebook

Copiez depuis `Backend/Version_00.ipynb` vers `Backend/api.py` :

- Les définitions d'agents
- Les fonctions de scraping
- La logique d'analyse
- Les exports

### 3. Tester l'intégration complète

Une fois les agents intégrés, testez :

1. Analyse complète d'un subreddit
2. Génération de recommandations
3. Export des résultats
4. Stockage des solutions en base

## 📊 Structure de données

Le frontend s'attend à recevoir :

```typescript
interface ChatResponse {
  success: boolean
  response: string
  analysis_results?: {
    subreddit: string
    subscribers: number
    status: string
  }
}
```

## 🐛 Dépannage

### Problème : "Erreur de connexion au serveur"

**Solutions :**
1. Vérifiez que le backend est démarré sur le port 8000
2. Vérifiez les variables d'environnement
3. Regardez les logs du backend

### Problème : "CORS Error"

**Solution :** Le CORS est configuré pour localhost:3000. Si vous utilisez un autre port, modifiez `Backend/api.py` :

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "votre_autre_origin"],
    # ...
)
```

### Problème : "Module 'agents' not found"

**Solution :** Installez ou configurez le module agents selon votre notebook.

## 📁 Structure finale

```
Projet_Reddit/
├── Backend/
│   ├── api.py                 # ✅ API FastAPI
│   ├── start-backend.py       # ✅ Script de lancement
│   ├── requirements.txt       # ✅ Dépendances
│   ├── .env                   # À créer
│   └── Version_00.ipynb       # Votre notebook original
├── Frontend/
│   ├── app/page.tsx           # ✅ Interface utilisateur
│   ├── lib/api.ts             # ✅ Client API
│   ├── components/            # ✅ Composants React
│   └── package.json           # ✅ Configuration
└── GUIDE_LANCEMENT.md         # ✅ Ce guide
```

## 🎯 Prochaines améliorations

1. **Intégration complète des agents** du notebook
2. **Authentification utilisateur** (optionnel)
3. **Déploiement** sur serveur
4. **Monitoring** et logs
5. **Tests automatisés**

---

🎉 **Votre application est prête à être utilisée !**

Pour toute question, vérifiez d'abord les logs du backend et frontend. 