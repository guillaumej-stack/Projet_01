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
Projet_01/
├── Backend/                 # API FastAPI
│   ├── app/
│   │   ├── scrapers/        # Scrapers Reddit
│   │   ├── chatbot/         # Logique IA
│   │   ├── api/             # Endpoints API
│   │   └── models/          # Modèles de données
│   ├── requirements.txt
│   └── main.py
├── Frontend/                # Next.js App
│   ├── src/
│   │   ├── components/      # Composants React
│   │   ├── pages/           # Pages Next.js
│   │   ├── hooks/           # Hooks personnalisés
│   │   └── utils/           # Utilitaires
│   ├── package.json
│   └── next.config.js
└── README.md
```

## 🚀 Installation

### Prérequis
- Python 3.8+
- Node.js 18+
- Compte Supabase
- Redis (optionnel)
- Comptes API : Reddit, OpenAI, Stripe

### Configuration

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd Projet_01
```

2. **Configuration Backend**
```bash
cd Backend
cp env.example .env
# Éditer .env avec vos clés API
```

3. **Configuration Frontend**
```bash
cd Frontend
cp .env.example .env.local
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
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` sur Windows
pip install -r requirements.txt
```

**Frontend**
```bash
cd Frontend
npm install
```

### Configuration Supabase

1. **Créer un projet Supabase**
   - Aller sur [supabase.com](https://supabase.com)
   - Créer un nouveau projet
   - Noter l'URL et les clés API

2. **Configurer la base de données**
   - Aller dans l'éditeur SQL de Supabase
   - Exécuter le script `Backend/supabase_schema.sql`
   - Cela créera toutes les tables et politiques de sécurité

3. **Configurer l'authentification**
   - Dans Supabase Dashboard > Authentication > Settings
   - Configurer les providers souhaités (Email, Google, etc.)
   - Activer "Enable email confirmations" si nécessaire

### Lancement

**Backend**
```bash
cd Backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**
```bash
cd Frontend
npm run dev
```

L'application sera disponible sur :
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000
- Documentation API : http://localhost:8000/docs

## 📊 Subreddits Ciblés

### 🇫🇷 Français
- r/france - Problèmes généraux
- r/QueFaire - Questions et conseils

### 🌍 International
- r/AskReddit - Questions générales
- r/Entrepreneur - Problèmes entrepreneuriaux
- r/SaaS - Problèmes SaaS

## 💰 Plans SaaS

- **Gratuit** : 10 requêtes/mois
- **Pro** : 100 requêtes/mois - $9.99/mois
- **Business** : Requêtes illimitées - $29.99/mois

## 🔧 Technologies

- **Backend** : FastAPI, PRAW (Reddit API), OpenAI Agent SDK
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

**Scraping**
- `POST /api/scraping/scrape-all` - Scraper tous les subreddits
- `POST /api/scraping/scrape-subreddit/{name}` - Scraper un subreddit
- `GET /api/scraping/posts` - Récupérer les posts scrapés
- `GET /api/scraping/posts/stats` - Statistiques des posts

**Chatbot**
- `POST /api/chatbot/chat` - Chat avec l'agent IA
- `GET /api/chatbot/sessions` - Sessions de chat
- `POST /api/chatbot/search-problems` - Recherche de problèmes

**Authentification**
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/auth/me` - Profil utilisateur

**Abonnement**
- `GET /api/subscription/plans` - Plans disponibles
- `POST /api/subscription/create-checkout-session` - Créer paiement
- `GET /api/subscription/current` - Abonnement actuel

## 🚀 Prochaines étapes

### Phase 1 - MVP (2-3 semaines)
- [ ] Finaliser l'authentification JWT
- [ ] Implémenter le système de quotas
- [ ] Créer l'interface de chat
- [ ] Ajouter les pages de tarification
- [ ] Intégrer Stripe

### Phase 2 - Fonctionnalités avancées (4-6 semaines)
- [ ] Dashboard utilisateur
- [ ] Export de données
- [ ] Notifications en temps réel
- [ ] API publique
- [ ] Analytics avancées

### Phase 3 - Scale (6-8 semaines)
- [ ] Cache Redis
- [ ] Background jobs avec Celery
- [ ] Monitoring et logging
- [ ] Tests automatisés
- [ ] CI/CD pipeline

### Phase 4 - Déploiement (2-3 semaines)
- [ ] Configuration production
- [ ] SSL et sécurité
- [ ] Monitoring production
- [ ] Documentation utilisateur
- [ ] Support client

## 🔐 Sécurité

- Authentification Supabase Auth (JWT sécurisé)
- Row Level Security (RLS) sur toutes les tables
- Validation des données avec Pydantic
- Rate limiting sur les API
- CORS configuré
- Variables d'environnement sécurisées
- Politiques de sécurité granulaires

## 📈 Monitoring

- Logs structurés
- Métriques de performance
- Alertes d'erreurs
- Dashboard de santé
- Analytics d'utilisation

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
