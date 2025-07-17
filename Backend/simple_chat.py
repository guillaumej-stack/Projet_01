#!/usr/bin/env python3
"""
Version simplifiée du système de chat pour identifier le problème
"""

import os
import asyncio
from dotenv import load_dotenv
import asyncpraw
from typing import Dict, Any

# Charger les variables d'environnement
load_dotenv(override=True)

# Configuration
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID") or ""
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET") or ""
REDDIT_USER_AGENT = "RedditScraper/1.0"

# Initialiser Reddit avec AsyncPRAW
reddit = asyncpraw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

async def simple_check_subreddit(subreddit_name: str) -> Dict[str, Any]:
    """Version simplifiée de check_subreddit_exists"""
    try:
        subreddit = await reddit.subreddit(subreddit_name)
        await subreddit.load()
        
        description = subreddit.public_description
        return {
            "exists": True,
            "subreddit": subreddit_name,
            "subscribers": subreddit.subscribers,
            "description": description[:200] + "..." if len(description) > 200 else description,
            "title": subreddit.title,
            "url": f"https://reddit.com/r/{subreddit_name}"
        }
    except Exception as e:
        return {
            "exists": False,
            "subreddit": subreddit_name,
            "error": str(e)
        }

async def simple_scrape_posts(subreddit_name: str, num_posts: int = 5) -> Dict[str, Any]:
    """Version simplifiée de scrape_subreddit_posts"""
    try:
        subreddit = await reddit.subreddit(subreddit_name)
        posts_data = []
        
        async for post in subreddit.top(limit=num_posts, time_filter="month"):
            posts_data.append({
                "title": post.title,
                "score": post.score,
                "num_comments": post.num_comments,
                "author": str(post.author) if post.author else "[deleted]",
                "url": f"https://reddit.com{post.permalink}",
                "selftext": post.selftext[:500] + "..." if len(post.selftext) > 500 else post.selftext,
            })
        
        return {
            "success": True,
            "subreddit": subreddit_name,
            "posts_count": len(posts_data),
            "posts": posts_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "subreddit": subreddit_name
        }

async def simple_chat_response(message: str) -> str:
    """Version simplifiée du chat qui traite directement les messages"""
    message = message.strip().lower()
    
    # Détecter si c'est un nom de subreddit
    if message.startswith("r/"):
        subreddit_name = message[2:]
    elif message.startswith("/r/"):
        subreddit_name = message[3:]
    else:
        # Supposer que c'est un nom de subreddit direct
        subreddit_name = message
    
    # Vérifier si le subreddit existe
    print(f"🔍 Vérification du subreddit: r/{subreddit_name}")
    check_result = await simple_check_subreddit(subreddit_name)
    
    if not check_result["exists"]:
        return f"❌ Erreur: Le subreddit 'r/{subreddit_name}' n'existe pas ou est inaccessible.\nErreur: {check_result.get('error', 'Unknown')}"
    
    # Subreddit existe, lancer l'analyse
    print(f"✅ Subreddit trouvé: r/{subreddit_name}")
    print(f"📊 Lancement de l'analyse...")
    
    scrape_result = await simple_scrape_posts(subreddit_name)
    
    if not scrape_result["success"]:
        return f"❌ Erreur lors du scraping: {scrape_result.get('error', 'Unknown')}"
    
    # Générer la réponse
    posts = scrape_result["posts"]
    response = f"""✅ Analyse du subreddit r/{subreddit_name} terminée !

📊 **Statistiques du subreddit:**
- Titre: {check_result['title']}
- Abonnés: {check_result['subscribers']:,}
- Description: {check_result['description']}

📋 **Posts analysés:** {scrape_result['posts_count']} posts récupérés

🔝 **Top posts récents:**"""
    
    for i, post in enumerate(posts[:3], 1):
        response += f"""
{i}. **{post['title']}**
   - Score: {post['score']}, Commentaires: {post['num_comments']}
   - Auteur: {post['author']}"""
    
    response += f"""

💡 **Prochaines étapes:**
- Analyser les douleurs des utilisateurs
- Identifier les solutions proposées
- Générer des recommandations business

L'analyse complète sera disponible prochainement !"""
    
    return response

async def test_simple_chat():
    """Test du système de chat simplifié"""
    print("🚀 Test du système de chat simplifié")
    
    # Test avec "france"
    test_message = "france"
    print(f"\n📝 Message test: '{test_message}'")
    
    response = await simple_chat_response(test_message)
    print(f"\n🤖 Réponse:")
    print(response)
    
    # Fermer la session Reddit
    await reddit.close()

if __name__ == "__main__":
    asyncio.run(test_simple_chat()) 