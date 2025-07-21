import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel
from functions import supabase

import praw
from openai import OpenAI
from supabase import create_client, Client
from agents import Agent, Runner, function_tool, trace, WebSearchTool

# Charger les variables d'environnement
load_dotenv()

# Configuration Reddit
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "RedditAnalysisSaaS/1.0"

# Configuration OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Initialiser les clients
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

openai_client = OpenAI(api_key=OPENAI_API_KEY)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



@function_tool
def check_subreddit_exists(subreddit_name: str) -> str:
    """
    Vérifie si un subreddit existe via l'API Reddit
    
    Args:
        subreddit_name: Nom du subreddit (sans le 'r/')
    
    Returns:
        JSON string avec les informations du subreddit
    """
    try:
        # Utiliser PRAW pour accéder au subreddit
        subreddit = reddit.subreddit(subreddit_name)
        
        # Récupérer les informations du subreddit
        subreddit_info = {
            "exists": True,
            "subreddit": subreddit_name,
            "subscribers": subreddit.subscribers,
            "description": subreddit.public_description,
            "title": subreddit.title,
            "url": f"https://reddit.com/r/{subreddit_name}"
        }
        
        return json.dumps(subreddit_info)
        
    except Exception as e:
        error_info = {
            "exists": False,
            "subreddit": subreddit_name,
            "error": str(e)
        }
        return json.dumps(error_info)


@function_tool
def scrape_subreddit_posts(subreddit_name: str, num_posts: int = 10, sort_criteria: str = "top", comments_limit: int = 10, time_filter: str = "month") -> str:
    """
    Scrape les posts d'un subreddit selon les paramètres donnés
    
    Args:
        subreddit_name: Nom du subreddit (sans le 'r/')
        num_posts: Nombre de posts à récupérer
        sort_criteria: Critère de tri (top, new, hot, best, rising)
        comments_limit: Nombre de commentaires par post
        time_filter: Filtre temporel pour top/rising
    
    Returns:
        Dict avec les posts scrapés
    """
    try:
        # Limiter les valeurs pour éviter les abus
        num_posts = min(num_posts, 50)
        comments_limit = min(comments_limit, 50)
        
        # Accéder au subreddit
        subreddit = reddit.subreddit(subreddit_name)
        
        # Mapper les critères de tri
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
        
        for post in posts:
            # Récupérer les commentaires
            post.comments.replace_more(limit=5)
            
            comments_data = []
            for comment in post.comments.list()[:comments_limit]:
                if hasattr(comment, 'body') and comment.body:
                    comments_data.append({
                        "author": str(comment.author) if comment.author else "[deleted]",
                        "body": comment.body,
                        "score": comment.score,
                        "created_utc": datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        "id": comment.id
                    })
            
            # Données du post
            post_data = {
                "title": post.title,
                "author": str(post.author) if post.author else "[deleted]",
                "score": post.score,
                "num_comments": post.num_comments,
                "url": f"https://reddit.com{post.permalink}",
                "selftext": post.selftext[:1000] + "..." if len(post.selftext) > 1000 else post.selftext,
                "comments": comments_data,
                "id": post.id
            }
            
            posts_data.append(post_data)
        
        result = {
            "success": True,
            "subreddit": subreddit_name,
            "sort_criteria": sort_criteria,
            "posts_count": len(posts_data),
            "posts": posts_data,
            "scraped_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return json.dumps(result)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "subreddit": subreddit_name
        }
        return json.dumps(error_result)

@function_tool
def store_solution_in_supabase(comment_id: str, post_id: str, author: str, solution_text: str, score: int, pain_type: str, intensity: int, subreddit: str, user_id: str = None) -> str:
    """
    Stocke une solution exceptionnelle dans Supabase
    
    Args:
        comment_id: ID du commentaire
        post_id: ID du post
        author: Auteur du commentaire
        solution_text: Texte de la solution
        score: Score du commentaire
        pain_type: Type de douleur adressée
        intensity: Intensité de la douleur (1-10)
        subreddit: Nom du subreddit
        user_id: ID de l'utilisateur (optionnel)
    
    Returns:
        Dict avec le statut du stockage
    """
    try:
        # Insérer dans Supabase
        result = supabase.table("solutions").insert({
            "comment_id": comment_id,
            "post_id": post_id,
            "author": author,
            "solution_text": solution_text,
            "score": score,
            "pain_type": pain_type,
            "intensity": intensity,
            "subreddit": subreddit,
            "user_id": user_id
        }).execute()
        
        success_result = {
            "success": True,
            "message": f"✅ Solution stockée pour {pain_type}",
            "solution_id": result.data[0]["id"] if result.data else None
        }
        return json.dumps(success_result)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        return json.dumps(error_result)


@function_tool
def calculate_pain_score(frequency: int, avg_upvotes: float, avg_comments: float, avg_intensity: float) -> str:
    """
    Calcule le score de priorité d'une douleur utilisateur
    
    Args:
        frequency: Nombre de posts mentionnant cette douleur
        avg_upvotes: Moyenne des upvotes des posts concernés
        avg_comments: Moyenne des commentaires des posts concernés
        avg_intensity: Intensité émotionnelle moyenne (1-10)
    
    Returns:
        Dict avec le score calculé et les détails
    """
    try:
        # Formule de scoring exacte de Version_00
        score = (frequency * 0.4) + (avg_upvotes * 0.2) + (avg_comments * 0.1) + (avg_intensity * 0.3)
        
        success_result = {
            "success": True,
            "total_score": round(score, 2),
            "components": {
                "frequency_component": round(frequency * 0.4, 2),
                "upvotes_component": round(avg_upvotes * 0.2, 2),
                "comments_component": round(avg_comments * 0.1, 2),
                "intensity_component": round(avg_intensity * 0.3, 2)
            }
        }
        return json.dumps(success_result)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        return json.dumps(error_result)

@function_tool
def store_exceptional_solution(comment_id: str, post_id: str, author: str, solution_text: str, score: int, pain_type: str, intensity: int, subreddit: str) -> str:
    """
    Stocke une solution exceptionnelle dans Supabase
    (Adapté de Version_00 pour Supabase)
    
    Args:
        comment_id: ID du commentaire
        post_id: ID du post
        author: Auteur du commentaire
        solution_text: Texte de la solution
        score: Score du commentaire
        pain_type: Type de douleur adressée
        intensity: Intensité de la douleur (1-10)
        subreddit: Nom du subreddit
    
    Returns:
        Dict avec le statut du stockage
    """
    try:
        result = supabase.table("solutions").insert({
            "comment_id": comment_id,
            "post_id": post_id,
            "author": author,
            "solution_text": solution_text,
            "score": score,
            "pain_type": pain_type,
            "intensity": intensity,
            "subreddit": subreddit
        }).execute()
        
        success_result = {
            "success": True,
            "message": f"✅ Solution stockée pour {pain_type}"
        }
        return json.dumps(success_result)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        return json.dumps(error_result)

@function_tool
def get_stored_solutions(subreddit: str = None) -> str:
    """
    Récupère les solutions stockées, optionnellement filtrées par subreddit
    (Adapté de Version_00 pour Supabase)
    
    Args:
        subreddit: Nom du subreddit (optionnel)
    
    Returns:
        Dict avec les solutions trouvées
    """
    try:
        # Construire la requête Supabase
        query = supabase.table("solutions").select("*").order("score", desc=True)
        
        if subreddit:
            query = query.eq("subreddit", subreddit)
        
        # Exécuter la requête
        result = query.execute()
        solutions = result.data
        
        # Convertir en format compatible Version_00
        solutions_list = []
        for sol in solutions:
            solutions_list.append({
                "id": sol["id"],
                "comment_id": sol["comment_id"],
                "post_id": sol["post_id"],
                "author": sol["author"],
                "solution_text": sol["solution_text"],
                "score": sol["score"],
                "pain_type": sol["pain_type"],
                "intensity": sol["intensity"],
                "subreddit": sol["subreddit"],
                "created_at": sol["created_at"]
            })
        
        success_result = {
            "success": True,
            "solutions": solutions_list,
            "count": len(solutions_list)
        }
        return json.dumps(success_result)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        return json.dumps(error_result)



@function_tool
def send_message_to_user(message: str, session_id: str = "default") -> str:
    """
    Enregistre un message assistant dans l'historique de conversation pour affichage immédiat dans le chat.
    """
    try:
        supabase.table("conversation_history").insert({
            "session_id": session_id,
            "user_message": None,
            "agent_response": message
        }).execute()
        return f"Message '{message}' envoyé à l'utilisateur"
    except Exception as e:
        return f"Erreur lors de l'envoi du message à l'utilisateur: {e}"

# class FlexibleDict(BaseModel):
#     class Config:
#         extra = "allow"
#         
#     def dict(self, **kwargs):
#         return super().dict(**kwargs)

# @function_tool
# def export_final_report(
#     analysis_data: FlexibleDict, 
#     recommendations_data: FlexibleDict, 
#     format_type: str = "pdf"
# ) -> str:
#     """
#     Exporte le rapport final d'analyse
#     
#     Args:
#         analysis_data: Données d'analyse
#         recommendations_data: Données de recommandations
#         format_type: Format d'export (pdf, json, csv)
#     
#     Returns:
#         Chaîne JSON avec le chemin du fichier exporté
#     """
#     try:
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         
#         # Convertir en dict pour compatibilité avec votre code existant
#         analysis_dict = analysis_data.dict() if hasattr(analysis_data, 'dict') else analysis_data
#         recommendations_dict = recommendations_data.dict() if hasattr(recommendations_data, 'dict') else recommendations_data
#         
#         subreddit = analysis_dict.get("subreddit", "unknown")
#         
#         # Créer le dossier exports s'il n'existe pas
#         Path("exports").mkdir(exist_ok=True)
#         
#         if format_type == "json":
#             filepath = f"exports/rapport_{subreddit}_{timestamp}.json"
#             with open(filepath, 'w', encoding='utf-8') as f:
#                 json.dump({
#                     "analysis": analysis_dict,
#                     "recommendations": recommendations_dict,
#                     "exported_at": timestamp
#                 }, f, ensure_ascii=False, indent=2)
#         
#         elif format_type == "txt":
#             filepath = f"exports/rapport_{subreddit}_{timestamp}.txt"
#             with open(filepath, 'w', encoding='utf-8') as f:
#                 f.write(f"RAPPORT D'ANALYSE - r/{subreddit}\n")
#                 f.write(f"Généré le: {timestamp}\n\n")
#                 f.write("ANALYSE DES DOULEURS:\n")
#                 f.write(json.dumps(analysis_dict, ensure_ascii=False, indent=2))
#                 f.write("\n\nRECOMANDATIONS:\n")
#                 f.write(json.dumps(recommendations_dict, ensure_ascii=False, indent=2))
#         
#         else:  # PDF par défaut
#             filepath = f"exports/rapport_{subreddit}_{timestamp}.pdf"
#             # Simuler l'export PDF (comme dans Version_00)
#             with open(filepath, 'w', encoding='utf-8') as f:
#                 f.write(f"RAPPORT PDF - r/{subreddit} - {timestamp}")
#         
#         return json.dumps({
#             "success": True,
#             "filepath": filepath,
#             "format": format_type,
#             "message": f"✅ Rapport exporté: {filepath}"
#         })
#         
#     except Exception as e:
#         return json.dumps({
#             "success": False,
#             "error": str(e)
#         })

        
# @function_tool
# def export_exceptional_solutions(subreddit: str, format_type: str = "csv") -> str:
#     """
#     Exporte les solutions exceptionnelles d'un subreddit
#     (Exact de Version_00)
#     
#     Args:
#         subreddit: Nom du subreddit
#         format_type: Format d'export (csv, json, txt)
#     
#     Returns:
#         Chaîne JSON avec le chemin du fichier exporté
#     """
#     try:
#         # Récupérer les solutions
#         solutions_data_json = get_stored_solutions(subreddit)
#         solutions_data = json.loads(solutions_data_json)
#         
#         if not solutions_data["success"]:
#             return solutions_data_json
#         
#         solutions = solutions_data["solutions"]
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         
#         # Créer le dossier exports s'il n'existe pas
#         Path("exports").mkdir(exist_ok=True)
#         
#         if format_type == "json":
#             filepath = f"exports/solutions_{subreddit}_{timestamp}.json"
#             with open(filepath, 'w', encoding='utf-8') as f:
#                 json.dump(solutions, f, ensure_ascii=False, indent=2)
#         
#         elif format_type == "txt":
#             filepath = f"exports/solutions_{subreddit}_{timestamp}.txt"
#             with open(filepath, 'w', encoding='utf-8') as f:
#                 f.write(f"SOLUTIONS EXCEPTIONNELLES - r/{subreddit}\n")
#                 f.write(f"Générées le: {timestamp}\n\n")
#                 for sol in solutions:
#                     f.write(f"--- SOLUTION #{sol['id']} ---\n")
#                     f.write(f"Type de douleur: {sol['pain_type']}\n")
#                     f.write(f"Auteur: {sol['author']}\n")
#                     f.write(f"Score: {sol['score']}\n")
#                     f.write(f"Solution: {sol['solution_text']}\n\n")
#         
#         else:  # CSV par défaut
#             filepath = f"exports/solutions_{subreddit}_{timestamp}.csv"
#             with open(filepath, 'w', encoding='utf-8') as f:
#                 f.write("ID,Pain Type,Author,Score,Solution\n")
#                 for sol in solutions:
#                     f.write(f"{sol['id']},{sol['pain_type']},{sol['author']},{sol['score']},\"{sol['solution_text']}\"\n")
#         
#         return json.dumps({
#             "success": True,
#             "filepath": filepath,
#             "format": format_type,
#             "message": f"✅ Solutions exportées: {filepath}"
#         })
#         
#     except Exception as e:
#         return json.dumps({
#             "success": False,
#             "error": str(e)
#         })

# @function_tool
# def export_both_reports(analysis_data: Any, recommendations_data: Any, subreddit: str, format_type: str = "pdf") -> str:
#     """
#     Exporte à la fois le rapport final et les solutions exceptionnelles
#     (Exact de Version_00)
#     
#     Args:
#         analysis_data: Données d'analyse
#         recommendations_data: Données de recommandations
#         subreddit: Nom du subreddit
#         format_type: Format d'export (pdf, json, csv)
#     
#     Returns:
#         Chaîne JSON avec les chemins des fichiers exportés
#     """
#     try:
#         # Exporter le rapport final
#         report_result_json = export_final_report(analysis_data, recommendations_data, format_type)
#         report_result = json.loads(report_result_json)
#         
#         # Exporter les solutions exceptionnelles
#         solutions_result_json = export_exceptional_solutions(subreddit, format_type)
#         solutions_result = json.loads(solutions_result_json)
#         
#         return json.dumps({
#             "success": True,
#             "report_export": report_result,
#             "solutions_export": solutions_result,
#             "message": "✅ Exports combinés terminés"
#         })
#         
#     except Exception as e:
#         return json.dumps({
#             "success": False,
#             "error": str(e)
#         })

# Fonctions d'export temporairement désactivées
pass