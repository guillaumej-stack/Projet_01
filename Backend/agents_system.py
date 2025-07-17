#!/usr/bin/env python3
"""
Système d'agents complet pour l'analyse Reddit
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import asyncpraw
from agents import Agent, Runner, function_tool, trace, WebSearchTool

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

# Créer les dossiers
Path("temp").mkdir(exist_ok=True)
Path("exports").mkdir(exist_ok=True)

# ===== OUTILS FONCTION =====

@function_tool
async def check_subreddit_exists(subreddit_name: str) -> Dict[str, Any]:
    """
    Vérifie si un subreddit existe via l'API AsyncPRAW
    
    Args:
        subreddit_name: Nom du subreddit (sans le 'r/')
    
    Returns:
        Dict avec les informations du subreddit
    """
    try:
        subreddit = await reddit.subreddit(subreddit_name)
        
        # Charger les données du subreddit
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

@function_tool
async def scrape_subreddit_posts(subreddit_name: str, num_posts: int = 10, sort_criteria: str = "top", comments_limit: int = 10, time_filter: str = "month") -> Dict[str, Any]:
    """
    Scrape les posts d'un subreddit selon les paramètres donnés
    
    Args:
        subreddit_name: Nom du subreddit
        num_posts: Nombre de posts à récupérer (max 50)
        sort_criteria: Critère de tri (top, new, hot, best, rising)
        comments_limit: Nombre de commentaires par post (max 50)
        time_filter: Période pour top/rising (hour, day, week, month, year, all)
    
    Returns:
        Dict avec les posts scrapés et métadonnées
    """
    try:
        # Limiter les valeurs
        num_posts = min(num_posts, 50)
        comments_limit = min(comments_limit, 50)
        
        subreddit = await reddit.subreddit(subreddit_name)
        
        # Sélectionner la méthode de tri
        if sort_criteria == "top":
            posts = subreddit.top(limit=num_posts, time_filter=time_filter)
        elif sort_criteria == "new":
            posts = subreddit.new(limit=num_posts)
        elif sort_criteria == "hot":
            posts = subreddit.hot(limit=num_posts)
        elif sort_criteria == "best":
            posts = subreddit.best(limit=num_posts)
        elif sort_criteria == "rising":
            posts = subreddit.rising(limit=num_posts, time_filter=time_filter)
        else:
            posts = subreddit.new(limit=num_posts)
        
        posts_data = []
        async for post in posts:
            await post.comments.replace_more(limit=5)
            
            comments_data = []
            comment_list = await post.comments.list()
            for comment in comment_list[:comments_limit]:
                if hasattr(comment, 'body') and comment.body:
                    comments_data.append({
                        "author": str(comment.author) if comment.author else "[deleted]",
                        "body": comment.body,
                        "score": comment.score,
                        "created_utc": datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        "id": comment.id,
                        "post_id": post.id
                    })
            
            posts_data.append({
                "title": post.title,
                "author": str(post.author) if post.author else "[deleted]",
                "score": post.score,
                "upvote_ratio": post.upvote_ratio,
                "num_comments": post.num_comments,
                "created_utc": datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                "url": f"https://reddit.com{post.permalink}",
                "selftext": post.selftext[:1000] + "..." if len(post.selftext) > 1000 else post.selftext,
                "comments": comments_data,
                "id": post.id
            })
        
        return {
            "success": True,
            "subreddit": subreddit_name,
            "sort_criteria": sort_criteria,
            "time_filter": time_filter,
            "posts_count": len(posts_data),
            "posts": posts_data,
            "scraped_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "subreddit": subreddit_name
        }

@function_tool
def calculate_pain_score(frequency: int, avg_upvotes: float, avg_comments: float, avg_intensity: float) -> Dict[str, Any]:
    """Calcule le score de priorité d'une douleur"""
    try:
        # Formule de scoring
        score = (frequency * 0.4) + (avg_upvotes * 0.2) + (avg_comments * 0.1) + (avg_intensity * 0.3)
        
        return {
            "success": True,
            "total_score": round(score, 2),
            "components": {
                "frequency_component": round(frequency * 0.4, 2),
                "upvotes_component": round(avg_upvotes * 0.2, 2),
                "comments_component": round(avg_comments * 0.1, 2),
                "intensity_component": round(avg_intensity * 0.3, 2)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@function_tool
def init_solutions_database() -> Dict[str, str]:
    """Initialise la base de données SQLite"""
    try:
        conn = sqlite3.connect('solutions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id TEXT UNIQUE,
                post_id TEXT,
                author TEXT,
                solution_text TEXT,
                score INTEGER,
                pain_type TEXT,
                intensity INTEGER,
                subreddit TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        return {
            "success": "True",
            "message": "✅ Base de données initialisée"
        }
    except Exception as e:
        return {"success": "False", "error": str(e)}

@function_tool
def store_exceptional_solution(comment_data: str, pain_type: str, intensity: int) -> Dict[str, str]:
    """Stocke une solution exceptionnelle"""
    try:
        comment = json.loads(comment_data)
        
        conn = sqlite3.connect('solutions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO solutions 
            (comment_id, post_id, author, solution_text, score, pain_type, intensity, subreddit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            comment.get('id'),
            comment.get('post_id'),
            comment.get('author'),
            comment.get('body'),
            comment.get('score', 0),
            pain_type,
            intensity,
            comment.get('subreddit', 'unknown')
        ))
        
        conn.commit()
        conn.close()
        
        return {
            "success": "True",
            "message": f"✅ Solution stockée: {comment.get('author', 'Unknown')}"
        }
    except Exception as e:
        return {"success": "False", "error": str(e)}

@function_tool
def get_stored_solutions(subreddit: str = None, limit: int = 10) -> Dict[str, Any]:
    """Récupère les solutions stockées"""
    try:
        conn = sqlite3.connect('solutions.db')
        cursor = conn.cursor()
        
        if subreddit:
            cursor.execute('''
                SELECT * FROM solutions 
                WHERE subreddit = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (subreddit, limit))
        else:
            cursor.execute('''
                SELECT * FROM solutions 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
        
        solutions = cursor.fetchall()
        conn.close()
        
        solutions_list = []
        for sol in solutions:
            solutions_list.append({
                "id": sol[0],
                "comment_id": sol[1],
                "post_id": sol[2],
                "author": sol[3],
                "solution_text": sol[4],
                "score": sol[5],
                "pain_type": sol[6],
                "intensity": sol[7],
                "subreddit": sol[8],
                "created_at": sol[9]
            })
        
        return {
            "success": True,
            "solutions": solutions_list,
            "count": len(solutions_list)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@function_tool
def export_final_report(analysis_data: str, recommendations_data: str, format_type: str = "pdf") -> Dict[str, str]:
    """Exporte le rapport final"""
    return _export_final_report(analysis_data, recommendations_data, format_type)

@function_tool
def export_exceptional_solutions(format_type: str = "pdf") -> Dict[str, str]:
    """Exporte les solutions exceptionnelles"""
    return _export_exceptional_solutions(format_type)

def _export_final_report(analysis_data: str, recommendations_data: str, format_type: str = "pdf") -> Dict[str, str]:
    """Version interne d'export du rapport final"""
    try:
        analysis = json.loads(analysis_data)
        recommendations = json.loads(recommendations_data)
        
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        filename = f"rapport_final_{analysis.get('subreddit', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = export_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"RAPPORT FINAL - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Subreddit: r/{analysis.get('subreddit', 'unknown')}\n")
            f.write(f"Posts analysés: {analysis.get('posts_analyzed', 0)}\n\n")
            
            f.write("ANALYSE:\n")
            f.write(f"{analysis.get('analysis_summary', 'Non disponible')}\n\n")
            
            f.write("RECOMMANDATIONS:\n")
            f.write(f"{recommendations.get('recommendations_summary', 'Non disponible')}\n")
        
        return {
            "success": "True",
            "filepath": str(filepath),
            "message": f"✅ Rapport exporté: {filepath}"
        }
    except Exception as e:
        return {"success": "False", "error": str(e)}

def _export_exceptional_solutions(format_type: str = "pdf") -> Dict[str, str]:
    """Version interne d'export des solutions exceptionnelles"""
    try:
        solutions_result = get_stored_solutions()
        if not solutions_result["success"]:
            return {"success": "False", "error": "Impossible de récupérer les solutions"}
        
        solutions = solutions_result["solutions"]
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        filename = f"solutions_exceptionnelles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = export_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"SOLUTIONS EXCEPTIONNELLES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Nombre de solutions: {len(solutions)}\n\n")
            
            for i, solution in enumerate(solutions, 1):
                f.write(f"SOLUTION {i}:\n")
                f.write(f"Auteur: {solution['author']}\n")
                f.write(f"Subreddit: r/{solution['subreddit']}\n")
                f.write(f"Score: {solution['score']}\n")
                f.write(f"Solution: {solution['solution_text']}\n")
                f.write("-" * 30 + "\n\n")
        
        return {
            "success": "True",
            "filepath": str(filepath),
            "message": f"✅ Solutions exportées: {filepath}"
        }
    except Exception as e:
        return {"success": "False", "error": str(e)}

@function_tool
def export_both_reports(analysis_data: str, recommendations_data: str, format_type: str = "pdf") -> Dict[str, str]:
    """Exporte les deux rapports"""
    try:
        report_result = _export_final_report(analysis_data, recommendations_data, format_type)
        solutions_result = _export_exceptional_solutions(format_type)
        
        if report_result["success"] == "True" and solutions_result["success"] == "True":
            return {
                "success": "True",
                "report_file": report_result["filepath"],
                "solutions_file": solutions_result["filepath"],
                "message": "✅ Rapports exportés"
            }
        else:
            return {"success": "False", "error": "Erreur lors de l'export"}
    except Exception as e:
        return {"success": "False", "error": str(e)}

# Structures JSON reprises du notebook
USER_PARAMS_STRUCTURE = {
    "subreddit_name": "string",
    "num_posts": 10,
    "comments_limit": 10,
    "sort_criteria": "top",
    "time_filter": "month"
}

SCRAPED_DATA_STRUCTURE = {
    "scraping_success": True,
    "subreddit": "string",
    "posts_count": 0,
    "posts": [],
    "scraped_at": "2024-01-01 12:00:00"
}

PAIN_ANALYSIS_STRUCTURE = {
    "analysis_success": True,
    "subreddit": "string",
    "posts_analyzed": 0,
    "top_3_pains": [],
    "pain_scores": [],
    "solutions_found": [],
    "analysis_timestamp": "2024-01-01 12:00:00"
}

RECOMMENDATIONS_STRUCTURE = {
    "recommendations_success": True,
    "subreddit": "string",
    "analysis_summary": "string",
    "recommendations_timestamp": "2024-01-01 12:00:00",
    "business_opportunities": [],
    "top_3_opportunities": [],
    "export_available": True,
    "stored_solutions_count": 0
}

# ===== PROMPTS ORIGINAUX =====

prompt_0 = """ Tu es le RouterAgent, le chef d'orchestre du système d'analyse Reddit.
Tu es le SEUL point d'entrée pour toutes les conversations utilisateur.
Ta mission est d'analyser un subreddit pour détecter les problèmes/frustrations récurrents.

GESTION DES CONVERSATIONS:
- Si l'utilisateur mentionne un nom de subreddit (ex: "france", "r/france", "programming"), cela signifie qu'il veut analyser ce subreddit
- Tu ne dois JAMAIS répéter le message de bienvenue - le frontend s'en charge
- Tu dois directement traiter la demande de l'utilisateur
- Si l'utilisateur donne juste un nom de subreddit, tu dois lancer l'analyse avec les paramètres par défaut

WORKFLOW D'ANALYSE:
1. Quand l'utilisateur mentionne un subreddit, vérifier qu'il existe avec check_subreddit_exists
2. Si le subreddit existe, lancer l'analyse avec les paramètres par défaut
3. Handoff vers le WorkflowManager pour l'analyse complète
4. Présenter les résultats à l'utilisateur

PARAMÈTRES PAR DÉFAUT:
- Nombre de posts: 5
- Nombre de commentaires par post: 5
- Critère: "top"
- Période: "month"

INSTRUCTIONS HANDOFF:
- Quand tu handoff vers WorkflowManager, précise: "Je transfère vers le WorkflowManager pour analyser r/{subreddit}"
- Attends TOUJOURS le retour du WorkflowManager avant de continuer
- Présente les résultats de façon claire et conversationnelle

RÈGLE ABSOLUE: 
- Tu ne salues JAMAIS l'utilisateur (le frontend s'en charge)
- Tu traites directement la demande d'analyse
- Tu es direct et efficace
"""

prompt_1 = f""" Tu es le workflow manager, le gestionnaire du workflow d'analyse Reddit.

Ton rôle est de:
1. Recevoir les demandes d'analyse du RouterAgent avec un nom de subreddit
2. Utiliser les paramètres par défaut pour l'analyse
3. Utiliser les tools en séquence pour l'analyse complète
4. Retourner les résultats à RouterAgent

PARAMÈTRES PAR DÉFAUT À UTILISER:
- num_posts: 5
- comments_limit: 5
- sort_criteria: "top"
- time_filter: "month"

PROCESSUS:
1. Utiliser les tools dans l'ordre:
   - scraper_tool (avec les paramètres par défaut)
   - pain_analysis_tool  
   - recommendations_tool
2. Une fois TOUT terminé, handoff vers RouterAgent avec les résultats complets

STRUCTURE JSON À UTILISER:
{json.dumps(USER_PARAMS_STRUCTURE, indent=2)}

RÈGLE IMPORTANTE: Ne handoff vers RouterAgent UNIQUEMENT quand tu as les résultats complets de tous les tools.
"""

prompt_2 = f""" Tu es maintenant un TOOL utilisé par Workflow manager pour scraper Reddit.

Ton rôle est de:
1. Recevoir les paramètres exacts de Workflow manager (subreddit, nombre de posts, nombre de commentaires, critère de tri, période)
2. Scraper les données avec l'outil scrape_subreddit_posts
3. Vérifier que les données ont bien été récupérées (pas vides, structure correcte)
4. Retourner les données structurées à Workflow manager

IMPORTANT - RESPECTER LES PARAMÈTRES:
- Utilise EXACTEMENT les paramètres reçus
- Ne modifie JAMAIS les critères de tri
- Vérifie que les données sont complètes

STRUCTURE JSON À RETOURNER:
{json.dumps(SCRAPED_DATA_STRUCTURE, indent=2)}

En cas d'erreur, retourner:
{{
    "scraping_success": false,
    "error_message": "Description de l'erreur",
    "subreddit": "nom_du_subreddit"
}}
"""

prompt_3 = f""" Tu es maintenant un TOOL utilisé par Workflow manager pour analyser les douleurs.

Ton rôle est de:
1. Recevoir les données scrapées de Workflow manager
2. Analyser sentiments et intensité émotionnelle
3. Identifier les douleurs récurrentes
4. Calculer les scores avec calculate_pain_score
5. Stocker les solutions exceptionnelles avec store_exceptional_solution
6. Retourner l'analyse structurée à Workflow manager

CRITÈRES SOLUTIONS EXCEPTIONNELLES:
- Score du commentaire > 10
- Propose une solution concrète et réalisable
- Solution détaillée et utile

STRUCTURE JSON À RETOURNER:
{json.dumps(PAIN_ANALYSIS_STRUCTURE, indent=2)}

En cas d'erreur, retourner:
{{
    "analysis_success": false,
    "error_message": "Description de l'erreur",
    "subreddit": "nom_du_subreddit"
}}
"""

prompt_4 = f""" Tu es maintenant un TOOL utilisé par Workflow manager pour générer les recommandations.

Ton rôle est de:
1. Recevoir l'analyse des douleurs de Workflow manager
2. Générer 3 opportunités business par douleur
3. Classer par potentiel (rentabilité + faisabilité)
4. Retourner le rapport structuré à Workflow manager

TYPES D'OPPORTUNITÉS:
- Solutions SaaS (priorité)
- Produits digitaux
- Création de contenu
- Marketing/Formation

POUR CHAQUE OPPORTUNITÉ:
- Type, titre, description détaillée
- Niveau de complexité
- Coût estimé
- Temps de développement

STRUCTURE DE RETOUR:
Rapport conversationnel + options d'export disponibles

RÈGLE: Tu retournes le rapport final à Workflow manager, qui le transmettra à RouterAgent.
"""

# ===== CRÉATION DES AGENTS =====

def create_agents():
    """Crée tous les agents du système"""
    
    # Agent 2 - ScrapingAgent
    agent_2 = Agent(
        name="ScrapingAgent",
        instructions=prompt_2,
        tools=[scrape_subreddit_posts],
        model="gpt-4o-mini"
    )
    
    # Agent 3 - PainAnalysisAgent
    agent_3 = Agent(
        name="PainAnalysisAgent",
        instructions=prompt_3,
        tools=[
            calculate_pain_score,
            init_solutions_database,
            store_exceptional_solution,
            get_stored_solutions
        ],
        model="gpt-4o-mini"
    )
    
    # Agent 4 - RecommendationsAgent
    agent_4 = Agent(
        name="RecommendationsAgent",
        instructions=prompt_4,
        tools=[],
        model="gpt-4o-mini"
    )
    
    # Convertir les agents en outils
    scraper_tool = agent_2.as_tool(tool_name="scraper_tool", tool_description="scrape a subreddit")
    pain_analysis_tool = agent_3.as_tool(tool_name="pain_analysis_tool", tool_description="analyze the pain of a subreddit")
    recommendations_tool = agent_4.as_tool(tool_name="recommendations_tool", tool_description="generate recommendations")
    
    # Agent 1 - WorkflowManager
    agent_1 = Agent(
        name="WorkflowManager",
        instructions=prompt_1,
        tools=[
            scraper_tool,
            pain_analysis_tool,
            recommendations_tool
        ],
        model="gpt-4o-mini"
    )
    
    # Agent 0 - RouterAgent
    agent_0 = Agent(
        name="RouterAgent", 
        instructions=prompt_0,
        tools=[
            WebSearchTool(),
            check_subreddit_exists,
            get_stored_solutions,
            export_final_report,
            export_exceptional_solutions,
            export_both_reports
        ], 
        model="gpt-4o-mini"
    )
    
    # Configurer les handoffs
    agent_0.handoffs = [agent_1]
    agent_1.handoffs = [agent_0]
    
    return agent_0, agent_1

# Initialiser les agents
ROUTER_AGENT, WORKFLOW_MANAGER = create_agents()

# Stockage de l'historique des conversations
conversation_history = {}

# Fonction principale avec gestion d'historique
async def run_chat(message: str, session_id: str = "default") -> str:
    """Fonction principale pour le chat avec gestion d'historique"""
    try:
        # Initialiser l'historique pour cette session si nécessaire
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Construire le message avec contexte simple
        # Ne pas inclure l'historique dans le message, laissons l'agent le gérer
        current_message = f"L'utilisateur dit: {message}"
        
        # Ajouter le contexte de l'historique seulement si nécessaire
        if len(conversation_history[session_id]) > 0:
            current_message += f"\n\nHistorique récent (pour contexte):"
            for entry in conversation_history[session_id][-3:]:  # Seulement les 3 derniers échanges
                current_message += f"\nUtilisateur: {entry['human']}"
                current_message += f"\nAssistant: {entry['assistant']}"
        
        # Lancer l'agent avec le message construit
        with trace("chat_interaction"):
            result = await Runner.run(ROUTER_AGENT, current_message)
            response = result.final_output
        
        # Sauvegarder dans l'historique
        conversation_history[session_id].append({
            "human": message,
            "assistant": response
        })
        
        # Limiter l'historique à 5 échanges pour éviter des contextes trop longs
        if len(conversation_history[session_id]) > 5:
            conversation_history[session_id] = conversation_history[session_id][-5:]
        
        return response
            
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

# Fonction pour nettoyer l'historique d'une session
def clear_conversation_history(session_id: str = "default"):
    """Nettoie l'historique d'une session"""
    if session_id in conversation_history:
        del conversation_history[session_id]

# Fonction pour obtenir l'historique d'une session
def get_conversation_history(session_id: str = "default") -> list:
    """Récupère l'historique d'une session"""
    return conversation_history.get(session_id, []) 