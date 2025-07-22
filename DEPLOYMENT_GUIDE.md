# Guide de Déploiement - Projet Reddit

Ce guide vous accompagne pour déployer votre projet Reddit sur Vercel (frontend) et Railway (backend).

## 📋 Prérequis

- Compte GitHub avec votre projet
- Compte Vercel (gratuit)
- Compte Railway (gratuit)
- Variables d'environnement configurées

## 🚀 Étape 1 : Déploiement du Backend sur Railway

### 1.1 Préparation du Repository

1. Assurez-vous que votre code est commité sur GitHub
2. Vérifiez que les fichiers suivants sont présents dans le dossier `Backend/` :
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `start_production.py`

### 1.2 Déploiement sur Railway

1. **Connectez-vous à Railway** :
   - Allez sur [railway.app](https://railway.app)
   - Connectez-vous avec votre compte GitHub

2. **Créez un nouveau projet** :
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre repository

3. **Configurez le service** :
   - Railway détectera automatiquement que c'est une application Python
   - Le `Procfile` sera utilisé pour démarrer l'application

4. **Configurez les variables d'environnement** :
   - Dans l'onglet "Variables" de votre projet Railway
   - Ajoutez toutes les variables nécessaires :
   ```
   REDDIT_CLIENT_ID=votre_client_id
   REDDIT_CLIENT_SECRET=votre_client_secret
   REDDIT_USER_AGENT=votre_user_agent
   OPENAI_API_KEY=votre_openai_key
   ANTHROPIC_API_KEY=votre_anthropic_key
   SUPABASE_URL=votre_supabase_url
   SUPABASE_KEY=votre_supabase_key
   ENVIRONMENT=production
   DEBUG=false
   ```

5. **Déployez** :
   - Railway déploiera automatiquement votre application
   - Notez l'URL générée (ex: `https://votre-app.railway.app`)

## 🌐 Étape 2 : Déploiement du Frontend sur Vercel

### 2.1 Préparation

1. Assurez-vous que le fichier `vercel.json` est présent dans le dossier `Frontend/`

### 2.2 Déploiement sur Vercel

1. **Connectez-vous à Vercel** :
   - Allez sur [vercel.com](https://vercel.com)
   - Connectez-vous avec votre compte GitHub

2. **Importez votre projet** :
   - Cliquez sur "New Project"
   - Importez votre repository GitHub
   - Sélectionnez le dossier `Frontend/` comme racine

3. **Configurez les variables d'environnement** :
   - Dans les paramètres du projet Vercel
   - Allez dans "Environment Variables"
   - Ajoutez :
   ```
   NEXT_PUBLIC_API_URL=https://votre-app.railway.app
   ```

4. **Déployez** :
   - Cliquez sur "Deploy"
   - Vercel déploiera automatiquement votre application Next.js

## 🔧 Configuration CORS

Pour que le frontend puisse communiquer avec le backend, vous devez configurer CORS dans votre API FastAPI.

Dans le fichier `Backend/core/api.py`, assurez-vous d'avoir :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Développement local
        "https://votre-app.vercel.app",  # URL de production Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 Vérification du Déploiement

### Backend (Railway)
1. Testez l'endpoint de santé : `https://votre-app.railway.app/health`
2. Vérifiez la documentation : `https://votre-app.railway.app/docs`

### Frontend (Vercel)
1. Visitez votre URL Vercel
2. Testez la connexion avec le backend
3. Vérifiez que les fonctionnalités marchent

## 🔄 Mise à Jour Continue

- **Railway** : Se met à jour automatiquement à chaque push sur GitHub
- **Vercel** : Se met à jour automatiquement à chaque push sur GitHub

## 🛠️ Dépannage

### Problèmes courants

1. **Erreur CORS** :
   - Vérifiez que l'URL du frontend est dans `allow_origins`
   - Redéployez le backend après modification

2. **Variables d'environnement manquantes** :
   - Vérifiez que toutes les variables sont configurées dans Railway
   - Redéployez après ajout de variables

3. **Erreur de build** :
   - Vérifiez les logs dans Railway/Vercel
   - Testez localement avant de déployer

### Logs et Monitoring

- **Railway** : Onglet "Deployments" pour voir les logs
- **Vercel** : Onglet "Functions" pour voir les logs

## 📞 Support

En cas de problème :
1. Vérifiez les logs de déploiement
2. Testez localement d'abord
3. Consultez la documentation de Railway et Vercel 