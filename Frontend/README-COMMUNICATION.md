# 🔗 Guide de Communication Frontend-Backend

## 📋 **Vue d'ensemble**

Ce guide explique comment le frontend Next.js communique avec le backend FastAPI après la réorganisation.

## 🏗️ **Architecture de Communication**

```
Frontend (Next.js) → API Client (axios) → Backend FastAPI (port 8000)
```

## ⚙️ **Configuration**

### 1. Variables d'environnement

Créez un fichier `.env.local` dans le dossier Frontend :

```bash
# Configuration API Backend FastAPI
NEXT_PUBLIC_API_URL=http://localhost:8000

# Mode de développement  
NODE_ENV=development
```

### 2. Configuration Next.js

Le fichier `next.config.js` est configuré pour :
- Définir l'URL de l'API par défaut
- Configurer les rewrites pour les appels API
- Gérer les headers CORS

## 🛠️ **Structure des API**

### Fichiers de communication :

```
Frontend/lib/
├── api.ts          # Client API principal avec tous les endpoints
├── api-utils.ts    # Utilitaires et helpers pour la communication
└── store.ts        # Gestion d'état (messages, analyses)
```

## 📡 **Endpoints disponibles**

### Backend FastAPI (port 8000) :

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/health` | GET | Vérification de l'état de l'API |
| `/chat` | POST | Chat principal avec RouterAgent |
| `/check_subreddit` | POST | Vérifier l'existence d'un subreddit |
| `/analyze` | POST | Analyser un subreddit |
| `/export` | POST | Exporter les résultats |
| `/clear_history` | DELETE | Effacer l'historique |

### Correspondance Frontend :

```typescript
// Exemples d'utilisation
import { redditAPI } from '@/lib/api'

// Chat principal
const response = await redditAPI.sendChatMessage(message, sessionId)

// Vérifier un subreddit
const checkResult = await redditAPI.checkSubreddit('programming')

// Analyser un subreddit
const analysis = await redditAPI.analyzeSubreddit('programming', 10, 5, 'top', 'month')

// Export
const exportResult = await redditAPI.exportResults('pdf', 'programming')

// Nettoyer l'historique
const clearResult = await redditAPI.clearChatHistory(sessionId)
```

## 🔧 **Utilitaires de Communication**

### `api-utils.ts` fournit :

1. **Vérification de connexion** :
```typescript
import { checkBackendConnection } from '@/lib/api-utils'

const status = await checkBackendConnection()
if (status.isHealthy) {
  // Backend disponible
}
```

2. **Appels API sécurisés** :
```typescript
import { safeApiCall } from '@/lib/api-utils'

const result = await safeApiCall(
  () => redditAPI.sendChatMessage(message),
  'Erreur lors de l\'envoi du message'
)
```

3. **Validation des paramètres** :
```typescript
import { validateAnalysisParams } from '@/lib/api-utils'

const errors = validateAnalysisParams({
  subredditName: 'programming',
  numPosts: 10,
  commentsLimit: 5
})
```

4. **Extraction automatique** :
```typescript
import { extractSubredditName, detectMessageType } from '@/lib/api-utils'

const subreddit = extractSubredditName('Analyse r/programming')
const messageType = detectMessageType('Analyse ce subreddit')
```

## 🚀 **Démarrage**

### 1. Backend (Terminal 1) :
```bash
cd Backend
uv run core/api.py
# ou
python core/api.py
```

### 2. Frontend (Terminal 2) :
```bash
cd Frontend
npm run dev
```

### 3. Vérification :
- Backend : http://localhost:8000
- Frontend : http://localhost:3000
- Health check : http://localhost:8000/health

## 🐛 **Débogage**

### Problèmes courants :

1. **Erreur CORS** :
   - Vérifiez que le backend est démarré
   - Confirmez que l'URL dans `.env.local` est correcte

2. **Timeout de connexion** :
   - Vérifiez que le port 8000 est libre
   - Redémarrez le backend

3. **Endpoints non trouvés** :
   - Vérifiez que vous utilisez la bonne version de l'API
   - Consultez http://localhost:8000/docs pour la documentation Swagger

### Logs utiles :

```bash
# Backend logs
cd Backend && uv run core/api.py

# Frontend logs (console du navigateur)
# Ouvrez les DevTools → Console
```

## ✅ **Fonctionnalités implémentées**

- ✅ Communication directe avec FastAPI
- ✅ Gestion d'erreurs automatique
- ✅ Validation des paramètres
- ✅ Monitoring de connexion
- ✅ Types TypeScript complets
- ✅ Retry automatique
- ✅ Toast notifications

## 🔄 **Prochaines étapes**

1. **Authentification** : Ajouter JWT si nécessaire
2. **WebSockets** : Pour les notifications en temps réel
3. **Cache** : Optimiser les requêtes répétées
4. **Offline** : Support mode hors ligne

---

**📞 Support** : En cas de problème, vérifiez d'abord les logs du backend et les DevTools du navigateur. 