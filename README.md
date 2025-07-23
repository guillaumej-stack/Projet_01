# Reddit Problem Scraper & AI Assistant

Un SaaS pour scraper les problèmes des utilisateurs Reddit et fournir des réponses intelligentes via un chatbot.

## 🎯 Fonctionnalités

### Scraping Reddit
- **Subreddits français** : r/france, r/QueFaire
- **Subreddits internationaux** : r/AskReddit, r/Entrepreneur, r/SaaS
- Extraction automatique des problèmes et questions
- Stockage structuré en base de données

### Chatbot IA
- Analyse contextuelle des problèmes
- Réponses personnalisées basées sur les données scrapées
- Recherche intelligente dans les forums spécifiques
- Interface conversationnelle intuitive

### SaaS avec Next.js
- Interface moderne et responsive
- Système d'authentification
- Plans d'abonnement avec Stripe
- Dashboard utilisateur

## 🏗️ Architecture

```
Projet_Reddit/
├── Backend/                 # API FastAPI, scripts, notebooks
│   ├── core/               # Modules principaux (API, agents, prompts, etc.)
│   ├── exports/            # Exports de données temporaires
│   ├── temp/               # Fichiers temporaires
│   ├── requirements.txt    # Dépendances Python
│   ├── pyproject.toml      # (optionnel) Configurations avancées
│   ├── start-backend.py    # Script de démarrage principal
│   ├── start_server.py     # Script de démarrage serveur (dev)
│   ├── start_production.py # Script de démarrage production
│   ├── simple_chat.py      # Script de chat simple
│   ├── debug.py            # Script de debug
│   ├── Test_01.ipynb       # Notebook d'exploration
│   ├── Version_00.ipynb    # Notebook d'exploration
│   └── ...
├── Frontend/               # Next.js App
│   ├── app/                # Entrée principale (layout, pages)
│   ├── components/         # Composants React
│   ├── lib/                # Librairies utilitaires
│   ├── env.example         # Exemple d'environnement
│   ├── package.json        # Dépendances JS
│   └── ...
├── README.md
├── GUIDE_LANCEMENT.md      # Guide de démarrage rapide
└── deploy.sh               # Script de déploiement
```

## 🚀 Installation

### Prérequis
- Python 3.10+
- Node.js 18+
- Compte Supabase
- Comptes API : Reddit, OpenAI, Stripe
- (Optionnel) Redis

### Configuration

1. **Cloner le projet**
```powershell
git clone <votre-repo>
cd Projet_Reddit
```

2. **Configuration Backend**
```powershell
cd Backend
# Copier et éditer vos variables d'environnement si besoin
# (exemple : cp env.example .env)
```

3. **Configuration Frontend**
```powershell
cd Frontend
cp env.example .env.local
# Éditer .env.local avec vos clés API
```

### Variables d'environnement

**Backend (.env)**
```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Reddit API
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Stripe
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_webhook_secret
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

### Installation des dépendances

**Backend**
```powershell
cd Backend
python -m venv venv
.\venv\Scripts\activate  # Pour Windows PowerShell
pip install -r requirements.txt
```

**Frontend**
```powershell
cd Frontend
npm install
```

### Lancement

**Backend**
```powershell
cd Backend
python start-backend.py  # ou python start_server.py pour dev
```

**Frontend**
```powershell
cd Frontend
npm run dev
```

L'application sera disponible sur :
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000

## 📊 Subreddits Ciblés

### 🇫🇷 Français
- r/france - Problèmes généraux
- r/QueFaire - Questions et conseils

### 🌍 International
- r/AskReddit - Questions générales
- r/Entrepreneur - Problèmes entrepreneuriaux
- r/SaaS - Problèmes SaaS


## 🔧 Technologies

- **Backend** : FastAPI, PRAW (Reddit API), OpenAI, Python 3.10+
- **Frontend** : Next.js, TypeScript, Tailwind CSS
- **Base de données** : Supabase (PostgreSQL + Auth + Real-time)
- **Paiement** : Stripe
- **Déploiement** : Vercel (Frontend) + Railway/Heroku (Backend)

## 📖 Utilisation

### 1. Scraping Reddit
```bash
# Scraper tous les subreddits
curl -X POST http://localhost:8000/api/scraping/scrape-all

# Scraper un subreddit spécifique
curl -X POST http://localhost:8000/api/scraping/scrape-subreddit/france
```

### 2. Chatbot IA
```bash
# Chat avec l'agent
curl -X POST http://localhost:8000/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Comment gérer le stress au travail ?",
    "language": "fr"
  }'
```

### 3. API Endpoints principaux

| Méthode | Chemin                | Description                                      | Corps attendu (JSON)                |
|---------|----------------------|--------------------------------------------------|-------------------------------------|
| GET     | `/`                  | Racine, infos API et endpoints                   | -                                   |
| GET     | `/health`            | Vérification de l'état de l'API                  | -                                   |
| POST    | `/chat`              | Chat avec l'agent IA principal                   | `{ "message": str, "session_id"?: str }` |
| POST    | `/check_subreddit`   | Vérifie l'existence d'un subreddit               | `{ "subreddit_name": str }`        |
| POST    | `/analyze`           | Analyse complète d'un subreddit                  | `{ "subreddit_name": str, "num_posts"?: int, "comments_limit"?: int, "sort_criteria"?: str, "time_filter"?: str }` |
| POST    | `/export`            | Exporte les résultats d'analyse                  | `{ "format_type"?: str, "subreddit"?: str }` |
| DELETE  | `/clear_history`     | Efface l'historique de conversation d'une session| `{ "session_id": str }`            |

#### Détail des schémas de requête

- **/chat** :
  ```json
  {
    "message": "Votre message ici",
    "session_id": "id_session" // optionnel
  }
  ```
- **/check_subreddit** :
  ```json
  {
    "subreddit_name": "NomDuSubreddit"
  }
  ```
- **/analyze** :
  ```json
  {
    "subreddit_name": "NomDuSubreddit",
    "num_posts": 5,                // optionnel
    "comments_limit": 5,           // optionnel
    "sort_criteria": "top",       // optionnel
    "time_filter": "month"        // optionnel
  }
  ```
- **/export** :
  ```json
  {
    "format_type": "pdf",         // optionnel (pdf, csv...)
    "subreddit": "NomDuSubreddit" // optionnel
  }
  ```
- **/clear_history** :
  ```json
  {
    "session_id": "id_session"
  }
  ```
