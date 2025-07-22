# ✅ Checklist de Déploiement

## 📋 Préparation du Repository

- [ ] Code commité sur GitHub
- [ ] Fichier `.gitignore` configuré
- [ ] Variables d'environnement locales sauvegardées

## 🚀 Backend (Railway)

### Fichiers de configuration
- [ ] `Backend/requirements.txt` ✅
- [ ] `Backend/Procfile` ✅
- [ ] `Backend/runtime.txt` ✅
- [ ] `Backend/railway.json` ✅
- [ ] `Backend/start_production.py` ✅

### Configuration API
- [ ] CORS configuré dans `Backend/core/api.py` ✅
- [ ] Endpoint `/health` fonctionnel ✅
- [ ] Variables d'environnement prêtes

### Variables d'environnement à configurer dans Railway
- [ ] `REDDIT_CLIENT_ID`
- [ ] `REDDIT_CLIENT_SECRET`
- [ ] `REDDIT_USER_AGENT`
- [ ] `OPENAI_API_KEY`
- [ ] `ANTHROPIC_API_KEY`
- [ ] `SUPABASE_URL`
- [ ] `SUPABASE_KEY`
- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=false`

## 🌐 Frontend (Vercel)

### Fichiers de configuration
- [ ] `Frontend/vercel.json` ✅
- [ ] `Frontend/package.json` ✅

### Configuration
- [ ] Variable `NEXT_PUBLIC_API_URL` à configurer dans Vercel
- [ ] URL du backend Railway à utiliser

## 🔧 Test de déploiement

### Backend
- [ ] Déploiement Railway réussi
- [ ] Endpoint `/health` accessible
- [ ] Documentation `/docs` accessible
- [ ] Logs sans erreur

### Frontend
- [ ] Déploiement Vercel réussi
- [ ] Application accessible
- [ ] Connexion au backend fonctionnelle
- [ ] Fonctionnalités testées

## 📝 Post-déploiement

- [ ] URLs sauvegardées
- [ ] Variables d'environnement documentées
- [ ] Tests de fonctionnalités complets
- [ ] Monitoring configuré

## 🚨 Problèmes courants à vérifier

- [ ] Erreurs CORS
- [ ] Variables d'environnement manquantes
- [ ] Timeout des requêtes
- [ ] Limites de rate limiting
- [ ] Connexion à Supabase

## 📞 Support

En cas de problème :
1. Vérifier les logs Railway/Vercel
2. Tester localement
3. Consulter la documentation
4. Vérifier les variables d'environnement 