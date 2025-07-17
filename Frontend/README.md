# Frontend Reddit Agents

Interface utilisateur moderne pour le système d'analyse Reddit avec Next.js et Tailwind CSS.

## 🚀 Fonctionnalités

- **Chat interactif** avec l'assistant Reddit
- **Analyse en temps réel** des subreddits
- **Affichage des résultats** avec visualisations
- **Export des données** (PDF, CSV, TXT)
- **Design responsive** et moderne
- **Animations fluides** avec Framer Motion

## 🛠️ Technologies

- **Next.js 14** - Framework React
- **TypeScript** - Typage statique
- **Tailwind CSS** - Styling utilitaire
- **Zustand** - Gestion d'état
- **Framer Motion** - Animations
- **Heroicons** - Icônes
- **React Hot Toast** - Notifications

## 📦 Installation

1. **Installer les dépendances :**
```bash
cd Frontend
npm install
```

2. **Configurer les variables d'environnement :**
```bash
# Créer le fichier .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Lancer le serveur de développement :**
```bash
npm run dev
```

4. **Ouvrir dans le navigateur :**
```
http://localhost:3000
```

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env.local` dans le dossier `Frontend` :

```env
# URL de votre backend Python
NEXT_PUBLIC_API_URL=http://localhost:8000

# Autres configurations
NEXT_PUBLIC_APP_NAME=Reddit Agents
```

### Intégration avec le Backend

Le frontend est configuré pour communiquer avec votre backend Python via :

1. **Proxy Next.js** : Les requêtes `/api/*` sont redirigées vers `http://localhost:8000`
2. **Service API** : `lib/api.ts` gère toutes les communications
3. **Types TypeScript** : Interfaces définies pour la cohérence des données

## 📁 Structure du projet

```
Frontend/
├── app/                    # App Router Next.js
│   ├── globals.css        # Styles globaux
│   ├── layout.tsx         # Layout principal
│   └── page.tsx           # Page d'accueil
├── components/            # Composants React
│   ├── ChatMessage.tsx    # Message du chat
│   ├── ChatInput.tsx      # Input du chat
│   ├── AnalysisResults.tsx # Résultats d'analyse
│   └── LoadingSpinner.tsx # Spinner de chargement
├── lib/                   # Utilitaires
│   ├── store.ts          # Store Zustand
│   └── api.ts            # Service API
├── package.json          # Dépendances
├── tailwind.config.js    # Configuration Tailwind
└── next.config.js        # Configuration Next.js
```

## 🎨 Design System

### Couleurs
- **Primary** : Bleu (#3b82f6)
- **Reddit** : Rouge (#ef4444)
- **Gray** : Nuances de gris pour l'interface

### Composants
- **Cards** : `.card` - Conteneurs avec ombre
- **Buttons** : `.btn-primary`, `.btn-secondary`
- **Inputs** : `.input-field` - Champs de saisie
- **Messages** : `.chat-message` - Messages du chat

## 🔌 API Integration

### Endpoints attendus

Le frontend s'attend à ce que votre backend Python expose ces endpoints :

```typescript
// Vérifier un subreddit
POST /check_subreddit
{ subreddit_name: string }

// Analyser un subreddit
POST /analyze_subreddit
{
  subreddit_name: string
  num_posts?: number
  comments_limit?: number
  sort_criteria?: string
  time_filter?: string
}

// Exporter les résultats
POST /export_results
{ format: 'pdf' | 'csv' | 'txt' }

// Récupérer les solutions stockées
GET /stored_solutions?subreddit=string
```

## 🚀 Déploiement

### Production
```bash
npm run build
npm start
```

### Vercel (recommandé)
1. Connectez votre repo GitHub à Vercel
2. Configurez les variables d'environnement
3. Déployez automatiquement

## 🔧 Développement

### Scripts disponibles
```bash
npm run dev      # Serveur de développement
npm run build    # Build de production
npm run start    # Serveur de production
npm run lint     # Linting ESLint
```

### Hot Reload
Le serveur de développement inclut :
- Hot reload automatique
- TypeScript en temps réel
- Tailwind CSS JIT

## 📱 Responsive Design

L'interface s'adapte automatiquement :
- **Desktop** : Layout en 3 colonnes
- **Tablet** : Layout en 2 colonnes
- **Mobile** : Layout en 1 colonne

## 🎯 Prochaines étapes

1. **Intégrer votre backend Python** en remplaçant les simulations
2. **Ajouter l'authentification** si nécessaire
3. **Implémenter le streaming** pour les réponses longues
4. **Ajouter des graphiques** pour les visualisations
5. **Optimiser les performances** avec le lazy loading

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

MIT License - voir le fichier LICENSE pour plus de détails. 